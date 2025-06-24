"""
Basic Evidence Service Test
Tests evidence extraction and storage without requiring API keys.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent))

from app.services.evidence_service import evidence_service, EvidencePoint, TranscriptContext
from app.repositories.evidence_repository import evidence_repository
from app.database.connection import db_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_evidence_extraction():
    """Test evidence extraction without full orchestrator."""
    
    # Sample MEDDPICC analysis result (simulated)
    mock_analysis = {
        "decision_criteria": {
            "criteria": {
                "technical": [
                    {"criterion": "Salesforce integration", "priority": "high", "business_unit": "IT"},
                    {"criterion": "SOC2 compliance", "priority": "high", "business_unit": "Security"}
                ],
                "financial": [
                    {"criterion": "20% ROI in year one", "priority": "medium", "business_unit": "Finance"}
                ]
            }
        },
        "champion": {
            "name": "John Williams",
            "rationale": "VP Marketing who will champion internally"
        },
        "economic_buyer": {
            "name": "Sarah Chen",
            "rationale": "CFO with budget authority"
        }
    }
    
    # Sample transcript
    test_transcript = """
    John Williams (VP Marketing): Thanks everyone for joining. We need to discuss our conversion optimization needs.
    
    Sarah Chen (CFO): Our budget for this initiative is $400K, and we need to see 20% ROI in year one.
    
    Mike Thompson (CTO): From a technical perspective, any solution must integrate seamlessly with our Salesforce instance.
    
    John Williams: I'll champion this solution internally if it meets our requirements.
    
    Mike Thompson: We also need SOC2 compliance for any new platform.
    """
    
    try:
        logger.info("Testing evidence extraction...")
        
        # Initialize database (uses config from .env)
        db_manager.initialize()
        
        # Test evidence extraction
        transcript_context = await evidence_service._create_transcript_context(
            test_transcript,
            "test_transcript_001",
            "test_analysis_001"
        )
        
        logger.info(f"Transcript segments created: {len(transcript_context.segments)}")
        
        # Extract evidence from mock analysis
        evidence_points = evidence_service._extract_evidence_from_analysis(
            mock_analysis,
            transcript_context
        )
        
        logger.info(f"Evidence points extracted: {len(evidence_points)}")
        
        # Show evidence details
        for i, evidence in enumerate(evidence_points):
            logger.info(f"Evidence {i+1}:")
            logger.info(f"  Type: {evidence.element_type}")
            logger.info(f"  Text: {evidence.evidence_text}")
            logger.info(f"  Position: {evidence.start_position}-{evidence.end_position}")
            logger.info(f"  Speaker: {evidence.speaker}")
            logger.info(f"  Confidence: {evidence.confidence}")
            logger.info("---")
        
        # Test evidence storage
        if evidence_points:
            logger.info("Testing evidence storage...")
            await evidence_service._store_evidence_batch(evidence_points, transcript_context)
            logger.info("Evidence stored successfully!")
            
            # Verify storage
            with db_manager.get_session() as session:
                stored_evidence = evidence_repository.get_evidence_by_analysis(
                    session, 
                    "test_analysis_001"
                )
                logger.info(f"Stored evidence records: {len(stored_evidence)}")
                
                # Test evidence context retrieval
                if stored_evidence:
                    test_evidence = stored_evidence[0]
                    context = evidence_repository.get_evidence_context(
                        session, 
                        test_evidence.id
                    )
                    
                    if context:
                        logger.info("Evidence context retrieved successfully!")
                        logger.info(f"Evidence: {context['evidence']['text']}")
                        logger.info(f"Confidence: {context['evidence']['confidence']}")
        
        logger.info("Evidence service test completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()


async def test_evidence_positioning():
    """Test evidence positioning accuracy."""
    try:
        logger.info("Testing evidence positioning...")
        
        test_text = "Sarah Chen (CFO): We need 20% ROI in year one."
        search_phrase = "20% ROI"
        
        # Find position
        start_pos = test_text.lower().find(search_phrase.lower())
        end_pos = start_pos + len(search_phrase)
        
        logger.info(f"Text: {test_text}")
        logger.info(f"Search: {search_phrase}")
        logger.info(f"Found at position: {start_pos}-{end_pos}")
        logger.info(f"Extracted: '{test_text[start_pos:end_pos]}'")
        
        # Test context extraction
        context_before = test_text[max(0, start_pos-20):start_pos]
        context_after = test_text[end_pos:end_pos+20]
        
        logger.info(f"Context before: '{context_before}'")
        logger.info(f"Context after: '{context_after}'")
        
    except Exception as e:
        logger.error(f"Positioning test failed: {e}")


if __name__ == "__main__":
    async def main():
        await test_evidence_extraction()
        await test_evidence_positioning()
    
    asyncio.run(main())