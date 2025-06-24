"""Base repository class for common database operations."""

import logging
from typing import List, Optional, Dict, Any, Generic, TypeVar, Type
from datetime import datetime

from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..database.base import Base

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
            limit: Optional limit
            
        Returns:
            List of model instances
        """
        try:
            stmt = select(self.model)
            if limit:
                stmt = stmt.limit(limit)
            
            result = session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting all {self.model.__name__}: {e}")
            raise
    
    def create(self, session: Session, **kwargs) -> ModelType:
        """Create a new record.
        
        Args:
            session: Database session
            **kwargs: Model field values
            
        Returns:
            Created model instance
        """
        try:
            instance = self.model(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating {self.model.__name__}: {e}")
            session.rollback()
            raise
    
    def update(self, session: Session, id: str, **kwargs) -> Optional[ModelType]:
        """Update a record by ID.
        
        Args:
            session: Database session
            id: Record ID
            **kwargs: Fields to update
            
        Returns:
            Updated model instance or None if not found
        """
        try:
            instance = self.get_by_id(session, id)
            if not instance:
                return None
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            instance.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating {self.model.__name__} {id}: {e}")
            session.rollback()
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
            if not instance:
                return False
            
            session.delete(instance)
            session.commit()
            return True
        except SQLAlchemyError as e:
            self.logger.error(f"Error deleting {self.model.__name__} {id}: {e}")
            session.rollback()
            raise