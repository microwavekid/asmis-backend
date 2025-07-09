// PATTERN_REF: MEDDPIC_ORCHESTRATOR_PATTERN
// DECISION_REF: DEC_2025-06-24_004: MEDDPICC card component with evidence display

"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { cn } from "@/lib/utils"
import { 
  Target,
  DollarSign,
  Calendar,
  Users,
  Zap,
  CheckSquare,
  Trophy,
  AlertTriangle,
  FileText,
  ExternalLink,
  Brain
} from "lucide-react"
import type { MEDDPICCAnalysis, Evidence } from "@/types/meddpicc"

interface MEDDPICCCardProps {
  analysis: MEDDPICCAnalysis
  evidence: Evidence[]
  onEvidenceClick?: (evidence: Evidence) => void
}

// PATTERN_REF: UI_DEBUGGING_PATTERN - Fix key mismatch between types and component
const MEDDPICC_ICONS = {
  metrics: Target,
  economic_buyer: DollarSign,
  decision_criteria: CheckSquare,
  decision_process: Calendar,
  identify_pain: AlertTriangle,
  champion: Trophy,
  competition: Users
}

const MEDDPICC_LABELS = {
  metrics: "Metrics",
  economic_buyer: "Economic Buyer",
  decision_criteria: "Decision Criteria", 
  decision_process: "Decision Process",
  identify_pain: "Identify Pain",
  champion: "Champion",
  competition: "Competition"
}

export function MEDDPICCCard({ analysis, evidence, onEvidenceClick }: MEDDPICCCardProps) {
  // Debug: Log component keys to identify mismatches
  if (analysis.components) {
    console.log('MEDDPICC Component Keys:', Object.keys(analysis.components))
    console.log('Expected Keys:', Object.keys(MEDDPICC_ICONS))
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-[var(--confidence-high)]"
    if (score >= 60) return "text-[var(--confidence-medium)]"
    return "text-[var(--confidence-low)]"
  }

  const getEvidenceForSection = (section: keyof typeof analysis.components) => {
    return evidence.filter(e => 
      e.meddpicc_category === section || 
      e.content.toLowerCase().includes(section.replace('_', ' '))
    )
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Brain className="h-5 w-5 text-[var(--ai-processing)]" />
              MEDDPICC Analysis
            </CardTitle>
            <CardDescription>
              AI-powered qualification framework with evidence backing
            </CardDescription>
          </div>
          <div className="text-right">
            <div className={`text-3xl font-bold ${getScoreColor(analysis.overallScore)}`}>
              {Math.round(analysis.overallScore)}%
            </div>
            <div className="text-sm text-[var(--content-secondary)]">
              Overall Score
            </div>
          </div>
        </div>
        
        {/* Overall Progress Bar */}
        <div className="mt-4">
          <Progress 
            value={analysis.overallScore} 
            className="h-2"
            style={{
              background: `var(--bg-border)`,
            }}
          />
          <div className="flex justify-between text-xs text-[var(--content-secondary)] mt-1">
            <span>Qualification Progress</span>
            <span>Confidence: {Math.round(analysis.completenessScore || 0)}%</span>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Component Breakdown */}
        <Accordion type="multiple" className="space-y-2">
          {Object.entries(analysis.components as Record<string, any>).map(([key, component]: [string, any]) => {
            const Icon = MEDDPICC_ICONS[key as keyof typeof MEDDPICC_ICONS]
            const label = MEDDPICC_LABELS[key as keyof typeof MEDDPICC_LABELS]
            const sectionEvidence = getEvidenceForSection(key as keyof typeof analysis.components)

            // Skip if no icon found (handles any key mismatches)
            if (!Icon || !label) return null

            return (
              <AccordionItem key={key} value={key} className="border border-[var(--bg-border)] rounded-lg">
                <AccordionTrigger className="px-4 py-3 hover:no-underline">
                  <div className="flex items-center justify-between w-full mr-4">
                    <div className="flex items-center gap-3">
                      <Icon className="h-4 w-4 text-[var(--content-secondary)]" />
                      <div className="text-left">
                        <div className="font-medium text-[var(--content-primary)]">
                          {label}
                        </div>
                        <div className="text-sm text-[var(--content-secondary)]">
                          {sectionEvidence.length} evidence pieces
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className={`text-lg font-bold ${getScoreColor(component.score)}`}>
                        {Math.round(component.score)}%
                      </div>
                      <Badge variant={component.status === 'identified' ? 'default' : 'secondary'}>
                        {component.status}
                      </Badge>
                    </div>
                  </div>
                </AccordionTrigger>

                <AccordionContent className="px-4 pb-4">
                  <div className="pl-7 space-y-3">
                    {/* Component Details */}
                    {component.details && (
                      <div className="p-3 bg-[var(--bg-subtle)] rounded-md">
                        <div className="text-sm text-[var(--content-primary)]">
                          {component.details}
                        </div>
                      </div>
                    )}

                    {/* Progress Bar for Component */}
                    <div>
                      <Progress 
                        value={component?.score || 0} 
                        className="h-1.5"
                      />
                      <div className="flex justify-between text-xs text-[var(--content-secondary)] mt-1">
                        <span>Confidence: {Math.round(component?.confidence || 0)}%</span>
                        {component.gaps && component.gaps.length > 0 && (
                          <span className="text-[var(--confidence-low)]">
                            {component.gaps.length} gaps identified
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Evidence */}
                    {sectionEvidence.length > 0 && (
                      <div>
                        <div className="text-sm font-medium text-[var(--content-primary)] mb-2">
                          Supporting Evidence
                        </div>
                        <div className="space-y-2">
                          {sectionEvidence.slice(0, 3).map((evidenceItem) => (
                            <div 
                              key={evidenceItem.id}
                              className="p-2 bg-[var(--bg-base-color)] border border-[var(--bg-border)] rounded-md hover:bg-[var(--bg-subtle)] transition-colors cursor-pointer"
                              onClick={() => onEvidenceClick?.(evidenceItem)}
                            >
                              <div className="flex items-start justify-between gap-2">
                                <div className="flex-1">
                                  <div className="text-sm font-medium text-[var(--content-primary)]">
                                    {evidenceItem.title}
                                  </div>
                                  <div className="text-xs text-[var(--content-secondary)] mt-1 line-clamp-2">
                                    {evidenceItem.content}
                                  </div>
                                </div>
                                <div className="flex items-center gap-1">
                                  <Badge variant="outline" className="text-xs">
                                    {Math.round(evidenceItem.confidence * 100)}%
                                  </Badge>
                                  <ExternalLink className="h-3 w-3 text-[var(--content-secondary)]" />
                                </div>
                              </div>
                            </div>
                          ))}
                          {sectionEvidence.length > 3 && (
                            <Button 
                              variant="ghost" 
                              size="sm" 
                              className="w-full text-[var(--ai-processing)]"
                            >
                              View {sectionEvidence.length - 3} more evidence pieces
                            </Button>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Gaps */}
                    {component.gaps && component.gaps.length > 0 && (
                      <div>
                        <div className="text-sm font-medium text-[var(--content-primary)] mb-2">
                          Information Gaps
                        </div>
                        <ul className="space-y-1">
                          {component.gaps?.map((gap: string, index: number) => (
                            <li key={index} className="text-sm text-[var(--confidence-low)] flex items-center">
                              <AlertTriangle className="w-3 h-3 mr-2" />
                              {gap}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </AccordionContent>
              </AccordionItem>
            )
          })}
        </Accordion>

        {/* Strategic Recommendations */}
        {analysis.strategic_recommendations && analysis.strategic_recommendations.length > 0 && (
          <div className="mt-6 pt-4 border-t border-[var(--bg-border)]">
            <div className="text-sm font-medium text-[var(--content-primary)] mb-3 flex items-center gap-2">
              <Zap className="h-4 w-4 text-[var(--ai-processing)]" />
              AI Strategic Recommendations
            </div>
            <div className="space-y-2">
              {analysis.strategic_recommendations?.map((rec: string, index: number) => (
                <div key={index} className="p-3 bg-[var(--ai-processing)]/5 border border-[var(--ai-processing)]/20 rounded-md">
                  <div className="text-sm text-[var(--content-primary)]">
                    {rec}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Risk Analysis */}
        {analysis.riskFactors && analysis.riskFactors.length > 0 && (
          <div className="mt-4 pt-4 border-t border-[var(--bg-border)]">
            <div className="text-sm font-medium text-[var(--content-primary)] mb-3 flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-[var(--confidence-low)]" />
              Risk Factors ({analysis.riskFactors.length})
            </div>
            <div className="space-y-2">
              {analysis.riskFactors?.map((risk: string, index: number) => (
                <div key={index} className="p-2 bg-[var(--confidence-low)]/5 border border-[var(--confidence-low)]/20 rounded-md">
                  <div className="text-sm text-[var(--content-primary)]">
                    {risk}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}