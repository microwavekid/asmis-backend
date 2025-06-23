"""Repository pattern implementation for ASMIS database operations."""

import logging
from typing import List, Optional, Dict, Any, Generic, TypeVar, Type
from datetime import datetime, timedelta

from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .base import Base
from .connection import db_manager
from .models import PromptTemplate, PromptVersion, AgentConfiguration, ProcessingSession, ImprintingTemplate
from .models import User
from .imprinting import imprinting_validator, ImprintingValidationResult

logger = logging.getLogger(__name__)

# Generic type for model classes
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository class with common database operations."""
    
    def __init__(self, model: Type[ModelType]):
        """Initialize the repository with a model class.
        
        Args:
            model: The SQLAlchemy model class
        """
        self.model = model
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_by_id(self, session: Session, id: str) -> Optional[ModelType]:
        """Get a record by ID.
        
        Args:
            session: Database session
            id: Record ID
            
        Returns:
            Model instance or None if not found
        """
        try:
            return session.get(self.model, id)
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting {self.model.__name__} by ID {id}: {e}")
            raise
    
    def get_all(self, session: Session, limit: Optional[int] = None) -> List[ModelType]:
        """Get all records.
        
        Args:
            session: Database session
            limit: Optional limit on number of records
            
        Returns:
            List of model instances
        """
        try:
            query = select(self.model)
            if limit:
                query = query.limit(limit)
            result = session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting all {self.model.__name__}: {e}")
            raise
    
    def create(self, session: Session, **kwargs) -> ModelType:
        """Create a new record.
        
        Args:
            session: Database session
            **kwargs: Field values for the new record
            
        Returns:
            Created model instance
        """
        try:
            instance = self.model(**kwargs)
            session.add(instance)
            session.flush()  # Get the ID without committing
            return instance
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating {self.model.__name__}: {e}")
            raise
    
    def update(self, session: Session, id: str, **kwargs) -> Optional[ModelType]:
        """Update a record by ID.
        
        Args:
            session: Database session
            id: Record ID
            **kwargs: Field values to update
            
        Returns:
            Updated model instance or None if not found
        """
        try:
            instance = self.get_by_id(session, id)
            if instance:
                for key, value in kwargs.items():
                    if hasattr(instance, key):
                        setattr(instance, key, value)
                session.flush()
            return instance
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating {self.model.__name__} {id}: {e}")
            raise
    
    def delete(self, session: Session, id: str) -> bool:
        """Delete a record by ID.
        
        Args:
            session: Database session
            id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            instance = self.get_by_id(session, id)
            if instance:
                session.delete(instance)
                return True
            return False
        except SQLAlchemyError as e:
            self.logger.error(f"Error deleting {self.model.__name__} {id}: {e}")
            raise


class PromptTemplateRepository(BaseRepository[PromptTemplate]):
    """Repository for prompt template operations."""
    
    def __init__(self):
        super().__init__(PromptTemplate)
    
    def get_by_agent_type(self, session: Session, agent_type: str) -> List[PromptTemplate]:
        """Get all active prompt templates for a specific agent type.
        
        Args:
            session: Database session
            agent_type: Type of agent
            
        Returns:
            List of prompt templates
        """
        try:
            query = select(PromptTemplate).where(
                PromptTemplate.agent_type == agent_type,
                PromptTemplate.is_active == True
            ).order_by(PromptTemplate.updated_at.desc())
            
            result = session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting templates for agent {agent_type}: {e}")
            raise
    
    def get_by_name_and_agent(self, session: Session, name: str, agent_type: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name and agent type.
        
        Args:
            session: Database session
            name: Template name
            agent_type: Agent type
            
        Returns:
            Prompt template or None if not found
        """
        try:
            query = select(PromptTemplate).where(
                PromptTemplate.name == name,
                PromptTemplate.agent_type == agent_type,
                PromptTemplate.is_active == True
            )
            result = session.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting template {name} for agent {agent_type}: {e}")
            raise
    
    def increment_usage(self, session: Session, template_id: str) -> None:
        """Increment the usage count for a template.
        
        Args:
            session: Database session
            template_id: Template ID
        """
        try:
            query = update(PromptTemplate).where(
                PromptTemplate.id == template_id
            ).values(
                usage_count=PromptTemplate.usage_count + 1,
                updated_at=datetime.utcnow()
            )
            session.execute(query)
        except SQLAlchemyError as e:
            self.logger.error(f"Error incrementing usage for template {template_id}: {e}")
            raise


class PromptVersionRepository(BaseRepository[PromptVersion]):
    """Repository for prompt version operations."""
    
    def __init__(self):
        super().__init__(PromptVersion)
    
    def get_by_template_id(self, session: Session, template_id: str) -> List[PromptVersion]:
        """Get all versions for a template.
        
        Args:
            session: Database session
            template_id: Template ID
            
        Returns:
            List of prompt versions
        """
        try:
            query = select(PromptVersion).where(
                PromptVersion.template_id == template_id
            ).order_by(PromptVersion.created_at.desc())
            
            result = session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting versions for template {template_id}: {e}")
            raise
    
    def get_current_version(self, session: Session, template_id: str) -> Optional[PromptVersion]:
        """Get the current version for a template.
        
        Args:
            session: Database session
            template_id: Template ID
            
        Returns:
            Current prompt version or None if not found
        """
        try:
            query = select(PromptVersion).where(
                PromptVersion.template_id == template_id,
                PromptVersion.is_current == True
            )
            result = session.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting current version for template {template_id}: {e}")
            raise
    
    def set_current_version(self, session: Session, template_id: str, version_id: str) -> None:
        """Set a version as the current version for a template.
        
        Args:
            session: Database session
            template_id: Template ID
            version_id: Version ID to set as current
        """
        try:
            # First, unset all current versions for this template
            session.execute(
                update(PromptVersion).where(
                    PromptVersion.template_id == template_id
                ).values(is_current=False)
            )
            
            # Then set the specified version as current
            session.execute(
                update(PromptVersion).where(
                    PromptVersion.id == version_id
                ).values(is_current=True)
            )
        except SQLAlchemyError as e:
            self.logger.error(f"Error setting current version {version_id} for template {template_id}: {e}")
            raise


class AgentConfigurationRepository(BaseRepository[AgentConfiguration]):
    """Repository for agent configuration operations."""
    
    def __init__(self):
        super().__init__(AgentConfiguration)
    
    def get_by_agent_type(self, session: Session, agent_type: str, environment: str = "production") -> List[AgentConfiguration]:
        """Get configurations for an agent type and environment.
        
        Args:
            session: Database session
            agent_type: Agent type
            environment: Environment name
            
        Returns:
            List of agent configurations
        """
        try:
            query = select(AgentConfiguration).where(
                AgentConfiguration.agent_type == agent_type,
                AgentConfiguration.environment == environment,
                AgentConfiguration.is_active == True
            )
            result = session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting configs for agent {agent_type}: {e}")
            raise
    
    def get_default_config(self, session: Session, agent_type: str, environment: str = "production") -> Optional[AgentConfiguration]:
        """Get the default configuration for an agent type.
        
        Args:
            session: Database session
            agent_type: Agent type
            environment: Environment name
            
        Returns:
            Default agent configuration or None if not found
        """
        try:
            query = select(AgentConfiguration).where(
                AgentConfiguration.agent_type == agent_type,
                AgentConfiguration.environment == environment,
                AgentConfiguration.is_default == True,
                AgentConfiguration.is_active == True
            )
            result = session.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting default config for agent {agent_type}: {e}")
            raise


class ProcessingSessionRepository(BaseRepository[ProcessingSession]):
    """Repository for processing session operations."""
    
    def __init__(self):
        super().__init__(ProcessingSession)
    
    def get_by_session_type(self, session: Session, session_type: str, limit: int = 100) -> List[ProcessingSession]:
        """Get processing sessions by type.
        
        Args:
            session: Database session
            session_type: Session type
            limit: Maximum number of sessions to return
            
        Returns:
            List of processing sessions
        """
        try:
            query = select(ProcessingSession).where(
                ProcessingSession.session_type == session_type
            ).order_by(ProcessingSession.created_at.desc()).limit(limit)
            
            result = session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting sessions for type {session_type}: {e}")
            raise
    
    def get_recent_sessions(self, session: Session, hours: int = 24, limit: int = 100) -> List[ProcessingSession]:
        """Get recent processing sessions.
        
        Args:
            session: Database session
            hours: Number of hours to look back
            limit: Maximum number of sessions to return
            
        Returns:
            List of recent processing sessions
        """
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            query = select(ProcessingSession).where(
                ProcessingSession.created_at >= cutoff_time
            ).order_by(ProcessingSession.created_at.desc()).limit(limit)
            
            result = session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting recent sessions: {e}")
            raise


class ImprintingTemplateRepository(BaseRepository[ImprintingTemplate]):
    """Repository for Template Imprinting Protocol operations."""
    
    def __init__(self):
        super().__init__(ImprintingTemplate)
    
    def create_imprinting_template(self, session: Session, name: str, agent_type: str,
                                 template_mode: Dict[str, Any], template_structure: Dict[str, Any],
                                 example_filled: Optional[Dict[str, Any]] = None,
                                 **kwargs) -> ImprintingTemplate:
        """Create a new imprinting template with validation.
        
        Args:
            session: Database session
            name: Template name
            agent_type: Agent type
            template_mode: Behavioral configuration
            template_structure: Template structure
            example_filled: Optional example
            **kwargs: Additional fields
            
        Returns:
            Created imprinting template
            
        Raises:
            ValueError: If validation fails
        """
        # Validate Template Imprinting Protocol structure
        validation_result = imprinting_validator.validate_imprinting_template(
            template_mode, template_structure, example_filled
        )
        
        if not validation_result.is_valid:
            raise ValueError(f"Template Imprinting validation failed: {validation_result.errors}")
        
        # Generate imprinting tokens (first 200 chars)
        import json
        full_template = {
            "template_mode": template_mode,
            "template": template_structure
        }
        imprinting_tokens = json.dumps(full_template)[:200]
        
        try:
            template = self.create(
                session,
                name=name,
                agent_type=agent_type,
                template_mode=template_mode,
                template_structure=template_structure,
                example_filled=example_filled,
                imprinting_tokens=imprinting_tokens,
                token_count=validation_result.token_count,
                adherence_score=validation_result.adherence_score,
                **kwargs
            )
            
            # Log warnings if any
            for warning in validation_result.warnings:
                self.logger.warning(f"Template '{name}': {warning}")
            
            return template
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating imprinting template {name}: {e}")
            raise
    
    def get_by_agent_type(self, session: Session, agent_type: str, 
                         active_only: bool = True) -> List[ImprintingTemplate]:
        """Get imprinting templates for an agent type.
        
        Args:
            session: Database session
            agent_type: Agent type
            active_only: Only return active templates
            
        Returns:
            List of imprinting templates
        """
        try:
            query = select(ImprintingTemplate).where(
                ImprintingTemplate.agent_type == agent_type
            )
            
            if active_only:
                query = query.where(ImprintingTemplate.is_active == True)
            
            query = query.order_by(
                ImprintingTemplate.priority.desc(),
                ImprintingTemplate.adherence_score.desc()
            )
            
            result = session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting imprinting templates for agent {agent_type}: {e}")
            raise
    
    def get_best_template(self, session: Session, agent_type: str) -> Optional[ImprintingTemplate]:
        """Get the best imprinting template for an agent type.
        
        Args:
            session: Database session
            agent_type: Agent type
            
        Returns:
            Best imprinting template or None
        """
        templates = self.get_by_agent_type(session, agent_type, active_only=True)
        return templates[0] if templates else None
    
    def update_performance_metrics(self, session: Session, template_id: str,
                                 adherence_score: float, success: bool) -> None:
        """Update performance metrics for an imprinting template.
        
        Args:
            session: Database session
            template_id: Template ID
            adherence_score: Measured adherence score
            success: Whether the imprinting was successful
        """
        try:
            template = self.get_by_id(session, template_id)
            if template:
                # Update usage count
                template.usage_count += 1
                
                # Update success rate
                if template.success_rate is None:
                    template.success_rate = 1.0 if success else 0.0
                else:
                    # Running average
                    total_uses = template.usage_count
                    current_successes = template.success_rate * (total_uses - 1)
                    new_successes = current_successes + (1 if success else 0)
                    template.success_rate = new_successes / total_uses
                
                # Update adherence score (running average)
                if template.adherence_score is None:
                    template.adherence_score = adherence_score
                else:
                    total_uses = template.usage_count
                    current_total = template.adherence_score * (total_uses - 1)
                    template.adherence_score = (current_total + adherence_score) / total_uses
                
                session.flush()
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating metrics for template {template_id}: {e}")
            raise


# PATTERN_REF: DATABASE_ACCESS_PATTERN
class UserRepository(BaseRepository[User]):
    """Repository for User entity operations (Template Imprinting Protocol enforced)."""

    def __init__(self):
        super().__init__(User)
        # DECISION_REF: See DEC_2025-06-22_001 (Repository pattern, error handling, type safety)

    def get_by_id(self, session: Session, user_id: str) -> Optional[User]:
        """
        Get a user by ID.
        Args:
            session: Database session
            user_id: User ID
        Returns:
            User instance or None if not found
        """
        try:
            return session.get(User, user_id)
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting User by ID {user_id}: {e}")
            raise

    def get_all(self, session: Session, limit: Optional[int] = None) -> List[User]:
        """
        Get all users.
        Args:
            session: Database session
            limit: Optional limit on number of users
        Returns:
            List of User instances
        """
        try:
            query = select(User)
            if limit:
                query = query.limit(limit)
            result = session.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting all Users: {e}")
            raise

    def create(self, session: Session, **kwargs) -> User:
        """
        Create a new user.
        Args:
            session: Database session
            **kwargs: User fields
        Returns:
            Created User instance
        """
        try:
            user = User(**kwargs)
            session.add(user)
            session.flush()
            return user
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating User: {e}")
            raise

    def update(self, session: Session, user_id: str, **kwargs) -> Optional[User]:
        """
        Update a user by ID.
        Args:
            session: Database session
            user_id: User ID
            **kwargs: Fields to update
        Returns:
            Updated User instance or None if not found
        """
        try:
            user = self.get_by_id(session, user_id)
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                session.flush()
            return user
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating User {user_id}: {e}")
            raise

    def delete(self, session: Session, user_id: str) -> bool:
        """
        Delete a user by ID.
        Args:
            session: Database session
            user_id: User ID
        Returns:
            True if deleted, False if not found
        """
        try:
            user = self.get_by_id(session, user_id)
            if user:
                session.delete(user)
                return True
            return False
        except SQLAlchemyError as e:
            self.logger.error(f"Error deleting User {user_id}: {e}")
            raise
# DECISION_REF: DEC_2025-06-22_001 | Pattern: DATABASE_ACCESS_PATTERN | Rationale: Enforces repository, error handling, type safety, connection pooling

# Repository instances for easy access
prompt_template_repo = PromptTemplateRepository()
prompt_version_repo = PromptVersionRepository()
agent_config_repo = AgentConfigurationRepository()
processing_session_repo = ProcessingSessionRepository()
imprinting_template_repo = ImprintingTemplateRepository()
user_repo = UserRepository()