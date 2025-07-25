"""Enhanced Pydantic schemas for the intelligent task execution system."""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List, Literal
from datetime import datetime
from enum import Enum


# Enums for task fields
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ExecutionMode(str, Enum):
    MANUAL = "manual"
    AI_ASSISTED = "ai_assisted"
    AI_SUPERVISED = "ai_supervised"
    AUTONOMOUS = "autonomous"

class TaskType(str, Enum):
    MANUAL = "manual"
    AI_SUGGESTED = "ai_suggested"
    AI_AUTOMATED = "ai_automated"

class ComplexityTier(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"

class TemplateType(str, Enum):
    SYSTEM = "system"
    TENANT = "tenant"
    USER = "user"

class VisibilityType(str, Enum):
    PRIVATE = "private"
    TEAM = "team"
    TENANT = "tenant"
    PUBLIC = "public"


# Base schemas
class TaskBase(BaseModel):
    """Base schema for task fields."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)
    status: TaskStatus = TaskStatus.PENDING
    due_date: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    
    # Relationships
    deal_id: Optional[str] = Field(None, pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    account_id: Optional[str] = Field(None, pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    stakeholder_id: Optional[str] = Field(None, pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    
    # Metadata
    tags: Optional[Dict[str, Any]] = Field(default_factory=dict)
    notes: Optional[str] = Field(None, max_length=10000)


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    assigned_to: Optional[str] = Field(None, pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    
    # Execution metadata
    task_type: TaskType = TaskType.MANUAL
    execution_mode: ExecutionMode = ExecutionMode.MANUAL
    source: str = Field("manual", max_length=50)
    
    # Template reference
    template_id: Optional[str] = Field(None, pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    template_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    # Context linking
    smart_capture_id: Optional[str] = Field(None, pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    transcript_segments: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[str] = Field(None, pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    
    # Execution updates
    execution_mode: Optional[ExecutionMode] = None
    execution_status: Optional[str] = None
    outcome_status: Optional[str] = None
    outcome_notes: Optional[str] = Field(None, max_length=10000)
    
    # Metadata
    tags: Optional[Dict[str, Any]] = None
    notes: Optional[str] = Field(None, max_length=10000)


class TaskAssignment(BaseModel):
    """Schema for assigning a task to a user."""
    assigned_to: str = Field(..., pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    notes: Optional[str] = Field(None, max_length=1000)


class TaskCompletion(BaseModel):
    """Schema for marking a task as completed."""
    outcome_status: Literal["successful", "failed", "partial", "cancelled"] = "successful"
    outcome_notes: Optional[str] = Field(None, max_length=10000)
    outcome_metrics: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TaskApproval(BaseModel):
    """Schema for approving or rejecting a task."""
    approval_status: Literal["approved", "rejected"] = "approved"
    approval_notes: Optional[str] = Field(None, max_length=1000)


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: str
    tenant_id: str
    user_id: str
    assigned_to: Optional[str] = None
    
    # Execution metadata
    task_type: TaskType
    execution_mode: ExecutionMode
    ai_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    ai_rationale: Optional[str] = None
    source: str
    
    # Credit tracking
    estimated_credits: int = Field(ge=0)
    actual_credits_used: int = Field(ge=0)
    complexity_tier: ComplexityTier
    
    # Context linking
    smart_capture_id: Optional[str] = None
    transcript_segments: Optional[Dict[str, Any]] = None
    
    # Execution tracking
    execution_status: str
    execution_method: str
    completed_at: Optional[datetime] = None
    
    # Approval workflow
    requires_approval: bool
    approval_status: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    
    # Template reference
    template_id: Optional[str] = None
    template_parameters: Optional[Dict[str, Any]] = None
    
    # Outcomes
    outcome_status: Optional[str] = None
    outcome_metrics: Optional[Dict[str, Any]] = None
    outcome_notes: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for paginated task list response."""
    tasks: List[TaskResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool


# Task Template Schemas
class TaskTemplateBase(BaseModel):
    """Base schema for task template fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)
    category: Optional[str] = Field(None, max_length=100)
    deal_stage: Optional[str] = Field(None, max_length=50)
    
    # Configuration
    fields: Dict[str, Any] = Field(default_factory=dict)
    default_values: Dict[str, Any] = Field(default_factory=dict)
    required_fields: List[str] = Field(default_factory=list)
    
    # Safety
    customer_facing: bool = False
    automation_eligible: bool = False
    
    # AI configuration
    ai_instructions: Optional[str] = Field(None, max_length=10000)
    success_criteria: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TaskTemplateCreate(TaskTemplateBase):
    """Schema for creating a new task template."""
    template_type: TemplateType = TemplateType.USER
    parent_template_id: Optional[str] = Field(None, pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    allow_override: bool = True
    visibility: VisibilityType = VisibilityType.PRIVATE
    
    # Credit configuration
    estimated_credits: int = Field(100, ge=0)
    complexity_tier: ComplexityTier = ComplexityTier.SIMPLE


class TaskTemplateUpdate(BaseModel):
    """Schema for updating an existing task template."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)
    category: Optional[str] = Field(None, max_length=100)
    
    # Configuration updates
    fields: Optional[Dict[str, Any]] = None
    default_values: Optional[Dict[str, Any]] = None
    required_fields: Optional[List[str]] = None
    
    # AI configuration
    ai_instructions: Optional[str] = Field(None, max_length=10000)
    success_criteria: Optional[Dict[str, Any]] = None
    
    # Credit updates
    estimated_credits: Optional[int] = Field(None, ge=0)
    complexity_tier: Optional[ComplexityTier] = None


class TaskTemplateResponse(TaskTemplateBase):
    """Schema for task template response."""
    id: str
    template_type: TemplateType
    tenant_id: str
    owner_user_id: Optional[str] = None
    
    # Template inheritance
    parent_template_id: Optional[str] = None
    allow_override: bool
    
    # Credit information
    estimated_credits: int
    complexity_tier: ComplexityTier
    
    # Usage tracking
    usage_count: int
    last_used_at: Optional[datetime] = None
    
    # Visibility
    visibility: VisibilityType
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True


# Task Execution History Schemas
class TaskExecutionHistoryResponse(BaseModel):
    """Schema for task execution history response."""
    id: str
    task_id: str
    execution_timestamp: datetime
    executor_type: str
    executor_id: str
    
    # Action details
    action_type: str
    action_details: Dict[str, Any]
    
    # Results
    result_status: str
    result_data: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None
    
    # Credit consumption
    credits_consumed: int
    credit_breakdown: Optional[Dict[str, Any]] = None
    
    # AI metrics
    ai_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    ai_model_used: Optional[str] = None
    
    # Performance
    duration_ms: Optional[int] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Bulk Operations
class BulkTaskCreate(BaseModel):
    """Schema for creating multiple tasks at once."""
    tasks: List[TaskCreate] = Field(..., min_items=1, max_items=50)
    link_to_context: bool = True
    

class BulkTaskResponse(BaseModel):
    """Schema for bulk task creation response."""
    created_tasks: List[TaskResponse]
    failed_tasks: List[Dict[str, Any]] = Field(default_factory=list)
    total_created: int
    total_failed: int


# AI Task Suggestion Schemas
class TaskSuggestionRequest(BaseModel):
    """Schema for requesting AI task suggestions."""
    context_type: Literal["smart_capture", "meddpicc", "meeting", "deal_stage"] = "smart_capture"
    context_id: str = Field(..., pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    include_templates: bool = True
    max_suggestions: int = Field(10, ge=1, le=20)
    min_confidence: float = Field(0.5, ge=0.0, le=1.0)


class TaskSuggestion(BaseModel):
    """Schema for a single AI task suggestion."""
    title: str
    description: str
    priority: TaskPriority
    estimated_credits: int
    complexity_tier: ComplexityTier
    ai_confidence: float = Field(..., ge=0.0, le=1.0)
    ai_rationale: str
    template_id: Optional[str] = None
    suggested_due_date: Optional[datetime] = None


class TaskSuggestionsResponse(BaseModel):
    """Schema for AI task suggestions response."""
    suggestions: List[TaskSuggestion]
    context_summary: str
    total_suggestions: int
    avg_confidence: float = Field(..., ge=0.0, le=1.0)


# Credit Estimation
class CreditEstimationRequest(BaseModel):
    """Schema for estimating task credits."""
    task_ids: Optional[List[str]] = Field(None, max_items=20)
    tasks: Optional[List[TaskCreate]] = Field(None, max_items=20)
    execution_plan: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @validator('*')
    def at_least_one_required(cls, v, values):
        if not values.get('task_ids') and not values.get('tasks'):
            raise ValueError('Either task_ids or tasks must be provided')
        return v


class CreditEstimation(BaseModel):
    """Schema for credit estimation response."""
    task_id: Optional[str] = None
    estimated_credits: int = Field(..., ge=0)
    complexity_tier: ComplexityTier
    breakdown: Dict[str, int] = Field(default_factory=dict)
    confidence: float = Field(..., ge=0.0, le=1.0)


class CreditEstimationResponse(BaseModel):
    """Schema for bulk credit estimation response."""
    estimations: List[CreditEstimation]
    total_estimated_credits: int
    avg_complexity: str
    warnings: List[str] = Field(default_factory=list)


# Template Recommendation
class TemplateRecommendationRequest(BaseModel):
    """Schema for requesting template recommendations."""
    deal_id: Optional[str] = Field(None, pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    context: Dict[str, Any] = Field(default_factory=dict)
    limit: int = Field(5, ge=1, le=20)
    include_system_templates: bool = True
    include_tenant_templates: bool = True


class TemplateRecommendation(BaseModel):
    """Schema for a single template recommendation."""
    template: TaskTemplateResponse
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    match_reasons: List[str] = Field(default_factory=list)


class TemplateRecommendationResponse(BaseModel):
    """Schema for template recommendations response."""
    recommendations: List[TemplateRecommendation]
    total_found: int
    context_matched: Dict[str, Any] = Field(default_factory=dict)