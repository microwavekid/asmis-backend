import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // For now, return mock data since backend is not running
    const mockResponse = {
      deals: [
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
            lastCalculated: new Date().toISOString()
          },
          momentum: {
            velocity: "accelerating",
            daysSinceLastActivity: 2,
            activitiesLast30Days: 15,
            engagementLevel: "high",
            keyMilestones: [
              { name: "Technical Demo", completed: true, completedAt: new Date().toISOString() },
              { name: "Security Review", completed: false, dueDate: new Date().toISOString() }
            ]
          },
          meddpiccAnalysis: {
            dealId: "deal_1",
            accountId: "acc_1",
            overallScore: 85,
            completenessScore: 78,
            lastUpdated: new Date().toISOString(),
            processingStatus: {
              status: "complete",
              progress: 100
            },
            metrics: {
              status: "complete",
              confidence: 90,
              evidence: [],
              lastUpdated: new Date().toISOString(),
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
              lastUpdated: new Date().toISOString(),
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
              lastUpdated: new Date().toISOString(),
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
              lastUpdated: new Date().toISOString(),
              steps: [
                { name: "Technical evaluation", owner: "CTO", timeline: "2 weeks", status: "in_progress" },
                { name: "Business case review", owner: "CFO", timeline: "1 week", status: "upcoming" }
              ],
              timelineIdentified: true,
              estimatedCloseDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
            },
            identifyPain: {
              status: "complete",
              confidence: 90,
              evidence: [],
              lastUpdated: new Date().toISOString(),
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
              lastUpdated: new Date().toISOString(),
              identified: true,
              person: {
                name: "Alex Chen",
                title: "VP Engineering",
                email: "alex.chen@optimizely.com"
              },
              strength: "strong",
              influence: "high",
              engagement: {
                lastContact: new Date().toISOString(),
                frequency: "weekly",
                quality: "proactive"
              }
            },
            competition: {
              status: "partial",
              confidence: 70,
              evidence: [],
              lastUpdated: new Date().toISOString(),
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
              createdAt: new Date().toISOString()
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
          createdAt: new Date().toISOString(),
          lastUpdated: new Date().toISOString()
        }
      ],
      total: 1,
      offset: 0,
      limit: 50,
      hasMore: false
    }

    return NextResponse.json(mockResponse)
  } catch (error) {
    console.error('Error in deals API:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}