"""
MEDDPIC analysis prompts for meeting transcripts.
"""
from typing import Dict, Any
from ..base import BasePrompt

class MEDDPICPrompt(BasePrompt):
    """Prompt template for MEDDPIC analysis of meeting transcripts."""
    
    def __init__(self, version: str = "1.0.0"):
        super().__init__(version)
        self.system_prompt = """You are a sales intelligence expert specializing in MEDDPIC analysis.
        Extract detailed MEDDPIC elements from sales meeting transcripts.
        Be precise, thorough, and always provide supporting evidence.
        For each element, assess confidence based on clarity and evidence strength.
        Format all dates and times in ISO format."""
        
        self.user_prompt_template = """Analyze this sales meeting transcript and extract comprehensive MEDDPIC elements.
        For each element, provide:
        1. The extracted information
        2. A confidence score (0-1)
        3. Supporting evidence from the transcript
        
        Return the analysis in JSON format with the following structure:
        {{
            "source_id": "{meeting_id}",
            "source_type": "transcript",
            "extracted_at": "{timestamp}",
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
    
    def format(self, meeting_id: str, transcript: str, timestamp: str) -> Dict[str, str]:
        """Format the prompt with the provided variables."""
        return {
            "system": self.system_prompt,
            "user": self.user_prompt_template.format(
                meeting_id=meeting_id,
                transcript=transcript,
                timestamp=timestamp
            )
        }
    
    def validate(self) -> bool:
        """Validate the prompt template."""
        required_vars = ["{meeting_id}", "{transcript}", "{timestamp}"]
        return all(var in self.user_prompt_template for var in required_vars)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert prompt to dictionary for storage."""
        data = super().to_dict()
        data.update({
            "system_prompt": self.system_prompt,
            "user_prompt_template": self.user_prompt_template
        })
        return data 