# PATTERN_REF: DATABASE_ACCESS_PATTERN
# Smart Capture repository implementation

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime

from app.database.models import SmartCaptureNote, SmartCaptureLinkedEntity

class SmartCaptureRepository:
    """Repository for Smart Capture operations."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def create_note(
        self,
        content: str,
        account_id: Optional[str] = None,
        deal_id: Optional[str] = None,
        capture_method: str = "manual",
        capture_location: Optional[str] = None,
        linked_entities: Optional[List[Dict[str, Any]]] = None
    ) -> SmartCaptureNote:
        """Create a new smart capture note with linked entities."""
        
        # Create the note
        note = SmartCaptureNote(
            id=str(uuid.uuid4()),
            content=content,
            account_id=account_id,
            deal_id=deal_id,
            capture_method=capture_method,
            capture_location=capture_location,
            created_at=datetime.utcnow()
        )
        
        # Add linked entities if provided
        if linked_entities:
            for entity_data in linked_entities:
                linked_entity = SmartCaptureLinkedEntity(
                    id=str(uuid.uuid4()),
                    note_id=note.id,
                    entity_id=entity_data['id'],
                    entity_type=entity_data['type'],
                    entity_name=entity_data['name'],
                    confidence=entity_data.get('confidence', 0.9)
                )
                note.linked_entities.append(linked_entity)
        
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        
        return note
    
    async def get_note_by_id(self, note_id: str) -> Optional[SmartCaptureNote]:
        """Get a smart capture note by ID."""
        query = select(SmartCaptureNote).options(
            selectinload(SmartCaptureNote.linked_entities)
        ).where(SmartCaptureNote.id == note_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def list_notes(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[SmartCaptureNote]:
        """List smart capture notes with optional filtering."""
        query = select(SmartCaptureNote).options(
            selectinload(SmartCaptureNote.linked_entities)
        )
        
        # Apply filters
        if filters:
            if 'account_id' in filters:
                query = query.where(SmartCaptureNote.account_id == filters['account_id'])
            if 'deal_id' in filters:
                query = query.where(SmartCaptureNote.deal_id == filters['deal_id'])
        
        # Order by creation date descending
        query = query.order_by(SmartCaptureNote.created_at.desc())
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete_note(self, note_id: str) -> bool:
        """Delete a smart capture note."""
        note = await self.get_note_by_id(note_id)
        if not note:
            return False
        
        await self.db.delete(note)
        await self.db.commit()
        return True