import logging
from typing import Dict, Any, List
from anthropic import AsyncAnthropic
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DocumentIntelligenceAgent:
    """
    Agent for analyzing formal documents (RFPs, requirements docs, etc.) using Claude API to extract MEDDPIC elements.
    Specializes in structured document analysis vs conversational analysis.
    
    Attributes:
        client (AsyncAnthropic): Anthropic API client
        model (str): Claude model to use for analysis
    """
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize the DocumentIntelligenceAgent.
        
        Args:
            api_key (str): Anthropic API key
            model (str): Claude model to use for analysis
        """
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
        
    async def extract_meddpic_from_document(
        self, 
        document_content: str, 
        document_id: str, 
        document_type: str
    ) -> Dict[str, Any]:
        """
        Extract comprehensive MEDDPIC data from a formal document with evidence and confidence scores.
        
        Args:
            document_content (str): The document text to analyze
            document_id (str): Unique identifier for the document
            document_type (str): Type of document ("rfp" | "requirements_doc" | "proposal" | "sow")
            
        Returns:
            Dict[str, Any]: Dictionary containing detailed MEDDPIC analysis with evidence
            
        Raises:
            anthropic.APIError: If there's an error with the Anthropic API
            ValueError: If the document content is empty or invalid
        """
        if not document_content or not isinstance(document_content, str):
            raise ValueError("Document content must be a non-empty string")
        if not document_id or not isinstance(document_id, str):
            raise ValueError("Document ID must be a non-empty string")
        if document_type not in ["rfp", "requirements_doc", "proposal", "sow"]:
            raise ValueError("Document type must be one of: rfp, requirements_doc, proposal, sow")
            
        try:
            # Construct the prompt for Claude
            prompt = f"""Analyze this {document_type} document and extract comprehensive MEDDPIC elements.
            Focus on formal document structure, numbered requirements, and explicit criteria.
            
            For each element, provide:
            1. The extracted information
            2. A confidence score (0-1)
            3. Supporting evidence from the document
            
            Document Analysis Guidelines:
            - Look for formal requirements sections and numbered criteria
            - Extract specific technical specifications and metrics
            - Identify explicit budget and timeline information
            - Focus on written requirements rather than implied needs
            - Pay special attention to evaluation criteria sections
            
            Return the analysis in JSON format with the following structure:
            {{
                "source_id": "{document_id}",
                "source_type": "{document_type}",
                "extracted_at": "{datetime.utcnow().isoformat()}",
                "metrics": {{
                    "identified": ["specific metrics and KPIs mentioned"],
                    "confidence": 0.0,
                    "evidence": ["supporting quotes from document"]
                }},
                "economic_buyer": {{
                    "identified": "name and role if mentioned",
                    "confidence": 0.0,
                    "evidence": "supporting quote"
                }},
                "decision_criteria": {{
                    "criteria": ["list of formal criteria mentioned"],
                    "confidence": 0.0,
                    "evidence": ["supporting quotes"]
                }},
                "decision_process": {{
                    "steps": ["formal process steps mentioned"],
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
            - 0.9-1.0: Explicit, written requirements with clear specifications
            - 0.7-0.8: Clear requirements but some details missing
            - 0.5-0.6: Implied requirements with reasonable evidence
            - 0.3-0.4: Weak or indirect evidence
            - 0.0-0.2: Very uncertain or speculative

            Document Content:
            {document_content}
            """
            
            # Make API call to Claude
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,  # Low temperature for more consistent results
                system="""You are a document intelligence expert specializing in MEDDPIC analysis.
                Extract detailed MEDDPIC elements from formal documents like RFPs and requirements docs.
                Focus on structured content, numbered requirements, and explicit criteria.
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
                
                logger.info(f"Successfully extracted comprehensive MEDDPIC data from {document_type} document {document_id}")
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