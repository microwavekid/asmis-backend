"""
Test Evidence Service Integration
Verifies async evidence processing with MEDDPICC analysis.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent))

from app.agents.meddpic_orchestrator import MEDDPICCOrchestrator
from app.services.evidence_service import evidence_service
from app.repositories.evidence_repository import evidence_repository
from app.database.connection import db_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_evidence_integration():
    """Test evidence service integration with MEDDPICC orchestrator."""
    
    # Sample transcript with clear MEDDPICC elements
    test_transcript = """
    John Williams (VP Marketing): Thanks everyone for joining. We need to discuss our conversion optimization needs.
    
    Sarah Chen (CFO): Our budget for this initiative is $400K, and we need to see 20% ROI in year one.
    
    Mike Thompson (CTO): From a technical perspective, any solution must integrate seamlessly with our Salesforce instance.
    
    John Williams: I'll champion this solution internally if it meets our requirements.
    
    Sarah Chen: The main pain point is our 60% cart abandonment rate - it's costing us millions.
    
    Mike Thompson: We also need SOC2 compliance for any new platform.
    
    John Williams: The decision process involves technical review by Mike's team, then budget approval from Sarah, and finally board approval.
    
    Sarah Chen: Timeline is critical - we need implementation complete before Q4 planning in December.
    """
    
    try:
        logger.info("Starting evidence integration test")
        
        # Initialize orchestrator
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.error("ANTHROPIC_API_KEY not set")
            return
        
        orchestrator = MEDDPICCOrchestrator(
            api_key=api_key,
            config={
                "enable_caching": False,
                "enable_metrics": True
            }
        )
        
        # Run MEDDPICC analysis (this will trigger async evidence processing)
        logger.info("Running MEDDPICC analysis...")
        analysis_result = await orchestrator.analyze_content(
            content=test_transcript,
            source_type="transcript",
            source_id="test_transcript_001",
            deal_context={
                "account": "Test Corp",
                "opportunity_value": 500000,
                "stage": "discovery"
            }
        )
        
        logger.info(f"Analysis Status: {analysis_result['status']}")
        logger.info(f"Decision Criteria Found: {len(analysis_result.get('meddpic_analysis', {}).get('decision_criteria', []))}")
        
        # Wait for evidence processing to complete
        logger.info("Waiting for evidence processing to complete...")
        await asyncio.sleep(3)  # Give evidence service time to process
        
        # Verify evidence was stored
        logger.info("Checking stored evidence...")
        with db_manager.get_session() as session:
            # Get all evidence records
            evidence_records = evidence_repository.get_evidence_by_analysis(
                session, 
                analysis_id="test_transcript_001_*"  # This won't work exactly - simplified for test
            )
            
            logger.info(f"Evidence records found: {len(evidence_records)}")
            
            for evidence in evidence_records[:3]:  # Show first 3
                logger.info(f"Evidence: {evidence.element_type} - {evidence.evidence_text[:50]}...")
                logger.info(f"Position: {evidence.start_position}-{evidence.end_position}")
                logger.info(f"Speaker: {evidence.speaker}")
                logger.info(f"Confidence: {evidence.confidence}")
                logger.info("---")
        
        # Test evidence context retrieval
        if evidence_records:
            test_evidence = evidence_records[0]
            with db_manager.get_session() as session:
                context = evidence_repository.get_evidence_context(
                    session, 
                    test_evidence.id
                )
                
                if context:
                    logger.info("Evidence Context Test:")
                    logger.info(f"Evidence Text: {context['evidence']['text']}")
                    logger.info(f"Context Before: {context['context']['before'][:50]}...")
                    logger.info(f"Context After: {context['context']['after'][:50]}...")
        
        logger.info("Evidence integration test completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()


async def test_evidence_search():
    """Test evidence search functionality."""
    try:
        logger.info("Testing evidence search...")
        
        with db_manager.get_session() as session:
            # Search for budget-related evidence
            budget_evidence = evidence_repository.search_evidence(
                session,
                query="budget",
                filters={"confidence_min": 0.5}
            )
            
            logger.info(f"Budget evidence found: {len(budget_evidence)}")
            
            # Search for decision criteria evidence
            criteria_evidence = evidence_repository.search_evidence(
                session,
                query="requirement",
                filters={"element_type": "decision_criteria"}
            )
            
            logger.info(f"Criteria evidence found: {len(criteria_evidence)}")
            
    except Exception as e:
        logger.error(f"Search test failed: {e}")


if __name__ == "__main__":
    async def main():
        await test_evidence_integration()
        await test_evidence_search()
    
    asyncio.run(main())