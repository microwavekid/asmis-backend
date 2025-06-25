// Evidence System Types for ASMIS

export interface EvidenceFilters {
  types?: ('transcript' | 'email' | 'document' | 'note')[];
  confidenceMin?: number;
  confidenceMax?: number;
  dateFrom?: Date;
  dateTo?: Date;
  categories?: string[];
  sources?: string[];
}

export interface EvidenceListResponse {
  evidence: Evidence[];
  total: number;
  offset: number;
  limit: number;
  hasMore: boolean;
  nextOffset?: number;
}

export interface EvidenceSource {
  id: string;
  type: 'transcript' | 'email' | 'document' | 'note';
  name: string;
  description?: string;
  url?: string;
  createdAt: Date;
  processedAt?: Date;
  metadata: {
    duration?: number; // For transcripts (minutes)
    attendees?: string[]; // For meetings
    sender?: string; // For emails
    recipients?: string[]; // For emails
    pageCount?: number; // For documents
    fileSize?: number; // bytes
  };
}

export interface EvidenceContext {
  evidenceId: string;
  beforeText: string; // Text before the evidence (for context)
  evidenceText: string; // The actual evidence text
  afterText: string; // Text after the evidence (for context)
  speakerName?: string; // For transcripts
  speakerRole?: string; // For transcripts
  timestamp?: string; // Time in transcript/meeting
  pageNumber?: number; // For documents
  paragraphIndex?: number; // Position in document
}

export interface EvidenceCitation {
  text: string; // The text to be cited
  evidenceId: string;
  confidence: number;
  position: {
    start: number;
    end: number;
  };
  tooltip?: {
    sourceInfo: string;
    excerpt: string;
    confidence: number;
    viewSourceAction?: () => void;
  };
}

export interface EvidenceOverlay {
  isOpen: boolean;
  position: {
    x: number;
    y: number;
  };
  evidence: Evidence;
  context?: EvidenceContext;
  actions: {
    viewSource: () => void;
    copyReference: () => void;
    reportIssue: () => void;
  };
}

export interface EvidencePanel {
  dealId: string;
  isOpen: boolean;
  filters: EvidenceFilters;
  sortBy: 'date' | 'confidence' | 'relevance';
  sortOrder: 'asc' | 'desc';
  selectedEvidence?: Evidence[];
  viewMode: 'list' | 'grouped' | 'timeline';
}

export interface EvidenceHighlight {
  evidenceId: string;
  text: string;
  color?: string; // Custom highlight color
  isActive: boolean;
  onClick?: () => void;
  onHover?: () => void;
}

export interface EvidenceStats {
  totalCount: number;
  byType: {
    transcript: number;
    email: number;
    document: number;
    note: number;
  };
  byConfidence: {
    high: number; // 80-100
    medium: number; // 60-79
    low: number; // 0-59
  };
  recentlyAdded: number; // Last 24 hours
  sourcesProcessed: number;
}

// Re-export the base Evidence type from meddpicc.ts to avoid duplication
export type { Evidence } from './meddpicc';