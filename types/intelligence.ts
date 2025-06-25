// Deal Intelligence Types for ASMIS

import { MEDDPICCAnalysis, DealStage, Evidence, Risk, Recommendation } from './meddpicc';

export interface DealIntelligence {
  accountId: string;
  accountName: string;
  dealId: string;
  dealName: string;
  dealValue?: number;
  stage: DealStage;
  health: DealHealth;
  momentum: DealMomentum;
  
  // Core analysis
  meddpiccAnalysis: MEDDPICCAnalysis;
  
  // Actionable insights
  nextActions: Action[];
  opportunities: Opportunity[];
  
  // Processing status
  processingQueue: ProcessingQueue;
  
  // Activity timeline
  timeline: TimelineEvent[];
  
  // Metadata
  createdAt: Date;
  lastUpdated: Date;
  owner?: string;
  team?: string[];
}

export interface DealHealth {
  score: number; // 0-100
  trend: 'improving' | 'stable' | 'declining';
  factors: {
    positive: string[];
    negative: string[];
    neutral: string[];
  };
  lastCalculated: Date;
}

export interface DealMomentum {
  velocity: 'accelerating' | 'steady' | 'stalled' | 'reversing';
  daysSinceLastActivity: number;
  activitiesLast30Days: number;
  engagementLevel: 'high' | 'medium' | 'low';
  keyMilestones: {
    name: string;
    completed: boolean;
    completedAt?: Date;
    dueDate?: Date;
  }[];
}

export interface Action {
  id: string;
  type: 'email' | 'call' | 'meeting' | 'internal' | 'document' | 'analysis';
  priority: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  suggestedBy: 'ai' | 'user' | 'system';
  reasoning?: string; // Why this action is recommended
  dueDate?: Date;
  assignee?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'dismissed';
  relatedEvidence?: Evidence[];
  automationAvailable?: boolean;
  createdAt: Date;
}

export interface Opportunity {
  id: string;
  type: 'upsell' | 'cross_sell' | 'expansion' | 'renewal' | 'strategic';
  title: string;
  description: string;
  potentialValue?: number;
  confidence: number; // 0-100
  reasoning: string;
  suggestedApproach?: string;
  relatedEvidence: Evidence[];
  identifiedAt: Date;
}

export interface ProcessingQueue {
  items: ProcessingItem[];
  activeCount: number;
  queuedCount: number;
  completedCount: number;
  failedCount: number;
}

export interface ProcessingItem {
  id: string;
  type: 'transcript' | 'document' | 'email' | 'analysis';
  name: string;
  status: 'queued' | 'processing' | 'complete' | 'failed';
  progress?: number; // 0-100
  currentStep?: string;
  startedAt?: Date;
  completedAt?: Date;
  error?: string;
  resultSummary?: {
    evidenceExtracted: number;
    insightsGenerated: number;
    confidenceAverage: number;
  };
}

export interface TimelineEvent {
  id: string;
  type: TimelineEventType;
  title: string;
  description: string;
  timestamp: Date;
  actor?: {
    type: 'user' | 'ai' | 'system';
    name: string;
    id?: string;
  };
  metadata?: {
    evidence?: Evidence;
    previousValue?: any;
    newValue?: any;
    source?: string;
    confidence?: number;
  };
  relatedEvents?: string[]; // IDs of related events
}

export type TimelineEventType = 
  | 'evidence_extracted'
  | 'insight_generated'
  | 'stage_changed'
  | 'health_updated'
  | 'stakeholder_identified'
  | 'risk_identified'
  | 'action_completed'
  | 'document_processed'
  | 'email_processed'
  | 'transcript_processed'
  | 'user_note'
  | 'system_alert';

export interface AccountIntelligence {
  accountId: string;
  accountName: string;
  industry?: string;
  size?: 'enterprise' | 'mid_market' | 'smb';
  
  // Relationship overview
  relationshipHealth: 'strong' | 'good' | 'fair' | 'poor';
  engagementScore: number; // 0-100
  
  // Deal summary
  activeDeals: number;
  totalDealValue: number;
  averageDealHealth: number;
  dealsAtRisk: number;
  
  // Stakeholder network
  stakeholders: Stakeholder[];
  organizationalChart?: OrganizationalNode[];
  
  // Historical context
  previousDeals?: {
    won: number;
    lost: number;
    totalValue: number;
  };
  
  // Strategic insights
  strategicValue: 'high' | 'medium' | 'low';
  expansionPotential: number; // 0-100
  churnRisk: number; // 0-100
}

export interface Stakeholder {
  id: string;
  name: string;
  title: string;
  email?: string;
  phone?: string;
  role: 'champion' | 'economic_buyer' | 'technical_buyer' | 'influencer' | 'blocker' | 'unknown';
  influence: 'high' | 'medium' | 'low';
  sentiment: 'positive' | 'neutral' | 'negative' | 'unknown';
  lastContact?: Date;
  engagementLevel: 'high' | 'medium' | 'low';
  notes?: string;
  relationships?: {
    stakeholderId: string;
    relationshipType: 'reports_to' | 'peer' | 'influences' | 'collaborates_with';
  }[];
}

export interface OrganizationalNode {
  stakeholderId: string;
  parentId?: string;
  children?: OrganizationalNode[];
}