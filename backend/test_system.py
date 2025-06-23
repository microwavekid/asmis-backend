import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from app.agents.meddpic_orchestrator import MEDDPICCOrchestrator
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file in the current directory
env_path = Path('.') / '.env'
logger.debug(f"Loading .env from: {env_path.absolute()}")
load_dotenv(dotenv_path=env_path)
logger.debug(f"Current working directory: {os.getcwd()}")
logger.debug(f"Environment variables loaded: {os.environ.get('ANTHROPIC_API_KEY') is not None}")

async def test_full_system():
    # Use your actual API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Please set ANTHROPIC_API_KEY environment variable")
        return
    
    logger.debug(f"API key loaded: {api_key[:8]}...{api_key[-4:]}")
    logger.debug(f"API key length: {len(api_key)}")
    logger.debug(f"API key contains newlines: {'\\n' in api_key}")
    logger.debug(f"API key contains spaces: {' ' in api_key}")
    logger.debug(f"API key starts with: {repr(api_key[:10])}")
    logger.debug(f"API key ends with: {repr(api_key[-10:])}")
    
    print("🔑 Using API key from environment variable")
    
    orchestrator = MEDDPICCOrchestrator(
        api_key=api_key,
        config={
            "enable_caching": True,
            "enable_metrics": True
        }
    )
    
    # Test 1: Health check
    print("1. Testing Health Check...")
    health = await orchestrator.health_check()
    print(f"   ✓ Orchestrator: {health['orchestrator']}")
    print(f"   ✓ Meeting Agent: {health['agents']['meeting_agent']}")
    print(f"   ✓ Document Agent: {health['agents']['document_agent']}")
    print(f"   ✓ Action Items Agent: {health['agents']['action_items_agent']}")
    print(f"   ✓ Stakeholder Agent: {health['agents']['stakeholder_agent']}")
    
    # Test 2: Meeting transcript
    print("\n2. Testing Meeting Analysis...")
    meeting_result = await orchestrator.analyze_content(
        content="""
        Sarah (CFO): We need to improve conversion rates by 30% before Q4.
        John (VP Sales): I have $75K budget approved for this initiative.
        Mike (CTO): The solution must integrate with Salesforce.
        John: I'll champion this internally. Our main pain is cart abandonment.
        """,
        source_type="transcript",
        source_id="meeting_001"
    )
    print(f"   ✓ Status: {meeting_result['status']}")
    print(f"   ✓ Processing Time: {meeting_result['metadata']['processing_time_seconds']:.2f}s")
    if "stakeholder_intelligence" in meeting_result.get("extraction_result", {}):
        stakeholder_info = meeting_result["extraction_result"]["stakeholder_intelligence"]
        if "stakeholders" in stakeholder_info:
            print(f"   ✓ Stakeholder Analysis: Found {len(stakeholder_info['stakeholders'])} stakeholders.")
        else:
            print("   ✗ Stakeholder Analysis: No stakeholders found in result.")
    else:
        print("   ✗ Stakeholder Analysis: Not run or failed.")
    
    # Test 3: Cache hit
    print("\n3. Testing Cache...")
    cached_result = await orchestrator.analyze_content(
        content="""
        Sarah (CFO): We need to improve conversion rates by 30% before Q4.
        John (VP Sales): I have $75K budget approved for this initiative.
        Mike (CTO): The solution must integrate with Salesforce.
        John: I'll champion this internally. Our main pain is cart abandonment.
        """,
        source_type="transcript",
        source_id="meeting_001"
    )
    
    # Test 4: Document analysis
    print("\n4. Testing Document Analysis...")
    doc_result = await orchestrator.analyze_content(
        content="""
        Request for Proposal
        Budget: $50,000 - $100,000
        Timeline: Q3 2024
        Requirements:
        1. Salesforce integration
        2. Real-time analytics
        Evaluation Criteria:
        - Technical capabilities (40%)
        - Cost (30%)
        - Support (30%)
        """,
        source_type="rfp",
        source_id="rfp_001"
    )
    print(f"   ✓ Status: {doc_result['status']}")
    
    # Test 5: Metrics
    print("\n5. Final Metrics:")
    metrics = orchestrator.get_metrics()
    print(f"   ✓ Total Analyses: {metrics['total_analyses']}")
    print(f"   ✓ Successful: {metrics['successful_analyses']}")
    print(f"   ✓ Cache Hits: {metrics['cache_hits']}")
    print(f"   ✓ Cache Hit Rate: {metrics['cache_hits'] / max(metrics['total_analyses'], 1) * 100:.1f}%")

if __name__ == "__main__":
    asyncio.run(test_full_system()) 

