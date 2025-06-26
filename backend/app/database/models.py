"""Database models for ASMIS backend."""

from typing import Any, Dict, Optional
from datetime import datetime

from sqlalchemy import String, Text, JSON, ForeignKey, Index, UniqueConstraint, Boolean, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin, SoftDeleteMixin


class PromptTemplate(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Model for prompt templates used by AI agents."""
    
    __tablename__ = "prompt_templates"
    
    # Core fields
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Agent and version information
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    
    # Metadata and configuration
    template_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)
    variables: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Template Imprinting Protocol fields
    template_mode: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)
    imprinting_tokens: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pattern_adherence_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    is_imprinting_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Template structure for imprinting
    template_structure: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)
    behavioral_constraints: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Performance and usage tracking
    usage_count: Mapped[int] = mapped_column(default=0, nullable=False)
    avg_confidence_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    imprinting_success_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Relationships
    versions: Mapped[list["PromptVersion"]] = relationship(
        "PromptVersion", 
        back_populates="template",
        cascade="all, delete-orphan"
    )
    
    # Table constraints and indexes
    __table_args__ = (
        UniqueConstraint('name', 'agent_type', name='uq_template_name_agent'),
        Index('ix_template_agent_type', 'agent_type'),
        Index('ix_template_active', 'is_active'),
        Index('ix_template_usage', 'usage_count'),
        Index('ix_template_imprinting', 'is_imprinting_enabled'),
        Index('ix_template_adherence', 'pattern_adherence_score'),
    )
    
    def __repr__(self) -> str:
        return f"<PromptTemplate(name='{self.name}', agent_type='{self.agent_type}')>"


class PromptVersion(Base, UUIDMixin, TimestampMixin):
    """Model for prompt template versions with change tracking."""
    
    __tablename__ = "prompt_versions"
    
    # Reference to parent template
    template_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("prompt_templates.id"),
        nullable=False
    )
    
    # Version information
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    change_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Version metadata
    is_current: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Performance tracking for this version
    usage_count: Mapped[int] = mapped_column(default=0, nullable=False)
    avg_confidence_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    success_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Relationships
    template: Mapped["PromptTemplate"] = relationship(
        "PromptTemplate", 
        back_populates="versions"
    )
    
    # Table constraints and indexes
    __table_args__ = (
        UniqueConstraint('template_id', 'version', name='uq_version_template_version'),
        Index('ix_version_template_id', 'template_id'),
        Index('ix_version_current', 'is_current'),
        Index('ix_version_usage', 'usage_count'),
    )
    
    def __repr__(self) -> str:
        return f"<PromptVersion(template_id='{self.template_id}', version='{self.version}')>"


class AgentConfiguration(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Model for agent-specific configuration settings."""
    
    __tablename__ = "agent_configurations"
    
    # Agent identification
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Configuration data
    config_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    
    # Environment and deployment settings
    environment: Mapped[str] = mapped_column(String(50), nullable=False, default="production")
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)
    
    # Table constraints and indexes
    __table_args__ = (
        UniqueConstraint('agent_type', 'name', 'environment', name='uq_agent_config'),
        Index('ix_config_agent_type', 'agent_type'),
        Index('ix_config_environment', 'environment'),
        Index('ix_config_default', 'is_default'),
    )
    
    def __repr__(self) -> str:
        return f"<AgentConfiguration(agent_type='{self.agent_type}', name='{self.name}')>"


class ImprintingTemplate(Base, UUIDMixin, TimestampMixin):
    """Model for Template Imprinting Protocol configurations."""
    
    __tablename__ = "imprinting_templates"
    
    # Template identification
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    
    # Template Imprinting Protocol core structure
    template_mode: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    template_structure: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    example_filled: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Behavioral constraints
    forbidden_children: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    required_actions: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    
    # First token optimization
    imprinting_tokens: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int] = mapped_column(nullable=False)
    
    # Performance tracking
    adherence_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    usage_count: Mapped[int] = mapped_column(default=0, nullable=False)
    success_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Configuration
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    priority: Mapped[int] = mapped_column(default=100, nullable=False)
    
    # Table constraints and indexes
    __table_args__ = (
        UniqueConstraint('name', 'agent_type', 'version', name='uq_imprinting_name_agent_version'),
        Index('ix_imprinting_agent_type', 'agent_type'),
        Index('ix_imprinting_active', 'is_active'),
        Index('ix_imprinting_priority', 'priority'),
        Index('ix_imprinting_adherence', 'adherence_score'),
        Index('ix_imprinting_tokens', 'token_count'),
    )
    
    def __repr__(self) -> str:
        return f"<ImprintingTemplate(name='{self.name}', agent_type='{self.agent_type}')>"


class ProcessingSession(Base, UUIDMixin, TimestampMixin):
    """Model for tracking AI processing sessions and results."""
    
    __tablename__ = "processing_sessions"
    
    # Session identification
    session_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Processing details
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_template_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("prompt_templates.id"),
        nullable=True
    )
    imprinting_template_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("imprinting_templates.id"),
        nullable=True
    )
    
    # Input and output data
    input_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    output_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    # Processing metrics
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    confidence_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(nullable=True)
    token_usage: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    # Template Imprinting metrics
    imprinting_adherence_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    pattern_violations: Mapped[Optional[int]] = mapped_column(nullable=True)
    first_token_effective: Mapped[Optional[bool]] = mapped_column(nullable=True)
    
    # Error tracking
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(default=0, nullable=False)
    
    # Table constraints and indexes
    __table_args__ = (
        Index('ix_session_type', 'session_type'),
        Index('ix_session_agent_type', 'agent_type'),
        Index('ix_session_status', 'status'),
        Index('ix_session_created_at', 'created_at'),
        Index('ix_session_source', 'source_type', 'source_id'),
    )
    
    def __repr__(self) -> str:
        return f"<ProcessingSession(session_type='{self.session_type}', status='{self.status}')>"


# Multi-Source Evidence System Models

class Transcript(Base, UUIDMixin, TimestampMixin):
    """Model for meeting transcripts."""
    __tablename__ = "transcripts"
    
    # Core transcript information
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Meeting metadata
    meeting_date: Mapped[datetime] = mapped_column(nullable=False)
    attendees: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    meeting_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Source tracking
    source_platform: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # "zoom", "teams", etc.
    source_file_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Business context
    account_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    deal_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Processing status
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relationships
    segments: Mapped[list["TranscriptSegment"]] = relationship(
        "TranscriptSegment", 
        back_populates="transcript",
        cascade="all, delete-orphan"
    )
    evidence: Mapped[list["IntelligenceEvidence"]] = relationship(
        "IntelligenceEvidence",
        back_populates="transcript",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index('ix_transcript_date', 'meeting_date'),
        Index('ix_transcript_account', 'account_id'),
        Index('ix_transcript_deal', 'deal_id'),
        Index('ix_transcript_processed', 'is_processed'),
    )
    
    def __repr__(self) -> str:
        return f"<Transcript(title='{self.title}', date='{self.meeting_date}')>"


class TranscriptSegment(Base, UUIDMixin, TimestampMixin):
    """Model for structured transcript segments with precise positioning."""
    __tablename__ = "transcript_segments"
    
    # Reference to parent transcript
    transcript_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("transcripts.id"),
        nullable=False
    )
    
    # Speaker information
    speaker: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Timing information
    start_time: Mapped[str] = mapped_column(String(10), nullable=False)  # "00:15:32"
    end_time: Mapped[str] = mapped_column(String(10), nullable=False)    # "00:15:45"
    
    # Content and positioning
    text: Mapped[str] = mapped_column(Text, nullable=False)
    start_position: Mapped[int] = mapped_column(Integer, nullable=False)  # Character position in full transcript
    end_position: Mapped[int] = mapped_column(Integer, nullable=False)    # Character position in full transcript
    word_count: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships
    transcript: Mapped["Transcript"] = relationship(
        "Transcript",
        back_populates="segments"
    )
    
    __table_args__ = (
        Index('ix_segment_transcript', 'transcript_id'),
        Index('ix_segment_position', 'start_position', 'end_position'),
        Index('ix_segment_time', 'start_time'),
        Index('ix_segment_speaker', 'speaker'),
    )
    
    def __repr__(self) -> str:
        return f"<TranscriptSegment(speaker='{self.speaker}', time='{self.start_time}')>"


class IntelligenceEvidence(Base, UUIDMixin, TimestampMixin):
    """Model for evidence linking with precise positioning."""
    __tablename__ = "intelligence_evidence"
    
    # Analysis reference
    analysis_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Element classification
    element_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "decision_criteria", "champion", etc.
    element_key: Mapped[str] = mapped_column(String(100), nullable=False)  # Specific criterion ID or element identifier
    
    # Evidence content
    evidence_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Source information (transcript)
    transcript_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("transcripts.id"),
        nullable=True
    )
    segment_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("transcript_segments.id"),
        nullable=True
    )
    
    # Source information (document)
    document_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("documents.id"),
        nullable=True
    )
    
    # Precise positioning
    start_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    end_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Context
    speaker: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    context_before: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    context_after: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Quality metrics
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # 0.0-1.0
    extraction_type: Mapped[str] = mapped_column(String(50), nullable=False, default="explicit")  # "explicit", "inferred", "sentiment"
    
    # Relationships
    transcript: Mapped[Optional["Transcript"]] = relationship(
        "Transcript",
        back_populates="evidence"
    )
    document: Mapped[Optional["Document"]] = relationship(
        "Document",
        back_populates="evidence"
    )
    
    __table_args__ = (
        Index('ix_evidence_analysis_element', 'analysis_id', 'element_type', 'element_key'),
        Index('ix_evidence_transcript', 'transcript_id', 'start_position'),
        Index('ix_evidence_document', 'document_id'),
        Index('ix_evidence_confidence', 'confidence'),
        Index('ix_evidence_type', 'extraction_type'),
    )
    
    def __repr__(self) -> str:
        return f"<IntelligenceEvidence(type='{self.element_type}', confidence={self.confidence})>"


class Document(Base, UUIDMixin, TimestampMixin):
    """Model for documents with structure."""
    __tablename__ = "documents"
    
    # Business context
    deal_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    account_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Document information
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "pdf", "docx", "pptx", "xlsx"
    file_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_pages: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Content
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    document_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    uploaded_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    
    # Processing status
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relationships
    sections: Mapped[list["DocumentSection"]] = relationship(
        "DocumentSection",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    evidence: Mapped[list["IntelligenceEvidence"]] = relationship(
        "IntelligenceEvidence",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index('ix_document_deal', 'deal_id'),
        Index('ix_document_account', 'account_id'),
        Index('ix_document_type', 'document_type'),
        Index('ix_document_uploaded', 'uploaded_at'),
        Index('ix_document_processed', 'is_processed'),
    )
    
    def __repr__(self) -> str:
        return f"<Document(title='{self.title}', type='{self.document_type}')>"


class DocumentSection(Base, UUIDMixin, TimestampMixin):
    """Model for document sections/pages."""
    __tablename__ = "document_sections"
    
    # Reference to parent document
    document_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("documents.id"),
        nullable=False
    )
    
    # Section information
    section_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'page', 'chapter', 'section'
    section_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    page_start: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    page_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Content
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    
    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="sections"
    )
    
    __table_args__ = (
        Index('ix_section_document', 'document_id'),
        Index('ix_section_type', 'section_type'),
        Index('ix_section_pages', 'page_start', 'page_end'),
    )
    
    def __repr__(self) -> str:
        return f"<DocumentSection(document_id='{self.document_id}', name='{self.section_name}')>"


class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Model for application users."""
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Table constraints and indexes
    __table_args__ = (
        UniqueConstraint('username', name='uq_user_username'),
        UniqueConstraint('email', name='uq_user_email'),
        Index('ix_user_active', 'is_active'),
    )

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"


# Smart Capture Core Business Entity Models

class Account(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Model for customer accounts/companies."""
    __tablename__ = "accounts"
    
    # Company information
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # "startup", "smb", "enterprise"
    
    # Contact information
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    headquarters: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Business context
    account_type: Mapped[str] = mapped_column(String(50), nullable=False, default="prospect")  # "prospect", "customer", "partner"
    annual_revenue: Mapped[Optional[float]] = mapped_column(nullable=True)
    employee_count: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    # CRM integration
    external_crm_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    crm_source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # "salesforce", "hubspot", etc.
    
    # Metadata
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Assignments
    account_owner: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # User ID
    
    # Relationships
    deals: Mapped[list["Deal"]] = relationship(
        "Deal",
        back_populates="account",
        cascade="all, delete-orphan"
    )
    stakeholders: Mapped[list["Stakeholder"]] = relationship(
        "Stakeholder",
        back_populates="account",
        cascade="all, delete-orphan"
    )
    smart_capture_notes: Mapped[list["SmartCaptureNote"]] = relationship(
        "SmartCaptureNote",
        back_populates="account"
    )
    
    __table_args__ = (
        Index('ix_account_name', 'name'),
        Index('ix_account_domain', 'domain'),
        Index('ix_account_type', 'account_type'),
        Index('ix_account_owner', 'account_owner'),
        Index('ix_account_industry', 'industry'),
    )
    
    def __repr__(self) -> str:
        return f"<Account(name='{self.name}', type='{self.account_type}')>"


class Deal(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Model for sales opportunities/deals."""
    __tablename__ = "deals"
    
    # Reference to account
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id"),
        nullable=False
    )
    
    # Deal information
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    deal_type: Mapped[str] = mapped_column(String(50), nullable=False, default="new_business")  # "new_business", "expansion", "renewal"
    
    # Financial information
    amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    probability: Mapped[Optional[float]] = mapped_column(nullable=True)  # 0-100
    
    # Timeline
    close_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    sales_cycle_length: Mapped[Optional[int]] = mapped_column(nullable=True)  # days
    
    # Deal stage and status
    stage: Mapped[str] = mapped_column(String(50), nullable=False, default="discovery")
    # "discovery", "technical_evaluation", "business_evaluation", "negotiation", "closing", "closed_won", "closed_lost"
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")  # "active", "paused", "closed"
    
    # Competition and positioning
    competitive_situation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # "no_competition", "favored", "competitive", "disadvantaged"
    primary_competitors: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # CRM integration
    external_crm_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    crm_source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Assignments
    deal_owner: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # User ID
    sales_engineer: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # User ID
    
    # Metadata
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Relationships
    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="deals"
    )
    meddpicc_analysis: Mapped[Optional["MEDDPICCAnalysis"]] = relationship(
        "MEDDPICCAnalysis",
        back_populates="deal",
        uselist=False
    )
    smart_capture_notes: Mapped[list["SmartCaptureNote"]] = relationship(
        "SmartCaptureNote",
        back_populates="deal"
    )
    
    __table_args__ = (
        Index('ix_deal_account', 'account_id'),
        Index('ix_deal_stage', 'stage'),
        Index('ix_deal_status', 'status'),
        Index('ix_deal_close_date', 'close_date'),
        Index('ix_deal_owner', 'deal_owner'),
        Index('ix_deal_amount', 'amount'),
    )
    
    def __repr__(self) -> str:
        return f"<Deal(name='{self.name}', stage='{self.stage}', amount={self.amount})>"


class Stakeholder(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Model for people/contacts within accounts."""
    __tablename__ = "stakeholders"
    
    # Reference to account
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.id"),
        nullable=False
    )
    
    # Personal information
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Professional information
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    seniority_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # "individual", "manager", "director", "vp", "c_level"
    
    # MEDDPICC roles
    role_economic_buyer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_technical_buyer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_champion: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_influencer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_user: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_blocker: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Influence and engagement
    influence_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # "high", "medium", "low"
    engagement_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # "champion", "supporter", "neutral", "skeptic", "blocker"
    
    # Relationship information
    reports_to_stakeholder_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("stakeholders.id"),
        nullable=True
    )
    
    # Communication preferences
    preferred_communication: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # "email", "phone", "slack", "teams"
    last_contact_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    contact_frequency: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # "daily", "weekly", "monthly", "sporadic"
    
    # Social and external links
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    external_contact_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # CRM contact ID
    
    # Metadata
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Relationships
    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="stakeholders"
    )
    reports_to: Mapped[Optional["Stakeholder"]] = relationship(
        "Stakeholder",
        remote_side="Stakeholder.id",
        back_populates="direct_reports"
    )
    direct_reports: Mapped[list["Stakeholder"]] = relationship(
        "Stakeholder",
        back_populates="reports_to"
    )
    smart_capture_notes: Mapped[list["SmartCaptureNote"]] = relationship(
        "SmartCaptureNote",
        back_populates="stakeholder"
    )
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    __table_args__ = (
        Index('ix_stakeholder_account', 'account_id'),
        Index('ix_stakeholder_name', 'first_name', 'last_name'),
        Index('ix_stakeholder_email', 'email'),
        Index('ix_stakeholder_title', 'title'),
        Index('ix_stakeholder_roles', 'role_economic_buyer', 'role_champion'),
        Index('ix_stakeholder_reports_to', 'reports_to_stakeholder_id'),
    )
    
    def __repr__(self) -> str:
        return f"<Stakeholder(name='{self.full_name}', title='{self.title}')>"


class Partner(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Model for partner companies and relationships."""
    __tablename__ = "partners"
    
    # Partner company information
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    partner_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "system_integrator", "reseller", "technology", "consulting"
    tier: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # "platinum", "gold", "silver", "bronze"
    
    # Contact information
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    primary_contact_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    primary_contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    primary_contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Partnership details
    specialties: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    regions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    certification_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Relationship strength
    relationship_strength: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # "strong", "developing", "weak"
    last_collaboration_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Performance metrics
    deals_influenced: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_deal_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Status and metadata
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")  # "active", "inactive", "pending"
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Relationships
    smart_capture_notes: Mapped[list["SmartCaptureNote"]] = relationship(
        "SmartCaptureNote",
        back_populates="partner"
    )
    
    __table_args__ = (
        Index('ix_partner_name', 'name'),
        Index('ix_partner_type', 'partner_type'),
        Index('ix_partner_tier', 'tier'),
        Index('ix_partner_status', 'status'),
    )
    
    def __repr__(self) -> str:
        return f"<Partner(name='{self.name}', type='{self.partner_type}')>"


class MEDDPICCAnalysis(Base, UUIDMixin, TimestampMixin):
    """Model for structured MEDDPICC analysis data with evidence tracking."""
    __tablename__ = "meddpicc_analyses"
    
    # Reference to deal
    deal_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("deals.id"),
        nullable=False,
        unique=True  # One analysis per deal
    )
    
    # Overall scoring
    overall_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # 0-100
    completeness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # 0-100
    last_scored_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Processing status
    processing_status: Mapped[str] = mapped_column(String(20), nullable=False, default="idle")  # "idle", "processing", "complete", "error"
    processing_progress: Mapped[Optional[float]] = mapped_column(nullable=True)  # 0-100
    current_step: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # MEDDPICC Component Scores (0-100 each)
    metrics_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    economic_buyer_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    decision_criteria_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    decision_process_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    identify_pain_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    champion_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    competition_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    # MEDDPICC Component Status ("complete", "partial", "missing")
    metrics_status: Mapped[str] = mapped_column(String(20), nullable=False, default="missing")
    economic_buyer_status: Mapped[str] = mapped_column(String(20), nullable=False, default="missing")
    decision_criteria_status: Mapped[str] = mapped_column(String(20), nullable=False, default="missing")
    decision_process_status: Mapped[str] = mapped_column(String(20), nullable=False, default="missing")
    identify_pain_status: Mapped[str] = mapped_column(String(20), nullable=False, default="missing")
    champion_status: Mapped[str] = mapped_column(String(20), nullable=False, default="missing")
    competition_status: Mapped[str] = mapped_column(String(20), nullable=False, default="missing")
    
    # Structured MEDDPICC Data
    metrics_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    economic_buyer_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    decision_criteria_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    decision_process_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    identify_pain_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    champion_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    competition_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Insights and recommendations
    key_insights: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    risk_factors: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    recommendations: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Metadata
    analysis_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")
    confidence_threshold: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)
    
    # Relationships
    deal: Mapped["Deal"] = relationship(
        "Deal",
        back_populates="meddpicc_analysis"
    )
    evidence_items: Mapped[list["MEDDPICCEvidence"]] = relationship(
        "MEDDPICCEvidence",
        back_populates="analysis",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index('ix_meddpicc_deal', 'deal_id'),
        Index('ix_meddpicc_overall_score', 'overall_score'),
        Index('ix_meddpicc_completeness', 'completeness_score'),
        Index('ix_meddpicc_processing', 'processing_status'),
        Index('ix_meddpicc_scored_at', 'last_scored_at'),
    )
    
    def __repr__(self) -> str:
        return f"<MEDDPICCAnalysis(deal_id='{self.deal_id}', score={self.overall_score})>"


class MEDDPICCEvidence(Base, UUIDMixin, TimestampMixin):
    """Model for linking evidence to specific MEDDPICC components."""
    __tablename__ = "meddpicc_evidence"
    
    # Reference to analysis
    analysis_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("meddpicc_analyses.id"),
        nullable=False
    )
    
    # MEDDPICC component
    component: Mapped[str] = mapped_column(String(50), nullable=False)  # "metrics", "economic_buyer", etc.
    sub_component: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Specific element within component
    
    # Evidence content and positioning
    evidence_text: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)  # Highlighted portion
    
    # Source information
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "transcript", "document", "note", "email"
    source_id: Mapped[str] = mapped_column(String(100), nullable=False)  # Reference to source record
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)  # Display name
    source_timestamp: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # "14:23" for transcripts
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Positioning within source
    start_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    end_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Quality metrics
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # 0.0-1.0
    extraction_type: Mapped[str] = mapped_column(String(50), nullable=False, default="explicit")  # "explicit", "inferred", "sentiment"
    business_implication: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Extraction metadata
    extracted_by: Mapped[str] = mapped_column(String(100), nullable=False)  # AI agent or user
    extraction_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # "smart_capture", "transcript_analysis", etc.
    validated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    validated_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Relationships
    analysis: Mapped["MEDDPICCAnalysis"] = relationship(
        "MEDDPICCAnalysis",
        back_populates="evidence_items"
    )
    
    __table_args__ = (
        Index('ix_meddpicc_evidence_analysis_component', 'analysis_id', 'component'),
        Index('ix_meddpicc_evidence_source', 'source_type', 'source_id'),
        Index('ix_meddpicc_evidence_confidence', 'confidence'),
        Index('ix_meddpicc_evidence_extraction', 'extraction_type'),
        Index('ix_meddpicc_evidence_validated', 'validated_at'),
    )
    
    def __repr__(self) -> str:
        return f"<MEDDPICCEvidence(component='{self.component}', confidence={self.confidence})>"


# Smart Capture System Models

class SmartCaptureNote(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Model for Smart Capture notes with context and extraction tracking."""
    __tablename__ = "smart_capture_notes"
    
    # Note content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Auto-generated or user-provided
    
    # Context detection
    context_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # "deal", "account", "stakeholder", "partner", "global"
    context_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    context_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0.0-1.0
    
    # Entity relationships (nullable - may reference one or multiple)
    account_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("accounts.id"),
        nullable=True
    )
    deal_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("deals.id"),
        nullable=True
    )
    stakeholder_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("stakeholders.id"),
        nullable=True
    )
    partner_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("partners.id"),
        nullable=True
    )
    
    # Processing status
    processing_status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")  # "pending", "processing", "completed", "failed"
    processing_started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    processing_completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    processing_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Extraction results
    entities_extracted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    relationships_extracted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    meddpicc_elements_extracted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    overall_extraction_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0.0-1.0
    
    # Source and capture context
    capture_method: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")  # "manual", "voice_to_text", "email_import"
    capture_location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # URL or page where captured
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # User information
    created_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # User ID
    
    # Metadata
    tags: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    raw_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Relationships
    account: Mapped[Optional["Account"]] = relationship(
        "Account",
        back_populates="smart_capture_notes"
    )
    deal: Mapped[Optional["Deal"]] = relationship(
        "Deal",
        back_populates="smart_capture_notes"
    )
    stakeholder: Mapped[Optional["Stakeholder"]] = relationship(
        "Stakeholder",
        back_populates="smart_capture_notes"
    )
    partner: Mapped[Optional["Partner"]] = relationship(
        "Partner",
        back_populates="smart_capture_notes"
    )
    entity_extractions: Mapped[list["EntityExtraction"]] = relationship(
        "EntityExtraction",
        back_populates="note",
        cascade="all, delete-orphan"
    )
    entity_links: Mapped[list["EntityLink"]] = relationship(
        "EntityLink",
        back_populates="note",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index('ix_note_context', 'context_type'),
        Index('ix_note_processing', 'processing_status'),
        Index('ix_note_account', 'account_id'),
        Index('ix_note_deal', 'deal_id'),
        Index('ix_note_stakeholder', 'stakeholder_id'),
        Index('ix_note_partner', 'partner_id'),
        Index('ix_note_created_by', 'created_by'),
        Index('ix_note_capture_method', 'capture_method'),
    )
    
    def __repr__(self) -> str:
        return f"<SmartCaptureNote(title='{self.title}', context='{self.context_type}')>"


class EntityExtraction(Base, UUIDMixin, TimestampMixin):
    """Model for extracted entities from Smart Capture notes."""
    __tablename__ = "entity_extractions"
    
    # Reference to note
    note_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("smart_capture_notes.id"),
        nullable=False
    )
    
    # Extracted entity information
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "person", "company", "deal", "partner", "meddpicc_element"
    entity_subtype: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # "stakeholder", "champion", "decision_criteria", etc.
    
    # Extracted text and positioning
    extracted_text: Mapped[str] = mapped_column(Text, nullable=False)
    start_position: Mapped[int] = mapped_column(Integer, nullable=False)
    end_position: Mapped[int] = mapped_column(Integer, nullable=False)
    context_before: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    context_after: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Entity attributes (structured data extracted about the entity)
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    # Examples:
    # {"name": "John Smith", "title": "CTO", "company": "ABC Corp"}
    # {"criteria": "site performance", "priority": "must_have", "our_position": "meets"}
    
    # Confidence and quality
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # 0.0-1.0
    extraction_method: Mapped[str] = mapped_column(String(50), nullable=False)  # "nlp", "regex", "manual", "llm"
    
    # Matching and linking
    matched_entity_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # ID of matched existing entity
    matched_entity_table: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # "accounts", "stakeholders", etc.
    match_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0.0-1.0
    requires_disambiguation: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Processing metadata
    processed_by: Mapped[str] = mapped_column(String(100), nullable=False)  # AI agent or extraction service
    processing_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")
    
    # User validation
    validated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validated_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    validated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    validation_action: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # "accepted", "rejected", "modified"
    
    # Relationships
    note: Mapped["SmartCaptureNote"] = relationship(
        "SmartCaptureNote",
        back_populates="entity_extractions"
    )
    
    __table_args__ = (
        Index('ix_extraction_note', 'note_id'),
        Index('ix_extraction_type', 'entity_type', 'entity_subtype'),
        Index('ix_extraction_confidence', 'confidence'),
        Index('ix_extraction_matched', 'matched_entity_id', 'matched_entity_table'),
        Index('ix_extraction_requires_disambiguation', 'requires_disambiguation'),
        Index('ix_extraction_validated', 'validated'),
    )
    
    def __repr__(self) -> str:
        return f"<EntityExtraction(type='{self.entity_type}', text='{self.extracted_text[:50]}...')>"


class EntityLink(Base, UUIDMixin, TimestampMixin):
    """Model for linking Smart Capture notes to multiple entities (many-to-many)."""
    __tablename__ = "entity_links"
    
    # Reference to note
    note_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("smart_capture_notes.id"),
        nullable=False
    )
    
    # Entity reference (polymorphic)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "account", "deal", "stakeholder", "partner"
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    
    # Link metadata
    link_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "mentioned", "primary_context", "updated", "created"
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # 0.0-1.0
    
    # What was updated or extracted about this entity
    update_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fields_updated: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Processing information
    created_by_extraction: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    extraction_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("entity_extractions.id"),
        nullable=True
    )
    
    # User validation
    validated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validated_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    validated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Relationships
    note: Mapped["SmartCaptureNote"] = relationship(
        "SmartCaptureNote",
        back_populates="entity_links"
    )
    
    __table_args__ = (
        Index('ix_link_note', 'note_id'),
        Index('ix_link_entity', 'entity_type', 'entity_id'),
        Index('ix_link_type', 'link_type'),
        Index('ix_link_confidence', 'confidence'),
        Index('ix_link_validated', 'validated'),
        UniqueConstraint('note_id', 'entity_type', 'entity_id', 'link_type', name='uq_entity_link'),
    )
    
    def __repr__(self) -> str:
        return f"<EntityLink(note_id='{self.note_id}', entity='{self.entity_type}:{self.entity_id}')>"


class EntityRecognitionCache(Base, UUIDMixin, TimestampMixin):
    """Model for caching entity recognition results for performance."""
    __tablename__ = "entity_recognition_cache"
    
    # Search/input text
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)  # SHA-256 of normalized input
    
    # Recognition results
    recognized_entities: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    # Structure: {
    #   "matches": [{"type": "stakeholder", "id": "123", "name": "John Smith", "confidence": 95}],
    #   "suggestions": [{"type": "account", "id": "456", "name": "ABC Corp", "confidence": 87}]
    # }
    
    # Cache metadata
    cache_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")
    hit_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_hit: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Expiration
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    
    __table_args__ = (
        Index('ix_cache_hash', 'input_hash'),
        Index('ix_cache_expires', 'expires_at'),
        Index('ix_cache_version', 'cache_version'),
    )
    
    def __repr__(self) -> str:
        return f"<EntityRecognitionCache(hash='{self.input_hash[:16]}...', hits={self.hit_count})>"