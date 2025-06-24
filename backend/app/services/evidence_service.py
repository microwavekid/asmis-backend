"""
Async Evidence Service for Multi-Source Intelligence
Handles evidence extraction, positioning, and storage for MEDDPICC analysis.
"""

import asyncio
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from ..database.connection import db_manager
from ..database.models import IntelligenceEvidence, Transcript, TranscriptSegment
from ..repositories.evidence_repository import EvidenceRepository

logger = logging.getLogger(__name__)


@dataclass
class EvidencePoint:
    """Evidence point with positioning information."""
    element_type: str  # "decision_criteria", "champion", etc.
    element_key: str   # Specific element identifier
    evidence_text: str
    start_position: int
    end_position: int
    speaker: Optional[str] = None
    timestamp: Optional[str] = None
    confidence: float = 0.0
    extraction_type: str = "explicit"


@dataclass
class TranscriptContext:
    """Transcript context for evidence extraction."""
    transcript_id: str
    content: str
    segments: List[Dict[str, Any]]
    analysis_id: str


class EvidenceService:
    """
    Async evidence extraction and storage service.
    Handles positioning and context for evidence overlay system.
    """
    
    def __init__(self):
        """Initialize evidence service."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.evidence_repo = EvidenceRepository()
    
    async def process_analysis_evidence(
        self, 
        analysis_result: Dict[str, Any], 
        transcript_content: str,
        transcript_id: str,
        analysis_id: str
    ) -> None:
        """
        Process MEDDPICC analysis results and extract evidence asynchronously.
        
        Args:
            analysis_result: Complete MEDDPICC analysis results
            transcript_content: Full transcript content
            transcript_id: Transcript database ID
            analysis_id: Analysis session ID
        """
        try:
            self.logger.info(f"Starting evidence processing for analysis {analysis_id}")
            
            # Create transcript context
            transcript_context = await self._create_transcript_context(
                transcript_content, transcript_id, analysis_id
            )
            
            # Extract evidence points from analysis
            evidence_points = self._extract_evidence_from_analysis(
                analysis_result, transcript_context
            )
            
            self.logger.info(f"Extracted {len(evidence_points)} evidence points")
            
            # Store evidence in database
            if evidence_points:
                await self._store_evidence_batch(evidence_points, transcript_context)
            
            self.logger.info(f"Evidence processing complete for analysis {analysis_id}")
            
        except Exception as e:
            self.logger.error(f"Error processing evidence for analysis {analysis_id}: {e}")
            # Don't raise - this is background processing
    
    async def _create_transcript_context(
        self, 
        content: str, 
        transcript_id: str, 
        analysis_id: str
    ) -> TranscriptContext:
        """Create transcript context with segments."""
        # Parse transcript into segments (simplified for now)
        segments = self._parse_transcript_segments(content)
        
        return TranscriptContext(
            transcript_id=transcript_id,
            content=content,
            segments=segments,
            analysis_id=analysis_id
        )
    
    def _parse_transcript_segments(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse transcript content into segments with speaker and timing.
        This is a simplified version - would be enhanced based on transcript format.
        """
        segments = []
        
        # Basic pattern for speaker detection (Speaker: text)
        speaker_pattern = r'^(\w+(?:\s+\w+)*?):\s+(.+)$'
        
        lines = content.split('\n')
        current_position = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                current_position += 1
                continue
                
            match = re.match(speaker_pattern, line)
            if match:
                speaker = match.group(1)
                text = match.group(2)
                
                segments.append({
                    'speaker': speaker,
                    'text': text,
                    'start_position': current_position,
                    'end_position': current_position + len(line),
                    'timestamp': None  # Would extract from actual transcript format
                })
            
            current_position += len(line) + 1  # +1 for newline
        
        return segments
    
    def _extract_evidence_from_analysis(
        self, 
        analysis_result: Dict[str, Any], 
        context: TranscriptContext
    ) -> List[EvidencePoint]:
        """Extract evidence points from MEDDPICC analysis result."""
        evidence_points = []
        
        try:
            # Extract decision criteria evidence
            if 'decision_criteria' in analysis_result:
                criteria_evidence = self._extract_criteria_evidence(
                    analysis_result['decision_criteria'], context
                )
                evidence_points.extend(criteria_evidence)
            
            # Extract champion evidence
            if 'champion' in analysis_result:
                champion_evidence = self._extract_champion_evidence(
                    analysis_result['champion'], context
                )
                evidence_points.extend(champion_evidence)
            
            # Extract economic buyer evidence
            if 'economic_buyer' in analysis_result:
                economic_buyer_evidence = self._extract_economic_buyer_evidence(
                    analysis_result['economic_buyer'], context
                )
                evidence_points.extend(economic_buyer_evidence)
            
            # Extract other MEDDPICC elements as needed
            # (metrics, decision_process, paper_process, implicate_pain, competition)
            
        except Exception as e:
            self.logger.error(f"Error extracting evidence from analysis: {e}")
        
        return evidence_points
    
    def _extract_criteria_evidence(
        self, 
        criteria_data: Any, 
        context: TranscriptContext
    ) -> List[EvidencePoint]:
        """Extract evidence for decision criteria."""
        evidence_points = []
        
        try:
            # Handle both old format (list) and new format (dict with categories)
            if isinstance(criteria_data, dict) and 'criteria' in criteria_data:
                # New structured format
                for category, criteria_list in criteria_data['criteria'].items():
                    for i, criterion in enumerate(criteria_list):
                        if isinstance(criterion, dict) and 'criterion' in criterion:
                            evidence = self._find_evidence_in_transcript(
                                criterion['criterion'], context, 'decision_criteria', f"{category}_{i}"
                            )
                            if evidence:
                                evidence_points.append(evidence)
            elif isinstance(criteria_data, list):
                # Old format - simple list
                for i, criterion in enumerate(criteria_data):
                    criterion_text = criterion if isinstance(criterion, str) else str(criterion)
                    evidence = self._find_evidence_in_transcript(
                        criterion_text, context, 'decision_criteria', f"criterion_{i}"
                    )
                    if evidence:
                        evidence_points.append(evidence)
        
        except Exception as e:
            self.logger.error(f"Error extracting criteria evidence: {e}")
        
        return evidence_points
    
    def _extract_champion_evidence(
        self, 
        champion_data: Any, 
        context: TranscriptContext
    ) -> List[EvidencePoint]:
        """Extract evidence for champion identification."""
        evidence_points = []
        
        try:
            if isinstance(champion_data, dict):
                if 'name' in champion_data:
                    evidence = self._find_evidence_in_transcript(
                        champion_data['name'], context, 'champion', 'name'
                    )
                    if evidence:
                        evidence_points.append(evidence)
                
                if 'rationale' in champion_data:
                    evidence = self._find_evidence_in_transcript(
                        champion_data['rationale'], context, 'champion', 'rationale'
                    )
                    if evidence:
                        evidence_points.append(evidence)
        
        except Exception as e:
            self.logger.error(f"Error extracting champion evidence: {e}")
        
        return evidence_points
    
    def _extract_economic_buyer_evidence(
        self, 
        economic_buyer_data: Any, 
        context: TranscriptContext
    ) -> List[EvidencePoint]:
        """Extract evidence for economic buyer identification."""
        evidence_points = []
        
        try:
            if isinstance(economic_buyer_data, dict):
                if 'name' in economic_buyer_data:
                    evidence = self._find_evidence_in_transcript(
                        economic_buyer_data['name'], context, 'economic_buyer', 'name'
                    )
                    if evidence:
                        evidence_points.append(evidence)
        
        except Exception as e:
            self.logger.error(f"Error extracting economic buyer evidence: {e}")
        
        return evidence_points
    
    def _find_evidence_in_transcript(
        self, 
        evidence_text: str, 
        context: TranscriptContext, 
        element_type: str, 
        element_key: str
    ) -> Optional[EvidencePoint]:
        """
        Find evidence text in transcript and determine positioning.
        """
        try:
            # Simple text search - would be enhanced with fuzzy matching
            evidence_text_clean = evidence_text.strip().lower()
            content_lower = context.content.lower()
            
            # Find the evidence in the transcript
            start_pos = content_lower.find(evidence_text_clean)
            if start_pos == -1:
                # Try partial matching for key phrases
                words = evidence_text_clean.split()
                if len(words) > 3:
                    # Try with first few words
                    partial_text = ' '.join(words[:3])
                    start_pos = content_lower.find(partial_text)
                    if start_pos != -1:
                        evidence_text_clean = partial_text
            
            if start_pos == -1:
                self.logger.debug(f"Evidence text not found in transcript: {evidence_text[:50]}...")
                return None
            
            end_pos = start_pos + len(evidence_text_clean)
            
            # Find associated speaker and timestamp
            speaker, timestamp = self._find_speaker_context(start_pos, context)
            
            return EvidencePoint(
                element_type=element_type,
                element_key=element_key,
                evidence_text=evidence_text,
                start_position=start_pos,
                end_position=end_pos,
                speaker=speaker,
                timestamp=timestamp,
                confidence=0.8,  # Would calculate based on matching accuracy
                extraction_type="explicit"
            )
        
        except Exception as e:
            self.logger.error(f"Error finding evidence in transcript: {e}")
            return None
    
    def _find_speaker_context(
        self, 
        position: int, 
        context: TranscriptContext
    ) -> Tuple[Optional[str], Optional[str]]:
        """Find speaker and timestamp for a given position in transcript."""
        for segment in context.segments:
            if (segment['start_position'] <= position <= segment['end_position']):
                return segment.get('speaker'), segment.get('timestamp')
        return None, None
    
    async def _store_evidence_batch(
        self, 
        evidence_points: List[EvidencePoint], 
        context: TranscriptContext
    ) -> None:
        """Store evidence points in database using batch operations."""
        try:
            with db_manager.get_session() as session:
                evidence_records = []
                
                for evidence_point in evidence_points:
                    # Calculate context before/after
                    context_before, context_after = self._extract_context(
                        evidence_point.start_position, 
                        evidence_point.end_position,
                        context.content
                    )
                    
                    evidence_record = IntelligenceEvidence(
                        analysis_id=context.analysis_id,
                        element_type=evidence_point.element_type,
                        element_key=evidence_point.element_key,
                        evidence_text=evidence_point.evidence_text,
                        transcript_id=context.transcript_id,
                        start_position=evidence_point.start_position,
                        end_position=evidence_point.end_position,
                        speaker=evidence_point.speaker,
                        timestamp=evidence_point.timestamp,
                        context_before=context_before,
                        context_after=context_after,
                        confidence=evidence_point.confidence,
                        extraction_type=evidence_point.extraction_type
                    )
                    evidence_records.append(evidence_record)
                
                # Bulk insert
                session.add_all(evidence_records)
                session.commit()
                
                self.logger.info(f"Stored {len(evidence_records)} evidence records")
        
        except Exception as e:
            self.logger.error(f"Error storing evidence batch: {e}")
            raise
    
    def _extract_context(
        self, 
        start_pos: int, 
        end_pos: int, 
        content: str, 
        context_chars: int = 150
    ) -> Tuple[str, str]:
        """Extract context before and after evidence position."""
        context_start = max(0, start_pos - context_chars)
        context_end = min(len(content), end_pos + context_chars)
        
        context_before = content[context_start:start_pos].strip()
        context_after = content[end_pos:context_end].strip()
        
        return context_before, context_after


# Global evidence service instance
evidence_service = EvidenceService()