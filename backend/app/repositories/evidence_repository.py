"""
Evidence Repository for multi-source evidence management.
Handles evidence storage and retrieval with positioning support.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .base_repository import BaseRepository
from ..database.models import (
    IntelligenceEvidence, 
    Transcript, 
    TranscriptSegment, 
    Document, 
    DocumentSection
)
from ..database.connection import db_manager

logger = logging.getLogger(__name__)


class EvidenceRepository(BaseRepository[IntelligenceEvidence]):
    """Repository for evidence management operations."""
    
    def __init__(self):
        """Initialize evidence repository."""
        super().__init__(IntelligenceEvidence)
    
    def get_evidence_by_analysis(
        self, 
        session: Session, 
        analysis_id: str
    ) -> List[IntelligenceEvidence]:
        """
        Get all evidence for a specific analysis.
        
        Args:
            session: Database session
            analysis_id: Analysis ID
            
        Returns:
            List of evidence records
        """
        try:
            stmt = select(IntelligenceEvidence).where(
                IntelligenceEvidence.analysis_id == analysis_id
            ).order_by(IntelligenceEvidence.start_position)
            
            result = session.execute(stmt)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting evidence by analysis {analysis_id}: {e}")
            raise
    
    def get_evidence_by_element(
        self, 
        session: Session, 
        analysis_id: str, 
        element_type: str, 
        element_key: Optional[str] = None
    ) -> List[IntelligenceEvidence]:
        """
        Get evidence for a specific MEDDPICC element.
        
        Args:
            session: Database session
            analysis_id: Analysis ID
            element_type: Type of element (e.g., "decision_criteria")
            element_key: Specific element key (optional)
            
        Returns:
            List of evidence records
        """
        try:
            conditions = [
                IntelligenceEvidence.analysis_id == analysis_id,
                IntelligenceEvidence.element_type == element_type
            ]
            
            if element_key:
                conditions.append(IntelligenceEvidence.element_key == element_key)
            
            stmt = select(IntelligenceEvidence).where(
                and_(*conditions)
            ).order_by(IntelligenceEvidence.confidence.desc())
            
            result = session.execute(stmt)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting evidence by element {element_type}: {e}")
            raise
    
    def get_evidence_context(
        self, 
        session: Session, 
        evidence_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get full context for evidence overlay display.
        
        Args:
            session: Database session
            evidence_id: Evidence ID
            
        Returns:
            Evidence context data for overlay
        """
        try:
            evidence = self.get_by_id(session, evidence_id)
            if not evidence:
                return None
            
            # Get transcript information if available
            transcript_info = None
            if evidence.transcript_id:
                transcript = session.get(Transcript, evidence.transcript_id)
                if transcript:
                    transcript_info = {
                        "meeting_title": transcript.title,
                        "meeting_date": transcript.meeting_date.isoformat(),
                        "attendees": transcript.attendees or []
                    }
            
            # Get document information if available
            document_info = None
            if evidence.document_id:
                document = session.get(Document, evidence.document_id)
                if document:
                    document_info = {
                        "document_title": document.title,
                        "document_type": document.document_type,
                        "total_pages": document.total_pages
                    }
            
            return {
                "evidence": {
                    "text": evidence.evidence_text,
                    "highlighted_start": evidence.start_position,
                    "highlighted_end": evidence.end_position,
                    "confidence": evidence.confidence,
                    "extraction_type": evidence.extraction_type
                },
                "context": {
                    "before": evidence.context_before,
                    "after": evidence.context_after,
                    "speaker": evidence.speaker,
                    "timestamp": evidence.timestamp
                },
                "source_info": {
                    "transcript": transcript_info,
                    "document": document_info
                },
                "navigation": {
                    "transcript_id": evidence.transcript_id,
                    "document_id": evidence.document_id,
                    "segment_id": evidence.segment_id
                }
            }
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting evidence context {evidence_id}: {e}")
            raise
    
    def search_evidence(
        self, 
        session: Session, 
        query: str, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[IntelligenceEvidence]:
        """
        Search evidence across all sources.
        
        Args:
            session: Database session
            query: Search query
            filters: Optional filters (source_type, date_range, etc.)
            
        Returns:
            List of matching evidence records
        """
        try:
            # Basic text search - would be enhanced with full-text search
            conditions = [
                IntelligenceEvidence.evidence_text.ilike(f"%{query}%")
            ]
            
            # Apply filters if provided
            if filters:
                if "element_type" in filters:
                    conditions.append(
                        IntelligenceEvidence.element_type == filters["element_type"]
                    )
                
                if "confidence_min" in filters:
                    conditions.append(
                        IntelligenceEvidence.confidence >= filters["confidence_min"]
                    )
                
                if "extraction_type" in filters:
                    conditions.append(
                        IntelligenceEvidence.extraction_type == filters["extraction_type"]
                    )
            
            stmt = select(IntelligenceEvidence).where(
                and_(*conditions)
            ).order_by(IntelligenceEvidence.confidence.desc()).limit(50)
            
            result = session.execute(stmt)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error searching evidence: {e}")
            raise
    
    def get_evidence_timeline(
        self, 
        session: Session, 
        deal_id: Optional[str] = None, 
        account_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get evidence timeline for deal or account.
        
        Args:
            session: Database session
            deal_id: Deal ID (optional)
            account_id: Account ID (optional)
            
        Returns:
            Timeline of evidence across meetings/documents
        """
        try:
            # This would join evidence with transcripts/documents
            # to create a chronological timeline
            # Simplified implementation for now
            
            conditions = []
            
            if deal_id:
                # Would need to join with transcripts/documents to filter by deal
                pass
            
            if account_id:
                # Would need to join with transcripts/documents to filter by account
                pass
            
            stmt = select(IntelligenceEvidence).order_by(
                IntelligenceEvidence.created_at.desc()
            ).limit(100)
            
            result = session.execute(stmt)
            evidence_records = result.scalars().all()
            
            # Convert to timeline format
            timeline = []
            for evidence in evidence_records:
                timeline.append({
                    "evidence_id": evidence.id,
                    "element_type": evidence.element_type,
                    "evidence_text": evidence.evidence_text,
                    "confidence": evidence.confidence,
                    "timestamp": evidence.created_at.isoformat(),
                    "source_type": "transcript" if evidence.transcript_id else "document"
                })
            
            return timeline
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting evidence timeline: {e}")
            raise


class TranscriptRepository(BaseRepository[Transcript]):
    """Repository for transcript management operations."""
    
    def __init__(self):
        """Initialize transcript repository."""
        super().__init__(Transcript)
    
    def get_by_deal(
        self, 
        session: Session, 
        deal_id: str
    ) -> List[Transcript]:
        """Get all transcripts for a deal."""
        try:
            stmt = select(Transcript).where(
                Transcript.deal_id == deal_id
            ).order_by(Transcript.meeting_date.desc())
            
            result = session.execute(stmt)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting transcripts by deal {deal_id}: {e}")
            raise
    
    def create_with_segments(
        self, 
        session: Session, 
        transcript_data: Dict[str, Any], 
        segments: List[Dict[str, Any]]
    ) -> Transcript:
        """Create transcript with associated segments."""
        try:
            # Create transcript
            transcript = Transcript(**transcript_data)
            session.add(transcript)
            session.flush()  # Get the ID
            
            # Create segments
            for segment_data in segments:
                segment = TranscriptSegment(
                    transcript_id=transcript.id,
                    **segment_data
                )
                session.add(segment)
            
            session.commit()
            return transcript
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating transcript with segments: {e}")
            session.rollback()
            raise


# Repository instances
evidence_repository = EvidenceRepository()
transcript_repository = TranscriptRepository()