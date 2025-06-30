// MEDDPICC Analysis Types for ASMIS

export type MEDDPICCCategory = 
  | 'metrics'
  | 'economic_buyer'
  | 'decision_criteria'
  | 'decision_process'
  | 'identify_pain'
  | 'champion'
  | 'competition';

export type DealStage = 
  | 'discovery'
  | 'technical_evaluation'
  | 'business_evaluation'
  | 'negotiation'
  | 'closing'
  | 'closed_won'
  | 'closed_lost';

export interface MEDDPICCAnalysis {
  dealId: string;
  accountId: string;
  overallScore: number; // 0-100
  completenessScore: number; // 0-100
  lastUpdated: Date | string;
  processingStatus: ProcessingStatus;
  
  // Components structure (new format)
  components: {
    metrics: MEDDPICCComponent;
    economicBuyer: MEDDPICCComponent;
    decisionCriteria: MEDDPICCComponent;
    decisionProcess: MEDDPICCComponent;
    identifyPain: MEDDPICCComponent;
    champion: MEDDPICCComponent;
    competition: MEDDPICCComponent;
  };
  
  // Legacy individual components (for backward compatibility)
  metrics?: MetricEvidence;
  economicBuyer?: EconomicBuyerEvidence;
  decisionCriteria?: DecisionCriteriaEvidence;
  decisionProcess?: DecisionProcessEvidence;
  identifyPain?: PainPointEvidence;
  champion?: ChampionEvidence;
  competition?: CompetitionEvidence;
  
  // Aggregated insights
  keyInsights: Insight[];
  riskFactors: string[]; // Simplified to strings for UI rendering
  recommendations: Recommendation[];
  strategic_recommendations: string[]; // Add missing property
}

export interface ProcessingStatus {
  status: 'idle' | 'processing' | 'complete' | 'error' | 'not_started';
  progress?: number; // 0-100
  estimatedTimeRemaining?: number; // seconds
  currentStep?: string; // "Extracting stakeholders..."
  lastError?: string;
  message?: string; // Add message field
}

// New simplified component interface for UI compatibility
export interface MEDDPICCComponent {
  status: 'complete' | 'partial' | 'not_started' | 'missing';
  confidence: number; // 0-100
  evidence: Evidence[];
  gaps: string[]; // Information gaps identified
  lastUpdated: string | Date;
  score?: number; // Component score (0-100)
}

export interface BaseEvidence {
  status: 'complete' | 'partial' | 'missing';
  confidence: number; // 0-100
  evidence: Evidence[];
  lastUpdated: Date;
}

export interface MetricEvidence extends BaseEvidence {
  identifiedMetrics: {
    type: 'roi' | 'cost_reduction' | 'efficiency' | 'revenue' | 'other';
    value: string;
    target?: string;
    timeline?: string;
  }[];
  quantified: boolean;
  businessImpact?: string;
}

export interface EconomicBuyerEvidence extends BaseEvidence {
  identified: boolean;
  person?: {
    name: string;
    title: string;
    email?: string;
  };
  accessLevel: 'direct' | 'through_champion' | 'no_access';
  buyingAuthority: 'confirmed' | 'likely' | 'unclear';
}

export interface DecisionCriteriaEvidence extends BaseEvidence {
  criteria: {
    category: 'technical' | 'business' | 'financial' | 'operational';
    requirement: string;
    priority: 'must_have' | 'nice_to_have' | 'optional';
    ourPosition: 'meets' | 'partially_meets' | 'does_not_meet' | 'unknown';
  }[];
  formalRequirements: boolean;
  evaluationProcess?: string;
}

export interface DecisionProcessEvidence extends BaseEvidence {
  steps: {
    name: string;
    owner?: string;
    timeline?: string;
    status: 'completed' | 'in_progress' | 'upcoming' | 'blocked';
  }[];
  timelineIdentified: boolean;
  estimatedCloseDate?: Date;
  paperProcess?: {
    type: 'legal' | 'procurement' | 'security' | 'compliance';
    complexity: 'simple' | 'moderate' | 'complex';
    estimatedDuration?: number; // days
  }[];
}

export interface PainPointEvidence extends BaseEvidence {
  pains: {
    description: string;
    impact: 'critical' | 'high' | 'medium' | 'low';
    currentState?: string;
    desiredState?: string;
    costOfInaction?: string;
  }[];
  urgency: 'immediate' | 'quarterly' | 'annual' | 'undefined';
  businessDrivers: string[];
}

export interface ChampionEvidence extends BaseEvidence {
  identified: boolean;
  person?: {
    name: string;
    title: string;
    email?: string;
  };
  strength: 'strong' | 'developing' | 'weak';
  influence: 'high' | 'medium' | 'low';
  engagement: {
    lastContact?: Date;
    frequency: 'daily' | 'weekly' | 'monthly' | 'sporadic';
    quality: 'proactive' | 'responsive' | 'passive';
  };
}

export interface CompetitionEvidence extends BaseEvidence {
  competitors: {
    name: string;
    status: 'incumbent' | 'evaluating' | 'eliminated' | 'unknown';
    strengths?: string[];
    weaknesses?: string[];
    ourAdvantages?: string[];
  }[];
  competitiveLandscape: 'no_competition' | 'favored' | 'competitive' | 'disadvantaged';
  differentiators: string[];
}

export interface Evidence {
  id: string;
  type: 'transcript' | 'email' | 'document' | 'note';
  title: string; // Title/summary of the evidence
  content: string;
  excerpt: string; // The specific highlighted portion
  meddpicc_category?: MEDDPICCCategory; // Which MEDDPICC component this evidence supports
  source: {
    id: string;
    name: string; // "Demo Call - Oct 23"
    timestamp?: string; // "14:23" for transcripts
    url?: string; // For documents
  };
  position: {
    start: number; // Character position in source
    end: number;
  };
  confidence: number; // 0-100
  businessImplication?: string;
  extractedBy: string; // AI agent that extracted this
  createdAt: Date;
  validatedAt?: Date;
}

export interface Insight {
  id: string;
  type: 'opportunity' | 'risk' | 'action' | 'observation';
  category: MEDDPICCCategory;
  title: string;
  description: string;
  impact: 'critical' | 'high' | 'medium' | 'low';
  evidence: Evidence[];
  suggestedAction?: string;
  createdAt: Date;
}

export interface Risk {
  id: string;
  category: MEDDPICCCategory;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  likelihood: 'certain' | 'likely' | 'possible' | 'unlikely';
  mitigation?: string;
  evidence: Evidence[];
  identifiedAt: Date;
}

export interface Recommendation {
  id: string;
  type: 'immediate' | 'short_term' | 'strategic';
  category: MEDDPICCCategory;
  title: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  expectedOutcome?: string;
  effort: 'low' | 'medium' | 'high';
  suggestedOwner?: string;
  dueDate?: Date;
  evidence: Evidence[];
}