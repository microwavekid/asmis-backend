// Deal Intelligence API

import { apiClient, transformDateStrings } from './client'
import type { DealIntelligence, TimelineEvent } from '@/types/intelligence'
import type { MEDDPICCAnalysis } from '@/types/meddpicc'

export interface DealsListParams {
  accountId?: string
  stage?: string
  healthMin?: number
  limit?: number
  offset?: number
  sortBy?: 'health' | 'value' | 'closeDate' | 'lastUpdated'
  sortOrder?: 'asc' | 'desc'
}

export interface DealsListResponse {
  deals: DealIntelligence[]
  total: number
  offset: number
  limit: number
  hasMore: boolean
}

export const dealsAPI = {
  // Get all deals with filtering
  async list(params: DealsListParams = {}): Promise<DealsListResponse> {
    const searchParams = new URLSearchParams()
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value.toString())
      }
    })
    
    const response = await apiClient.get<DealsListResponse>(
      `/api/deals?${searchParams.toString()}`
    )
    
    return {
      ...response,
      deals: response.deals.map(transformDateStrings)
    }
  },

  // Get specific deal intelligence
  async getIntelligence(dealId: string): Promise<DealIntelligence> {
    const response = await apiClient.get<DealIntelligence>(
      `/api/deals/${dealId}/intelligence`
    )
    return transformDateStrings(response)
  },

  // Get MEDDPICC analysis for a deal
  async getMEDDPICC(dealId: string): Promise<MEDDPICCAnalysis> {
    const response = await apiClient.get<MEDDPICCAnalysis>(
      `/api/deals/${dealId}/meddpicc`
    )
    return transformDateStrings(response)
  },

  // Get deal timeline
  async getTimeline(dealId: string, limit = 50): Promise<TimelineEvent[]> {
    const response = await apiClient.get<{ events: TimelineEvent[] }>(
      `/api/deals/${dealId}/timeline?limit=${limit}`
    )
    return response.events.map(transformDateStrings)
  },

  // Create new deal
  async create(dealData: {
    name: string
    accountId: string
    value?: number
    expectedCloseDate?: string
    stage?: string
  }): Promise<DealIntelligence> {
    const response = await apiClient.post<DealIntelligence>(
      '/api/deals',
      dealData
    )
    return transformDateStrings(response)
  },

  // Update deal
  async update(
    dealId: string, 
    updates: Partial<{
      name: string
      value: number
      expectedCloseDate: string
      stage: string
    }>
  ): Promise<DealIntelligence> {
    const response = await apiClient.put<DealIntelligence>(
      `/api/deals/${dealId}`,
      updates
    )
    return transformDateStrings(response)
  },

  // Trigger MEDDPICC analysis
  async triggerAnalysis(dealId: string): Promise<{ jobId: string }> {
    return apiClient.post(`/api/deals/${dealId}/analyze`)
  },

  // Upload transcript for deal
  async uploadTranscript(
    dealId: string,
    file: File,
    metadata?: {
      title?: string
      meetingDate?: string
      attendees?: string[]
    }
  ): Promise<{ transcriptId: string; processingJobId: string }> {
    return apiClient.uploadFile(
      `/api/deals/${dealId}/transcripts`,
      file,
      metadata ? { metadata: JSON.stringify(metadata) } : undefined
    )
  },

  // Get deal stats/summary
  async getStats(): Promise<{
    totalDeals: number
    totalValue: number
    averageHealth: number
    dealsAtRisk: number
    byStage: Record<string, number>
  }> {
    return apiClient.get('/api/deals/stats')
  },

  // Search deals
  async search(query: string, filters?: {
    accountIds?: string[]
    stages?: string[]
    minValue?: number
    maxValue?: number
  }): Promise<DealIntelligence[]> {
    const params = { q: query, ...filters }
    const searchParams = new URLSearchParams()
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        if (Array.isArray(value)) {
          value.forEach(v => searchParams.append(key, v.toString()))
        } else {
          searchParams.append(key, value.toString())
        }
      }
    })
    
    const response = await apiClient.get<{ deals: DealIntelligence[] }>(
      `/api/deals/search?${searchParams.toString()}`
    )
    
    return response.deals.map(transformDateStrings)
  }
}

// WebSocket hook for real-time deal updates
export function createDealWebSocket(dealId: string) {
  const ws = apiClient.createWebSocket(`/ws/deals/${dealId}`)
  
  return {
    ws,
    onUpdate: (callback: (update: {
      type: 'health_changed' | 'stage_changed' | 'evidence_added' | 'analysis_complete'
      data: any
    }) => void) => {
      ws.onmessage = (event) => {
        try {
          const update = JSON.parse(event.data)
          callback(transformDateStrings(update))
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }
    },
    close: () => ws.close()
  }
}