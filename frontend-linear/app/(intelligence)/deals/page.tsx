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
import { ContextSelector } from "@/components/ui/context-selector"
import type { MEDDPICCAnalysis, Evidence } from "@/types/meddpicc"
import { useDeals, useDealsStats, useDealMEDDPICC, useDealEvidence } from "@/hooks/use-deals"

interface ContextEntity {
  id: string
  name: string
  type: "account" | "deal"
  accountId?: string
  accountName?: string
  lastInteraction?: string
  value?: number
  stage?: string
}

// Mock data has been replaced with real API calls

export default function DealsPage() {
  const [selectedMEDDPICC, setSelectedMEDDPICC] = useState<{
    dealId: string
    dealName: string
  } | null>(null)

  const [filters, setFilters] = useState<FilterState>({
    search: '',
    stage: [],
    healthBand: [],
    valueBand: [],
    priority: []
  })

  const [currentView, setCurrentView] = useState('all')
  const [selectedAccount, setSelectedAccount] = useState<ContextEntity | null>(null)
  const [selectedDeal, setSelectedDeal] = useState<ContextEntity | null>(null)

  // API calls
  const { data: dealsData, isLoading: dealsLoading, error: dealsError } = useDeals()
  const { data: statsData, isLoading: statsLoading } = useDealsStats()
  const { data: meddpiccData, isLoading: meddpiccLoading } = useDealMEDDPICC(selectedMEDDPICC?.dealId || null)
  const { data: evidenceData, isLoading: evidenceLoading } = useDealEvidence(selectedMEDDPICC?.dealId || null)

  const deals = dealsData?.deals || []

  const filteredDeals = useMemo(() => {
    return deals.filter(deal => {
      // Account context filter - only show deals for selected account
      if (selectedAccount && deal.accountName !== selectedAccount.name) {
        return false
      }

      // Deal context filter - only show specific deal if selected
      if (selectedDeal && deal.dealId !== selectedDeal.id) {
        return false
      }

      // Search filter
      if (filters.search) {
        const searchLower = filters.search.toLowerCase()
        const matchesSearch = 
          deal.dealName.toLowerCase().includes(searchLower) ||
          deal.accountName.toLowerCase().includes(searchLower)
        if (!matchesSearch) return false
      }

      // Stage filter
      if (filters.stage.length > 0 && !filters.stage.includes(deal.stage)) {
        return false
      }

      // Health band filter
      if (filters.healthBand.length > 0) {
        const healthBand = deal.health.score >= 80 ? 'high' : deal.health.score >= 60 ? 'medium' : 'low'
        if (!filters.healthBand.includes(healthBand)) return false
      }

      // Value band filter  
      if (filters.valueBand.length > 0) {
        let valueBand = '0-100k'
        if (deal.dealValue && deal.dealValue >= 500000) valueBand = '500k+'
        else if (deal.dealValue && deal.dealValue >= 100000) valueBand = '100k-500k'
        
        if (!filters.valueBand.includes(valueBand)) return false
      }

      // Priority filter - removed since priority doesn't exist on DealIntelligence
      // if (filters.priority.length > 0 && !filters.priority.includes(deal.priority)) {
      //   return false
      // }

      return true
    })
  }, [deals, filters, selectedAccount, selectedDeal])

  // Convert DealIntelligence to Deal interface for the table
  const mappedDeals = useMemo(() => {
    return filteredDeals.map(deal => ({
      id: deal.dealId,
      name: deal.dealName,
      account: deal.accountName,
      stage: deal.stage,
      health: deal.health.score,
      value: deal.dealValue || 0,
      closeDate: new Date().toISOString(), // Placeholder - add closeDate to DealIntelligence if needed
      meddpiccScore: deal.meddpiccAnalysis?.overallScore || 0,
      confidence: deal.meddpiccAnalysis?.overallScore || 0, // Using MEDDPICC score as confidence for now
      priority: "medium" as const, // Default priority since not in DealIntelligence
      nextActions: deal.nextActions.map(action => action.title),
      risks: [] // Placeholder - would need to extract from meddpiccAnalysis.risks if available
    }))
  }, [filteredDeals])


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
    setSelectedMEDDPICC({
      dealId,
      dealName
    })
  }

  // Calculate summary metrics (fallback to API stats or calculate from filtered deals)
  const totalPipeline = statsData?.totalValue || filteredDeals.reduce((sum, deal) => sum + (deal.dealValue || 0), 0)
  const averageHealth = statsData?.averageHealth || (filteredDeals.length > 0 ? Math.round(filteredDeals.reduce((sum, deal) => sum + deal.health.score, 0) / filteredDeals.length) : 0)
  const highHealthDeals = filteredDeals.filter(deal => deal.health.score >= 80).length
  const atRiskDeals = statsData?.dealsAtRisk || filteredDeals.filter(deal => deal.health.score < 60).length

  const formatValue = (value: number) => {
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`
    } else if (value >= 1000) {
      return `$${(value / 1000).toFixed(0)}K`
    } else {
      return `$${value.toLocaleString()}`
    }
  }

  // Loading state
  if (dealsLoading) {
    return (
      <div className="flex flex-col h-full">
        <div className="flex-1 overflow-auto">
          <div className="p-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => (
                <Card key={i}>
                  <CardHeader className="pb-3">
                    <div className="h-4 bg-gray-200 rounded animate-pulse" />
                  </CardHeader>
                  <CardContent>
                    <div className="h-8 bg-gray-200 rounded animate-pulse mb-2" />
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-2/3" />
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Error state
  if (dealsError) {
    return (
      <div className="flex flex-col h-full">
        <div className="flex-1 overflow-auto">
          <div className="p-6">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="h-5 w-5 text-red-500" />
                  <div>
                    <h3 className="font-medium text-red-900">Failed to load deals</h3>
                    <p className="text-sm text-red-700">
                      {dealsError instanceof Error ? dealsError.message : 'An error occurred'}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="p-3 lg:p-4 xl:p-6 space-y-3 lg:space-y-4 xl:space-y-6">

      {/* Summary Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 lg:gap-3 xl:gap-4">
        <Card>
          <CardHeader className="pb-2 pt-3 lg:pt-4 px-3 lg:px-4">
            <CardTitle className="text-xs lg:text-sm font-medium text-[var(--content-secondary)]">
              Total Pipeline
            </CardTitle>
          </CardHeader>
          <CardContent className="px-3 lg:px-4 pb-3 lg:pb-4">
            <div className="text-lg lg:text-2xl font-bold text-[var(--content-primary)]">
              {formatValue(totalPipeline)}
            </div>
            <div className="flex items-center text-xs lg:text-sm text-[var(--confidence-high)]">
              <TrendingUp className="mr-1 h-3 w-3 lg:h-4 lg:w-4" />
              <span className="truncate">{filteredDeals.length} active deals</span>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2 pt-3 lg:pt-4 px-3 lg:px-4">
            <CardTitle className="text-xs lg:text-sm font-medium text-[var(--content-secondary)]">
              Average Health
            </CardTitle>
          </CardHeader>
          <CardContent className="px-3 lg:px-4 pb-3 lg:pb-4">
            <div className="text-lg lg:text-2xl font-bold text-[var(--content-primary)]">
              {averageHealth}%
            </div>
            <div className="flex items-center text-xs lg:text-sm text-[var(--confidence-high)]">
              <CheckCircle className="mr-1 h-3 w-3 lg:h-4 lg:w-4" />
              <span className="truncate">{highHealthDeals} high health deals</span>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2 pt-3 lg:pt-4 px-3 lg:px-4">
            <CardTitle className="text-xs lg:text-sm font-medium text-[var(--content-secondary)]">
              Closing Soon
            </CardTitle>
          </CardHeader>
          <CardContent className="px-3 lg:px-4 pb-3 lg:pb-4">
            <div className="text-lg lg:text-2xl font-bold text-[var(--content-primary)]">
              {filteredDeals.filter(d => d.stage === 'closing' || d.stage === 'negotiation').length}
            </div>
            <div className="flex items-center text-xs lg:text-sm text-[var(--confidence-medium)]">
              <Clock className="mr-1 h-3 w-3 lg:h-4 lg:w-4" />
              <span className="truncate">Next 30 days</span>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2 pt-3 lg:pt-4 px-3 lg:px-4">
            <CardTitle className="text-xs lg:text-sm font-medium text-[var(--content-secondary)]">
              At Risk
            </CardTitle>
          </CardHeader>
          <CardContent className="px-3 lg:px-4 pb-3 lg:pb-4">
            <div className="text-lg lg:text-2xl font-bold text-[var(--content-primary)]">
              {atRiskDeals}
            </div>
            <div className="flex items-center text-xs lg:text-sm text-[var(--confidence-low)]">
              <AlertTriangle className="mr-1 h-3 w-3 lg:h-4 lg:w-4" />
              <span className="truncate">Needs attention</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Account Context Filter - Compact Version */}
      {(selectedAccount || selectedDeal) && (
        <div className="flex items-center gap-2 p-3 bg-blue-50 border border-blue-200 rounded-md">
          <div className="text-sm text-blue-700">
            {selectedAccount && selectedDeal 
              ? `Viewing ${selectedDeal.name} in ${selectedAccount.name}`
              : selectedAccount 
              ? `Filtering by ${selectedAccount.name}`
              : `Viewing ${selectedDeal?.name}`}
          </div>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => {
              setSelectedAccount(null)
              setSelectedDeal(null)
            }}
            className="text-blue-700 hover:text-blue-900"
          >
            Clear filter
          </Button>
        </div>
      )}

      {/* Filters */}
      <DealsFilters 
        filters={filters}
        onFiltersChange={setFilters}
        onClearFilters={clearFilters}
      />

      {/* Deals Table */}
      <DealsTable
        deals={mappedDeals}
        meddpiccData={{}} // Will be loaded separately when needed
        onDealClick={handleDealClick}
        onMEDDPICCClick={handleMEDDPICCClick}
      />

      {/* Results Summary */}
      <div className="flex items-center justify-between text-sm text-[var(--content-secondary)]">
        <div>
          Showing {filteredDeals.length} of {dealsData?.total || 0} deals
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
          analysis={meddpiccData}
          evidence={evidenceData || []}
          dealName={selectedMEDDPICC.dealName}
          isLoading={meddpiccLoading || evidenceLoading}
        />
      )}
        </div>
      </div>
    </div>
  )
}