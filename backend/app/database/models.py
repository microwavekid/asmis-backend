"""Database models for ASMIS backend."""

from typing import Any, Dict, Optional
from datetime import datetime

from sqlalchemy import String, Text, JSON, ForeignKey, Index, UniqueConstraint, Boolean, Float
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