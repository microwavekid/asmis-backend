"""
Pydantic schemas for Deals API - MVP Backend-Frontend Integration
Defines request/response models compatible with Linear UI.

PATTERN_REF: MVP_FIRST_BUILDING_BLOCKS_PATTERN
DECISION_REF: DEC_2025-06-29_MVP_PIVOT_001
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Deal List Response (for deals table)
class DealListResponse(BaseModel):
    """Response model for deals list - compatible with Linear UI deals table."""
    id: str
    name: str
    account: str
    stage: str
    health: int = Field(..., ge=0, le=100, description="Deal health score 0-100")
    value: float
    closeDate: Optional[str] = Field(None, description="ISO date string")
    meddpiccScore: int = Field(..., ge=0, le=100, description="MEDDPICC score 0-100")
    confidence: float = Field(..., ge=0, le=100, description="Probability 0-100")
    priority: str = Field(..., pattern="^(high|medium|low)$")
    nextActions: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)


# Deal Creation Request
class DealCreate(BaseModel):
    """Request model for creating a new deal."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    account_id: str
    deal_type: Optional[str] = Field("new_business", pattern="^(new_business|expansion|renewal)$")
    amount: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field("USD", max_length=3)
    probability: Optional[float] = Field(None, ge=0, le=100)
    close_date: Optional[datetime] = None
    stage: Optional[str] = Field("discovery")
    status: Optional[str] = Field("active", pattern="^(active|paused|closed)$")
    competitive_situation: Optional[str] = Field(None, pattern="^(no_competition|favored|competitive|disadvantaged)$")
    deal_owner: Optional[str] = None
    sales_engineer: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[Dict[str, Any]] = Field(default_factory=dict)


# Deal Update Request
class DealUpdate(BaseModel):
    """Request model for updating an existing deal."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    amount: Optional[float] = Field(None, ge=0)
    probability: Optional[float] = Field(None, ge=0, le=100)
    close_date: Optional[datetime] = None
    stage: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(active|paused|closed)$")
    competitive_situation: Optional[str] = Field(None, pattern="^(no_competition|favored|competitive|disadvantaged)$")
    deal_owner: Optional[str] = None
    sales_engineer: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None


# Stakeholder Response
class StakeholderResponse(BaseModel):
    """Response model for stakeholder information."""
    id: str
    name: str
    title: Optional[str]
    email: Optional[str]
    department: Optional[str]
    seniority_level: Optional[str]
    roles: Dict[str, bool]
    influence_level: Optional[str]
    engagement_level: Optional[str]
    last_contact_date: Optional[str]


# MEDDPICC Component Response
class MEDDPICCComponentResponse(BaseModel):
    """Response model for individual MEDDPICC component."""
    score: int = Field(..., ge=0, le=100)
    status: str = Field(..., pattern="^(complete|partial|missing)$")
    data: Dict[str, Any] = Field(default_factory=dict)


# MEDDPICC Analysis Response
class MEDDPICCResponse(BaseModel):
    """Response model for complete MEDDPICC analysis."""
    deal_id: str
    overall_score: int = Field(..., ge=0, le=100)
    completeness_score: int = Field(..., ge=0, le=100)
    processing_status: str = Field(..., pattern="^(idle|processing|complete|error)$")
    last_scored_at: Optional[datetime]
    components: Dict[str, MEDDPICCComponentResponse]
    insights: Dict[str, Any] = Field(default_factory=dict)
    risks: Dict[str, Any] = Field(default_factory=dict)
    recommendations: Dict[str, Any] = Field(default_factory=dict)


# Detailed Deal Response
class DealResponse(BaseModel):
    """Response model for detailed deal information."""
    id: str
    name: str
    description: Optional[str]
    account_id: str
    account_name: str
    stage: str
    status: str
    amount: Optional[float]
    currency: str
    probability: Optional[float]
    close_date: Optional[datetime]
    deal_owner: Optional[str]
    sales_engineer: Optional[str]
    competitive_situation: Optional[str]
    primary_competitors: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str]
    tags: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    meddpicc_analysis: Optional[Dict[str, Any]] = None
    stakeholders: List[StakeholderResponse] = Field(default_factory=list)


# Transcript Analysis Request
class TranscriptAnalysisRequest(BaseModel):
    """Request model for analyzing transcript content."""
    content: str = Field(..., min_length=1)
    source_type: str = Field("transcript", pattern="^(transcript|meeting_notes|call_recording)$")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


# Analysis Status Response
class AnalysisStatusResponse(BaseModel):
    """Response model for analysis processing status."""
    deal_id: str
    status: str = Field(..., pattern="^(pending|processing|completed|failed)$")
    progress: Optional[float] = Field(None, ge=0, le=100)
    current_step: Optional[str] = None
    estimated_time_remaining: Optional[int] = Field(None, description="Seconds remaining")
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


# Account Response (basic)
class AccountResponse(BaseModel):
    """Response model for account information."""
    id: str
    name: str
    domain: Optional[str]
    industry: Optional[str]
    company_size: Optional[str]
    account_type: str
    website: Optional[str]
    headquarters: Optional[str]
    annual_revenue: Optional[float]
    employee_count: Optional[int]


# Deal Statistics Response
class DealStatsResponse(BaseModel):
    """Response model for deal statistics dashboard."""
    total_deals: int = Field(..., ge=0)
    total_value: float = Field(..., ge=0)
    average_deal_size: float = Field(..., ge=0)
    deals_by_stage: Dict[str, int] = Field(default_factory=dict)
    deals_by_priority: Dict[str, int] = Field(default_factory=dict)
    health_score_distribution: Dict[str, int] = Field(default_factory=dict)
    meddpicc_score_distribution: Dict[str, int] = Field(default_factory=dict)
    recent_activity: Dict[str, int] = Field(default_factory=dict)
    conversion_rates: Dict[str, float] = Field(default_factory=dict)


# Error Response
class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    detail: str
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = None