import logging
from typing import Dict, Any, List
from anthropic import AsyncAnthropic
from anthropic.types import Message
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MeetingIntelligenceAgent:
    """
    Agent for analyzing sales meeting transcripts using Claude API to extract MEDDPIC elements.
    
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
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
        
    async def extract_meddpic(self, transcript_text: str) -> Dict[str, Any]:
        """
        Extract MEDDPIC elements from a sales meeting transcript.
        
        Args:
            transcript_text (str): The meeting transcript text to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing MEDDPIC elements with confidence scores
            
        Raises:
            anthropic.APIError: If there's an error with the Anthropic API
            ValueError: If the transcript is empty or invalid
        """
        if not transcript_text or not isinstance(transcript_text, str):
            raise ValueError("Transcript text must be a non-empty string")
            
        try:
            # Construct the prompt for Claude
            prompt = f"""Analyze this sales meeting transcript and extract MEDDPIC elements. 
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
                system="You are a sales intelligence expert. Extract MEDDPIC elements from sales meeting transcripts. Be precise and thorough.",
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
                
                logger.info("Successfully extracted MEDDPIC elements from transcript")
                return meddpic_data
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Claude's response as JSON: {str(e)}")
                raise ValueError("Invalid response format from Claude API")
                
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during MEDDPIC extraction: {str(e)}")
            raise

    async def extract_meddpic_from_transcript(self, transcript: str, meeting_id: str) -> Dict[str, Any]:
        """
        Extract comprehensive MEDDPIC data from a sales meeting transcript with evidence and confidence scores.
        
        Args:
            transcript (str): The meeting transcript text to analyze
            meeting_id (str): Unique identifier for the meeting
            
        Returns:
            Dict[str, Any]: Dictionary containing detailed MEDDPIC analysis with evidence
            
        Raises:
            anthropic.APIError: If there's an error with the Anthropic API
            ValueError: If the transcript is empty or invalid
        """
        if not transcript or not isinstance(transcript, str):
            raise ValueError("Transcript text must be a non-empty string")
        if not meeting_id or not isinstance(meeting_id, str):
            raise ValueError("Meeting ID must be a non-empty string")
            
        try:
            # Construct the prompt for Claude
            prompt = f"""Analyze this sales meeting transcript and extract comprehensive MEDDPIC elements.
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
                "identified_pain": {{
                    "pain_points": ["pain points mentioned"],
                    "priority": ["high/medium/low for each pain"],
                    "confidence": 0.0,
                    "evidence": ["supporting quotes"]
                }},
                "champion": {{
                    "identified": "name if identified",
                    "strength": "none|developing|strong",
                    "confidence": 0.0,
                    "evidence": "supporting quote"
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
                system="""You are a sales intelligence expert specializing in MEDDPIC analysis.
                Extract detailed MEDDPIC elements from sales meeting transcripts.
                Be precise, thorough, and always provide supporting evidence.
                For each element, assess confidence based on clarity and evidence strength.
                Format all dates and times in ISO format.""",
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
                
                logger.info(f"Successfully extracted comprehensive MEDDPIC data for meeting {meeting_id}")
                return meddpic_data
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Claude's response as JSON: {str(e)}")
                raise ValueError("Invalid response format from Claude API")
                
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during MEDDPIC extraction: {str(e)}")
            raise 