# PATTERN_REF: AGENT_COMMUNICATION_PATTERN
# DECISION_REF: DEC_2025-07-02_001: Smart Capture API endpoint implementation

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import logging

from app.database.connection import get_db_session
from app.database.repositories import SmartCaptureRepository
from app.schemas.smart_capture import (
    SmartCaptureNoteCreate,
    SmartCaptureNoteResponse,
    LinkedEntity
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/smart-capture", tags=["smart-capture"])

@router.post("/notes", response_model=SmartCaptureNoteResponse)
async def create_smart_capture_note(
    note: SmartCaptureNoteCreate,
    db: AsyncSession = Depends(get_db_session)
) -> SmartCaptureNoteResponse:
    """Create a new smart capture note with linked entities."""
    try:
        logger.info(f"Creating smart capture note with {len(note.linked_entities)} linked entities")
        
        # Create repository instance
        repo = SmartCaptureRepository(db)
        
        # Create the note
        created_note = await repo.create_note(
            content=note.content,
            account_id=note.account_id,
            deal_id=note.deal_id,
            capture_method=note.capture_method,
            capture_location=note.capture_location,
            linked_entities=note.linked_entities
        )
        
        logger.info(f"Smart capture note created with ID: {created_note.id}")
        
        return SmartCaptureNoteResponse(
            id=created_note.id,
            content=created_note.content,
            account_id=created_note.account_id,
            deal_id=created_note.deal_id,
            capture_method=created_note.capture_method,
            capture_location=created_note.capture_location,
            linked_entities=[
                LinkedEntity(
                    id=entity.entity_id,
                    type=entity.entity_type,
                    name=entity.entity_name,
                    confidence=entity.confidence
                )
                for entity in created_note.linked_entities
            ],
            created_at=created_note.created_at
        )
        
    except Exception as e:
        logger.error(f"Error creating smart capture note: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notes/{note_id}", response_model=SmartCaptureNoteResponse)
async def get_smart_capture_note(
    note_id: str,
    db: AsyncSession = Depends(get_db_session)
) -> SmartCaptureNoteResponse:
    """Get a smart capture note by ID."""
    try:
        repo = SmartCaptureRepository(db)
        note = await repo.get_note_by_id(note_id)
        
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return SmartCaptureNoteResponse(
            id=note.id,
            content=note.content,
            account_id=note.account_id,
            deal_id=note.deal_id,
            capture_method=note.capture_method,
            capture_location=note.capture_location,
            linked_entities=[
                LinkedEntity(
                    id=entity.entity_id,
                    type=entity.entity_type,
                    name=entity.entity_name,
                    confidence=entity.confidence
                )
                for entity in note.linked_entities
            ],
            created_at=note.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting smart capture note: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notes", response_model=List[SmartCaptureNoteResponse])
async def list_smart_capture_notes(
    account_id: Optional[str] = None,
    deal_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db_session)
) -> List[SmartCaptureNoteResponse]:
    """List smart capture notes with optional filtering."""
    try:
        repo = SmartCaptureRepository(db)
        
        # Build filter criteria
        filters = {}
        if account_id:
            filters['account_id'] = account_id
        if deal_id:
            filters['deal_id'] = deal_id
        
        notes = await repo.list_notes(
            filters=filters,
            limit=limit,
            offset=offset
        )
        
        return [
            SmartCaptureNoteResponse(
                id=note.id,
                content=note.content,
                account_id=note.account_id,
                deal_id=note.deal_id,
                capture_method=note.capture_method,
                capture_location=note.capture_location,
                linked_entities=[
                    LinkedEntity(
                        id=entity.entity_id,
                        type=entity.entity_type,
                        name=entity.entity_name,
                        confidence=entity.confidence
                    )
                    for entity in note.linked_entities
                ],
                created_at=note.created_at
            )
            for note in notes
        ]
        
    except Exception as e:
        logger.error(f"Error listing smart capture notes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))