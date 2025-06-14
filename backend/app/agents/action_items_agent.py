import logging
from typing import Dict, List, Any
from anthropic import AsyncAnthropic
import json
from datetime import datetime
import anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ActionItemsAgent:
    """
    Agent for extracting action items from sales meeting transcripts using Claude API.
    Cost-optimized version using Claude Haiku model for efficient processing.
    
    Attributes:
        client (AsyncAnthropic): Anthropic API client
        model (str): Claude model to use for analysis
    """
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize the ActionItemsAgent.
        
        Args:
            api_key (str): Anthropic API key
            model (str): Claude model to use for analysis
        """
        try:
            logger.info(f"Initializing ActionItemsAgent with model: {model}")
            self.client = AsyncAnthropic(api_key=api_key)
            self.model = model
            logger.info("ActionItemsAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ActionItemsAgent: {str(e)}")
            raise
        
    async def extract_action_items(self, transcript_text: str) -> Dict[str, Any]:
        """
        Extract action items from a sales meeting transcript.
        
        Args:
            transcript_text (str): The meeting transcript text to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing action items with their details
            
        Raises:
            anthropic.APIError: If there's an error with the Anthropic API
            ValueError: If the transcript is empty or invalid
        """
        if not transcript_text or not isinstance(transcript_text, str):
            logger.error("Invalid transcript text provided")
            raise ValueError("Transcript text must be a non-empty string")
            
        try:
            logger.info("Starting action items extraction")
            # Construct the prompt for Claude
            prompt = f"""Extract action items from this sales meeting transcript.
            For each item, identify:
            - Task description
            - Owner (if mentioned)
            - Deadline (if mentioned)
            - Priority (High/Medium/Low based on urgency)
            - Context/reason
            - Confidence score (0-1)
            
            Return JSON with this structure:
            {{
                "action_items": [
                    {{
                        "task": "Action to be taken",
                        "owner": "Person responsible",
                        "deadline": "When due",
                        "priority": "High/Medium/Low",
                        "context": "Why important",
                        "confidence": 0.0
                    }}
                ]
            }}

            Transcript:
            {transcript_text}
            """
            
            logger.info("Making API call to Claude")
            # Make API call to Claude
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=2000,  # Reduced for Haiku's efficiency
                temperature=0.1,  # Low temperature for consistent results
                system="""Extract action items from sales meeting transcripts. Look for commitments, follow-ups, and next steps.
                For confidence scores:
                - 0.9-1.0: Clear commitments with all details
                - 0.7-0.8: Clear task, some details missing
                - 0.5-0.6: Implied tasks
                - 0.3-0.4: Unclear tasks
                - 0.0-0.2: Very uncertain""",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the response
            try:
                logger.info("Parsing Claude's response")
                response_text = message.content[0].text

                # Extract JSON from response (handle extra text)
                try:
                    # Try parsing as-is first
                    action_items_data = json.loads(response_text)
                except json.JSONDecodeError:
                    # If that fails, extract JSON from the response
                    start = response_text.find('{')
                    end = response_text.rfind('}') + 1
                    if start != -1 and end != 0:
                        json_text = response_text[start:end]
                        action_items_data = json.loads(json_text)
                    else:
                        raise ValueError("No valid JSON found in response")
                
                # Add timestamp to the response
                action_items_data["analysis_timestamp"] = datetime.utcnow().isoformat()
                
                logger.info(f"Successfully extracted {len(action_items_data['action_items'])} action items from transcript")
                return action_items_data
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Claude's response as JSON: {str(e)}")
                logger.error(f"Raw response: {response_text}")
                raise ValueError("Invalid response format from Claude API")
                
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during action items extraction: {str(e)}")
            raise 