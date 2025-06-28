// PATTERN_REF: FRONTEND_ROUTING_PATTERN
// DECISION_REF: DEC_2025-06-24_007: Linear-inspired deals table with filtering and sorting

"use client"

import { useState, useMemo } from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { 
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  ExternalLink,
  Calendar,
  DollarSign
} from "lucide-react"
import type { MEDDPICCAnalysis } from "@/types/meddpicc"

export interface Deal {
  id: string
  name: string
  account: string
  stage: string
  health: number
  value: number
  closeDate: string
  meddpiccScore: number
  confidence: number
  priority: "high" | "medium" | "low"
  nextActions: string[]
  risks: string[]
}

interface DealsTableProps {
  deals: Deal[]
  meddpiccData: Record<string, MEDDPICCAnalysis>
  onDealClick: (deal: Deal) => void
  onMEDDPICCClick: (dealId: string, dealName: string) => void
}

type SortField = 'name' | 'account' | 'stage' | 'health' | 'value' | 'closeDate' | 'meddpiccScore' | 'priority'
type SortDirection = 'asc' | 'desc' | null

export function DealsTable({ deals, meddpiccData, onDealClick, onMEDDPICCClick }: DealsTableProps) {
  const [sortField, setSortField] = useState<SortField | null>(null)
  const [sortDirection, setSortDirection] = useState<SortDirection>(null)

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      if (sortDirection === 'asc') {
        setSortDirection('desc')
      } else if (sortDirection === 'desc') {
        setSortField(null)
        setSortDirection(null)
      } else {
        setSortDirection('asc')
      }
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  const getSortIcon = (field: SortField) => {
    if (sortField !== field) {
      return <ArrowUpDown className="h-4 w-4 text-[var(--content-secondary)]" />
    }
    if (sortDirection === 'asc') {
      return <ArrowUp className="h-4 w-4 text-[var(--content-primary)]" />
    }
    if (sortDirection === 'desc') {
      return <ArrowDown className="h-4 w-4 text-[var(--content-primary)]" />
    }
    return <ArrowUpDown className="h-4 w-4 text-[var(--content-secondary)]" />
  }

  const sortedDeals = useMemo(() => {
    if (!sortField || !sortDirection) return deals

    return [...deals].sort((a, b) => {
      let aValue: any = a[sortField]
      let bValue: any = b[sortField]

      // Special handling for different field types
      if (sortField === 'closeDate') {
        aValue = new Date(aValue).getTime()
        bValue = new Date(bValue).getTime()
      } else if (sortField === 'priority') {
        const priorityOrder = { high: 3, medium: 2, low: 1 }
        aValue = priorityOrder[aValue as keyof typeof priorityOrder]
        bValue = priorityOrder[bValue as keyof typeof priorityOrder]
      }

      if (sortDirection === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0
      }
    })
  }, [deals, sortField, sortDirection])

  const getHealthColor = (health: number) => {
    if (health >= 80) return "text-[var(--confidence-high)]"
    if (health >= 60) return "text-[var(--confidence-medium)]"
    return "text-[var(--confidence-low)]"
  }

  const getHealthBadgeColor = (health: number) => {
    if (health >= 80) return "bg-[var(--confidence-high)]/20 text-[var(--confidence-high)]"
    if (health >= 60) return "bg-[var(--confidence-medium)]/20 text-[var(--confidence-medium)]"
    return "bg-[var(--confidence-low)]/20 text-[var(--confidence-low)]"
  }

  const getStageColor = (stage: string) => {
    switch (stage.toLowerCase()) {
      case 'closing':
        return "bg-[var(--confidence-high)]/20 text-[var(--confidence-high)]"
      case 'negotiation':
        return "bg-[var(--confidence-medium)]/20 text-[var(--confidence-medium)]"
      case 'technical evaluation':
        return "bg-[var(--ai-processing)]/20 text-[var(--ai-processing)]"
      default:
        return "bg-[var(--content-secondary)]/20 text-[var(--content-secondary)]"
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400"
      case 'medium':
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400"
      case 'low':
        return "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400"
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400"
    }
  }

  const formatValue = (value: number) => {
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`
    } else if (value >= 1000) {
      return `$${(value / 1000).toFixed(0)}K`
    } else {
      return `$${value.toLocaleString()}`
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    })
  }

  return (
    <div className="border border-[var(--bg-border)] rounded-lg bg-[var(--bg-base-color)] overflow-x-auto">
      <Table className="min-w-[700px] lg:min-w-[800px]">
        <TableHeader>
          <TableRow className="border-b border-[var(--bg-border)] hover:bg-transparent">
            <TableHead className="font-medium text-[var(--content-primary)]">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleSort('name')}
                className="h-auto p-0 font-medium hover:bg-transparent"
              >
                Deal Name
                {getSortIcon('name')}
              </Button>
            </TableHead>
            <TableHead className="font-medium text-[var(--content-primary)]">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleSort('account')}
                className="h-auto p-0 font-medium hover:bg-transparent"
              >
                Account
                {getSortIcon('account')}
              </Button>
            </TableHead>
            <TableHead className="font-medium text-[var(--content-primary)]">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleSort('stage')}
                className="h-auto p-0 font-medium hover:bg-transparent"
              >
                Stage
                {getSortIcon('stage')}
              </Button>
            </TableHead>
            <TableHead className="font-medium text-[var(--content-primary)]">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleSort('value')}
                className="h-auto p-0 font-medium hover:bg-transparent"
              >
                Value
                {getSortIcon('value')}
              </Button>
            </TableHead>
            <TableHead className="font-medium text-[var(--content-primary)]">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleSort('health')}
                className="h-auto p-0 font-medium hover:bg-transparent"
              >
                Health
                {getSortIcon('health')}
              </Button>
            </TableHead>
            <TableHead className="font-medium text-[var(--content-primary)]">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleSort('meddpiccScore')}
                className="h-auto p-0 font-medium hover:bg-transparent"
              >
                MEDDPICC
                {getSortIcon('meddpiccScore')}
              </Button>
            </TableHead>
            <TableHead className="font-medium text-[var(--content-primary)]">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleSort('closeDate')}
                className="h-auto p-0 font-medium hover:bg-transparent"
              >
                Close Date
                {getSortIcon('closeDate')}
              </Button>
            </TableHead>
            <TableHead className="font-medium text-[var(--content-primary)]">
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleSort('priority')}
                className="h-auto p-0 font-medium hover:bg-transparent"
              >
                Priority
                {getSortIcon('priority')}
              </Button>
            </TableHead>
            <TableHead className="w-12"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sortedDeals.map((deal) => (
            <TableRow 
              key={deal.id}
              className="border-b border-[var(--bg-border)] hover:bg-[var(--bg-subtle)] cursor-pointer transition-colors"
              onClick={() => onDealClick(deal)}
            >
              <TableCell className="font-medium text-[var(--content-primary)]">
                <div>
                  <div className="font-medium">{deal.name}</div>
                  {deal.risks.length > 0 && (
                    <div className="text-xs text-[var(--confidence-low)] mt-1">
                      {deal.risks.length} risk{deal.risks.length > 1 ? 's' : ''}
                    </div>
                  )}
                </div>
              </TableCell>
              <TableCell className="text-[var(--content-secondary)]">
                {deal.account}
              </TableCell>
              <TableCell>
                <Badge className={getStageColor(deal.stage)}>
                  {deal.stage}
                </Badge>
              </TableCell>
              <TableCell className="font-medium text-[var(--content-primary)]">
                <div className="flex items-center gap-1">
                  <DollarSign className="h-3 w-3 text-[var(--content-secondary)]" />
                  {formatValue(deal.value)}
                </div>
              </TableCell>
              <TableCell>
                <div className="flex items-center gap-2">
                  <div className={`text-sm font-medium ${getHealthColor(deal.health)}`}>
                    {deal.health}%
                  </div>
                  <div className="w-16">
                    <Progress value={deal.health} className="h-1.5" />
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation()
                    onMEDDPICCClick(deal.id, deal.name)
                  }}
                  className="h-auto p-1 text-[var(--ai-processing)] hover:bg-[var(--ai-processing)]/10"
                >
                  <div className="flex items-center gap-2">
                    <div className="text-sm font-medium">
                      {deal.meddpiccScore}%
                    </div>
                    <div className="w-12">
                      <Progress value={deal.meddpiccScore} className="h-1" />
                    </div>
                  </div>
                </Button>
              </TableCell>
              <TableCell className="text-[var(--content-secondary)]">
                <div className="flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {formatDate(deal.closeDate)}
                </div>
              </TableCell>
              <TableCell>
                <Badge className={getPriorityColor(deal.priority)}>
                  {deal.priority}
                </Badge>
              </TableCell>
              <TableCell>
                <Button 
                  variant="ghost" 
                  size="icon"
                  className="h-6 w-6 text-[var(--content-secondary)] hover:text-[var(--content-primary)]"
                  onClick={(e) => {
                    e.stopPropagation()
                    // TODO: Open deal workspace
                  }}
                >
                  <ExternalLink className="h-3 w-3" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}