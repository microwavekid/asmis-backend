# Evidence Overlay Feature Enhancement

## Overview
Interactive evidence visualization that allows users to hover over intelligence elements in the UI and see the original transcript context where that evidence was extracted, with highlighting and contextual focus.

## User Experience Flow
1. User views MEDDPICC analysis results in dashboard
2. User hovers over any evidence indicator (badge, icon, underlined text)
3. Overlay appears showing:
   - Original transcript excerpt with evidence highlighted
   - Surrounding context (±3 sentences)
   - Timestamp and speaker information
   - Confidence score for that evidence
   - Link to full transcript

## Backend Data Requirements

### Enhanced Evidence Storage
```python
@dataclass
class EvidencePointer:
    """Enhanced evidence with precise transcript location."""
    evidence_text: str
    transcript_id: str
    start_position: int  # Character position in transcript
    end_position: int    # Character position in transcript
    speaker: str
    timestamp: str       # When in meeting this was said
    confidence: float
    context_before: str  # ±150 characters before
    context_after: str   # ±150 characters after
    extraction_type: str # "explicit_mention", "inferred", "sentiment"
    
@dataclass
class TranscriptSegment:
    """Structured transcript with precise positioning."""
    segment_id: str
    transcript_id: str
    speaker: str
    start_time: str      # "00:15:32"
    end_time: str        # "00:15:45"
    text: str
    start_position: int  # Character position in full transcript
    end_position: int    # Character position in full transcript
    word_count: int
```

### Database Schema Enhancements
```sql
-- Enhanced transcript storage with positioning
CREATE TABLE transcript_segments (
    segment_id UUID PRIMARY KEY,
    transcript_id UUID REFERENCES transcripts(transcript_id),
    speaker VARCHAR(255),
    start_time VARCHAR(10),  -- "00:15:32"
    end_time VARCHAR(10),    -- "00:15:45" 
    text TEXT,
    start_position INTEGER,  -- Character position in full transcript
    end_position INTEGER,    -- Character position in full transcript
    word_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Evidence linking with precise positioning
CREATE TABLE intelligence_evidence (
    evidence_id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES meddpicc_analysis(analysis_id),
    element_type VARCHAR(50),  -- "decision_criteria", "champion", etc.
    element_key VARCHAR(100),  -- Specific criterion ID or element identifier
    evidence_text TEXT,
    transcript_id UUID REFERENCES transcripts(transcript_id),
    segment_id UUID REFERENCES transcript_segments(segment_id),
    start_position INTEGER,
    end_position INTEGER,
    speaker VARCHAR(255),
    timestamp VARCHAR(10),
    confidence FLOAT,
    context_before TEXT,
    context_after TEXT,
    extraction_type VARCHAR(50),  -- "explicit", "inferred", "sentiment"
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast evidence lookups
CREATE INDEX idx_evidence_analysis_element ON intelligence_evidence(analysis_id, element_type, element_key);
CREATE INDEX idx_evidence_transcript ON intelligence_evidence(transcript_id, start_position);
```

### Backend API Enhancements
```python
class EvidenceService:
    """Service for evidence overlay functionality."""
    
    def get_evidence_context(self, evidence_id: str) -> Dict[str, Any]:
        """Get full context for evidence overlay."""
        evidence = self.db.get_evidence_by_id(evidence_id)
        transcript = self.db.get_transcript(evidence.transcript_id)
        
        return {
            "evidence": {
                "text": evidence.evidence_text,
                "highlighted_start": evidence.start_position,
                "highlighted_end": evidence.end_position,
                "confidence": evidence.confidence,
                "extraction_type": evidence.extraction_type
            },
            "context": {
                "before": evidence.context_before,
                "after": evidence.context_after,
                "speaker": evidence.speaker,
                "timestamp": evidence.timestamp
            },
            "transcript_info": {
                "meeting_title": transcript.title,
                "meeting_date": transcript.date,
                "attendees": transcript.attendees
            },
            "navigation": {
                "transcript_id": evidence.transcript_id,
                "segment_id": evidence.segment_id
            }
        }
    
    def get_surrounding_context(self, transcript_id: str, position: int, 
                              context_chars: int = 300) -> str:
        """Get expanded context around evidence position."""
        transcript = self.db.get_full_transcript(transcript_id)
        
        start = max(0, position - context_chars)
        end = min(len(transcript.content), position + context_chars)
        
        return transcript.content[start:end]

# API Endpoints
@app.get("/api/evidence/{evidence_id}/context")
async def get_evidence_context(evidence_id: str):
    """Get evidence context for overlay display."""
    service = EvidenceService()
    return service.get_evidence_context(evidence_id)

@app.get("/api/evidence/{evidence_id}/expanded-context")
async def get_expanded_context(evidence_id: str, context_size: int = 500):
    """Get expanded context for full transcript view."""
    service = EvidenceService()
    return service.get_surrounding_context(evidence_id, context_size)
```

## Frontend Implementation

### UI Components
```typescript
// Evidence Badge Component
interface EvidenceBadge {
  evidenceId: string;
  confidenceScore: number;
  evidenceType: 'explicit' | 'inferred' | 'sentiment';
  text: string;
}

const EvidenceBadge: React.FC<EvidenceBadge> = ({ 
  evidenceId, confidenceScore, evidenceType, text 
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [overlayData, setOverlayData] = useState(null);
  
  const handleHover = async () => {
    if (!overlayData) {
      const response = await fetch(`/api/evidence/${evidenceId}/context`);
      const data = await response.json();
      setOverlayData(data);
    }
    setIsHovered(true);
  };

  return (
    <div 
      className="evidence-badge"
      onMouseEnter={handleHover}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Badge variant={getVariantByConfidence(confidenceScore)}>
        {getEvidenceIcon(evidenceType)}
        {confidenceScore > 0.8 ? 'High' : 'Medium'} Confidence
      </Badge>
      
      {isHovered && overlayData && (
        <EvidenceOverlay data={overlayData} position="below" />
      )}
    </div>
  );
};

// Evidence Overlay Component
interface EvidenceOverlayProps {
  data: {
    evidence: {
      text: string;
      highlighted_start: number;
      highlighted_end: number;
      confidence: number;
      extraction_type: string;
    };
    context: {
      before: string;
      after: string;
      speaker: string;
      timestamp: string;
    };
    transcript_info: {
      meeting_title: string;
      meeting_date: string;
      attendees: string[];
    };
  };
  position: 'above' | 'below' | 'right';
}

const EvidenceOverlay: React.FC<EvidenceOverlayProps> = ({ data, position }) => {
  const highlightedText = data.evidence.text;
  const fullContext = `${data.context.before}${highlightedText}${data.context.after}`;
  
  return (
    <div className={`evidence-overlay evidence-overlay--${position}`}>
      <div className="evidence-overlay__header">
        <div className="meeting-info">
          <h4>{data.transcript_info.meeting_title}</h4>
          <span className="speaker-time">
            {data.context.speaker} • {data.context.timestamp}
          </span>
        </div>
        <div className="confidence-score">
          <Badge variant="outline">
            {Math.round(data.evidence.confidence * 100)}% confident
          </Badge>
        </div>
      </div>
      
      <div className="evidence-overlay__content">
        <div className="transcript-excerpt">
          <span className="context-before">{data.context.before}</span>
          <mark className="evidence-highlight">{highlightedText}</mark>
          <span className="context-after">{data.context.after}</span>
        </div>
      </div>
      
      <div className="evidence-overlay__footer">
        <Button 
          variant="ghost" 
          size="sm"
          onClick={() => openFullTranscript(data.transcript_info.transcript_id)}
        >
          View Full Transcript →
        </Button>
      </div>
    </div>
  );
};
```

### CSS Styling
```css
.evidence-badge {
  position: relative;
  display: inline-block;
}

.evidence-overlay {
  position: absolute;
  z-index: 1000;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  min-width: 300px;
}

.evidence-overlay--below {
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 8px;
}

.evidence-overlay--above {
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 8px;
}

.evidence-overlay__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 8px;
}

.meeting-info h4 {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: #1e293b;
}

.speaker-time {
  font-size: 12px;
  color: #64748b;
}

.transcript-excerpt {
  font-size: 14px;
  line-height: 1.5;
  color: #475569;
}

.context-before,
.context-after {
  color: #94a3b8;
}

.evidence-highlight {
  background-color: #fef3c7;
  padding: 2px 4px;
  border-radius: 3px;
  font-weight: 500;
  color: #92400e;
}

.evidence-overlay__footer {
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px solid #f1f5f9;
  text-align: right;
}
```

### Dashboard Integration Examples
```typescript
// MEDDPICC Dashboard Component
const MEDDPICCDashboard = ({ dealAnalysis }) => {
  return (
    <div className="meddpicc-dashboard">
      {/* Decision Criteria Section */}
      <section className="criteria-section">
        <h3>Decision Criteria</h3>
        {dealAnalysis.decision_criteria.map(criterion => (
          <div key={criterion.id} className="criterion-card">
            <div className="criterion-header">
              <span className="criterion-text">{criterion.text}</span>
              <EvidenceBadge 
                evidenceId={criterion.evidence_id}
                confidenceScore={criterion.confidence}
                evidenceType={criterion.extraction_type}
                text="Source"
              />
            </div>
            <div className="criterion-meta">
              <Badge>{criterion.business_unit}</Badge>
              <Badge variant="outline">{criterion.priority}</Badge>
            </div>
          </div>
        ))}
      </section>
      
      {/* Champion Section */}
      <section className="champion-section">
        <h3>Champion</h3>
        <div className="champion-info">
          <span>{dealAnalysis.champion.name}</span>
          <EvidenceBadge 
            evidenceId={dealAnalysis.champion.evidence_id}
            confidenceScore={dealAnalysis.champion.confidence}
            evidenceType="explicit"
            text="Quote"
          />
        </div>
      </section>
    </div>
  );
};
```

## Intelligence Analysis Updates

### Enhanced Evidence Extraction
```python
class EvidenceEnhancedAnalyzer:
    """Enhanced analyzer that captures precise evidence positioning."""
    
    def extract_with_positions(self, transcript: str, transcript_id: str) -> Dict[str, Any]:
        """Extract intelligence with precise evidence positioning."""
        
        # Parse transcript into segments
        segments = self.parse_transcript_segments(transcript)
        
        # Extract intelligence with positioning
        meddpicc_analysis = {}
        
        for element_type in ['champion', 'economic_buyer', 'decision_criteria']:
            element_data, evidence_pointers = self.extract_element_with_evidence(
                element_type, transcript, segments, transcript_id
            )
            
            meddpicc_analysis[element_type] = element_data
            
            # Store evidence pointers
            for evidence in evidence_pointers:
                self.store_evidence_pointer(evidence, element_type, element_data['id'])
        
        return meddpicc_analysis
    
    def extract_element_with_evidence(self, element_type: str, transcript: str, 
                                    segments: List[TranscriptSegment], 
                                    transcript_id: str) -> Tuple[Dict, List[EvidencePointer]]:
        """Extract element and capture precise evidence locations."""
        
        evidence_pointers = []
        
        # Use regex or AI to find evidence with positions
        matches = self.find_evidence_matches(element_type, transcript)
        
        for match in matches:
            # Find which segment this evidence belongs to
            segment = self.find_containing_segment(match.start(), segments)
            
            evidence_pointer = EvidencePointer(
                evidence_text=match.group(),
                transcript_id=transcript_id,
                start_position=match.start(),
                end_position=match.end(),
                speaker=segment.speaker,
                timestamp=segment.start_time,
                confidence=self.calculate_evidence_confidence(match),
                context_before=transcript[max(0, match.start()-150):match.start()],
                context_after=transcript[match.end():match.end()+150],
                extraction_type="explicit_mention"
            )
            
            evidence_pointers.append(evidence_pointer)
        
        return self.build_element_data(matches), evidence_pointers
```

## Transcript Management System

### Overview
Full transcript viewing and management system that integrates with evidence overlay for seamless navigation from insight to source.

### UI Components

#### 1. Transcript Manager Dashboard
```typescript
// Main transcript listing and management
const TranscriptManager: React.FC = () => {
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [filters, setFilters] = useState({
    dateRange: 'last_30_days',
    account: null,
    deal: null,
    attendees: []
  });

  return (
    <div className="transcript-manager">
      <div className="transcript-manager__header">
        <h2>Meeting Transcripts</h2>
        <div className="actions">
          <Button variant="outline" onClick={handleExport}>
            Export Selected
          </Button>
          <Button onClick={handleUpload}>
            Upload Transcript
          </Button>
        </div>
      </div>

      <TranscriptFilters 
        filters={filters} 
        onFilterChange={setFilters} 
      />

      <TranscriptList 
        transcripts={transcripts}
        onTranscriptClick={navigateToViewer}
      />
    </div>
  );
};
```

#### 2. Transcript Viewer with Deep Linking
```typescript
interface TranscriptViewerProps {
  transcriptId: string;
  highlightPosition?: { start: number; end: number };
  scrollToEvidence?: boolean;
}

const TranscriptViewer: React.FC<TranscriptViewerProps> = ({ 
  transcriptId, 
  highlightPosition,
  scrollToEvidence 
}) => {
  const [transcript, setTranscript] = useState<TranscriptData>(null);
  const [activeSegment, setActiveSegment] = useState<string>(null);
  const segmentRefs = useRef<{ [key: string]: HTMLElement }>({});

  useEffect(() => {
    if (scrollToEvidence && highlightPosition) {
      // Scroll to and highlight the evidence
      const element = document.getElementById(`char-${highlightPosition.start}`);
      element?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [transcript, highlightPosition]);

  return (
    <div className="transcript-viewer">
      <TranscriptHeader 
        title={transcript?.title}
        date={transcript?.date}
        attendees={transcript?.attendees}
        duration={transcript?.duration}
      />

      <div className="transcript-viewer__content">
        <TranscriptSidebar
          segments={transcript?.segments}
          activeSegment={activeSegment}
          meddpiccElements={transcript?.extracted_intelligence}
          onSegmentClick={scrollToSegment}
        />

        <TranscriptBody
          segments={transcript?.segments}
          highlightPosition={highlightPosition}
          onSegmentInView={setActiveSegment}
        />

        <IntelligencePanel
          intelligence={transcript?.extracted_intelligence}
          onEvidenceClick={scrollToEvidence}
        />
      </div>
    </div>
  );
};
```

#### 3. Interactive Transcript Body
```typescript
const TranscriptBody: React.FC<TranscriptBodyProps> = ({ 
  segments, 
  highlightPosition 
}) => {
  return (
    <div className="transcript-body">
      {segments.map((segment, index) => (
        <TranscriptSegment
          key={segment.id}
          segment={segment}
          isHighlighted={isWithinHighlight(segment, highlightPosition)}
          renderContent={(text) => (
            <HighlightableText
              text={text}
              highlights={getHighlightsForSegment(segment)}
              onClick={handleTextSelection}
            />
          )}
        />
      ))}
    </div>
  );
};

const TranscriptSegment: React.FC<TranscriptSegmentProps> = ({ 
  segment, 
  isHighlighted,
  renderContent 
}) => {
  return (
    <div 
      className={`transcript-segment ${isHighlighted ? 'highlighted' : ''}`}
      id={`segment-${segment.id}`}
    >
      <div className="segment-header">
        <span className="speaker">{segment.speaker}</span>
        <span className="timestamp">{segment.timestamp}</span>
      </div>
      <div className="segment-content">
        {renderContent(segment.text)}
      </div>
      <div className="segment-actions">
        <Button size="sm" variant="ghost" onClick={() => copySegment(segment)}>
          Copy
        </Button>
        <Button size="sm" variant="ghost" onClick={() => annotateSegment(segment)}>
          Add Note
        </Button>
      </div>
    </div>
  );
};
```

### Deep Linking Navigation Flow

#### 1. From Evidence Overlay to Transcript
```typescript
// In Evidence Overlay Component
const navigateToTranscript = (transcriptId: string, evidencePosition: Position) => {
  // Navigate with state for highlighting
  router.push({
    pathname: `/transcripts/${transcriptId}`,
    query: {
      highlight: `${evidencePosition.start}-${evidencePosition.end}`,
      scrollTo: 'true'
    }
  });
};

// In Transcript Viewer
const { transcriptId } = router.params;
const { highlight, scrollTo } = router.query;

useEffect(() => {
  if (highlight) {
    const [start, end] = highlight.split('-').map(Number);
    setHighlightPosition({ start, end });
    
    if (scrollTo === 'true') {
      // Scroll to evidence after transcript loads
      scrollToPosition(start);
    }
  }
}, [highlight, scrollTo]);
```

#### 2. Synchronized Intelligence View
```typescript
// Intelligence panel showing extracted MEDDPICC elements
const IntelligencePanel: React.FC = ({ intelligence, onEvidenceClick }) => {
  return (
    <div className="intelligence-panel">
      <h3>Extracted Intelligence</h3>
      
      {/* Decision Criteria */}
      <section className="intelligence-section">
        <h4>Decision Criteria</h4>
        {intelligence.decision_criteria.map(criterion => (
          <div 
            key={criterion.id}
            className="intelligence-item"
            onClick={() => onEvidenceClick(criterion.evidence_position)}
          >
            <span className="criterion-text">{criterion.text}</span>
            <Badge>{criterion.priority}</Badge>
            <span className="evidence-link">View in transcript →</span>
          </div>
        ))}
      </section>

      {/* Risk Signals */}
      <section className="intelligence-section">
        <h4>Risk Signals</h4>
        {intelligence.risks.map(risk => (
          <div 
            className="risk-item"
            onClick={() => onEvidenceClick(risk.evidence_position)}
          >
            <Badge variant="destructive">{risk.severity}</Badge>
            <span>{risk.description}</span>
          </div>
        ))}
      </section>
    </div>
  );
};
```

### Enhanced Backend Support

#### Transcript Search & Navigation API
```python
@app.get("/api/transcripts")
async def list_transcripts(
    account_id: Optional[str] = None,
    deal_id: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    attendee: Optional[str] = None,
    search_query: Optional[str] = None
):
    """List and search transcripts with filtering."""
    filters = TranscriptFilters(
        account_id=account_id,
        deal_id=deal_id,
        date_range=(date_from, date_to),
        attendee=attendee,
        search_query=search_query
    )
    
    return transcript_service.search_transcripts(filters)

@app.get("/api/transcripts/{transcript_id}/structured")
async def get_structured_transcript(
    transcript_id: str,
    include_intelligence: bool = True
):
    """Get transcript with segments and extracted intelligence."""
    transcript = transcript_service.get_structured_transcript(transcript_id)
    
    if include_intelligence:
        # Include all MEDDPICC elements with evidence positions
        transcript['extracted_intelligence'] = intelligence_service.get_transcript_intelligence(transcript_id)
    
    return transcript

@app.post("/api/transcripts/{transcript_id}/annotate")
async def annotate_transcript_segment(
    transcript_id: str,
    segment_id: str,
    annotation: AnnotationRequest
):
    """Add user annotation to transcript segment."""
    return transcript_service.add_annotation(
        transcript_id, 
        segment_id, 
        annotation.text,
        annotation.user_id
    )
```

### Advanced Features

#### 1. Multi-Transcript Intelligence View
```typescript
// View intelligence across multiple meetings for a deal
const DealTranscriptTimeline: React.FC = ({ dealId }) => {
  const [transcripts, setTranscripts] = useState<TranscriptSummary[]>([]);
  
  return (
    <div className="transcript-timeline">
      {transcripts.map(transcript => (
        <TimelineItem key={transcript.id}>
          <div className="timeline-date">{transcript.date}</div>
          <div className="timeline-content">
            <h4>{transcript.title}</h4>
            <div className="key-insights">
              {transcript.key_insights.map(insight => (
                <InsightCard 
                  insight={insight}
                  onClick={() => navigateToEvidence(transcript.id, insight.position)}
                />
              ))}
            </div>
          </div>
        </TimelineItem>
      ))}
    </div>
  );
};
```

#### 2. Transcript Comparison View
```typescript
// Compare intelligence evolution across meetings
const TranscriptComparison: React.FC = ({ transcriptIds }) => {
  return (
    <div className="transcript-comparison">
      <ComparisonHeader transcripts={transcripts} />
      
      <div className="comparison-grid">
        {/* Show how decision criteria evolved */}
        <ComparisonRow element="decision_criteria">
          {transcripts.map(t => (
            <CriteriaEvolution 
              key={t.id}
              criteria={t.intelligence.decision_criteria}
              onEvidenceClick={(pos) => navigateToTranscript(t.id, pos)}
            />
          ))}
        </ComparisonRow>
        
        {/* Show stakeholder evolution */}
        <ComparisonRow element="stakeholders">
          {transcripts.map(t => (
            <StakeholderEvolution 
              stakeholders={t.intelligence.stakeholders}
              onEvidenceClick={(pos) => navigateToTranscript(t.id, pos)}
            />
          ))}
        </ComparisonRow>
      </div>
    </div>
  );
};
```

## Implementation Priority

### Phase 1: Backend Foundation
1. Enhanced evidence storage schema
2. Transcript segmentation and positioning
3. Evidence extraction with positions
4. API endpoints for evidence context

### Phase 2: Core Transcript Features
1. Transcript listing and search UI
2. Basic transcript viewer with segments
3. Deep linking from evidence overlay
4. Evidence highlighting in transcript

### Phase 3: Frontend Components  
1. Evidence badge component
2. Overlay component with positioning
3. Integration with existing dashboard components

### Phase 4: Advanced Features
1. Multi-transcript timeline view
2. Intelligence comparison across meetings
3. Transcript annotations and notes
4. Team collaboration features

## Success Metrics
- **User Engagement**: Hover rate on evidence badges
- **Trust Building**: User confidence in AI insights
- **Efficiency**: Time to validate intelligence claims
- **Transparency**: User understanding of AI reasoning

This feature bridges the gap between AI-generated insights and human verification, building trust through transparency and enabling rapid validation of intelligence claims.