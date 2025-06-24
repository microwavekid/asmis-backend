# Multi-Source Evidence System Enhancement

## Overview
Extend the evidence overlay and navigation system to support multiple evidence sources: transcripts, documents, and emails. Each source type has unique navigation and display requirements.

## Document Evidence System

### Document-Specific Challenges
- **Navigation**: Page/section based vs timestamp based
- **Formats**: PDF, Word, PowerPoint, Excel, Google Docs
- **Content Types**: Text, tables, charts, images
- **Evidence Spans**: May cross pages or be in non-text elements
- **Context**: Surrounding pages/sections vs surrounding conversation

### Backend Data Structure

#### Enhanced Evidence Storage for Documents
```python
@dataclass
class DocumentEvidence:
    """Evidence extracted from documents."""
    evidence_id: str
    document_id: str
    evidence_text: str
    evidence_type: str  # "text", "table", "chart", "image_caption"
    
    # Document-specific positioning
    page_number: int
    section_name: Optional[str]  # "Executive Summary", "Pricing", etc.
    paragraph_index: Optional[int]
    
    # Bounding box for visual elements
    bbox: Optional[Dict[str, float]]  # {"x": 100, "y": 200, "width": 300, "height": 150}
    
    # For text within documents
    start_offset: Optional[int]  # Character offset within page
    end_offset: Optional[int]
    
    # Context
    page_context: str  # Full text of the page
    adjacent_pages: Dict[str, str]  # {"previous": "...", "next": "..."}
    
    # Metadata
    confidence: float
    extraction_method: str  # "ocr", "native_text", "table_extraction", "chart_analysis"

@dataclass
class DocumentStructure:
    """Structured document representation."""
    document_id: str
    title: str
    document_type: str  # "pdf", "docx", "pptx", "xlsx"
    total_pages: int
    
    # Document outline
    sections: List[DocumentSection]
    
    # Extracted elements
    tables: List[TableElement]
    charts: List[ChartElement]
    images: List[ImageElement]
    
    # Metadata
    author: str
    created_date: str
    last_modified: str
    file_size: int
```

### Database Schema for Documents
```sql
-- Document storage with structure
CREATE TABLE documents (
    document_id UUID PRIMARY KEY,
    deal_id UUID REFERENCES deals(deal_id),
    account_id UUID REFERENCES accounts(account_id),
    title VARCHAR(500),
    document_type VARCHAR(50),
    file_path TEXT,
    total_pages INTEGER,
    extracted_text TEXT,
    metadata JSONB,
    uploaded_by VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Document sections/pages
CREATE TABLE document_sections (
    section_id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(document_id),
    section_type VARCHAR(50), -- 'page', 'chapter', 'section'
    section_name VARCHAR(255),
    page_start INTEGER,
    page_end INTEGER,
    content TEXT,
    content_hash VARCHAR(64),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Document evidence linking
CREATE TABLE document_evidence (
    evidence_id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES meddpicc_analysis(analysis_id),
    document_id UUID REFERENCES documents(document_id),
    element_type VARCHAR(50),
    element_key VARCHAR(100),
    evidence_text TEXT,
    evidence_type VARCHAR(50), -- 'text', 'table', 'chart', 'image'
    page_number INTEGER,
    section_name VARCHAR(255),
    paragraph_index INTEGER,
    bbox JSONB, -- Bounding box for visual elements
    start_offset INTEGER,
    end_offset INTEGER,
    confidence FLOAT,
    extraction_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for fast document evidence lookup
CREATE INDEX idx_doc_evidence_page ON document_evidence(document_id, page_number);
CREATE INDEX idx_doc_evidence_element ON document_evidence(analysis_id, element_type);
```

### Document Viewer UI Components

#### 1. Document Manager Dashboard
```typescript
const DocumentManager: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [filters, setFilters] = useState({
    documentType: 'all', // pdf, docx, pptx, xlsx
    dateRange: 'last_30_days',
    account: null,
    deal: null,
    tags: []
  });

  return (
    <div className="document-manager">
      <div className="document-manager__header">
        <h2>Sales Documents</h2>
        <div className="actions">
          <Button variant="outline" onClick={handleBulkExport}>
            Export Selected
          </Button>
          <Button onClick={handleUpload}>
            Upload Document
          </Button>
        </div>
      </div>

      <DocumentFilters 
        filters={filters} 
        onFilterChange={setFilters} 
      />

      <DocumentGrid 
        documents={documents}
        onDocumentClick={navigateToViewer}
        viewMode="grid" // or "list"
      />
    </div>
  );
};
```

#### 2. Document Viewer with Evidence Navigation
```typescript
interface DocumentViewerProps {
  documentId: string;
  highlightEvidence?: {
    page: number;
    bbox?: BoundingBox;
    textRange?: { start: number; end: number };
  };
  scrollToPage?: number;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ 
  documentId, 
  highlightEvidence,
  scrollToPage 
}) => {
  const [document, setDocument] = useState<DocumentData>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [zoom, setZoom] = useState(100);
  const [viewMode, setViewMode] = useState<'single' | 'continuous'>('single');

  useEffect(() => {
    if (scrollToPage) {
      navigateToPage(scrollToPage);
    }
    if (highlightEvidence) {
      navigateToPage(highlightEvidence.page);
      highlightRegion(highlightEvidence);
    }
  }, [scrollToPage, highlightEvidence]);

  return (
    <div className="document-viewer">
      <DocumentHeader 
        title={document?.title}
        documentType={document?.type}
        totalPages={document?.totalPages}
        metadata={document?.metadata}
      />

      <DocumentToolbar
        currentPage={currentPage}
        totalPages={document?.totalPages}
        zoom={zoom}
        onZoomChange={setZoom}
        onPageChange={setCurrentPage}
        onDownload={handleDownload}
        onPrint={handlePrint}
      />

      <div className="document-viewer__content">
        <DocumentOutline
          sections={document?.sections}
          currentPage={currentPage}
          onSectionClick={navigateToSection}
        />

        <DocumentCanvas
          document={document}
          currentPage={currentPage}
          zoom={zoom}
          viewMode={viewMode}
          highlights={getHighlightsForPage(currentPage)}
          onTextSelection={handleTextSelection}
          onElementClick={handleElementClick}
        />

        <IntelligencePanel
          intelligence={document?.extracted_intelligence}
          currentPage={currentPage}
          onEvidenceClick={navigateToEvidence}
        />
      </div>
    </div>
  );
};
```

#### 3. Document Canvas with Highlighting
```typescript
const DocumentCanvas: React.FC<DocumentCanvasProps> = ({
  document,
  currentPage,
  zoom,
  highlights
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  const renderPage = async (pageNum: number) => {
    if (document.type === 'pdf') {
      // PDF.js rendering with highlights
      const page = await pdfDoc.getPage(pageNum);
      const viewport = page.getViewport({ scale: zoom / 100 });
      
      // Render base PDF
      await page.render({ canvasContext, viewport }).promise;
      
      // Overlay highlights
      highlights.forEach(highlight => {
        if (highlight.bbox) {
          drawHighlightBox(canvasContext, highlight.bbox, viewport);
        }
      });
    } else {
      // HTML-based rendering for other formats
      renderDocumentHTML(document, pageNum, highlights);
    }
  };

  return (
    <div className="document-canvas">
      {document.type === 'pdf' ? (
        <canvas ref={canvasRef} />
      ) : (
        <div className="document-html-content">
          <HighlightableDocument
            content={document.pages[currentPage]}
            highlights={highlights}
            onTextSelect={onTextSelection}
          />
        </div>
      )}
      
      {/* Floating annotations */}
      {highlights.map(highlight => (
        <EvidenceAnnotation
          key={highlight.id}
          position={highlight.bbox}
          evidence={highlight.evidence}
          onClick={() => showEvidenceDetail(highlight)}
        />
      ))}
    </div>
  );
};
```

#### 4. Evidence Overlay for Documents
```typescript
const DocumentEvidenceOverlay: React.FC<DocumentEvidenceProps> = ({ 
  evidence,
  position 
}) => {
  return (
    <div className="document-evidence-overlay" style={getPositionStyle(position)}>
      <div className="evidence-header">
        <h4>{evidence.document_title}</h4>
        <span className="page-info">Page {evidence.page_number}</span>
      </div>
      
      <div className="evidence-content">
        {evidence.evidence_type === 'table' ? (
          <TablePreview data={evidence.table_data} highlighted={evidence.highlighted_cells} />
        ) : evidence.evidence_type === 'chart' ? (
          <ChartPreview 
            chartImage={evidence.chart_image} 
            caption={evidence.evidence_text}
          />
        ) : (
          <TextEvidence 
            text={evidence.evidence_text}
            context={evidence.page_context}
          />
        )}
      </div>
      
      <div className="evidence-actions">
        <Button 
          size="sm" 
          onClick={() => navigateToDocument(evidence.document_id, evidence.page_number)}
        >
          View in Document →
        </Button>
      </div>
    </div>
  );
};
```

### Document-Specific Features

#### 1. Multi-Format Support
```typescript
// Document type handlers
const documentHandlers = {
  pdf: {
    viewer: PDFViewer,
    extractor: PDFTextExtractor,
    highlighter: PDFHighlighter
  },
  docx: {
    viewer: WordViewer,
    extractor: WordTextExtractor,
    highlighter: WordHighlighter
  },
  pptx: {
    viewer: PowerPointViewer,
    extractor: SlideExtractor,
    highlighter: SlideHighlighter
  },
  xlsx: {
    viewer: ExcelViewer,
    extractor: SpreadsheetExtractor,
    highlighter: CellHighlighter
  }
};
```

#### 2. Visual Evidence Handling
```typescript
// Table evidence extraction and display
interface TableEvidence {
  tableId: string;
  documentId: string;
  pageNumber: number;
  headers: string[];
  rows: string[][];
  highlightedCells: Array<{row: number, col: number}>;
  extractedInsight: string; // "Pricing tier shows Enterprise at $50K/year"
}

// Chart evidence extraction
interface ChartEvidence {
  chartId: string;
  documentId: string;
  pageNumber: number;
  chartType: 'bar' | 'line' | 'pie' | 'other';
  chartImage: string; // base64 or URL
  extractedData: any; // Parsed data points
  insight: string; // "Competitor comparison shows 40% price advantage"
}
```

## Email Evidence System (High-Level Concept)

### Overview
Emails represent a unique evidence source with threading, attachments, and communication patterns that provide rich sales intelligence.

### Key Differences from Documents/Transcripts
- **Threading**: Evidence may span multiple emails in a thread
- **Participants**: Multiple stakeholders with varying engagement
- **Attachments**: Documents within emails
- **Temporal**: Time-based like transcripts but asynchronous
- **Sentiment**: Tone and urgency indicators

### Basic Email Evidence Structure
```python
@dataclass
class EmailEvidence:
    """Evidence extracted from email communications."""
    evidence_id: str
    email_id: str
    thread_id: str
    
    # Email-specific location
    email_section: str  # "subject", "body", "attachment_reference"
    paragraph_index: Optional[int]
    
    # Threading context
    position_in_thread: int
    previous_emails: List[str]  # IDs for context
    
    # Participants
    sender: str
    recipients: List[str]
    
    # Evidence details
    evidence_text: str
    sentiment: str  # "positive", "negative", "neutral", "urgent"
    
    # Metadata
    timestamp: datetime
    confidence: float
```

### Email Integration Concepts

#### 1. Email Thread Viewer
```typescript
// Visualize evidence across email threads
const EmailThreadViewer: React.FC = ({ threadId, highlightEvidence }) => {
  return (
    <div className="email-thread-viewer">
      {emails.map((email, index) => (
        <EmailMessage
          key={email.id}
          email={email}
          isCollapsed={index > 2 && !email.hasEvidence}
          highlights={getEvidenceForEmail(email.id)}
        />
      ))}
    </div>
  );
};
```

#### 2. Email Intelligence Extraction
- **Commitment Detection**: "I'll approve the budget by Friday"
- **Concern Identification**: "worried about integration complexity"
- **Timeline Extraction**: "need this before our Q4 planning"
- **Stakeholder Dynamics**: CC patterns, response times, engagement levels

#### 3. Integration Requirements
- **Email Provider APIs**: Gmail, Outlook, Exchange
- **Authentication**: OAuth2 for secure access
- **Privacy Controls**: Consent and data handling
- **Real-time Sync**: Webhook support for new emails

### Unified Evidence Search

#### Cross-Source Evidence Discovery
```typescript
// Search across all evidence sources
const UnifiedEvidenceSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({
    sources: ['transcripts', 'documents', 'emails'],
    dateRange: 'last_30_days',
    evidenceTypes: ['explicit', 'inferred'],
    meddpiccElements: []
  });

  const handleSearch = async () => {
    const results = await searchEvidence({
      query,
      ...filters
    });
    
    // Results grouped by source type
    return {
      transcripts: results.transcriptEvidence,
      documents: results.documentEvidence,
      emails: results.emailEvidence
    };
  };

  return (
    <div className="unified-search">
      <SearchBar value={query} onChange={setQuery} />
      <SearchFilters filters={filters} onChange={setFilters} />
      
      <SearchResults>
        {results.map(result => (
          <EvidenceCard
            key={result.id}
            evidence={result}
            sourceType={result.source_type}
            onClick={() => navigateToSource(result)}
          />
        ))}
      </SearchResults>
    </div>
  );
};
```

## Implementation Approach

### Phase 1: Document Evidence System
1. Document upload and parsing infrastructure
2. Evidence extraction with positioning for PDFs
3. Document viewer with highlighting
4. Evidence overlay for documents

### Phase 2: Email Integration Foundation
1. Email provider authentication
2. Basic email parsing and display
3. Thread visualization
4. Simple evidence extraction

### Phase 3: Unified Evidence Platform
1. Cross-source evidence search
2. Evidence timeline across all sources
3. Consolidated intelligence view
4. Evidence quality scoring across sources

## Evidence-Backed Content Generation

### Overview
Transform evidence system into a credible content generation engine where AI-created sales materials include specific citations to meetings, documents, and emails.

### Content Generation with Citations

#### 1. AI-Generated Differentiation Document
```markdown
# Competitive Differentiation: ASMIS vs HubSpot

## Cost Advantage
Our solution delivers 40% cost savings compared to HubSpot [1], aligning with your 
budget constraints of staying under $400K annually [2].

## Technical Superiority  
The seamless Salesforce integration you require [3] is native in our platform, 
while HubSpot integration presents complexity concerns [4].

## Timeline Alignment
Our 3-month implementation timeline [5] meets your Q4 launch requirements [6], 
unlike competitors with 6+ month rollouts.

---
**Sources:**
[1] HubSpot pricing comparison, shared in email thread, March
[2] Sarah Chen (CFO), Budget discussion meeting, March
[3] Mike Thompson (CTO), Technical requirements call, March
[4] Mike Thompson, email response, March: "HubSpot integration looks complex"
[5] Implementation timeline document, Section 3.2, shared March
[6] John Williams (VP Marketing), Discovery call, March
```

#### 2. Executive Summary with Evidence
```markdown
# Executive Summary: ASMIS Implementation Proposal

## Key Stakeholder Alignment
Based on our conversations with your team, we've identified strong alignment:

- **Budget Authority**: Sarah Chen (CFO) has confirmed budget availability within 
  your $400K range [Budget discussion meeting, March]
  
- **Technical Champion**: Mike Thompson (CTO) expressed enthusiasm for our 
  Salesforce integration approach [Email, March: "This looks promising"]
  
- **Business Champion**: John Williams (VP Marketing) committed to internal 
  advocacy [Discovery call, March: "I'll champion this solution internally"]

## Decision Criteria Fulfillment
Your evaluation criteria are comprehensively addressed:

1. **20% ROI Requirement** [Document: Business Case Template, page 2]
   - Our solution delivers 25% ROI in year one [Analysis: ROI_Calculation.xlsx]

2. **Q4 Implementation Deadline** [Email thread: March 8-10]  
   - 3-month timeline confirmed [Document: Implementation_Plan.pdf, Section 2]

3. **SOC2 Compliance** [Security requirements email, March 9]
   - Full compliance documentation provided [Document: Security_Compliance.pdf]
```

### Backend Enhancement for Citation Generation

#### Key Distinction: Storage vs Display
```
Backend Storage (Full Precision):
├── Timestamp: "14:32" 
├── Date: "2024-03-15"
├── Character positions: start=1250, end=1450
└── Speaker: "Sarah Chen (CFO)"

Citation Display (Natural):
├── Date: "March" (if this year)
├── Date: "last March" (if last year)  
├── Date: "March 2022" (if 2+ years ago)
└── No timestamp shown

Hover Overlay (Precise Details):
├── Shows: "Sarah Chen (CFO) at 14:32"
├── Context: "±3 sentences around evidence"
└── Link: Direct to transcript at exact timestamp
```

#### Citation Engine
```python
class CitationEngine:
    """Generates credible citations for AI content."""
    
    def __init__(self):
        self.evidence_service = EvidenceService()
        
        # Citation style preferences for different source types
        self.citation_styles = {
            'transcript': {
                'formal': "{speaker}, {meeting_title}, {date}",
                'conversational': "As {speaker} mentioned in our {meeting_type}",
                'reference': "Per our discussion with {speaker}"
            },
            'document': {
                'formal': "{document_title}, Page {page_number}",
                'section': "{document_title}, {section_name}",
                'reference': "As outlined in {document_title}"
            },
            'email': {
                'formal': "{sender}, email, {date}",
                'conversational': "In {sender}'s email",
                'quote': "{sender}: \"{quote}\""
            }
        }
        
    def generate_cited_content(self, content_type: str, deal_id: str, 
                              template: str) -> CitedContent:
        """Generate content with evidence citations."""
        
        # Get all evidence for this deal
        evidence_pool = self.evidence_service.get_deal_evidence(deal_id)
        
        # Extract claims that need citation
        claims = self._extract_claims(template)
        
        # Match claims to evidence
        citations = []
        for claim in claims:
            supporting_evidence = self._find_supporting_evidence(claim, evidence_pool)
            if supporting_evidence:
                citation = self._create_citation(supporting_evidence)
                citations.append(citation)
        
        # Generate content with inline citations
        cited_content = self._weave_citations(template, claims, citations)
        
        return CitedContent(
            content=cited_content,
            citations=citations,
            credibility_score=self._calculate_credibility(citations)
        )
    
    def _create_citation(self, evidence: Evidence) -> Citation:
        """Create formatted citation from evidence."""
        if evidence.source_type == "transcript":
            # Natural citation format for transcripts
            # NOTE: Backend stores precise timestamp for navigation, but citation uses natural date
            formatted_date = self._format_natural_date(evidence.date)
            return Citation(
                id=evidence.id,
                format=f"{evidence.speaker}, {evidence.meeting_title}, {formatted_date}",
                quote=evidence.evidence_text,
                link=f"/transcripts/{evidence.transcript_id}?highlight={evidence.start}-{evidence.end}",
                credibility=evidence.confidence,
                # Keep precise details for hover/navigation
                precise_timestamp=evidence.timestamp,
                precise_date=evidence.date
            )
        elif evidence.source_type == "document":
            return Citation(
                id=evidence.id,
                format=f"{evidence.document_title}, Page {evidence.page_number}, "
                       f"{evidence.section_name if evidence.section_name else ''}",
                quote=evidence.evidence_text,
                link=f"/documents/{evidence.document_id}?page={evidence.page_number}&highlight=true",
                credibility=evidence.confidence
            )
        elif evidence.source_type == "email":
            return Citation(
                id=evidence.id,
                format=f"{evidence.sender}, email, {evidence.date}",
                quote=evidence.evidence_text,
                link=f"/emails/{evidence.email_id}?thread={evidence.thread_id}",
                credibility=evidence.confidence
            )
    
    def _format_natural_date(self, date_str: str) -> str:
        """Format date naturally based on recency."""
        from datetime import datetime, timedelta
        
        evidence_date = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()
        
        # Calculate time difference
        time_diff = now - evidence_date
        
        if time_diff.days < 365:  # This year
            return evidence_date.strftime("%B")  # "March"
        elif time_diff.days < 730:  # Last year
            return f"last {evidence_date.strftime('%B')}"  # "last March"
        else:  # 2+ years ago
            return evidence_date.strftime("%B %Y")  # "March 2022"
    
    # Example outputs:
    # Evidence from March 2024 (current year) → "March"
    # Evidence from March 2023 (last year) → "last March"  
    # Evidence from March 2022 (2+ years) → "March 2022"

@dataclass
class CitedContent:
    """Content with embedded citations."""
    content: str
    citations: List[Citation]
    credibility_score: float
    evidence_coverage: float  # Percentage of claims backed by evidence
    
@dataclass 
class Citation:
    """Individual citation reference."""
    id: str
    format: str  # Human-readable citation for display
    quote: str   # Actual evidence text
    link: str    # Deep link to source with precise positioning
    credibility: float
    # Precise details stored for hover/navigation (not displayed in citation)
    precise_timestamp: Optional[str] = None  # "14:32" for hover overlay
    precise_date: Optional[str] = None       # "2024-03-15" for system use
```

### Content Templates with Citation Placeholders

#### 1. Proposal Generator
```python
PROPOSAL_TEMPLATE = """
# Proposal: {solution_name} for {account_name}

## Executive Summary
Based on our discovery process, {solution_name} directly addresses your key requirements:

{CITE_REQUIREMENT_1: "Budget alignment"}
{CITE_REQUIREMENT_2: "Technical integration needs"} 
{CITE_REQUIREMENT_3: "Timeline requirements"}

## Value Proposition
Our solution delivers:
- {CITE_ROI_CLAIM: "Cost savings or ROI metrics"}
- {CITE_EFFICIENCY_CLAIM: "Operational improvements"}
- {CITE_COMPETITIVE_ADVANTAGE: "Differentiation vs competitors"}

## Implementation Plan
Your team's requirements for {CITE_TIMELINE_REQUIREMENT} align perfectly with our 
{CITE_IMPLEMENTATION_PLAN} approach.

## Next Steps
As discussed with {CITE_DECISION_MAKER}, we propose:
1. {CITE_NEXT_STEP_1}
2. {CITE_NEXT_STEP_2}
"""
```

#### 2. Follow-up Email Generator
```python
FOLLOWUP_EMAIL_TEMPLATE = """
Subject: Following up on {meeting_title} - Next Steps

Hi {primary_contact},

Thank you for the productive conversation {CITE_MEETING_REFERENCE}. I wanted to 
follow up on the key points we discussed:

**Your Requirements:**
- {CITE_KEY_REQUIREMENT_1}
- {CITE_KEY_REQUIREMENT_2}

**Our Proposed Solution:**
As {CITE_STAKEHOLDER_FEEDBACK}, our approach addresses your concerns about 
{CITE_MAIN_CONCERN} while delivering {CITE_KEY_BENEFIT}.

**Next Steps:**
Per your request {CITE_NEXT_STEP_REQUEST}, I'll {proposed_action}.

**Timeline:**
To meet your {CITE_DEADLINE_REQUIREMENT}, we propose moving forward with 
{CITE_PROPOSED_TIMELINE}.

Best regards,
{sales_rep}

---
*All references above link to specific moments in our conversations and shared documents.*
"""
```

### UI Integration for Cited Content

#### 1. Content Generator with Citation Preview
```typescript
const CitedContentGenerator: React.FC = ({ dealId, contentType }) => {
  const [template, setTemplate] = useState('');
  const [generatedContent, setGeneratedContent] = useState<CitedContent>(null);
  const [showCitations, setShowCitations] = useState(true);

  const generateContent = async () => {
    const result = await citationEngine.generateCitedContent(
      contentType, 
      dealId, 
      template
    );
    setGeneratedContent(result);
  };

  return (
    <div className="cited-content-generator">
      <div className="generator-controls">
        <Select value={contentType}>
          <option value="proposal">Proposal</option>
          <option value="differentiation">Differentiation Doc</option>
          <option value="executive_summary">Executive Summary</option>
          <option value="follow_up_email">Follow-up Email</option>
        </Select>
        
        <Button onClick={generateContent}>
          Generate with Citations
        </Button>
      </div>

      <div className="content-preview">
        <CitedContentViewer 
          content={generatedContent}
          showCitations={showCitations}
          onCitationClick={navigateToSource}
        />
        
        <div className="credibility-metrics">
          <Badge>
            Credibility: {Math.round(generatedContent?.credibility_score * 100)}%
          </Badge>
          <Badge>
            Evidence Coverage: {Math.round(generatedContent?.evidence_coverage * 100)}%
          </Badge>
        </div>
      </div>
    </div>
  );
};
```

#### 2. Interactive Citations in Content
```typescript
const CitedContentViewer: React.FC = ({ content, showCitations }) => {
  const renderContentWithCitations = (text: string) => {
    // Replace citation markers with interactive elements
    return text.replace(/\[(\d+)\]/g, (match, citationId) => {
      const citation = citations.find(c => c.id === citationId);
      return (
        <CitationMarker
          key={citationId}
          citation={citation}
          onHover={showCitationPreview}
          onClick={navigateToSource}
        />
      );
    });
  };

  return (
    <div className="cited-content">
      <div className="content-body">
        {renderContentWithCitations(content.content)}
      </div>
      
      {showCitations && (
        <div className="citations-section">
          <h4>Sources</h4>
          {content.citations.map(citation => (
            <CitationReference 
              key={citation.id}
              citation={citation}
              onClick={() => navigateToSource(citation.link)}
            />
          ))}
        </div>
      )}
    </div>
  );
};
```

## Benefits

### For Sales Teams
- **Credible Content**: Every claim backed by specific evidence
- **Instant Credibility**: Prospects see you've done your homework
- **Personalized Materials**: Content specific to their conversations
- **Quick Navigation**: Jump to any evidence source instantly
- **Trust Building**: Full transparency in AI insights

### For Sales Leaders
- **Professional Image**: Materials that reference actual conversations
- **Competitive Advantage**: Cited claims vs generic competitors
- **Deal Intelligence**: Complete view of all deal communications
- **Quality Control**: Evidence coverage metrics for content
- **Coaching Opportunities**: See how deals progress through evidence

### For Prospects/Customers
- **Trust**: Claims tied to their actual statements
- **Relevance**: Content reflects their specific situation  
- **Transparency**: Can verify every reference
- **Professionalism**: Detailed, evidence-based approach

### For RevOps
- **Content Analytics**: Which evidence drives decisions
- **Win/Loss Analysis**: Evidence patterns in successful deals
- **Message Effectiveness**: Track cited content performance
- **Process Insights**: Understand what content drives decisions