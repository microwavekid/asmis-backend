// Deal Intelligence API

import { apiClient, transformDateStrings } from './client'
import type { DealIntelligence, TimelineEvent } from '@/types/intelligence'
import type { MEDDPICCAnalysis, Evidence } from '@/types/meddpicc'

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
    try {
      const searchParams = new URLSearchParams()
      
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString())
        }
      })
      
      // Use fetch directly for Next.js API routes
      const response = await fetch(`/api/deals?${searchParams.toString()}`)
      if (!response.ok) {
        throw new Error(`API returned ${response.status}`)
      }
      const data = await response.json() as DealsListResponse
      
      return {
        ...data,
        deals: data.deals.map(transformDateStrings)
      }
    } catch (error) {
      // Fallback to mock data when API is unavailable
      console.warn('API unavailable, using mock data:', error)
      return getMockDealsData(params)
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
    const response = await fetch(`/api/deals/${dealId}/meddpicc`)
    if (!response.ok) {
      throw new Error(`API returned ${response.status}`)
    }
    const data = await response.json()
    return transformDateStrings(data)
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

  // Get deal evidence
  async getEvidence(dealId: string): Promise<Evidence[]> {
    return apiClient.get(`/api/deals/${dealId}/evidence`)
  },

  // Trigger analysis for a deal
  async triggerAnalysis(dealId: string, file: File): Promise<{ 
    message: string
    jobId: string 
    analysisResult: any 
  }> {
    return apiClient.uploadFile(`/api/deals/${dealId}/analyze`, file)
  },

  // Get deal stats/summary
  async getStats(): Promise<{
    totalDeals: number
    totalValue: number
    averageHealth: number
    dealsAtRisk: number
    byStage: Record<string, number>
  }> {
    try {
      const response = await fetch('/api/deals/stats')
      if (!response.ok) {
        throw new Error(`API returned ${response.status}`)
      }
      return response.json()
    } catch (error) {
      console.warn('API unavailable, using mock stats:', error)
      return {
        totalDeals: 2,
        totalValue: 430000,
        averageHealth: 78,
        dealsAtRisk: 0,
        byStage: {
          'technical_evaluation': 1,
          'negotiation': 1
        }
      }
    }
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

// Mock data fallback
function getMockDealsData(params: DealsListParams = {}): DealsListResponse {
  const mockDeals: DealIntelligence[] = [
    {
      accountId: "acc_1",
      accountName: "Optimizely Inc",
      dealId: "deal_1",
      dealName: "Q4 Implementation",
      dealValue: 150000,
      stage: "technical_evaluation",
      health: {
        score: 85,
        trend: "improving",
        factors: {
          positive: ["Strong champion", "Clear decision criteria"],
          negative: ["Technical concerns"],
          neutral: ["Budget approved"]
        },
        lastCalculated: new Date()
      },
      momentum: {
        velocity: "accelerating",
        daysSinceLastActivity: 2,
        activitiesLast30Days: 15,
        engagementLevel: "high",
        keyMilestones: [
          { name: "Technical Demo", completed: true, completedAt: new Date() },
          { name: "Security Review", completed: false, dueDate: new Date() }
        ]
      },
      meddpiccAnalysis: {
        dealId: "deal_1",
        accountId: "acc_1",
        overallScore: 85,
        completenessScore: 78,
        lastUpdated: new Date(),
        processingStatus: {
          status: "complete",
          progress: 100
        },
        metrics: {
          status: "complete",
          confidence: 90,
          evidence: [],
          lastUpdated: new Date(),
          identifiedMetrics: [
            { type: "cost_reduction", value: "25% reduction in processing time", target: "Q1 2025", timeline: "3 months" }
          ],
          quantified: true,
          businessImpact: "Significant cost savings and efficiency gains"
        },
        economicBuyer: {
          status: "complete",
          confidence: 85,
          evidence: [],
          lastUpdated: new Date(),
          identified: true,
          person: {
            name: "Sarah Johnson",
            title: "CFO",
            email: "sarah.johnson@optimizely.com"
          },
          accessLevel: "through_champion",
          buyingAuthority: "confirmed"
        },
        decisionCriteria: {
          status: "complete",
          confidence: 80,
          evidence: [],
          lastUpdated: new Date(),
          criteria: [
            { category: "technical", requirement: "Cloud-native architecture", priority: "must_have", ourPosition: "meets" },
            { category: "business", requirement: "ROI within 12 months", priority: "must_have", ourPosition: "meets" }
          ],
          formalRequirements: true,
          evaluationProcess: "RFP with technical and business evaluation phases"
        },
        decisionProcess: {
          status: "partial",
          confidence: 75,
          evidence: [],
          lastUpdated: new Date(),
          steps: [
            { name: "Technical evaluation", owner: "CTO", timeline: "2 weeks", status: "in_progress" },
            { name: "Business case review", owner: "CFO", timeline: "1 week", status: "upcoming" }
          ],
          timelineIdentified: true,
          estimatedCloseDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
        },
        identifyPain: {
          status: "complete",
          confidence: 90,
          evidence: [],
          lastUpdated: new Date(),
          pains: [
            { description: "Manual processes causing delays", impact: "high", currentState: "90% manual", desiredState: "80% automated", costOfInaction: "$50k quarterly loss" }
          ],
          urgency: "quarterly",
          businessDrivers: ["Digital transformation", "Cost reduction"]
        },
        champion: {
          status: "complete",
          confidence: 95,
          evidence: [],
          lastUpdated: new Date(),
          identified: true,
          person: {
            name: "Alex Chen",
            title: "VP Engineering",
            email: "alex.chen@optimizely.com"
          },
          strength: "strong",
          influence: "high",
          engagement: {
            lastContact: new Date(),
            frequency: "weekly",
            quality: "proactive"
          }
        },
        competition: {
          status: "partial",
          confidence: 70,
          evidence: [],
          lastUpdated: new Date(),
          competitors: [
            { name: "CompetitorX", status: "evaluating", strengths: ["Lower price"], weaknesses: ["Limited features"], ourAdvantages: ["Better integration"] }
          ],
          competitiveLandscape: "competitive",
          differentiators: ["Superior API", "Better support"]
        },
        keyInsights: [],
        riskFactors: [],
        recommendations: []
      },
      nextActions: [
        {
          id: "action_1",
          type: "call",
          priority: "high",
          title: "Follow up on technical questions",
          description: "Address remaining technical concerns from evaluation",
          suggestedBy: "ai",
          status: "pending",
          createdAt: new Date()
        }
      ],
      opportunities: [],
      processingQueue: {
        items: [],
        activeCount: 0,
        queuedCount: 0,
        completedCount: 5,
        failedCount: 0
      },
      timeline: [],
      createdAt: new Date(),
      lastUpdated: new Date()
    },
    {
      accountId: "acc_2",
      accountName: "Salesforce Corp",
      dealId: "deal_2", 
      dealName: "Enterprise Expansion",
      dealValue: 280000,
      stage: "negotiation",
      health: {
        score: 72,
        trend: "stable",
        factors: {
          positive: ["Budget confirmed"],
          negative: ["Competition present"],
          neutral: ["Timeline uncertain"]
        },
        lastCalculated: new Date()
      },
      momentum: {
        velocity: "steady",
        daysSinceLastActivity: 5,
        activitiesLast30Days: 8,
        engagementLevel: "medium",
        keyMilestones: [
          { name: "Proposal Submitted", completed: true, completedAt: new Date() },
          { name: "Contract Review", completed: false, dueDate: new Date() }
        ]
      },
      meddpiccAnalysis: {
        dealId: "deal_2",
        accountId: "acc_2",
        overallScore: 72,
        completenessScore: 82,
        lastUpdated: new Date(),
        processingStatus: {
          status: "complete",
          progress: 100
        },
        metrics: {
          status: "partial",
          confidence: 75,
          evidence: [],
          lastUpdated: new Date(),
          identifiedMetrics: [
            { type: "revenue", value: "15% revenue increase", target: "2025", timeline: "6 months" }
          ],
          quantified: false,
          businessImpact: "Revenue growth potential identified but not fully quantified"
        },
        economicBuyer: {
          status: "complete",
          confidence: 80,
          evidence: [],
          lastUpdated: new Date(),
          identified: true,
          person: {
            name: "Michael Torres",
            title: "VP Finance",
            email: "michael.torres@salesforce.com"
          },
          accessLevel: "direct",
          buyingAuthority: "likely"
        },
        decisionCriteria: {
          status: "complete",
          confidence: 85,
          evidence: [],
          lastUpdated: new Date(),
          criteria: [
            { category: "technical", requirement: "Salesforce integration", priority: "must_have", ourPosition: "meets" },
            { category: "financial", requirement: "Under $300k budget", priority: "must_have", ourPosition: "meets" }
          ],
          formalRequirements: true,
          evaluationProcess: "Internal evaluation with vendor comparison"
        },
        decisionProcess: {
          status: "partial",
          confidence: 70,
          evidence: [],
          lastUpdated: new Date(),
          steps: [
            { name: "Proposal review", owner: "VP Finance", timeline: "1 week", status: "completed" },
            { name: "Contract negotiation", owner: "Legal", timeline: "2 weeks", status: "in_progress" }
          ],
          timelineIdentified: false,
          estimatedCloseDate: new Date(Date.now() + 45 * 24 * 60 * 60 * 1000)
        },
        identifyPain: {
          status: "partial",
          confidence: 65,
          evidence: [],
          lastUpdated: new Date(),
          pains: [
            { description: "Data silos affecting reporting", impact: "medium", currentState: "Fragmented data", desiredState: "Unified reporting", costOfInaction: "Unknown" }
          ],
          urgency: "annual",
          businessDrivers: ["Data consolidation"]
        },
        champion: {
          status: "partial",
          confidence: 60,
          evidence: [],
          lastUpdated: new Date(),
          identified: true,
          person: {
            name: "Jennifer Wu",
            title: "Director Operations", 
            email: "jennifer.wu@salesforce.com"
          },
          strength: "developing",
          influence: "medium",
          engagement: {
            lastContact: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
            frequency: "monthly",
            quality: "responsive"
          }
        },
        competition: {
          status: "partial",
          confidence: 55,
          evidence: [],
          lastUpdated: new Date(),
          competitors: [
            { name: "CompetitorY", status: "incumbent", strengths: ["Existing relationship"], weaknesses: ["Outdated technology"], ourAdvantages: ["Modern platform"] },
            { name: "CompetitorZ", status: "evaluating", strengths: ["Lower cost"], weaknesses: ["Limited features"], ourAdvantages: ["Full feature set"] }
          ],
          competitiveLandscape: "disadvantaged",
          differentiators: ["Advanced analytics", "Better user experience"]
        },
        keyInsights: [],
        riskFactors: [],
        recommendations: []
      },
      nextActions: [
        {
          id: "action_2",
          type: "meeting",
          priority: "medium",
          title: "Schedule stakeholder alignment call",
          description: "Align all stakeholders on proposal",
          suggestedBy: "ai",
          status: "pending",
          createdAt: new Date()
        }
      ],
      opportunities: [],
      processingQueue: {
        items: [],
        activeCount: 0,
        queuedCount: 0,
        completedCount: 3,
        failedCount: 0
      },
      timeline: [],
      createdAt: new Date(),
      lastUpdated: new Date()
    }
  ]

  return {
    deals: mockDeals,
    total: mockDeals.length,
    offset: params.offset || 0,
    limit: params.limit || 50,
    hasMore: false
  }
}