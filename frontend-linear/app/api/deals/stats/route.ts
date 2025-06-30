import { NextResponse } from 'next/server'

const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'

export async function GET() {
  try {
    const res = await fetch(`${backendUrl}/api/v1/deals/stats`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    if (!res.ok) {
      throw new Error(`Backend returned status ${res.status}`)
    }
    const data = await res.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error proxying to backend (deals stats):', error)
    // Fallback to mock stats data if backend is unavailable
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
  }
}