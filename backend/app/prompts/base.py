"""
Base prompt management system for ASMIS agents.
"""
from typing import Dict, Any, Optional
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BasePrompt:
    """Base class for all prompt templates."""
    
    def __init__(self, version: str = "1.0.0"):
        self.version = version
        self.last_updated = datetime.utcnow().isoformat()
    
    def format(self, **kwargs) -> str:
        """Format the prompt template with provided variables."""
        raise NotImplementedError("Subclasses must implement format()")
    
    def validate(self) -> bool:
        """Validate the prompt template."""
        raise NotImplementedError("Subclasses must implement validate()")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert prompt to dictionary for storage."""
        return {
            "version": self.version,
            "last_updated": self.last_updated,
            "template": self.__class__.__name__
        }

class PromptManager:
    """Manages prompt templates and their versions."""
    
    def __init__(self):
        self.prompts: Dict[str, BasePrompt] = {}
    
    def register_prompt(self, name: str, prompt: BasePrompt) -> None:
        """Register a new prompt template."""
        self.prompts[name] = prompt
        logger.info(f"Registered prompt template: {name} (v{prompt.version})")
    
    def get_prompt(self, name: str) -> Optional[BasePrompt]:
        """Get a prompt template by name."""
        return self.prompts.get(name)
    
    def list_prompts(self) -> Dict[str, Dict[str, Any]]:
        """List all registered prompts and their metadata."""
        return {
            name: prompt.to_dict() 
            for name, prompt in self.prompts.items()
        }
    
    def export_prompts(self, filepath: str) -> None:
        """Export all prompts to a JSON file."""
        data = {
            name: prompt.to_dict()
            for name, prompt in self.prompts.items()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Exported prompts to: {filepath}")
    
    def import_prompts(self, filepath: str) -> None:
        """Import prompts from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        # Implementation would depend on how prompts are stored/loaded
        logger.info(f"Imported prompts from: {filepath}") 