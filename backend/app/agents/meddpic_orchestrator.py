"""
✅ Applied: MEDDPICC_ORCHESTRATOR_PATTERN
MEDDPICC Orchestrator - Central Intelligence Coordinator for ASMIS

This module serves as the meta-coordinator for the multi-agent sales intelligence
system, orchestrating specialized agents to provide comprehensive MEDDPICC analysis
from various content sources using Template Imprinting Protocol.

PATTERN_REF: MEDDPICC_ORCHESTRATOR_PATTERN
DECISION_REF: TIP_MEDDPICC_CONVERSION_001
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import traceback
from anthropic import AsyncAnthropic, APIError
from anthropic.types import Message
import json

from .meeting_intelligence_agent import MeetingIntelligenceAgent
from .document_intelligence_agent import DocumentIntelligenceAgent
from .action_items_agent import ActionItemsAgent
from .stakeholder_intelligence_agent import StakeholderIntelligenceAgent

# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL imports
from ..database.repository import imprinting_template_repo, db_manager
from ..database.models import ImprintingTemplate

# PATTERN_REF: MEDDPICC_COMPLETENESS_SCORING_PATTERN imports
from ..intelligence.meddpicc_scoring import MEDDPICCScoring

# Evidence Service imports
from ..services.evidence_service import evidence_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SourceType(Enum):
    """Supported content source types for intelligence analysis."""
    # Meeting-related sources
    TRANSCRIPT = "transcript"
    MEETING_NOTES = "meeting_notes"
    CALL_RECORDING = "call_recording"
    
    # Document-related sources
    RFP = "rfp"
    REQUIREMENTS_DOC = "requirements_doc"
    PROPOSAL = "proposal"
    SOW = "sow"


class ProcessingStatus(Enum):
    """Status of intelligence processing."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL_SUCCESS = "partial_success"


@dataclass
class AnalysisContext:
    """Container for analysis context information."""
    content: str
    source_type: SourceType
    source_id: str
    deal_context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: str = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


# PATTERN_REF: MEDDPICC_ORCHESTRATOR_PATTERN
class MEDDPICCOrchestrator:
    """
    Central intelligence coordinator for ASMIS multi-agent system.
    ✅ Applied: MEDDPICC_ORCHESTRATOR_PATTERN
    
    Orchestrates specialized agents to provide comprehensive sales intelligence
    from meeting transcripts, documents, and other sources using Template Imprinting Protocol.
    Designed to evolve from simple routing to sophisticated cross-source synthesis and strategic
    recommendations with neural-first behavioral enforcement.
    
    Attributes:
        meeting_agent (MeetingIntelligenceAgent): Agent for analyzing meeting content
        document_agent (DocumentIntelligenceAgent): Agent for analyzing formal documents
        action_items_agent (ActionItemsAgent): Agent for extracting action items
        stakeholder_agent (StakeholderIntelligenceAgent): Agent for stakeholder analysis
        imprinting_template (Optional[ImprintingTemplate]): Active template for behavioral control
        synthesis_agent (Optional[Any]): Future agent for cross-source MEDDPICC synthesis
        campaign_agent (Optional[Any]): Future agent for campaign trigger detection
        pattern_agent (Optional[Any]): Future agent for pattern recognition
    
    DECISION_REF: TIP_MEDDPICC_CONVERSION_001 - Converted to Template Imprinting Protocol
    """
    
    # Source type categorization
    MEETING_SOURCES = {SourceType.TRANSCRIPT, SourceType.MEETING_NOTES, SourceType.CALL_RECORDING}
    DOCUMENT_SOURCES = {SourceType.RFP, SourceType.REQUIREMENTS_DOC, SourceType.PROPOSAL, SourceType.SOW}
    
    # Default configuration
    DEFAULT_CONFIG = {
        "enable_caching": True,
        "cache_ttl_minutes": 30,
        "enable_metrics": True,
        "confidence_threshold": 0.7,
        "parallel_processing": True,
        "max_retries": 3,
        "timeout_seconds": 60,
        "extract_action_items": True,
        "extract_stakeholder_intelligence": True
    }
    
    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MEDDPICC Orchestrator with Template Imprinting Protocol.
        ✅ Applied: MEDDPICC_ORCHESTRATOR_PATTERN
        
        Args:
            api_key: API key for AI services
            config: Optional configuration overrides
        """
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API key must be a non-empty string")
            
        self.api_key = api_key
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        
        # PATTERN_REF: MEDDPICC_ORCHESTRATOR_PATTERN - Initialize template system
        self.imprinting_template: Optional[ImprintingTemplate] = None
        self.template_loaded = False
        
        # Initialize agents
        self._initialize_agents()
        
        # Initialize scoring engine
        self.scoring_engine = MEDDPICCScoring()
        
        # Initialize caching if enabled
        self._cache = {} if self.config["enable_caching"] else None
        
        # Initialize metrics tracking if enabled
        self.metrics = {
            "total_analyses": 0,
            "successful_analyses": 0,
            "failed_analyses": 0,
            "average_processing_time": 0.0,
            "cache_hits": 0,
            "cache_misses": 0,
            "action_items_extracted": 0,
            "template_adherence_score": 0.0  # PATTERN_REF: Template adherence tracking
        } if self.config["enable_metrics"] else None
        
        logger.info("MEDDPICCOrchestrator initialized successfully with Template Imprinting Protocol")
        # DECISION_REF: TIP_MEDDPICC_CONVERSION_001
    
    def _initialize_agents(self):
        """Initialize extraction and intelligence agents."""
        try:
            self.meeting_agent = MeetingIntelligenceAgent(self.api_key)
            self.document_agent = DocumentIntelligenceAgent(self.api_key)
            self.action_items_agent = ActionItemsAgent(self.api_key)
            self.stakeholder_agent = StakeholderIntelligenceAgent(self.api_key)
            
            # Future agents - initialize as None for now
            self.synthesis_agent = None
            self.campaign_agent = None
            self.pattern_agent = None
            
            logger.info("Agents initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agents: {str(e)}")
            # Initialize as None for graceful degradation
            self.meeting_agent = None
            self.document_agent = None
            self.action_items_agent = None
    
    async def analyze_content(
        self,
        content: str,
        source_type: str,
        source_id: str,
        deal_context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Orchestrate comprehensive intelligence analysis of content.
        
        Args:
            content: The content to analyze
            source_type: Type of content source (e.g., "transcript", "rfp")
            source_id: Unique identifier for the content source
            deal_context: Optional context about the deal/opportunity
            metadata: Additional metadata about the content
            
        Returns:
            Dict containing comprehensive intelligence analysis
        """
        start_time = datetime.utcnow()
        
        try:
            # Validate inputs
            self._validate_inputs(content, source_type, source_id)
            source_type_enum = SourceType(source_type.lower())
            
            # Create analysis context
            context = AnalysisContext(
                content=content,
                source_type=source_type_enum,
                source_id=source_id,
                deal_context=deal_context,
                metadata=metadata
            )
            
            # Check cache if enabled
            if self._cache is not None:
                cached_result = self._get_cached_result(source_id)
                if cached_result:
                    self._update_metrics(success=True, start_time=start_time, cache_hit=True)
                    logger.info(f"Returning cached result for {source_id}")
                    return cached_result
            
            # Perform extraction
            extraction_result = await self._extract_intelligence(context)
            
            # Generate strategic recommendations
            recommendations = self._generate_recommendations(extraction_result)
            
            # Calculate MEDDPICC completeness score
            meddpicc_data = extraction_result.get("meddpic_analysis", {})
            completeness_score = self.scoring_engine.calculate_completeness_score(meddpicc_data)
            
            # Build final result
            result = self._build_result(
                extraction_result=extraction_result,
                recommendations=recommendations,
                completeness_score=completeness_score,
                context=context,
                start_time=start_time
            )
            
            # Cache result if enabled
            if self._cache is not None:
                self._cache_result(source_id, result)
            
            # Update metrics
            self._update_metrics(success=True, start_time=start_time)
            
            # Async evidence processing (fire and forget)
            if source_type_enum == SourceType.TRANSCRIPT:
                asyncio.create_task(
                    self._process_evidence_async(
                        result, content, source_id, context
                    )
                )
            
            logger.info(f"Successfully completed analysis for {source_id}")
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed for {source_id}: {str(e)}")
            logger.debug(traceback.format_exc())
            
            self._update_metrics(success=False, start_time=start_time)
            
            # Return error response
            return self._build_error_response(e, source_type, source_id, start_time)
    
    def _validate_inputs(self, content: str, source_type: str, source_id: str):
        """Validate input parameters."""
        if not content or not isinstance(content, str):
            raise ValueError("Content must be a non-empty string")
        if not source_type or not isinstance(source_type, str):
            raise ValueError("Source type must be a non-empty string")
        if not source_id or not isinstance(source_id, str):
            raise ValueError("Source ID must be a non-empty string")
        
        try:
            SourceType(source_type.lower())
        except ValueError:
            supported = [st.value for st in SourceType]
            raise ValueError(f"Unsupported source type '{source_type}'. Supported: {supported}")
    
    def _get_cached_result(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Get cached result if available and not expired."""
        if source_id not in self._cache:
            return None
            
        cached_entry = self._cache[source_id]
        age_minutes = (datetime.utcnow() - cached_entry["timestamp"]).total_seconds() / 60
        
        if age_minutes < self.config["cache_ttl_minutes"]:
            return cached_entry["result"]
        
        # Remove expired entry
        del self._cache[source_id]
        return None
    
    def _cache_result(self, source_id: str, result: Dict[str, Any]):
        """Cache analysis result."""
        self._cache[source_id] = {
            "result": result,
            "timestamp": datetime.utcnow()
        }
    
    def _preprocess_content(self, content: str) -> str:
        """Preprocess content to reduce API payload size while preserving key information."""
        if len(content) <= 1000:  # Skip preprocessing for short content
            return content
            
        # Remove excessive whitespace
        content = ' '.join(content.split())
        
        # Remove common filler words in transcripts
        filler_words = [
            'um', 'uh', 'ah', 'like', 'you know', 'kind of', 'sort of',
            'I mean', 'basically', 'actually', 'literally', 'honestly',
            'obviously', 'clearly', 'definitely', 'absolutely'
        ]
        
        for filler in filler_words:
            content = content.replace(f' {filler} ', ' ')
            content = content.replace(f' {filler.capitalize()} ', ' ')
        
        # Remove timestamp patterns (e.g., [00:12:34] or 12:34)
        import re
        content = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', content)
        content = re.sub(r'\b\d{1,2}:\d{2}\b', '', content)
        
        # Clean up extra spaces
        content = ' '.join(content.split())
        
        return content

    async def _extract_intelligence(self, context: AnalysisContext) -> Dict[str, Any]:
        """Extract intelligence using appropriate agent."""
        results = {}
        tasks = []
        
        # Add timing for debugging parallel execution
        parallel_start = datetime.utcnow()
        logger.info(f"Starting parallel extraction for {context.source_id}")
        
        # Preprocess content to reduce API payload
        processed_content = self._preprocess_content(context.content)
        if len(processed_content) != len(context.content):
            logger.info(f"Content preprocessed: {len(context.content)} -> {len(processed_content)} characters")

        # Determine MEDDPICC task
        meddpic_task = None
        if context.source_type in self.MEETING_SOURCES:
            if not self.meeting_agent:
                raise RuntimeError("Meeting agent not available")
            meddpic_task = self.meeting_agent.extract_meddpic_from_transcript(
                transcript=processed_content,
                meeting_id=context.source_id
            )
        elif context.source_type in self.DOCUMENT_SOURCES:
            if not self.document_agent:
                raise RuntimeError("Document agent not available")
            meddpic_task = self.document_agent.extract_meddpic_from_document(
                document_content=processed_content,
                document_id=context.source_id,
                document_type=context.source_type.value
            )
        else:
            raise ValueError(f"No agent available for source type: {context.source_type.value}")

        tasks.append(("meddpic", meddpic_task))

        # Determine Action Items task (if enabled) and wrap it for safe execution
        action_items_task_exists = False
        if self.config["extract_action_items"] and self.action_items_agent:
            action_items_task_exists = True
            async def safe_action_items_extraction():
                try:
                    task_start = datetime.utcnow()
                    result = await self.action_items_agent.extract_action_items(processed_content)
                    task_time = (datetime.utcnow() - task_start).total_seconds()
                    logger.info(f"Action items extraction took {task_time:.2f}s")
                    return result
                except Exception as e:
                    logger.error(f"Failed to extract action items: {str(e)}")
                    return {"error": str(e), "status": "failed"}
            tasks.append(("action_items", safe_action_items_extraction()))
        
        # Determine Stakeholder Intelligence task (if enabled and is meeting source)
        stakeholder_intelligence_task_exists = False
        if (self.config.get("extract_stakeholder_intelligence", True) and
            context.source_type in self.MEETING_SOURCES and
            self.stakeholder_agent):
            stakeholder_intelligence_task_exists = True
            async def safe_stakeholder_intelligence_extraction():
                try:
                    task_start = datetime.utcnow()
                    result = await self.stakeholder_agent.extract_comprehensive_stakeholder_intelligence(processed_content)
                    task_time = (datetime.utcnow() - task_start).total_seconds()
                    logger.info(f"Stakeholder intelligence extraction took {task_time:.2f}s")
                    return result
                except Exception as e:
                    logger.error(f"Failed to extract stakeholder intelligence: {str(e)}")
                    return {"error": str(e), "status": "failed"}
            tasks.append(("stakeholder", safe_stakeholder_intelligence_extraction()))
        
        # Run tasks in parallel with timing
        logger.info(f"Running {len(tasks)} tasks in parallel")
        try:
            results_list = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
            parallel_time = (datetime.utcnow() - parallel_start).total_seconds()
            logger.info(f"Parallel execution completed in {parallel_time:.2f}s")
        except Exception as e:
            # This catches exceptions from asyncio.gather itself, not the tasks within
            logger.error(f"An unexpected error occurred during parallel extraction: {str(e)}")
            raise

        # Process results by matching with task names
        task_names = [task[0] for task in tasks]
        for i, (task_name, result) in enumerate(zip(task_names, results_list)):
            if isinstance(result, Exception):
                if task_name == "meddpic":
                    # If MEDDPICC extraction failed, re-raise it as it's a critical component
                    raise result
                else:
                    results[f"{task_name}_error"] = str(result)
            else:
                if task_name == "meddpic":
                    results["meddpic_analysis"] = result
                elif task_name == "action_items":
                    if isinstance(result, dict) and result.get("status") == "failed":
                        results["action_items_error"] = result["error"]
                    else:
                        results["action_items"] = result
                        if self.metrics:
                            self.metrics["action_items_extracted"] += len(result.get("action_items", []))
                elif task_name == "stakeholder":
                    if isinstance(result, dict) and result.get("status") == "failed":
                        results["stakeholder_intelligence_error"] = result["error"]
                    else:
                        results["stakeholder_intelligence"] = result

        return results
    
    def _generate_recommendations(self, extraction_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategic recommendations based on extraction results."""
        recommendations = []
        
        # Analyze MEDDPICC components for gaps
        for component in ["metrics", "economic_buyer", "decision_criteria", "decision_process", "paper_process", "implicate_pain", "champion", "competition"]:
            if component in extraction_result:
                confidence = extraction_result[component].get("confidence", 0)
                if confidence < self.config["confidence_threshold"]:
                    recommendations.append({
                        "type": "action",
                        "priority": "high" if component in ["economic_buyer", "champion"] else "medium",
                        "component": component,
                        "title": f"Strengthen {component.replace('_', ' ').title()}",
                        "description": f"Low confidence ({confidence:.2f}) in {component}. Further discovery needed.",
                        "suggested_actions": self._get_component_actions(component)
                    })
        
        return recommendations
    
    def _get_component_actions(self, component: str) -> List[str]:
        """Get suggested actions for a MEDDPICC component."""
        actions_map = {
            "metrics": [
                "Schedule metrics definition session",
                "Document current state baseline",
                "Define success criteria with stakeholder"
            ],
            "economic_buyer": [
                "Map organizational structure",
                "Request introduction to budget holder",
                "Prepare executive briefing"
            ],
            "decision_criteria": [
                "Conduct requirements workshop",
                "Create evaluation scorecard",
                "Document must-have vs nice-to-have features"
            ],
            "champion": [
                "Identify potential champions",
                "Build champion enablement plan",
                "Schedule 1:1 with key influencers"
            ],
            "decision_process": [
                "Map complete decision-making process",
                "Identify all stakeholders involved",
                "Clarify timeline and milestones"
            ],
            "paper_process": [
                "Understand contracting requirements",
                "Map procurement/legal approval steps",
                "Identify compliance or security reviews needed"
            ],
            "implicate_pain": [
                "Dig deeper into underlying business issues",
                "Quantify business impact of problems",
                "Connect pain to broader strategic initiatives"
            ],
            "competition": [
                "Research competitive landscape",
                "Develop differentiation strategy",
                "Prepare competitive positioning materials"
            ]
        }
        return actions_map.get(component, ["Further discovery needed"])
    
    def _build_result(
        self,
        extraction_result: Dict[str, Any],
        recommendations: List[Dict[str, Any]],
        completeness_score: Any,
        context: AnalysisContext,
        start_time: datetime
    ) -> Dict[str, Any]:
        """Build standardized result format."""
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "status": ProcessingStatus.COMPLETED.value,
            "source_type": context.source_type.value,
            "source_id": context.source_id,
            "extraction_result": extraction_result,
            "strategic_recommendations": recommendations,
            "meddpicc_completeness": {
                "overall_score": completeness_score.overall_score,
                "qualification_status": completeness_score.qualification_status,
                "element_scores": {k: {
                    "score": v.total_score,
                    "weight": v.weight,
                    "gaps": v.gaps,
                    "recommendations": v.recommendations
                } for k, v in completeness_score.element_scores.items()},
                "critical_gaps": completeness_score.critical_gaps,
                "next_actions": completeness_score.next_actions,
                "meeting_objectives": completeness_score.meeting_objectives
            },
            "metadata": {
                "timestamp": context.timestamp,
                "processing_time_seconds": processing_time,
                "orchestrator_version": "2.0.0",
                "deal_context": context.deal_context,
                "confidence_threshold": self.config["confidence_threshold"]
            }
        }
    
    def _build_error_response(
        self,
        error: Exception,
        source_type: str,
        source_id: str,
        start_time: datetime
    ) -> Dict[str, Any]:
        """Build error response."""
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "status": ProcessingStatus.FAILED.value,
            "source_type": source_type,
            "source_id": source_id,
            "error": {
                "message": str(error),
                "type": type(error).__name__
            },
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "processing_time_seconds": processing_time,
                "orchestrator_version": "2.0.0"
            }
        }
    
    def _update_metrics(self, success: bool, start_time: datetime, cache_hit: bool = False):
        """Update performance metrics if enabled."""
        if not self.metrics:
            return
        
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        self.metrics["total_analyses"] += 1
        if success:
            self.metrics["successful_analyses"] += 1
        else:
            self.metrics["failed_analyses"] += 1
        
        if cache_hit:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
        
        # Update rolling average
        total = self.metrics["total_analyses"]
        current_avg = self.metrics["average_processing_time"]
        self.metrics["average_processing_time"] = ((current_avg * (total - 1)) + processing_time) / total
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on orchestrator and agents."""
        health_status = {
            "orchestrator": "healthy",
            "agents": {
                "meeting_agent": "healthy" if self.meeting_agent else "unavailable",
                "document_agent": "healthy" if self.document_agent else "unavailable",
                "action_items_agent": "healthy" if self.action_items_agent else "unavailable",
                "stakeholder_agent": "healthy" if self.stakeholder_agent else "unavailable",
                "synthesis_agent": "not_implemented",
                "campaign_agent": "not_implemented",
                "pattern_agent": "not_implemented"
            },
            "configuration": {
                "caching_enabled": self.config["enable_caching"],
                "metrics_enabled": self.config["enable_metrics"],
                "parallel_processing": self.config["parallel_processing"]
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if self.metrics:
            health_status["metrics"] = self.metrics.copy()
        
        return health_status
    
    def get_metrics(self) -> Optional[Dict[str, Any]]:
        """Get current performance metrics."""
        return self.metrics.copy() if self.metrics else None
    
    def clear_cache(self):
        """Clear the analysis cache."""
        if self._cache is not None:
            self._cache.clear()
            logger.info("Cache cleared")
    
    async def _process_evidence_async(
        self, 
        analysis_result: Dict[str, Any], 
        content: str, 
        source_id: str, 
        context: 'AnalysisContext'
    ) -> None:
        """
        Process evidence extraction asynchronously.
        
        Args:
            analysis_result: Complete analysis results
            content: Original transcript content
            source_id: Source identifier
            context: Analysis context
        """
        try:
            logger.info(f"Starting async evidence processing for {source_id}")
            
            # Extract MEDDPICC analysis from result
            meddpicc_analysis = analysis_result.get("meddpic_analysis", {})
            
            # Generate unique analysis ID for this session
            analysis_id = f"{source_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            # Process evidence through evidence service
            await evidence_service.process_analysis_evidence(
                analysis_result=meddpicc_analysis,
                transcript_content=content,
                transcript_id=source_id,  # Using source_id as transcript_id for now
                analysis_id=analysis_id
            )
            
            logger.info(f"Evidence processing completed for {source_id}")
            
        except Exception as e:
            logger.error(f"Error in async evidence processing for {source_id}: {e}")
            # Don't raise - this is background processing


# Example usage
if __name__ == "__main__":
    import os
    
    async def example_usage():
        # Initialize orchestrator
        api_key = os.getenv("ANTHROPIC_API_KEY", "your-api-key")
        orchestrator = MEDDPICCOrchestrator(
            api_key=api_key,
            config={
                "enable_caching": True,
                "enable_metrics": True,
                "cache_ttl_minutes": 60
            }
        )
        
        # Example: Analyze meeting transcript
        meeting_result = await orchestrator.analyze_content(
            content="""
            Sarah (CFO): We need to improve conversion rates by 30% before Q4.
            John (VP): I have $75K budget approved for this initiative.
            Mike: The solution must integrate with Salesforce.
            John: I'll champion this internally. Our main pain is cart abandonment.
            """,
            source_type="transcript",
            source_id="meeting_12345",
            deal_context={
                "account": "Acme Corp",
                "opportunity_value": 250000,
                "stage": "discovery"
            }
        )
        
        print(f"Analysis Status: {meeting_result['status']}")
        print(f"Recommendations: {len(meeting_result['strategic_recommendations'])}")
        
        # Check health
        health = await orchestrator.health_check()
        print(f"System Health: {health['orchestrator']}")
        
        # Get metrics
        metrics = orchestrator.get_metrics()
        if metrics:
            print(f"Total Analyses: {metrics['total_analyses']}")
            print(f"Cache Hit Rate: {metrics['cache_hits'] / max(metrics['total_analyses'], 1) * 100:.1f}%")
    
    # Run example
    # asyncio.run(example_usage()) 