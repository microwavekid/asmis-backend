"use client"

import React, { useState, useMemo } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { 
  Target, 
  TrendingUp, 
  Clock, 
  AlertTriangle,
  CheckCircle,
  ExternalLink,
  Brain,
  Plus
} from "lucide-react"

import { DealsTable, type Deal } from "@/components/intelligence/deals-table"
import { DealsFilters, type FilterState } from "@/components/intelligence/deals-filters"
import { MEDDPICCModal } from "@/components/intelligence/meddpicc-modal"
import { ViewsDropdown } from "@/components/intelligence/views-dropdown"
import type { MEDDPICCAnalysis, Evidence } from "@/types/meddpicc"

// Mock MEDDPICC analysis data
const mockMEDDPICCData: Record<string, MEDDPICCAnalysis> = {
  d1: {
    overall_score: 78,
    confidence_score: 85,
    components: {
      metrics: { score: 85, confidence: 90, status: "identified", details: "ROI metrics clearly defined: 40% cost reduction, 6-month payback", gaps: [] },
      economic_buyer: { score: 60, confidence: 70, status: "suspected", details: "CTO involved but CFO approval needed", gaps: ["Need direct access to CFO", "Budget authority unclear"] },
      decision_criteria: { score: 90, confidence: 95, status: "identified", details: "Technical compatibility, cost-effectiveness, implementation timeline", gaps: [] },
      decision_process: { score: 70, confidence: 80, status: "identified", details: "Technical evaluation -> Budget approval -> Contract", gaps: ["Timeline not fully defined"] },
      paper_process: { score: 65, confidence: 75, status: "suspected", details: "Standard procurement process expected", gaps: ["Legal requirements unclear", "Approval workflow undefined"] },
      implicate_the_pain: { score: 95, confidence: 90, status: "identified", details: "Current system causing significant operational inefficiencies", gaps: [] },
      champion: { score: 80, confidence: 85, status: "identified", details: "VP Engineering strongly advocating", gaps: [] },
      competition: { score: 50, confidence: 60, status: "suspected", details: "Two other vendors in consideration", gaps: ["Competitor strengths unknown", "Differentiation strategy needed"] }
    },
    strategic_recommendations: [
      "Schedule CFO meeting to establish budget authority",
      "Develop competitive differentiation strategy",
      "Define clear implementation timeline with milestones"
    ],
    risk_factors: [
      "Budget approval may be delayed due to Q4 freeze",
      "Strong technical competition from incumbent vendor"
    ],
    last_updated: "2024-06-24T07:30:00Z"
  },
  d2: {
    overall_score: 85,
    confidence_score: 89,
    components: {
      metrics: { score: 95, confidence: 95, status: "identified", details: "Clear revenue impact: $2M ARR increase projected", gaps: [] },
      economic_buyer: { score: 90, confidence: 95, status: "identified", details: "Head of Payments confirmed as decision maker", gaps: [] },
      decision_criteria: { score: 85, confidence: 90, status: "identified", details: "Integration ease, compliance, cost per transaction", gaps: [] },
      decision_process: { score: 80, confidence: 85, status: "identified", details: "Technical review -> Legal review -> Approval", gaps: [] },
      paper_process: { score: 75, confidence: 80, status: "identified", details: "Standard MSA with custom DPA requirements", gaps: ["Final contract terms being negotiated"] },
      implicate_the_pain: { score: 90, confidence: 85, status: "identified", details: "Current payment failures costing $50K monthly", gaps: [] },
      champion: { score: 85, confidence: 90, status: "identified", details: "Technical lead and product manager both advocating", gaps: [] },
      competition: { score: 70, confidence: 75, status: "identified", details: "Adyen is alternative option being evaluated", gaps: [] }
    },
    strategic_recommendations: [
      "Expedite legal review to meet month-end deadline",
      "Highlight cost-per-transaction advantage over Adyen"
    ],
    risk_factors: [
      "Legal review may extend past target close date"
    ],
    last_updated: "2024-06-24T07:30:00Z"
  },
  d3: {
    overall_score: 92,
    confidence_score: 96,
    components: {
      metrics: { score: 95, confidence: 95, status: "identified", details: "Team productivity increase: 25% faster development cycles", gaps: [] },
      economic_buyer: { score: 100, confidence: 100, status: "identified", details: "CEO directly involved in decision", gaps: [] },
      decision_criteria: { score: 90, confidence: 95, status: "identified", details: "User experience, integration capabilities, pricing", gaps: [] },
      decision_process: { score: 95, confidence: 95, status: "identified", details: "Internal consensus reached, moving to contract", gaps: [] },
      paper_process: { score: 85, confidence: 90, status: "identified", details: "Standard terms accepted, final signatures pending", gaps: [] },
      implicate_the_pain: { score: 90, confidence: 85, status: "identified", details: "Current tool limitations blocking team growth", gaps: [] },
      champion: { score: 95, confidence: 100, status: "identified", details: "Head of Engineering is strong internal champion", gaps: [] },
      competition: { score: 85, confidence: 80, status: "identified", details: "Evaluated Notion and Monday, chose us for technical superiority", gaps: [] }
    },
    strategic_recommendations: [
      "Fast-track contract execution to meet Q4 targets",
      "Prepare onboarding plan for immediate post-signature deployment"
    ],
    risk_factors: [],
    last_updated: "2024-06-24T07:30:00Z"
  }
}

// Mock deal data
const mockDeals: Deal[] = [
  {
    id: "d1",
    name: "Enterprise SaaS Implementation",
    account: "Optimizely Enterprise",
    stage: "Technical Evaluation",
    health: 85,
    value: 250000,
    closeDate: "2024-12-15",
    meddpiccScore: 78,
    confidence: 92,
    priority: "high",
    nextActions: ["Schedule executive review", "Address integration concerns"],
    risks: ["Technical complexity", "Timeline constraints"],
  },
  {
    id: "d2", 
    name: "Payment Integration Expansion",
    account: "Stripe Payments",
    stage: "Negotiation",
    health: 72,
    value: 180000,
    closeDate: "2024-11-30",
    meddpiccScore: 85,
    confidence: 89,
    priority: "medium",
    nextActions: ["Finalize pricing", "Legal review"],
    risks: ["Budget approval pending"],
  },
  {
    id: "d3",
    name: "Team Expansion License",
    account: "Linear Software",
    stage: "Closing",
    health: 95,
    value: 120000,
    closeDate: "2024-10-31",
    meddpiccScore: 92,
    confidence: 96,
    priority: "high",
    nextActions: ["Execute contract"],
    risks: [],
  },
  {
    id: "d4",
    name: "API Platform Integration",
    account: "GitHub Enterprise",
    stage: "Discovery",
    health: 60,
    value: 75000,
    closeDate: "2025-02-28",
    meddpiccScore: 45,
    confidence: 70,
    priority: "low",
    nextActions: ["Conduct technical discovery", "Map integration requirements"],
    risks: ["Complex technical requirements", "Multiple decision makers"],
  },
  {
    id: "d5",
    name: "Analytics Platform Upgrade",
    account: "Notion Labs",
    stage: "Negotiation",
    health: 88,
    value: 320000,
    closeDate: "2024-11-15",
    meddpiccScore: 82,
    confidence: 94,
    priority: "high",
    nextActions: ["Finalize contract terms", "Schedule implementation planning"],
    risks: [],
  },
]

// Mock evidence data for MEDDPICC analysis
const mockEvidenceData: Record<string, Evidence[]> = {
  d1: [
    {
      id: "e1",
      type: "transcript",
      title: "CTO discusses ROI expectations",
      content: "We're looking for at least a 40% cost reduction in our deployment pipeline. Based on our calculations, that would save us approximately $500K annually.",
      source: "Executive Review Meeting - 2024-06-15",
      timestamp: "2024-06-15T10:30:00Z",
      confidence: 0.95,
      meddpicc_category: "metrics"
    },
    {
      id: "e2",
      type: "email",
      title: "CFO approval requirement mentioned",
      content: "Just a heads up - any purchase over $100K will need CFO approval. I can help facilitate that meeting once we're ready.",
      source: "Email from VP Engineering",
      timestamp: "2024-06-18T14:20:00Z",
      confidence: 0.85,
      meddpicc_category: "economic_buyer"
    },
    {
      id: "e3",
      type: "transcript",
      title: "Integration requirements discussed",
      content: "The solution must integrate with our existing CI/CD pipeline. We use Jenkins for builds and Kubernetes for deployment.",
      source: "Technical Deep Dive - 2024-06-10",
      timestamp: "2024-06-10T15:45:00Z",
      confidence: 0.92,
      meddpicc_category: "decision_criteria"
    },
    {
      id: "e4",
      type: "transcript",
      title: "Current system pain points",
      content: "Our deployment failures are costing us 20 hours per week in engineering time. That's almost $100K per month in lost productivity.",
      source: "Discovery Call - 2024-06-01",
      timestamp: "2024-06-01T09:15:00Z",
      confidence: 0.88,
      meddpicc_category: "implicate_the_pain"
    },
    {
      id: "e5",
      type: "email",
      title: "Competition mentioned",
      content: "FYI - we're also evaluating CircleCI and GitLab. Your solution seems stronger on the enterprise features we need.",
      source: "Email from DevOps Lead",
      timestamp: "2024-06-20T11:00:00Z",
      confidence: 0.78,
      meddpicc_category: "competition"
    }
  ],
  d2: [
    {
      id: "e6",
      type: "transcript",
      title: "Revenue impact quantified",
      content: "With better payment processing, we estimate we can increase our transaction volume by 30%, which translates to about $2M in additional ARR.",
      source: "Business Case Review - 2024-06-22",
      timestamp: "2024-06-22T13:30:00Z",
      confidence: 0.93,
      meddpicc_category: "metrics"
    },
    {
      id: "e7",
      type: "transcript",
      title: "Head of Payments decision authority",
      content: "I have full budget authority for this initiative. The board has already approved the investment as part of our payment infrastructure upgrade.",
      source: "Executive Alignment Call - 2024-06-19",
      timestamp: "2024-06-19T10:00:00Z",
      confidence: 0.97,
      meddpicc_category: "economic_buyer"
    },
    {
      id: "e8",
      type: "document",
      title: "Compliance requirements documented",
      content: "Solution must be PCI DSS Level 1 compliant and support our multi-region deployment requirements.",
      source: "RFP Document - Section 3.2",
      timestamp: "2024-06-05T08:00:00Z",
      confidence: 0.91,
      meddpicc_category: "decision_criteria"
    },
    {
      id: "e9",
      type: "transcript",
      title: "Current payment failure costs",
      content: "We're losing about $50K per month due to payment failures. Our current provider's uptime is only 99.5%, which isn't acceptable for our scale.",
      source: "Problem Discovery Session - 2024-06-12",
      timestamp: "2024-06-12T14:00:00Z",
      confidence: 0.89,
      meddpicc_category: "implicate_the_pain"
    }
  ],
  d3: [
    {
      id: "e10",
      type: "transcript",
      title: "Productivity metrics defined",
      content: "Our goal is to reduce project planning time by 25% and increase developer velocity by 30%. Based on our team size, that's worth about $3M annually.",
      source: "CEO Strategy Session - 2024-06-20",
      timestamp: "2024-06-20T09:00:00Z",
      confidence: 0.96,
      meddpicc_category: "metrics"
    },
    {
      id: "e11",
      type: "transcript",
      title: "CEO direct involvement",
      content: "This is a strategic initiative for us. I'm personally involved in the decision and have allocated budget from our digital transformation fund.",
      source: "Executive Sponsor Meeting - 2024-06-21",
      timestamp: "2024-06-21T16:00:00Z",
      confidence: 1.0,
      meddpicc_category: "economic_buyer"
    },
    {
      id: "e12",
      type: "email",
      title: "Head of Engineering advocacy",
      content: "I've been championing this internally for months. The team is excited about the potential. I'm confident this will transform how we work.",
      source: "Email from Head of Engineering",
      timestamp: "2024-06-23T08:30:00Z",
      confidence: 0.94,
      meddpicc_category: "champion"
    }
  ]
}

export default function DealsPage() {
  const [selectedMEDDPICC, setSelectedMEDDPICC] = useState<{
    analysis: MEDDPICCAnalysis
    dealName: string
    dealId: string
  } | null>(null)

  const [filters, setFilters] = useState<FilterState>({
    search: '',
    stage: [],
    healthBand: [],
    valueBand: [],
    priority: []
  })

  const [currentView, setCurrentView] = useState('all')

  const filteredDeals = useMemo(() => {
    return mockDeals.filter(deal => {
      // Search filter
      if (filters.search) {
        const searchLower = filters.search.toLowerCase()
        const matchesSearch = 
          deal.name.toLowerCase().includes(searchLower) ||
          deal.account.toLowerCase().includes(searchLower)
        if (!matchesSearch) return false
      }

      // Stage filter
      if (filters.stage.length > 0 && !filters.stage.includes(deal.stage)) {
        return false
      }

      // Health band filter
      if (filters.healthBand.length > 0) {
        const healthBand = deal.health >= 80 ? 'high' : deal.health >= 60 ? 'medium' : 'low'
        if (!filters.healthBand.includes(healthBand)) return false
      }

      // Value band filter  
      if (filters.valueBand.length > 0) {
        let valueBand = '0-100k'
        if (deal.value >= 500000) valueBand = '500k+'
        else if (deal.value >= 100000) valueBand = '100k-500k'
        
        if (!filters.valueBand.includes(valueBand)) return false
      }

      // Priority filter
      if (filters.priority.length > 0 && !filters.priority.includes(deal.priority)) {
        return false
      }

      return true
    })
  }, [filters])

  const clearFilters = () => {
    setFilters({
      search: '',
      stage: [],
      healthBand: [],
      valueBand: [],
      priority: []
    })
  }

  const handleDealClick = (deal: Deal) => {
    // TODO: Navigate to deal workspace
    console.log('Deal clicked:', deal.name)
  }

  const handleMEDDPICCClick = (dealId: string, dealName: string) => {
    if (mockMEDDPICCData[dealId]) {
      setSelectedMEDDPICC({
        analysis: mockMEDDPICCData[dealId],
        dealName,
        dealId
      })
    }
  }

  // Calculate summary metrics
  const totalPipeline = filteredDeals.reduce((sum, deal) => sum + deal.value, 0)
  const averageHealth = Math.round(filteredDeals.reduce((sum, deal) => sum + deal.health, 0) / filteredDeals.length)
  const highHealthDeals = filteredDeals.filter(deal => deal.health >= 80).length
  const atRiskDeals = filteredDeals.filter(deal => deal.health < 60 || deal.risks.length > 0).length

  const formatValue = (value: number) => {
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`
    } else if (value >= 1000) {
      return `$${(value / 1000).toFixed(0)}K`
    } else {
      return `$${value.toLocaleString()}`
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="p-6 space-y-6">

      {/* Summary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-[var(--content-secondary)]">
              Total Pipeline
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[var(--content-primary)]">
              {formatValue(totalPipeline)}
            </div>
            <div className="flex items-center text-sm text-[var(--confidence-high)]">
              <TrendingUp className="mr-1 h-4 w-4" />
              {filteredDeals.length} active deals
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-[var(--content-secondary)]">
              Average Health
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[var(--content-primary)]">
              {averageHealth}%
            </div>
            <div className="flex items-center text-sm text-[var(--confidence-high)]">
              <CheckCircle className="mr-1 h-4 w-4" />
              {highHealthDeals} high health deals
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-[var(--content-secondary)]">
              Closing Soon
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[var(--content-primary)]">
              {filteredDeals.filter(d => new Date(d.closeDate) <= new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)).length}
            </div>
            <div className="flex items-center text-sm text-[var(--confidence-medium)]">
              <Clock className="mr-1 h-4 w-4" />
              Next 30 days
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-[var(--content-secondary)]">
              At Risk
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-[var(--content-primary)]">
              {atRiskDeals}
            </div>
            <div className="flex items-center text-sm text-[var(--confidence-low)]">
              <AlertTriangle className="mr-1 h-4 w-4" />
              Needs attention
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <DealsFilters 
        filters={filters}
        onFiltersChange={setFilters}
        onClearFilters={clearFilters}
      />

      {/* Deals Table */}
      <DealsTable
        deals={filteredDeals}
        meddpiccData={mockMEDDPICCData}
        onDealClick={handleDealClick}
        onMEDDPICCClick={handleMEDDPICCClick}
      />

      {/* Results Summary */}
      <div className="flex items-center justify-between text-sm text-[var(--content-secondary)]">
        <div>
          Showing {filteredDeals.length} of {mockDeals.length} deals
        </div>
        <div>
          Pipeline value: {formatValue(totalPipeline)}
        </div>
      </div>

      {/* MEDDPICC Details Modal */}
      {selectedMEDDPICC && (
        <MEDDPICCModal
          open={true}
          onOpenChange={(open) => {
            if (!open) {
              setSelectedMEDDPICC(null)
            }
          }}
          analysis={selectedMEDDPICC.analysis}
          evidence={mockEvidenceData[selectedMEDDPICC.dealId] || []}
          dealName={selectedMEDDPICC.dealName}
        />
      )}
        </div>
      </div>
    </div>
  )
}