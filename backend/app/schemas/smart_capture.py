# PATTERN_REF: AGENT_COMMUNICATION_PATTERN
# Smart Capture schemas for API validation

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class LinkedEntity(BaseModel):
    """Linked entity in a smart capture note."""
    id: str
    type: Literal["account", "deal", "contact", "opportunity"]
    name: str
    confidence: float = Field(ge=0.0, le=1.0, default=0.9)

class SmartCaptureNoteCreate(BaseModel):
    """Request model for creating a smart capture note."""
    content: str = Field(..., min_length=1, description="Note content")
    account_id: Optional[str] = None
    deal_id: Optional[str] = None
    linked_entities: List[LinkedEntity] = Field(default_factory=list)
    capture_method: Literal["manual", "voice", "import"] = "manual"
    capture_location: Optional[str] = None

class SmartCaptureNoteResponse(BaseModel):
    """Response model for smart capture note."""
    id: str
    content: str
    account_id: Optional[str] = None
    deal_id: Optional[str] = None
    linked_entities: List[LinkedEntity]
    capture_method: str
    capture_location: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True