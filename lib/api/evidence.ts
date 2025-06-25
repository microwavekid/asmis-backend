// Evidence API

import { apiClient, transformDateStrings } from './client'
import type { Evidence } from '@/types/meddpicc'
import type { EvidenceFilters, EvidenceListResponse, EvidenceContext, EvidenceStats } from '@/types/evidence'

export const evidenceAPI = {
  // List evidence with filtering and pagination
  async list(
    dealId: string,
    filters: EvidenceFilters = {},
    options: {
      offset?: number
      limit?: number
      sortBy?: 'date' | 'confidence' | 'relevance'
      sortOrder?: 'asc' | 'desc'
    } = {}
  ): Promise<EvidenceListResponse> {
    const params = new URLSearchParams()
    params.append('dealId', dealId)
    
    // Add filters
    if (filters.types?.length) {
      filters.types.forEach(type => params.append('types', type))
    }
    if (filters.confidenceMin) params.append('confidenceMin', filters.confidenceMin.toString())
    if (filters.confidenceMax) params.append('confidenceMax', filters.confidenceMax.toString())
    if (filters.dateFrom) params.append('dateFrom', filters.dateFrom.toISOString())
    if (filters.dateTo) params.append('dateTo', filters.dateTo.toISOString())
    if (filters.categories?.length) {
      filters.categories.forEach(cat => params.append('categories', cat))
    }
    if (filters.sources?.length) {
      filters.sources.forEach(source => params.append('sources', source))
    }
    
    // Add options
    if (options.offset) params.append('offset', options.offset.toString())
    if (options.limit) params.append('limit', options.limit.toString())
    if (options.sortBy) params.append('sortBy', options.sortBy)
    if (options.sortOrder) params.append('sortOrder', options.sortOrder)
    
    const response = await apiClient.get<EvidenceListResponse>(
      `/api/evidence?${params.toString()}`
    )
    
    return {
      ...response,
      evidence: response.evidence.map(transformDateStrings)
    }
  },

  // Get specific evidence with full context
  async getContext(evidenceId: string): Promise<EvidenceContext> {
    const response = await apiClient.get<EvidenceContext>(
      `/api/evidence/${evidenceId}/context`
    )
    return transformDateStrings(response)
  },

  // Get evidence by category (for MEDDPICC)
  async getByCategory(
    dealId: string,
    category: 'metrics' | 'economic_buyer' | 'decision_criteria' | 'decision_process' | 'identify_pain' | 'champion' | 'competition'
  ): Promise<Evidence[]> {
    const response = await apiClient.get<{ evidence: Evidence[] }>(
      `/api/evidence/category/${category}?dealId=${dealId}`
    )
    return response.evidence.map(transformDateStrings)
  },

  // Search evidence
  async search(
    query: string,
    dealId?: string,
    filters?: EvidenceFilters
  ): Promise<Evidence[]> {
    const params = new URLSearchParams()
    params.append('q', query)
    if (dealId) params.append('dealId', dealId)
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined) {
          if (Array.isArray(value)) {
            value.forEach(v => params.append(key, v.toString()))
          } else {
            params.append(key, value.toString())
          }
        }
      })
    }
    
    const response = await apiClient.get<{ evidence: Evidence[] }>(
      `/api/evidence/search?${params.toString()}`
    )
    return response.evidence.map(transformDateStrings)
  },

  // Get evidence statistics
  async getStats(dealId: string): Promise<EvidenceStats> {
    return apiClient.get<EvidenceStats>(`/api/evidence/stats?dealId=${dealId}`)
  },

  // Add manual evidence/note
  async addNote(
    dealId: string,
    note: {
      content: string
      category?: string
      confidence?: number
      businessImplication?: string
    }
  ): Promise<Evidence> {
    const response = await apiClient.post<Evidence>(
      `/api/evidence/notes`,
      { dealId, ...note }
    )
    return transformDateStrings(response)
  },

  // Update evidence (e.g., mark as validated, update confidence)
  async update(
    evidenceId: string,
    updates: {
      confidence?: number
      businessImplication?: string
      validated?: boolean
    }
  ): Promise<Evidence> {
    const response = await apiClient.put<Evidence>(
      `/api/evidence/${evidenceId}`,
      updates
    )
    return transformDateStrings(response)
  },

  // Report evidence issue
  async reportIssue(
    evidenceId: string,
    issue: {
      type: 'incorrect' | 'misleading' | 'outdated' | 'other'
      description: string
    }
  ): Promise<{ reportId: string }> {
    return apiClient.post(`/api/evidence/${evidenceId}/report`, issue)
  },

  // Export evidence
  async export(
    dealId: string,
    format: 'json' | 'csv' | 'pdf',
    filters?: EvidenceFilters
  ): Promise<{ downloadUrl: string }> {
    const params = new URLSearchParams()
    params.append('dealId', dealId)
    params.append('format', format)
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined) {
          if (Array.isArray(value)) {
            value.forEach(v => params.append(key, v.toString()))
          } else {
            params.append(key, value.toString())
          }
        }
      })
    }
    
    return apiClient.post(`/api/evidence/export?${params.toString()}`)
  },

  // Get related evidence (evidence that appears in same sources)
  async getRelated(evidenceId: string, limit = 10): Promise<Evidence[]> {
    const response = await apiClient.get<{ evidence: Evidence[] }>(
      `/api/evidence/${evidenceId}/related?limit=${limit}`
    )
    return response.evidence.map(transformDateStrings)
  }
}

// Real-time evidence updates
export function createEvidenceWebSocket(dealId: string) {
  const ws = apiClient.createWebSocket(`/ws/evidence/${dealId}`)
  
  return {
    ws,
    onEvidenceAdded: (callback: (evidence: Evidence) => void) => {
      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          if (message.type === 'evidence_added') {
            callback(transformDateStrings(message.evidence))
          }
        } catch (error) {
          console.error('Failed to parse evidence WebSocket message:', error)
        }
      }
    },
    onEvidenceUpdated: (callback: (evidence: Evidence) => void) => {
      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          if (message.type === 'evidence_updated') {
            callback(transformDateStrings(message.evidence))
          }
        } catch (error) {
          console.error('Failed to parse evidence WebSocket message:', error)
        }
      }
    },
    close: () => ws.close()
  }
}