// PATTERN_REF: SMART_CAPTURE_UI_PATTERN
// DECISION_REF: DEC_2025-07-08_002
// Clean data mapping utilities for converting DealIntelligence to Deal table format

import { DealIntelligence } from '@/types/intelligence'

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

/**
 * Converts DealIntelligence to Deal interface for table display
 * with robust fallbacks and clean transformation logic
 */
export function mapDealIntelligenceToDeal(deal: DealIntelligence): Deal {
  return {
    id: deal.dealId,
    name: deal.dealName,
    account: deal.accountName,
    stage: formatStage(deal.stage),
    health: deal.health?.score || 0,
    value: deal.dealValue || 0,
    closeDate: extractCloseDate(deal),
    meddpiccScore: deal.meddpiccAnalysis?.overallScore || 0,
    confidence: extractConfidence(deal),
    priority: derivePriority(deal),
    nextActions: extractNextActions(deal),
    risks: extractRisks(deal)
  }
}

/**
 * Formats stage from snake_case to Display Case
 */
function formatStage(stage: string): string {
  const stageMap: Record<string, string> = {
    'discovery': 'Discovery',
    'technical_evaluation': 'Technical Evaluation',
    'business_evaluation': 'Business Evaluation',
    'negotiation': 'Negotiation',
    'closing': 'Closing',
    'closed_won': 'Closed Won',
    'closed_lost': 'Closed Lost'
  }
  
  return stageMap[stage] || stage.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

/**
 * Extracts close date with robust fallback logic
 */
function extractCloseDate(deal: DealIntelligence): string {
  // Try MEDDPICC decision process first
  if (deal.meddpiccAnalysis?.decisionProcess?.estimatedCloseDate) {
    return new Date(deal.meddpiccAnalysis.decisionProcess.estimatedCloseDate).toISOString()
  }
  
  // Try momentum milestones
  const closeMilestone = deal.momentum?.keyMilestones?.find(m => 
    m.name.toLowerCase().includes('close') || 
    m.name.toLowerCase().includes('contract') ||
    m.name.toLowerCase().includes('sign')
  )
  if (closeMilestone?.dueDate) {
    return new Date(closeMilestone.dueDate).toISOString()
  }
  
  // Default based on stage
  const stageToCloseDays: Record<string, number> = {
    'closing': 7,
    'negotiation': 30,
    'business_evaluation': 60,
    'technical_evaluation': 75,
    'discovery': 90
  }
  
  const daysFromNow = stageToCloseDays[deal.stage] || 90
  return new Date(Date.now() + daysFromNow * 24 * 60 * 60 * 1000).toISOString()
}

/**
 * Extracts confidence score with fallback logic
 */
function extractConfidence(deal: DealIntelligence): number {
  // Prefer completeness score
  if (deal.meddpiccAnalysis?.completenessScore) {
    return deal.meddpiccAnalysis.completenessScore
  }
  
  // Fallback to overall score with adjustment
  if (deal.meddpiccAnalysis?.overallScore) {
    return deal.meddpiccAnalysis.overallScore * 0.8
  }
  
  // Final fallback based on health
  return deal.health?.score ? deal.health.score * 0.7 : 0
}

/**
 * Derives priority based on multiple factors
 */
function derivePriority(deal: DealIntelligence): "high" | "medium" | "low" {
  // Critical actions = high priority
  if (deal.nextActions?.some(a => a.priority === 'critical')) {
    return "high"
  }
  
  // Poor health = high priority
  if ((deal.health?.score || 0) < 60) {
    return "high"
  }
  
  // High priority actions = high priority
  if (deal.nextActions?.some(a => a.priority === 'high')) {
    return "high"
  }
  
  // Closing/negotiation stages = high priority
  if (deal.stage === 'closing' || deal.stage === 'negotiation') {
    return "high"
  }
  
  // Medium priority actions = medium priority
  if (deal.nextActions?.some(a => a.priority === 'medium')) {
    return "medium"
  }
  
  // Good health = low priority, otherwise medium
  return (deal.health?.score || 0) >= 80 ? "low" : "medium"
}

/**
 * Extracts next actions as simple string array
 */
function extractNextActions(deal: DealIntelligence): string[] {
  return deal.nextActions?.map(action => action.title) || []
}

/**
 * Extracts risks from multiple sources
 */
function extractRisks(deal: DealIntelligence): string[] {
  const risks: string[] = []
  
  // Add MEDDPICC risk factors
  if (deal.meddpiccAnalysis?.riskFactors) {
    risks.push(...deal.meddpiccAnalysis.riskFactors)
  }
  
  // Add health-based risks
  if ((deal.health?.score || 0) < 60) {
    risks.push('Low deal health')
  }
  
  // Add momentum-based risks
  if (deal.momentum?.velocity === 'stalled' || deal.momentum?.velocity === 'reversing') {
    risks.push('Deal momentum issues')
  }
  
  // Add competition risks
  if (deal.meddpiccAnalysis?.competition?.competitors?.some(c => c.status === 'evaluating')) {
    risks.push('Active competition')
  }
  
  return risks
}

/**
 * Batch mapping function for multiple deals
 */
export function mapDealsIntelligenceToDeals(deals: DealIntelligence[]): Deal[] {
  return deals.map(mapDealIntelligenceToDeal)
}