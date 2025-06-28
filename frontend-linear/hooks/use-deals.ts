"use client"

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { dealsAPI } from '@/lib/api/deals'
import type { Deal } from '@/components/intelligence/deals-table'
import type { MEDDPICCAnalysis, Evidence } from '@/types/meddpicc'

// Hook for deals list
export function useDeals(params?: {
  stage?: string
  healthMin?: number
  limit?: number
  offset?: number
}) {
  return useQuery({
    queryKey: ['deals', params],
    queryFn: () => dealsAPI.list(params),
    staleTime: 30000, // 30 seconds
    refetchOnWindowFocus: false,
  })
}

// Hook for deal statistics
export function useDealsStats() {
  return useQuery({
    queryKey: ['deals-stats'],
    queryFn: () => dealsAPI.getStats(),
    staleTime: 60000, // 1 minute
    refetchOnWindowFocus: false,
  })
}

// Hook for specific deal MEDDPICC analysis
export function useDealMEDDPICC(dealId: string | null) {
  return useQuery({
    queryKey: ['deal-meddpicc', dealId],
    queryFn: () => dealId ? dealsAPI.getMEDDPICC(dealId) : null,
    enabled: !!dealId,
    staleTime: 60000, // 1 minute
    refetchOnWindowFocus: false,
  })
}

// Hook for deal evidence
export function useDealEvidence(dealId: string | null) {
  return useQuery({
    queryKey: ['deal-evidence', dealId],
    queryFn: () => dealId ? dealsAPI.getEvidence(dealId) : null,
    enabled: !!dealId,
    staleTime: 60000, // 1 minute
    refetchOnWindowFocus: false,
  })
}

// Hook for triggering deal analysis
export function useTriggerAnalysis() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ dealId, file }: { dealId: string; file: File }) =>
      dealsAPI.triggerAnalysis(dealId, file),
    onSuccess: (data, variables) => {
      // Invalidate related queries to refetch fresh data
      queryClient.invalidateQueries({ queryKey: ['deal-meddpicc', variables.dealId] })
      queryClient.invalidateQueries({ queryKey: ['deal-evidence', variables.dealId] })
      queryClient.invalidateQueries({ queryKey: ['deals'] })
    },
  })
}

// Hook for real-time deal updates (WebSocket)
export function useDealUpdates(dealId: string | null) {
  const queryClient = useQueryClient()
  
  // This would typically use useEffect to set up WebSocket connection
  // For now, we'll just return a placeholder
  return {
    isConnected: false,
    connectionStatus: 'disconnected' as const,
    lastUpdate: null,
  }
}