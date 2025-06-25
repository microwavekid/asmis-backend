// React Query hooks for evidence data

import React from 'react'
import { useQuery, useMutation, useQueryClient, useInfiniteQuery } from '@tanstack/react-query'
import { evidenceAPI } from '@/lib/api/evidence'
import type { Evidence } from '@/types/meddpicc'
import type { EvidenceFilters, EvidenceStats } from '@/types/evidence'

// Query keys for cache management
export const evidenceKeys = {
  all: ['evidence'] as const,
  lists: () => [...evidenceKeys.all, 'list'] as const,
  list: (dealId: string, filters: EvidenceFilters) => 
    [...evidenceKeys.lists(), dealId, filters] as const,
  details: () => [...evidenceKeys.all, 'detail'] as const,
  detail: (id: string) => [...evidenceKeys.details(), id] as const,
  context: (id: string) => [...evidenceKeys.detail(id), 'context'] as const,
  category: (dealId: string, category: string) => 
    [...evidenceKeys.all, 'category', dealId, category] as const,
  stats: (dealId: string) => [...evidenceKeys.all, 'stats', dealId] as const,
  search: (query: string, dealId?: string, filters?: EvidenceFilters) =>
    [...evidenceKeys.all, 'search', query, dealId, filters] as const,
  related: (id: string) => [...evidenceKeys.detail(id), 'related'] as const,
}

// Get evidence list with pagination
export function useEvidence(
  dealId: string,
  filters: EvidenceFilters = {},
  options: {
    sortBy?: 'date' | 'confidence' | 'relevance'
    sortOrder?: 'asc' | 'desc'
  } = {}
) {
  return useInfiniteQuery({
    queryKey: evidenceKeys.list(dealId, filters),
    queryFn: ({ pageParam = 0 }) =>
      evidenceAPI.list(dealId, filters, {
        offset: pageParam,
        limit: 20,
        ...options,
      }),
    getNextPageParam: (lastPage) => lastPage.hasMore ? lastPage.nextOffset : undefined,
    staleTime: 30 * 1000, // 30 seconds
    enabled: !!dealId,
  })
}

// Get evidence context
export function useEvidenceContext(evidenceId: string) {
  return useQuery({
    queryKey: evidenceKeys.context(evidenceId),
    queryFn: () => evidenceAPI.getContext(evidenceId),
    staleTime: 5 * 60 * 1000, // 5 minutes (context doesn't change often)
    enabled: !!evidenceId,
  })
}

// Get evidence by MEDDPICC category
export function useEvidenceByCategory(
  dealId: string,
  category: 'metrics' | 'economic_buyer' | 'decision_criteria' | 'decision_process' | 'identify_pain' | 'champion' | 'competition'
) {
  return useQuery({
    queryKey: evidenceKeys.category(dealId, category),
    queryFn: () => evidenceAPI.getByCategory(dealId, category),
    staleTime: 1 * 60 * 1000, // 1 minute
    enabled: !!dealId && !!category,
  })
}

// Search evidence
export function useSearchEvidence(
  query: string,
  dealId?: string,
  filters?: EvidenceFilters
) {
  return useQuery({
    queryKey: evidenceKeys.search(query, dealId, filters),
    queryFn: () => evidenceAPI.search(query, dealId, filters),
    staleTime: 30 * 1000, // 30 seconds
    enabled: query.length > 2, // Only search with 3+ characters
  })
}

// Get evidence statistics
export function useEvidenceStats(dealId: string) {
  return useQuery({
    queryKey: evidenceKeys.stats(dealId),
    queryFn: () => evidenceAPI.getStats(dealId),
    staleTime: 2 * 60 * 1000, // 2 minutes
    enabled: !!dealId,
  })
}

// Get related evidence
export function useRelatedEvidence(evidenceId: string, limit = 10) {
  return useQuery({
    queryKey: [...evidenceKeys.related(evidenceId), limit],
    queryFn: () => evidenceAPI.getRelated(evidenceId, limit),
    staleTime: 5 * 60 * 1000, // 5 minutes
    enabled: !!evidenceId,
  })
}

// Mutations

// Add manual note
export function useAddNote(dealId: string) {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (note: Parameters<typeof evidenceAPI.addNote>[1]) =>
      evidenceAPI.addNote(dealId, note),
    onSuccess: (newEvidence) => {
      // Invalidate evidence lists
      queryClient.invalidateQueries({ queryKey: evidenceKeys.lists() })
      queryClient.invalidateQueries({ queryKey: evidenceKeys.stats(dealId) })
      
      // Add to cache
      queryClient.setQueryData(
        evidenceKeys.detail(newEvidence.id),
        newEvidence
      )
    },
  })
}

// Update evidence
export function useUpdateEvidence() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ 
      evidenceId, 
      updates 
    }: {
      evidenceId: string
      updates: Parameters<typeof evidenceAPI.update>[1]
    }) => evidenceAPI.update(evidenceId, updates),
    onSuccess: (updatedEvidence) => {
      // Update cache
      queryClient.setQueryData(
        evidenceKeys.detail(updatedEvidence.id),
        updatedEvidence
      )
      
      // Invalidate lists that might contain this evidence
      queryClient.invalidateQueries({ queryKey: evidenceKeys.lists() })
    },
  })
}

// Report evidence issue
export function useReportEvidenceIssue() {
  return useMutation({
    mutationFn: ({ 
      evidenceId, 
      issue 
    }: {
      evidenceId: string
      issue: Parameters<typeof evidenceAPI.reportIssue>[1]
    }) => evidenceAPI.reportIssue(evidenceId, issue),
  })
}

// Export evidence
export function useExportEvidence() {
  return useMutation({
    mutationFn: ({ 
      dealId, 
      format, 
      filters 
    }: {
      dealId: string
      format: 'json' | 'csv' | 'pdf'
      filters?: EvidenceFilters
    }) => evidenceAPI.export(dealId, format, filters),
    onSuccess: (response) => {
      // Trigger download
      window.open(response.downloadUrl, '_blank')
    },
  })
}

// Real-time evidence updates
export function useEvidenceRealtime(dealId: string) {
  const queryClient = useQueryClient()
  
  return {
    subscribe: () => {
      const { ws, onEvidenceAdded, onEvidenceUpdated, close } = 
        evidenceAPI.createEvidenceWebSocket(dealId)
      
      onEvidenceAdded((evidence) => {
        // Add to cache optimistically
        queryClient.setQueryData(
          evidenceKeys.detail(evidence.id),
          evidence
        )
        
        // Invalidate lists to show new evidence
        queryClient.invalidateQueries({ queryKey: evidenceKeys.lists() })
        queryClient.invalidateQueries({ queryKey: evidenceKeys.stats(dealId) })
      })
      
      onEvidenceUpdated((evidence) => {
        // Update cache
        queryClient.setQueryData(
          evidenceKeys.detail(evidence.id),
          evidence
        )
        
        // Invalidate lists that might show this evidence
        queryClient.invalidateQueries({ queryKey: evidenceKeys.lists() })
      })
      
      return close
    }
  }
}

// Custom hook for evidence filtering
export function useEvidenceFilters(initialFilters: EvidenceFilters = {}) {
  const [filters, setFilters] = React.useState<EvidenceFilters>(initialFilters)
  
  const updateFilter = <K extends keyof EvidenceFilters>(
    key: K,
    value: EvidenceFilters[K]
  ) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }
  
  const clearFilters = () => {
    setFilters({})
  }
  
  const hasActiveFilters = Object.values(filters).some(value => 
    value !== undefined && 
    value !== null && 
    (!Array.isArray(value) || value.length > 0)
  )
  
  return {
    filters,
    updateFilter,
    clearFilters,
    hasActiveFilters,
    setFilters,
  }
}