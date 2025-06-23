"""
✅ Applied: TEMPLATE_IMPRINTING_PROTOCOL
Template Loading Utility for ASMIS Agents

Provides centralized template loading and validation for Template Imprinting Protocol.

PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
DECISION_REF: TIP_MEDDPIC_CONVERSION_001
"""

import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

from ..database.repository import imprinting_template_repo, db_manager
from ..database.models import ImprintingTemplate

logger = logging.getLogger(__name__)


# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
class TemplateLoader:
    """
    Centralized template loading for Template Imprinting Protocol.
    ✅ Applied: TEMPLATE_IMPRINTING_PROTOCOL
    """
    
    @staticmethod
    async def load_template(agent_type: str) -> Optional[ImprintingTemplate]:
        """
        Load the best imprinting template for an agent type.
        
        Args:
            agent_type: Type of agent (e.g., 'meddpic_orchestrator')
            
        Returns:
            Best imprinting template or None if not found
            
        PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
        """
        try:
            async with db_manager.get_session() as session:
                template = imprinting_template_repo.get_best_template(session, agent_type)
                
                if template:
                    logger.info(f"Loaded imprinting template '{template.name}' for agent '{agent_type}'")
                    logger.info(f"Template adherence score: {template.adherence_score}")
                    return template
                else:
                    logger.warning(f"No imprinting template found for agent type '{agent_type}'")
                    return None
                    
        except Exception as e:
            logger.error(f"Error loading template for agent '{agent_type}': {e}")
            return None
    
    @staticmethod
    def validate_template_adherence(result: Dict[str, Any], template: ImprintingTemplate) -> float:
        """
        Calculate adherence score based on template requirements.
        
        Args:
            result: Agent processing result
            template: Imprinting template
            
        Returns:
            Adherence score (0.0 to 1.0)
            
        PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
        """
        try:
            # Get adherence scoring from template
            adherence_rules = template.template_structure.get("adherence_scoring", {})
            
            # Check for required components
            required_components = template.template_structure.get("validation_rules", {}).get("required_components", [])
            present_components = sum(1 for component in required_components if component in str(result))
            
            if required_components:
                component_score = present_components / len(required_components)
            else:
                component_score = 1.0
            
            # Check for forbidden patterns
            forbidden_patterns = template.template_structure.get("validation_rules", {}).get("forbidden_patterns", [])
            forbidden_found = sum(1 for pattern in forbidden_patterns if pattern in str(result))
            
            if forbidden_patterns:
                forbidden_penalty = forbidden_found / len(forbidden_patterns)
            else:
                forbidden_penalty = 0.0
            
            # Calculate final score
            final_score = max(0.0, component_score - forbidden_penalty)
            
            logger.debug(f"Template adherence calculation: components={component_score:.2f}, penalties={forbidden_penalty:.2f}, final={final_score:.2f}")
            
            return final_score
            
        except Exception as e:
            logger.error(f"Error calculating template adherence: {e}")
            return 0.5  # Default moderate score on error
    
    @staticmethod
    async def update_template_performance(template_id: str, adherence_score: float, success: bool):
        """
        Update template performance metrics.
        
        Args:
            template_id: Template ID
            adherence_score: Measured adherence score
            success: Whether the operation was successful
            
        PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
        """
        try:
            async with db_manager.get_session() as session:
                imprinting_template_repo.update_performance_metrics(
                    session, template_id, adherence_score, success
                )
                await session.commit()
                logger.debug(f"Updated performance metrics for template {template_id}")
                
        except Exception as e:
            logger.error(f"Error updating template performance: {e}")


# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
@asynccontextmanager
async def template_context(agent_type: str):
    """
    Context manager for template loading and cleanup.
    
    Args:
        agent_type: Type of agent
        
    Yields:
        Loaded template or None
        
    PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
    DECISION_REF: TIP_MEDDPIC_CONVERSION_001
    """
    template = None
    try:
        template = await TemplateLoader.load_template(agent_type)
        yield template
    except Exception as e:
        logger.error(f"Error in template context: {e}")
        yield None
    finally:
        if template:
            logger.debug(f"Template context cleanup for {agent_type}")


# Convenience functions for common agent types
async def load_orchestrator_template() -> Optional[ImprintingTemplate]:
    """Load template for MEDDPIC orchestrator."""
    return await TemplateLoader.load_template("meddpic_orchestrator")


async def load_agent_template(agent_type: str) -> Optional[ImprintingTemplate]:
    """Load template for specific agent type."""
    return await TemplateLoader.load_template(agent_type)


# DECISION_REF: TIP_MEDDPIC_CONVERSION_001 - Template loading system for neural-first agents