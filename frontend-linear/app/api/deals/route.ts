import { NextRequest, NextResponse } from 'next/server'

const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'

export async function GET(request: NextRequest) {
  try {
    // Fetch from backend
    const response = await fetch(`${backendUrl}/api/v1/deals/`)
    
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`)
    }
    
    const backendDeals = await response.json()
    
    // Transform backend response to match frontend expectations
    const transformedData = {
      deals: backendDeals.map((deal: any) => ({
        // Core fields
        dealId: deal.id,
        dealName: deal.name,
        accountId: deal.id, // Using deal ID temporarily
        accountName: deal.account,
        dealValue: deal.value,
        stage: deal.stage || 'discovery',
        
        // Health data
        health: {
          score: deal.health || 0,
          trend: 'stable',
          factors: {
            positive: [],
            negative: [],
            neutral: []
          },
          lastCalculated: new Date().toISOString()
        },
        
        // Momentum data
        momentum: {
          velocity: 'steady',
          daysSinceLastActivity: 0,
          activitiesLast30Days: 0,
          engagementLevel: 'medium',
          keyMilestones: []
        },
        
        // MEDDPICC analysis
        meddpiccAnalysis: {
          dealId: deal.id,
          accountId: deal.id,
          overallScore: deal.meddpiccScore || 0,
          completenessScore: 0,
          lastUpdated: new Date().toISOString(),
          processingStatus: {
            status: deal.meddpiccScore > 0 ? 'complete' : 'not_started',
            progress: deal.meddpiccScore > 0 ? 100 : 0
          },
          metrics: { status: 'missing', confidence: 0, evidence: [], lastUpdated: new Date().toISOString() },
          economicBuyer: { status: 'missing', confidence: 0, evidence: [], lastUpdated: new Date().toISOString() },
          decisionCriteria: { status: 'missing', confidence: 0, evidence: [], lastUpdated: new Date().toISOString() },
          decisionProcess: { status: 'missing', confidence: 0, evidence: [], lastUpdated: new Date().toISOString() },
          identifyPain: { status: 'missing', confidence: 0, evidence: [], lastUpdated: new Date().toISOString() },
          champion: { status: 'missing', confidence: 0, evidence: [], lastUpdated: new Date().toISOString() },
          competition: { status: 'missing', confidence: 0, evidence: [], lastUpdated: new Date().toISOString() },
          keyInsights: [],
          riskFactors: [],
          recommendations: []
        },
        
        // Actions and opportunities
        nextActions: deal.nextActions || [],
        opportunities: [],
        
        // Processing queue
        processingQueue: {
          items: [],
          activeCount: 0,
          queuedCount: 0,
          completedCount: 0,
          failedCount: 0
        },
        
        // Timeline and metadata
        timeline: [],
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString()
      })),
      total: backendDeals.length,
      offset: 0,
      limit: 50,
      hasMore: false
    }
    
    return NextResponse.json(transformedData)
    
  } catch (error) {
    console.error('Error fetching from backend:', error)
    
    // Return fallback mock data
    return NextResponse.json({
      deals: [],
      total: 0,
      offset: 0,
      limit: 50,
      hasMore: false
    })
  }
}