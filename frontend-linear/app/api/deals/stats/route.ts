import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Mock stats data
    const stats = {
      totalDeals: 2,
      totalValue: 430000,
      averageHealth: 78,
      dealsAtRisk: 0,
      byStage: {
        'technical_evaluation': 1,
        'negotiation': 1
      }
    }

    return NextResponse.json(stats)
  } catch (error) {
    console.error('Error in deals stats API:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}