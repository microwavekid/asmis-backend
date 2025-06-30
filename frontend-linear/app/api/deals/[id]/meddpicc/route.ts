import { NextRequest, NextResponse } from 'next/server'

const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const response = await fetch(`${backendUrl}/api/v1/deals/${id}/meddpicc`)
    
    if (!response.ok) {
      // Return a properly structured MEDDPICC analysis when no analysis exists
      return NextResponse.json({
        dealId: id,
        accountId: id,
        overallScore: 0,
        completenessScore: 0,
        lastUpdated: new Date().toISOString(),
        processingStatus: {
          status: 'not_started',
          progress: 0,
          message: 'No analysis performed yet. Upload a transcript to begin.'
        },
        components: {
          metrics: { 
            status: 'not_started', 
            confidence: 0, 
            evidence: [],
            gaps: ['No metrics identified', 'ROI not quantified', 'Business impact unknown'],
            lastUpdated: new Date().toISOString(),
            score: 0
          },
          economicBuyer: { 
            status: 'not_started', 
            confidence: 0, 
            evidence: [],
            gaps: ['Economic buyer not identified', 'Decision authority unclear'],
            lastUpdated: new Date().toISOString(),
            score: 0
          },
          decisionCriteria: { 
            status: 'not_started', 
            confidence: 0, 
            evidence: [],
            gaps: ['Decision criteria unknown', 'Evaluation process unclear'],
            lastUpdated: new Date().toISOString(),
            score: 0
          },
          decisionProcess: { 
            status: 'not_started', 
            confidence: 0, 
            evidence: [],
            gaps: ['Decision process not mapped', 'Timeline unknown'],
            lastUpdated: new Date().toISOString(),
            score: 0
          },
          identifyPain: { 
            status: 'not_started', 
            confidence: 0, 
            evidence: [],
            gaps: ['Pain points not identified', 'Urgency unclear'],
            lastUpdated: new Date().toISOString(),
            score: 0
          },
          champion: { 
            status: 'not_started', 
            confidence: 0, 
            evidence: [],
            gaps: ['Champion not identified', 'Internal support unknown'],
            lastUpdated: new Date().toISOString(),
            score: 0
          },
          competition: { 
            status: 'not_started', 
            confidence: 0, 
            evidence: [],
            gaps: ['Competitive landscape unknown', 'Alternatives unclear'],
            lastUpdated: new Date().toISOString(),
            score: 0
          }
        },
        keyInsights: [],
        riskFactors: [],
        recommendations: [
          {
            priority: 'high',
            action: 'Upload meeting transcript or notes',
            rationale: 'MEDDPICC analysis requires conversation data',
            timeframe: 'Next action'
          }
        ],
        strategic_recommendations: [
          'Upload meeting transcript or notes to begin MEDDPICC analysis',
          'Schedule discovery call to gather qualification data',
          'Identify key stakeholders and decision makers',
          'Document current pain points and business drivers'
        ]
      })
    }
    
    const data = await response.json()
    
    // Transform backend data to match frontend expectations
    const transformedData = {
      ...data,
      overallScore: data.overallScore || data.overall_score || 0,
      strategic_recommendations: data.strategic_recommendations || [],
      riskFactors: data.riskFactors || [],
      components: data.components || {}
    }
    
    return NextResponse.json(transformedData)
    
  } catch (error) {
    console.error('Error fetching MEDDPICC analysis:', error)
    
    // Return minimal structure as fallback
    return NextResponse.json({
      dealId: 'unknown',
      accountId: 'unknown',
      overallScore: 0,
      completenessScore: 0,
      lastUpdated: new Date().toISOString(),
      components: {},
      processingStatus: {
        status: 'error',
        progress: 0,
        message: 'Failed to load analysis'
      },
      keyInsights: [],
      riskFactors: [],
      recommendations: [],
      strategic_recommendations: []
    })
  }
}