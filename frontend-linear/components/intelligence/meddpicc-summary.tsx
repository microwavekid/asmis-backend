// PATTERN_REF: MEDDPIC_ORCHESTRATOR_PATTERN
// DECISION_REF: DEC_2025-06-24_005: MEDDPICC summary card for deal listings

"use client"

import { Badge } from "@/components/ui/badge" 
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { 
  Target,
  DollarSign,
  Calendar,
  Users,
  CheckSquare,
  FileText,
  AlertTriangle,
  Trophy,
  MoreHorizontal
} from "lucide-react"
import type { MEDDPICCAnalysis } from "@/types/meddpicc"

interface MEDDPICCSummaryProps {
  analysis: MEDDPICCAnalysis
  compact?: boolean
  onViewDetails?: () => void
}

const COMPONENT_ICONS = {
  metrics: Target,
  economic_buyer: DollarSign,
  decision_criteria: CheckSquare,
  decision_process: Calendar,
  paper_process: FileText,
  implicate_the_pain: AlertTriangle,
  champion: Trophy,
  competition: Users
}

export function MEDDPICCSummary({ analysis, compact = false, onViewDetails }: MEDDPICCSummaryProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-[var(--confidence-high)]"
    if (score >= 60) return "text-[var(--confidence-medium)]"
    return "text-[var(--confidence-low)]"
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return "bg-[var(--confidence-high)]/10"
    if (score >= 60) return "bg-[var(--confidence-medium)]/10"
    return "bg-[var(--confidence-low)]/10"
  }

  const topComponents = Object.entries(analysis.components)
    .sort(([,a], [,b]) => b.score - a.score)
    .slice(0, compact ? 3 : 4)

  const riskCount = analysis.risk_factors.length
  const gapCount = Object.values(analysis.components).reduce((sum, comp) => sum + comp.gaps.length, 0)

  if (compact) {
    return (
      <div className="flex items-center justify-between p-3 bg-[var(--bg-subtle)] rounded-lg">
        <div className="flex items-center gap-3">
          <div className={`text-lg font-bold ${getScoreColor(analysis.overall_score)}`}>
            {Math.round(analysis.overall_score)}%
          </div>
          <div className="text-sm text-[var(--content-secondary)]">
            MEDDPICC
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          {topComponents.slice(0, 3).map(([key, component]) => {
            const Icon = COMPONENT_ICONS[key as keyof typeof COMPONENT_ICONS]
            return (
              <div 
                key={key}
                className={`p-1.5 rounded ${getScoreBgColor(component.score)}`}
                title={`${key}: ${Math.round(component.score)}%`}
              >
                <Icon className={`h-3 w-3 ${getScoreColor(component.score)}`} />
              </div>
            )
          })}
          
          {onViewDetails && (
            <Button variant="ghost" size="sm" onClick={onViewDetails}>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm font-medium text-[var(--content-primary)]">
            MEDDPICC Analysis
          </div>
          <div className="text-xs text-[var(--content-secondary)]">
            AI-powered qualification
          </div>
        </div>
        <div className="text-right">
          <div className={`text-xl font-bold ${getScoreColor(analysis.overall_score)}`}>
            {Math.round(analysis.overall_score)}%
          </div>
          <div className="text-xs text-[var(--content-secondary)]">
            Overall
          </div>
        </div>
      </div>

      {/* Progress */}
      <div>
        <Progress value={analysis.overall_score} className="h-1.5" />
        <div className="flex justify-between text-xs text-[var(--content-secondary)] mt-1">
          <span>Qualification</span>
          <span>Confidence: {Math.round(analysis.confidence_score)}%</span>
        </div>
      </div>

      {/* Component Icons Row */}
      <div className="flex items-center justify-between">
        {topComponents.map(([key, component]) => {
          const Icon = COMPONENT_ICONS[key as keyof typeof COMPONENT_ICONS]
          return (
            <div key={key} className="flex flex-col items-center">
              <div className={`p-2 rounded-full ${getScoreBgColor(component.score)}`}>
                <Icon className={`h-4 w-4 ${getScoreColor(component.score)}`} />
              </div>
              <div className={`text-xs font-medium mt-1 ${getScoreColor(component.score)}`}>
                {Math.round(component.score)}%
              </div>
            </div>
          )
        })}
      </div>

      {/* Status Indicators */}
      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center gap-3">
          {riskCount > 0 && (
            <Badge variant="destructive" className="text-xs">
              {riskCount} risks
            </Badge>
          )}
          {gapCount > 0 && (
            <Badge variant="secondary" className="text-xs">
              {gapCount} gaps
            </Badge>
          )}
        </div>
        
        {onViewDetails && (
          <Button variant="ghost" size="sm" onClick={onViewDetails}>
            View Details
          </Button>
        )}
      </div>
    </div>
  )
}