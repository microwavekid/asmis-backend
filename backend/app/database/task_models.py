"""Enhanced Task models for the intelligent task execution system."""

from typing import Any, Dict, Optional, List
from datetime import datetime

from sqlalchemy import String, Text, JSON, ForeignKey, Index, UniqueConstraint, Boolean, Float, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin, SoftDeleteMixin


class Task(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Enhanced model for tasks with AI execution capabilities."""
    __tablename__ = "tasks"
    
    # Multi-tenant isolation
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenants.id"),
        nullable=False,
        index=True
    )
    
    # Core fields
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # User ownership and assignment
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)  # Task owner
    assigned_to: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)  # Assigned user
    
    # Standard task fields
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    # "pending", "in_progress", "completed", "blocked", "cancelled"
    due_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    # "low", "medium", "high", "urgent"
    
    # Relationships to business entities
    deal_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("deals.id"), nullable=True)
    account_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("accounts.id"), nullable=True)
    stakeholder_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("stakeholders.id"), nullable=True)
    
    # Execution metadata
    task_type: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")
    # "manual", "ai_suggested", "ai_automated"
    execution_mode: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")
    # "manual", "ai_assisted", "ai_supervised", "autonomous"
    ai_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0.0-1.0
    ai_rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")
    # "smart_capture", "manual", "meddpicc", "template", "automation"
    
    # Credit tracking
    estimated_credits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    actual_credits_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    complexity_tier: Mapped[str] = mapped_column(String(20), nullable=False, default="simple")
    # "simple", "medium", "complex"
    
    # Context linking
    smart_capture_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("smart_capture_notes.id"), 
        nullable=True
    )
    transcript_segments: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    # {"segments": [{"start": 0, "end": 100, "text": "...", "timestamp": "00:15:32"}]}
    
    # Execution tracking
    execution_status: Mapped[str] = mapped_column(String(50), nullable=False, default="not_started")
    # "not_started", "executing", "completed", "failed", "partial"
    execution_method: Mapped[str] = mapped_column(String(50), nullable=False, default="manual")
    # "manual", "ai_assisted", "ai_executed"
    execution_steps: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    execution_context: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Approval workflow
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    approval_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # "pending", "approved", "rejected"
    approved_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Template reference
    template_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("task_templates.id"), 
        nullable=True
    )
    template_parameters: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Outcomes
    outcome_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # "successful", "failed", "partial", "cancelled"
    outcome_metrics: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    outcome_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    tags: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="owned_tasks"
    )
    assignee: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="assigned_tasks"
    )
    approver: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[approved_by],
        back_populates="approved_tasks"
    )
    account: Mapped[Optional["Account"]] = relationship(
        "Account",
        back_populates="tasks"
    )
    deal: Mapped[Optional["Deal"]] = relationship(
        "Deal",
        back_populates="tasks"
    )
    stakeholder: Mapped[Optional["Stakeholder"]] = relationship(
        "Stakeholder",
        back_populates="tasks"
    )
    smart_capture_note: Mapped[Optional["SmartCaptureNote"]] = relationship(
        "SmartCaptureNote",
        back_populates="tasks"
    )
    template: Mapped[Optional["TaskTemplate"]] = relationship(
        "TaskTemplate",
        back_populates="tasks"
    )
    execution_history: Mapped[List["TaskExecutionHistory"]] = relationship(
        "TaskExecutionHistory",
        back_populates="task",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index('ix_task_tenant_status', 'tenant_id', 'status'),
        Index('ix_task_tenant_assignee', 'tenant_id', 'assigned_to'),
        Index('ix_task_tenant_due_date', 'tenant_id', 'due_date'),
        Index('ix_task_deal', 'deal_id'),
        Index('ix_task_account', 'account_id'),
        Index('ix_task_stakeholder', 'stakeholder_id'),
        Index('ix_task_priority_due', 'priority', 'due_date'),
        Index('ix_task_execution_mode', 'execution_mode'),
        Index('ix_task_task_type', 'task_type'),
        Index('ix_task_template', 'template_id'),
        CheckConstraint('ai_confidence >= 0.0 AND ai_confidence <= 1.0', name='check_ai_confidence_range'),
        CheckConstraint('estimated_credits >= 0', name='check_estimated_credits_positive'),
        CheckConstraint('actual_credits_used >= 0', name='check_actual_credits_positive'),
    )
    
    def __repr__(self) -> str:
        return f"<Task(title='{self.title}', status='{self.status}', mode='{self.execution_mode}')>"


class TaskTemplate(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Model for task templates with hierarchical ownership."""
    __tablename__ = "task_templates"
    
    # Ownership hierarchy
    template_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # "system", "tenant", "user"
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenants.id"),
        nullable=False,
        index=True
    )
    owner_user_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("users.id"), 
        nullable=True
    )
    
    # Template inheritance
    parent_template_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("task_templates.id"),
        nullable=True
    )
    allow_override: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Configuration
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # "follow_up", "research", "preparation", "communication", "analysis"
    deal_stage: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # "discovery", "technical_evaluation", "business_evaluation", "negotiation", "closing"
    trigger_conditions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    # {"event": "meeting_completed", "filters": {"meeting_type": "discovery"}}
    
    # Customizable fields
    fields: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    # {"title": {"type": "string", "default": "Follow up with {stakeholder_name}"},
    #  "description": {"type": "text", "template": "..."}}
    default_values: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    required_fields: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    
    # Credit estimation
    estimated_credits: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    complexity_tier: Mapped[str] = mapped_column(String(20), nullable=False, default="simple")
    
    # Safety and automation
    customer_facing: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    automation_eligible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    whitelist_actions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    # {"allowed": ["send_internal_email", "update_crm"], "forbidden": ["send_customer_email"]}
    
    # AI configuration
    ai_instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    success_criteria: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    best_practices: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    
    # Usage tracking
    usage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Visibility (for future marketplace)
    visibility: Mapped[str] = mapped_column(String(20), nullable=False, default="private")
    # "private", "team", "tenant", "public"
    
    # Relationships
    owner: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="task_templates"
    )
    parent_template: Mapped[Optional["TaskTemplate"]] = relationship(
        "TaskTemplate",
        remote_side="TaskTemplate.id",
        back_populates="child_templates"
    )
    child_templates: Mapped[List["TaskTemplate"]] = relationship(
        "TaskTemplate",
        back_populates="parent_template"
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="template"
    )
    
    __table_args__ = (
        UniqueConstraint('tenant_id', 'name', 'template_type', name='uq_template_name_per_type'),
        Index('ix_template_type', 'template_type'),
        Index('ix_template_tenant', 'tenant_id'),
        Index('ix_template_owner', 'owner_user_id'),
        Index('ix_template_parent', 'parent_template_id'),
        Index('ix_template_category', 'category'),
        Index('ix_template_stage', 'deal_stage'),
        Index('ix_template_visibility', 'visibility'),
        Index('ix_template_usage', 'usage_count'),
        CheckConstraint('estimated_credits >= 0', name='check_template_credits_positive'),
    )
    
    def __repr__(self) -> str:
        return f"<TaskTemplate(name='{self.name}', type='{self.template_type}')>"


class TaskExecutionHistory(Base, UUIDMixin, TimestampMixin):
    """Model for tracking task execution history and audit trail."""
    __tablename__ = "task_execution_history"
    
    # Reference to task
    task_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tasks.id"),
        nullable=False
    )
    
    # Execution timestamp and performer
    execution_timestamp: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    executor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # "human", "ai_assisted", "ai_autonomous"
    executor_id: Mapped[str] = mapped_column(String(36), nullable=False)  # User ID or AI agent ID
    
    # Execution details
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # "status_change", "content_generation", "assignment", "approval", "execution_step"
    action_details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    # {"from_status": "pending", "to_status": "in_progress", "reason": "..."}
    
    steps_taken: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    # [{"step": 1, "action": "generate_email", "result": "success", "duration_ms": 1200}]
    tools_used: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    # ["email_generator", "crm_updater"]
    data_accessed: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    # {"deal": "deal_id", "stakeholder": "stakeholder_id", "transcript": "segment_ids"}
    
    # Credit consumption
    credits_consumed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    credit_breakdown: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    # {"email_generation": 300, "context_analysis": 150}
    
    # Results
    result_status: Mapped[str] = mapped_column(String(50), nullable=False)
    # "success", "partial_success", "failed", "cancelled"
    result_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True, default=dict)
    error_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # AI-specific metrics
    ai_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0.0-1.0
    ai_model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ai_prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ai_completion_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Performance metrics
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Relationships
    task: Mapped["Task"] = relationship(
        "Task",
        back_populates="execution_history"
    )
    
    __table_args__ = (
        Index('ix_execution_task', 'task_id'),
        Index('ix_execution_timestamp', 'execution_timestamp'),
        Index('ix_execution_type', 'executor_type'),
        Index('ix_execution_action', 'action_type'),
        Index('ix_execution_result', 'result_status'),
        CheckConstraint('credits_consumed >= 0', name='check_execution_credits_positive'),
        CheckConstraint('ai_confidence >= 0.0 AND ai_confidence <= 1.0', name='check_execution_confidence_range'),
    )
    
    def __repr__(self) -> str:
        return f"<TaskExecutionHistory(task_id='{self.task_id}', action='{self.action_type}', status='{self.result_status}')>"