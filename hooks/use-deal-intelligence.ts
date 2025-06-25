// React Query hooks for deal intelligence data

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { dealsAPI } from '@/lib/api/deals'
import type { DealIntelligence, TimelineEvent } from '@/types/intelligence'
import type { MEDDPICCAnalysis } from '@/types/meddpicc'

// Query keys for cache management
export const dealKeys = {
  all: ['deals'] as const,
  lists: () => [...dealKeys.all, 'list'] as const,
  list: (filters: Record<string, any>) => [...dealKeys.lists(), filters] as const,
  details: () => [...dealKeys.all, 'detail'] as const,
  detail: (id: string) => [...dealKeys.details(), id] as const,
  intelligence: (id: string) => [...dealKeys.detail(id), 'intelligence'] as const,
  meddpicc: (id: string) => [...dealKeys.detail(id), 'meddpicc'] as const,
  timeline: (id: string) => [...dealKeys.detail(id), 'timeline'] as const,
  stats: () => [...dealKeys.all, 'stats'] as const,
}

// Get deal intelligence
export function useDealIntelligence(dealId: string) {
  return useQuery({
    queryKey: dealKeys.intelligence(dealId),
    queryFn: () => dealsAPI.getIntelligence(dealId),
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // 1 minute
    enabled: !!dealId,
  })
}

// Get MEDDPICC analysis
export function useMEDDPICC(dealId: string) {
  return useQuery({
    queryKey: dealKeys.meddpicc(dealId),
    queryFn: () => dealsAPI.getMEDDPICC(dealId),
    staleTime: 1 * 60 * 1000, // 1 minute
    enabled: !!dealId,
  })
}

// Get deal timeline
export function useDealTimeline(dealId: string, limit = 50) {
  return useQuery({
    queryKey: [...dealKeys.timeline(dealId), limit],
    queryFn: () => dealsAPI.getTimeline(dealId, limit),
    staleTime: 30 * 1000, // 30 seconds
    enabled: !!dealId,
  })
}

// List deals with filters
export function useDeals(params: Parameters<typeof dealsAPI.list>[0] = {}) {
  return useQuery({
    queryKey: dealKeys.list(params),
    queryFn: () => dealsAPI.list(params),
    staleTime: 1 * 60 * 1000, // 1 minute
  })
}

// Get deal stats
export function useDealStats() {
  return useQuery({
    queryKey: dealKeys.stats(),
    queryFn: () => dealsAPI.getStats(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

// Search deals
export function useSearchDeals(
  query: string,
  filters?: Parameters<typeof dealsAPI.search>[1]
) {
  return useQuery({
    queryKey: [...dealKeys.all, 'search', query, filters],
    queryFn: () => dealsAPI.search(query, filters),
    staleTime: 30 * 1000, // 30 seconds
    enabled: query.length > 2, // Only search with 3+ characters
  })
}

// Mutations

// Create deal
export function useCreateDeal() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: dealsAPI.create,
    onSuccess: (newDeal) => {
      // Invalidate deals list
      queryClient.invalidateQueries({ queryKey: dealKeys.lists() })
      
      // Add to cache
      queryClient.setQueryData(
        dealKeys.intelligence(newDeal.dealId),
        newDeal
      )
    },
  })
}

// Update deal
export function useUpdateDeal(dealId: string) {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (updates: Parameters<typeof dealsAPI.update>[1]) =>
      dealsAPI.update(dealId, updates),
    onSuccess: (updatedDeal) => {
      // Update cache
      queryClient.setQueryData(
        dealKeys.intelligence(dealId),
        updatedDeal
      )
      
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: dealKeys.lists() })
      queryClient.invalidateQueries({ queryKey: dealKeys.stats() })
    },
  })
}

// Trigger MEDDPICC analysis
export function useTriggerAnalysis(dealId: string) {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: () => dealsAPI.triggerAnalysis(dealId),
    onSuccess: () => {
      // Optimistically update status to processing
      queryClient.setQueryData(
        dealKeys.intelligence(dealId),
        (old: DealIntelligence | undefined) => {
          if (!old) return old
          return {
            ...old,
            meddpiccAnalysis: {
              ...old.meddpiccAnalysis,
              processingStatus: {
                status: 'processing' as const,
                progress: 0,
                currentStep: 'Starting analysis...',
              }
            }
          }
        }
      )
      
      // Invalidate MEDDPICC query to refetch
      queryClient.invalidateQueries({ queryKey: dealKeys.meddpicc(dealId) })
    },
  })
}

// Upload transcript
export function useUploadTranscript(dealId: string) {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (params: {
      file: File
      metadata?: Parameters<typeof dealsAPI.uploadTranscript>[2]
    }) => dealsAPI.uploadTranscript(dealId, params.file, params.metadata),
    onSuccess: () => {
      // Invalidate evidence and intelligence queries
      queryClient.invalidateQueries({ queryKey: dealKeys.intelligence(dealId) })
      queryClient.invalidateQueries({ queryKey: dealKeys.timeline(dealId) })
    },
  })
}

// Real-time updates hook
export function useDealRealtime(dealId: string) {
  const queryClient = useQueryClient()
  
  return {
    subscribe: () => {
      const { ws, onUpdate, close } = dealsAPI.createDealWebSocket(dealId)
      
      onUpdate((update) => {
        switch (update.type) {
          case 'health_changed':
          case 'stage_changed':
            // Update intelligence cache
            queryClient.setQueryData(
              dealKeys.intelligence(dealId),
              (old: DealIntelligence | undefined) => {
                if (!old) return old
                return { ...old, ...update.data }
              }
            )
            break
            
          case 'evidence_added':
            // Invalidate evidence-related queries
            queryClient.invalidateQueries({ queryKey: dealKeys.intelligence(dealId) })
            queryClient.invalidateQueries({ queryKey: dealKeys.meddpicc(dealId) })
            break
            
          case 'analysis_complete':
            // Refresh MEDDPICC analysis
            queryClient.invalidateQueries({ queryKey: dealKeys.meddpicc(dealId) })
            queryClient.invalidateQueries({ queryKey: dealKeys.intelligence(dealId) })
            break
        }
      })
      
      return close
    }
  }
}