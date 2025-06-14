import asyncio
import os
from app.agents.meeting_intelligence_agent import MeetingIntelligenceAgent

async def test_enhanced_meddpic():
    print("🧪 Testing Enhanced MEDDPIC Extraction...")
    
    # Initialize agent
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not found in environment")
        return
        
    agent = MeetingIntelligenceAgent(api_key)
    
    # Sample transcript
    sample_transcript = """
    Sarah Chen (CFO): We need to improve our conversion rates by at least 30% before Q4 ends. 
    John Williams (VP Marketing): I have budget approval for up to $75K for this initiative.
    Mike Thompson (CTO): The main criteria is it must integrate with our Salesforce instance.
    John: I'll be advocating for this solution internally. Our biggest pain point is cart abandonment.
    """
    
    try:
        print("📊 Running MEDDPIC analysis...")
        
        # Test the enhanced method
        result = await agent.extract_meddpic_from_transcript(
            transcript=sample_transcript,
            meeting_id="test_meeting_123"
        )
        
        print("✅ SUCCESS! Here's what was extracted:")
        print(f"📊 Metrics: {result['metrics']['identified']}")
        print(f"💰 Economic Buyer: {result['economic_buyer']['identified']}")
        print(f"🎯 Champion: {result['champion']['identified']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_meddpic())