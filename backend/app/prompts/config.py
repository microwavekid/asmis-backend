"""
Configuration settings for the prompt management system.
"""
from typing import Dict, Any
import os
from pathlib import Path

# Base directory for prompt storage
PROMPT_DIR = Path(__file__).parent

# Directory for prompt exports
EXPORT_DIR = PROMPT_DIR / "exports"

# Default prompt versions
DEFAULT_VERSIONS = {
    "meddpic": "1.0.0",
    "action_items": "1.0.0",
    "document_analysis": "1.0.0"
}

# Prompt validation settings
VALIDATION_SETTINGS = {
    "max_prompt_length": 4000,  # Maximum length of a prompt in characters
    "min_confidence_score": 0.0,
    "max_confidence_score": 1.0,
    "required_fields": {
        "meddpic": [
            "metrics",
            "economic_buyer",
            "decision_criteria",
            "decision_process",
            "identified_pain",
            "champion"
        ],
        "action_items": [
            "task",
            "owner",
            "deadline",
            "priority",
            "context",
            "confidence"
        ]
    }
}

# Performance tracking settings
PERFORMANCE_SETTINGS = {
    "metrics": [
        "response_time",
        "token_usage",
        "confidence_scores",
        "evidence_quality"
    ],
    "logging_level": "INFO"
}

def get_prompt_config() -> Dict[str, Any]:
    """Get the complete prompt configuration."""
    return {
        "prompt_dir": str(PROMPT_DIR),
        "export_dir": str(EXPORT_DIR),
        "default_versions": DEFAULT_VERSIONS,
        "validation": VALIDATION_SETTINGS,
        "performance": PERFORMANCE_SETTINGS
    }

def ensure_directories():
    """Ensure all required directories exist."""
    EXPORT_DIR.mkdir(parents=True, exist_ok=True) 