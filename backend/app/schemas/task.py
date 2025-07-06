from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field("open", pattern="^(open|in_progress|completed)$")
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    account_id: Optional[str] = None
    deal_id: Optional[str] = None
    stakeholder_id: Optional[str] = None
    tags: Optional[Dict[str, Any]] = Field(default_factory=dict)
    notes: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(open|in_progress|completed)$")
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    tags: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    due_date: Optional[datetime]
    priority: Optional[str]
    account_id: Optional[str]
    deal_id: Optional[str]
    stakeholder_id: Optional[str]
    tags: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime 