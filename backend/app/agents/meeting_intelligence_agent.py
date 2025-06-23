import logging
from typing import Dict, Any, List
from anthropic import AsyncAnthropic, APIError
from anthropic.types import Message
import json
from datetime import datetime
import warnings

# PATTERN_REF: AGENT_COMMUNICATION_PATTERN - Competition inference integration
from ..intelligence.competition_inference import CompetitionInferenceEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MeetingIntelligenceAgent:
    """
    Agent for analyzing sales meeting transcripts using Claude API to extract MEDDPICC elements.
    
    Attributes:
        client (anthropic.Anthropic): Anthropic API client
        model (str): Claude model to use for analysis
    """
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize the MeetingIntelligenceAgent.
        
        Args:
            api_key (str): Anthropic API key
            model (str): Claude model to use for analysis
        """
        try:
            self.client = AsyncAnthropic(api_key=api_key)
            self.model = model
            self.competition_engine = CompetitionInferenceEngine()
            logger.info("Successfully initialized Anthropic client and competition engine")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {str(e)}")
            raise
    
    def __del__(self):
        """Cleanup when the agent is destroyed."""
        try:
            if hasattr(self, 'client'):
                # Async client doesn't need explicit cleanup
                pass
        except Exception as e:
            logger.error(f"Error during client cleanup: {str(e)}")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        try:
            if hasattr(self, 'client'):
                # Async client doesn't need explicit cleanup
                pass
        except Exception as e:
            logger.error(f"Error during async context cleanup: {str(e)}")
    
    async def extract_meddpic(self, transcript_text: str) -> Dict[str, Any]:
        """
        DEPRECATED: This method is deprecated and will be removed in a future version.
        Please use extract_meddpic_from_transcript() instead, which provides more comprehensive
        analysis including evidence and better structured output.

        Extract MEDDPICC elements from a sales meeting transcript.
        
        Args:
            transcript_text (str): The meeting transcript text to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing MEDDPICC elements with confidence scores
            
        Raises:
            APIError: If there's an error with the Anthropic API
            ValueError: If the transcript is empty or invalid
        """
        warnings.warn(
            "extract_meddpic() is deprecated and will be removed in a future version. "
            "Please use extract_meddpic_from_transcript() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        if not transcript_text or not isinstance(transcript_text, str):
            raise ValueError("Transcript text must be a non-empty string")
            
        try:
            # Construct the prompt for Claude
            prompt = f"""Analyze this sales meeting transcript and extract MEDDPICC elements. 
            For each element, provide the extracted information and a confidence score (0-1).
            Return the analysis in JSON format with the following structure:
            {{
                "metrics": {{
                    "extracted": "List of KPIs, targets, and measurements mentioned",
                    "confidence": 0.0
                }},
                "economic_buyer": {{
                    "extracted": "Who controls the budget and makes the final decision",
                    "confidence": 0.0
                }},
                "decision_criteria": {{
                    "extracted": "What factors matter for their selection",
                    "confidence": 0.0
                }},
                "decision_process": {{
                    "extracted": "How they make decisions and timeline",
                    "confidence": 0.0
                }},
                "identified_pain": {{
                    "extracted": "Problems and challenges mentioned",
                    "confidence": 0.0
                }},
                "champion": {{
                    "extracted": "Who supports our solution",
                    "confidence": 0.0
                }}
            }}

            Transcript:
            {transcript_text}
            """
            
            # Make API call to Claude
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,  # Low temperature for more consistent results
                system="You are a sales intelligence expert. Extract MEDDPICC elements from sales meeting transcripts. Be precise and thorough.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the response
            try:
                response_text = message.content[0].text
                meddpic_data = json.loads(response_text)
                
                # Add timestamp to the response
                meddpic_data["analysis_timestamp"] = datetime.utcnow().isoformat()
                
                logger.info("Successfully extracted MEDDPICC elements from transcript")
                return meddpic_data
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Claude's response as JSON: {str(e)}")
                raise ValueError("Invalid response format from Claude API")
                
        except APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during MEDDPICC extraction: {str(e)}")
            raise

    async def extract_meddpic_from_transcript(self, transcript: str, meeting_id: str) -> Dict[str, Any]:
        """
        Extract comprehensive MEDDPICC data from a sales meeting transcript with evidence and confidence scores.
        
        Args:
            transcript (str): The meeting transcript text to analyze
            meeting_id (str): Unique identifier for the meeting
            
        Returns:
            Dict[str, Any]: Dictionary containing detailed MEDDPICC analysis with evidence
            
        Raises:
            APIError: If there's an error with the Anthropic API
            ValueError: If the transcript is empty or invalid
        """
        if not transcript or not isinstance(transcript, str):
            raise ValueError("Transcript text must be a non-empty string")
        if not meeting_id or not isinstance(meeting_id, str):
            raise ValueError("Meeting ID must be a non-empty string")
            
        try:
            # Construct the prompt for Claude
            prompt = f"""Analyze this sales meeting transcript and extract comprehensive MEDDPICC elements.
            For each element, provide:
            1. The extracted information
            2. A confidence score (0-1)
            3. Supporting evidence from the transcript
            
            Return the analysis in JSON format with the following structure:
            {{
                "source_id": "{meeting_id}",
                "source_type": "transcript",
                "extracted_at": "{datetime.utcnow().isoformat()}",
                "metrics": {{
                    "identified": ["specific metrics mentioned"],
                    "confidence": 0.0,
                    "evidence": ["supporting quotes from transcript"]
                }},
                "economic_buyer": {{
                    "identified": "name and role if mentioned",
                    "confidence": 0.0,
                    "evidence": "supporting quote"
                }},
                "decision_criteria": {{
                    "criteria": ["list of criteria mentioned"],
                    "confidence": 0.0,
                    "evidence": ["supporting quotes"]
                }},
                "decision_process": {{
                    "steps": ["process steps mentioned"],
                    "timeline": "timeline if mentioned",
                    "confidence": 0.0,
                    "evidence": ["supporting quotes"]
                }},
                "paper_process": {{
                    "steps": ["contracting/legal/procurement steps mentioned"],
                    "timeline": "procurement timeline if mentioned",
                    "requirements": ["legal or compliance requirements"],
                    "confidence": 0.0,
                    "evidence": ["supporting quotes"]
                }},
                "implicate_pain": {{
                    "underlying_issues": ["deeper business problems implied"],
                    "business_impact": ["impact on revenue, efficiency, growth"],
                    "urgency_signals": ["indicators of pain severity"],
                    "confidence": 0.0,
                    "evidence": ["supporting quotes"]
                }},
                "champion": {{
                    "identified": "name if identified",
                    "strength": "none|developing|strong",
                    "confidence": 0.0,
                    "evidence": "supporting quote"
                }},
                "competition": {{
                    "competitors": ["list of competitors mentioned or inferred"],
                    "explicit_mentions": ["competitors explicitly mentioned"],
                    "inferred_competitors": ["competitors inferred from context"],
                    "strengths": ["their competitive strengths"],
                    "weaknesses": ["their competitive weaknesses"],
                    "positioning": "how we compare",
                    "confidence": 0.0,
                    "evidence": ["supporting quotes and inference signals"]
                }}
            }}

            For confidence scores:
            - 0.9-1.0: Clear, explicit information with strong evidence
            - 0.7-0.8: Clear information but some details missing
            - 0.5-0.6: Implied information with reasonable evidence
            - 0.3-0.4: Weak or indirect evidence
            - 0.0-0.2: Very uncertain or speculative

            Transcript:
            {transcript}
            """
            
            # Make API call to Claude
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,  # Low temperature for more consistent results
                system="""You are a sales intelligence expert specializing in MEDDPICC analysis.
                Extract detailed MEDDPICC elements from sales meeting transcripts.
                Be precise, thorough, and always provide supporting evidence.
                For each element, assess confidence based on clarity and evidence strength.
                Format all dates and times in ISO format.
                
                For Competition analysis:
                - Identify explicitly mentioned competitors
                - Look for implicit competitive signals (features, integrations, budget ranges)
                - Assess competitive positioning and differentiation opportunities
                - Note both strengths and weaknesses of competitors""",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the response
            try:
                response_text = message.content[0].text
                meddpic_data = json.loads(response_text)
                
                # Enhance competition analysis with inference engine
                competition_analysis = self.competition_engine.analyze_competition(
                    transcript, 
                    context={"meeting_id": meeting_id, "timestamp": datetime.utcnow().isoformat()}
                )
                
                # Merge competition analysis with extracted data
                if "competition" in meddpic_data:
                    # Extract competition data from inference engine
                    inference_data = competition_analysis.get("competition", {})
                    
                    # Combine explicit mentions with inferred competitors
                    explicit_competitors = meddpic_data["competition"].get("competitors", [])
                    inferred_competitors = [comp.competitor_name for comp in inference_data.get("inferred_competitors", [])]
                    
                    meddpic_data["competition"].update({
                        "explicit_mentions": explicit_competitors,
                        "inferred_competitors": inferred_competitors,
                        "all_competitors": list(set(explicit_competitors + inferred_competitors)),
                        "relevant_solutions": inference_data.get("relevant_solutions", []),
                        "inference_signals": inference_data.get("competitive_signals", []),
                        "competitive_intelligence": inference_data.get("competitive_analysis", {}),
                        "threat_assessment": inference_data.get("threat_assessment", {})
                    })
                    
                    # Update confidence based on both explicit and implicit signals
                    if inferred_competitors:
                        current_confidence = meddpic_data["competition"].get("confidence", 0.0)
                        inference_confidence = inference_data.get("confidence_score", 0.0)
                        # Weighted average: explicit mentions get higher weight
                        combined_confidence = (current_confidence * 0.7) + (inference_confidence * 0.3)
                        meddpic_data["competition"]["confidence"] = min(1.0, combined_confidence)
                
                logger.info(f"Successfully extracted comprehensive MEDDPICC data with competition inference for meeting {meeting_id}")
                return meddpic_data
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Claude's response as JSON: {str(e)}")
                raise ValueError("Invalid response format from Claude API")
                
        except APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during MEDDPICC extraction: {str(e)}")
            raise 