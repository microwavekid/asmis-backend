import logging
from typing import Dict, Any, List, Tuple
from anthropic import AsyncAnthropic, APIError
import json
from datetime import datetime
import re

# Enhanced relationship mapping
from ..intelligence.stakeholder_relationship_mapping import enhance_stakeholder_relationships

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StakeholderIntelligenceAgent:
    """
    Agent for analyzing stakeholder information from sales meeting transcripts using Claude API.
    
    Attributes:
        client (AsyncAnthropic): Anthropic API client
        model (str): Claude model to use for analysis
    """
    
    # Constants for validation and truncation
    WARN_TRANSCRIPT_LENGTH = 50_000  # characters - warn but continue
    MAX_SAFE_LENGTH = 80_000  # characters - truncate beyond this
    MAX_TOKENS = 15_000  # estimated tokens
    WARN_TOKENS = 10_000  # estimated tokens
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize the StakeholderIntelligenceAgent.
        
        Args:
            api_key (str): Anthropic API key
            model (str): Claude model to use for analysis
        """
        try:
            self.client = AsyncAnthropic(api_key=api_key)
            self.model = model
            logger.info("Successfully initialized Anthropic client")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {str(e)}")
            raise
    
    def _preprocess_transcript(self, transcript: str) -> str:
        """
        Clean and normalize the transcript text.
        
        Args:
            transcript (str): Raw transcript text
            
        Returns:
            str: Cleaned transcript text
            
        Raises:
            ValueError: If transcript contains no meaningful content
        """
        try:
            # Normalize line endings
            cleaned = transcript.replace('\r\n', '\n').replace('\r', '\n')
            
            # Remove excessive whitespace
            cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)  # Multiple newlines
            cleaned = re.sub(r'[ \t]+', ' ', cleaned)  # Multiple spaces/tabs
            
            # Remove leading/trailing whitespace
            cleaned = cleaned.strip()
            
            # Validate content
            if not cleaned or cleaned.isspace():
                raise ValueError("Transcript contains no meaningful content")
            
            # Log preprocessing results
            original_length = len(transcript)
            cleaned_length = len(cleaned)
            if original_length != cleaned_length:
                logger.info(f"Preprocessed transcript: {original_length} -> {cleaned_length} characters")
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error preprocessing transcript: {str(e)}")
            raise
    
    def _intelligent_truncate(self, transcript: str, max_chars: int = None) -> str:
        """
        Intelligently truncate transcript to preserve stakeholder information.
        
        Strategy:
        1. Keep first 30% (meeting setup, introductions, stakeholder introductions)
        2. Keep last 30% (decisions, next steps, action items, key stakeholders)
        3. Sample middle 40% focusing on stakeholder and decision-making discussions
        
        Args:
            transcript (str): Full transcript text
            max_chars (int): Maximum characters to keep (defaults to MAX_SAFE_LENGTH)
            
        Returns:
            str: Intelligently truncated transcript
        """
        if max_chars is None:
            max_chars = self.MAX_SAFE_LENGTH
            
        if len(transcript) <= max_chars:
            return transcript
            
        try:
            # Split into paragraphs/sections (preserve structure)
            sections = transcript.split('\n\n')
            total_sections = len(sections)
            
            if total_sections <= 3:
                # Very few sections, just truncate from middle
                return transcript[:max_chars]
            
            # Calculate section allocations
            opening_sections = max(1, int(total_sections * 0.30))
            closing_sections = max(1, int(total_sections * 0.30))
            middle_sections = total_sections - opening_sections - closing_sections
            
            # Always keep opening and closing
            kept_sections = sections[:opening_sections] + sections[-closing_sections:]
            
            # Add middle sections that contain stakeholder-relevant keywords
            stakeholder_keywords = [
                'CEO', 'CTO', 'CFO', 'SVP', 'COO', 'VP', 'director', 'manager', 'head of',
                'Lead', 'Executive', 'Managing Director', 'General Manager', 'Product Manager', 'Project Manager', 'Product Owner', 'Analyst', 'Data Scientist',
                'reports to', 'team lead', 'department', 'budget', 'decision',
                'approve', 'authority', 'sign off', 'champion', 'influencer',
                'buyer', 'procurement', 'legal', 'security', 'compliance'
            ]
            
            middle_start = opening_sections
            middle_end = total_sections - closing_sections
            middle_available = sections[middle_start:middle_end]
            
            # Score and select best middle sections
            scored_sections = []
            for i, section in enumerate(middle_available):
                score = 0
                section_lower = section.lower()
                
                # Score based on stakeholder-relevant content
                for keyword in stakeholder_keywords:
                    score += section_lower.count(keyword)
                
                # Bonus for sections with names (likely stakeholder mentions)
                names_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
                score += len(re.findall(names_pattern, section)) * 2
                
                scored_sections.append((score, i, section))
            
            # Sort by score and select top sections that fit in remaining space
            scored_sections.sort(reverse=True, key=lambda x: x[0])
            
            current_length = sum(len(s) for s in kept_sections) + len(kept_sections) * 2  # +2 for \n\n
            remaining_space = max_chars - current_length
            
            for score, idx, section in scored_sections:
                if len(section) + 2 <= remaining_space:  # +2 for \n\n
                    kept_sections.insert(-closing_sections, section)
                    remaining_space -= len(section) + 2
                
                if remaining_space < 100:  # Not much space left
                    break
            
            truncated = '\n\n'.join(kept_sections)
            
            # Final length check and truncate if still too long
            if len(truncated) > max_chars:
                truncated = truncated[:max_chars]
                # Try to end at a sentence boundary
                last_period = truncated.rfind('.')
                if last_period > max_chars * 0.9:  # If we're close to the end
                    truncated = truncated[:last_period + 1]
            
            logger.info(f"Intelligently truncated transcript: {len(transcript)} -> {len(truncated)} characters")
            logger.info(f"Preserved {opening_sections} opening + {closing_sections} closing + selected middle sections")
            
            return truncated
            
        except Exception as e:
            logger.error(f"Error during intelligent truncation: {str(e)}")
            # Fallback to simple truncation
            logger.info("Falling back to simple truncation")
            return transcript[:max_chars]
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in the text.
        Uses a rough approximation of 4 characters per token.
        
        Args:
            text (str): Text to estimate tokens for
            
        Returns:
            int: Estimated number of tokens
        """
        try:
            # Rough estimate: 4 characters per token
            estimated_tokens = len(text) // 4
            
            # Add buffer for prompt template
            estimated_tokens += 1000  # Approximate tokens for prompt template
            
            logger.info(f"Estimated tokens: {estimated_tokens}")
            return estimated_tokens
            
        except Exception as e:
            logger.error(f"Error estimating tokens: {str(e)}")
            raise
    
    def _validate_and_prepare_transcript(self, transcript: str) -> str:
        """
        Validate transcript length, apply intelligent truncation if needed.
        
        Args:
            transcript (str): Transcript text to validate and prepare
            
        Returns:
            str: Prepared transcript ready for analysis
        """
        try:
            # Check transcript length and warn if large
            transcript_length = len(transcript)
            logger.info(f"Transcript length: {transcript_length} characters")
            
            if transcript_length > self.WARN_TRANSCRIPT_LENGTH:
                logger.warning(f"Large transcript detected ({transcript_length} characters)")
            
            # Apply intelligent truncation if needed
            if transcript_length > self.MAX_SAFE_LENGTH:
                logger.info("Applying intelligent truncation to optimize analysis")
                transcript = self._intelligent_truncate(transcript)
            
            # Estimate and log tokens (but don't block processing)
            estimated_tokens = self._estimate_tokens(transcript)
            
            if estimated_tokens > self.WARN_TOKENS:
                logger.warning(f"High token count (estimated {estimated_tokens} tokens)")
                
        except Exception as e:
            logger.error(f"Error preparing transcript: {str(e)}")
            raise
            
        return transcript
    
    async def extract_comprehensive_stakeholder_intelligence(self, transcript: str) -> Dict[str, Any]:
        """
        Extract comprehensive stakeholder intelligence from a sales meeting transcript.
        
        Args:
            transcript (str): The meeting transcript text to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing stakeholder and relationship analysis with evidence and metadata
        
        Raises:
            APIError: If there's an error with the Anthropic API
            ValueError: If the transcript is empty or invalid
        """
        if not transcript or not isinstance(transcript, str):
            raise ValueError("Transcript text must be a non-empty string")
            
        import time
        start_time = time.time()
        try:
            # Preprocess, validate, and prepare transcript (with intelligent truncation if needed)
            cleaned_transcript = self._preprocess_transcript(transcript)
            prepared_transcript = self._validate_and_prepare_transcript(cleaned_transcript)
            
            # Construct the prompt for Claude
            prompt = f"""Analyze this sales meeting transcript and extract comprehensive stakeholder intelligence.
            For each stakeholder, provide:
            1. Name, title, department
            2. Role classification (economic_buyer|champion|influencer|technical_decision_maker|user|gatekeeper)
            3. Confidence score (0-1)
            4. Supporting evidence (quote)
            5. Whether this is a new stakeholder (is_new: true/false)
            6. Suggested position for visualization (x, y, confidence)
            
            For relationships, provide:
            - from_stakeholder (name)
            - to_stakeholder (name)
            - relationship_type (reports_to|influences|collaborates|supports)
            - strength (0-1)
            - confidence (0-1)
            - evidence (quote)
            - bidirectional (true/false)
            
            Return the analysis in JSON format with the following structure:
            {{
              "stakeholders": [
                {{
                  "name": "string",
                  "title": "string", 
                  "department": "string",
                  "role_classification": "economic_buyer|champion|influencer|technical_decision_maker|user|gatekeeper",
                  "confidence": 0.95,
                  "evidence": "Supporting quote from transcript",
                  "is_new": true,
                  "suggested_position": {{"x": 100, "y": 200, "confidence": 0.8}}
                }}
              ],
              "relationships": [
                {{
                  "from_stakeholder": "John Smith",
                  "to_stakeholder": "Sarah Chen", 
                  "relationship_type": "reports_to|influences|collaborates|supports",
                  "strength": 0.85,
                  "confidence": 0.9,
                  "evidence": "Supporting quote",
                  "bidirectional": false
                }}
              ],
              "analysis_metadata": {{
                "processing_time_seconds": 2.1,
                "total_stakeholders_identified": 4,
                "new_stakeholders": 2,
                "high_confidence_extractions": 6,
                "auto_apply_ready": 4,
                "review_queue_items": 2,
                "analysis_timestamp": "{datetime.utcnow().isoformat()}"
              }}
            }}

            For confidence scores:
            - 0.9-1.0: Clear, explicit information with strong evidence
            - 0.7-0.8: Clear information but some details missing
            - 0.5-0.6: Implied information with reasonable evidence
            - 0.3-0.4: Weak or indirect evidence
            - 0.0-0.2: Very uncertain or speculative

            Transcript:
            {prepared_transcript}
            """
            
            # Make API call to Claude
            try:
                message = await self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    temperature=0.1,  # Low temperature for more consistent results
                    system="""You are a stakeholder intelligence expert specializing in sales meeting analysis.\nExtract detailed stakeholder and relationship information from sales meeting transcripts.\nBe precise, thorough, and always provide supporting evidence.\nFor each stakeholder and relationship, assess confidence based on clarity and evidence strength.\nFocus on accuracy over completeness.""",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            except APIError as e:
                if "token limit" in str(e).lower():
                    logger.error("Unexpected token limit error despite truncation")
                    raise ValueError(
                        "Transcript processing failed due to size constraints. "
                        "Please try with a shorter transcript."
                    ) from e
                raise
            
            # Parse the response
            try:
                response_text = message.content[0].text
                result = json.loads(response_text)
                # Post-process metadata
                processing_time = round(time.time() - start_time, 2)
                if "analysis_metadata" not in result:
                    result["analysis_metadata"] = {}
                result["analysis_metadata"]["processing_time_seconds"] = processing_time
                if "analysis_timestamp" not in result["analysis_metadata"]:
                    result["analysis_metadata"]["analysis_timestamp"] = datetime.utcnow().isoformat()
                # Optionally count and fill other metadata fields if missing
                if "stakeholders" in result:
                    result["analysis_metadata"]["total_stakeholders_identified"] = len(result["stakeholders"])
                    result["analysis_metadata"]["new_stakeholders"] = sum(1 for s in result["stakeholders"] if s.get("is_new"))
                    result["analysis_metadata"]["high_confidence_extractions"] = sum(1 for s in result["stakeholders"] if s.get("confidence", 0) >= 0.85)
                    result["analysis_metadata"]["auto_apply_ready"] = sum(1 for s in result["stakeholders"] if s.get("confidence", 0) >= 0.85)
                    result["analysis_metadata"]["review_queue_items"] = sum(1 for s in result["stakeholders"] if 0.5 <= s.get("confidence", 0) < 0.85)
                # Enhance with relationship mapping
                enhanced_result = enhance_stakeholder_relationships(result, prepared_transcript)
                
                # Merge enhanced data back into result
                result['enhanced_stakeholder_analysis'] = enhanced_result
                result['relationship_mapping'] = {
                    'network_analysis': enhanced_result['network_analysis'],
                    'decision_pathways': enhanced_result['decision_pathways'],
                    'enhanced_relationships': enhanced_result['enhanced_relationships']
                }
                
                # Update metadata with enhancement info
                if 'analysis_metadata' not in result:
                    result['analysis_metadata'] = {}
                
                result['analysis_metadata']['relationship_mapping_applied'] = True
                result['analysis_metadata']['enhanced_stakeholders'] = len(enhanced_result['enhanced_stakeholders'])
                result['analysis_metadata']['decision_pathways'] = len(enhanced_result['decision_pathways'])
                result['analysis_metadata']['key_approvers'] = len(enhanced_result['network_analysis']['key_approvers'])
                result['analysis_metadata']['champion_candidates'] = len(enhanced_result['network_analysis']['champion_candidates'])
                
                logger.info(f"Successfully extracted comprehensive stakeholder intelligence with relationship mapping")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Claude's response as JSON: {str(e)}")
                raise ValueError("Invalid response format from Claude API")
                
        except APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during stakeholder intelligence extraction: {str(e)}")
            raise