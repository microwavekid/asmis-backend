"""Base repository class for common database operations."""

import logging
from typing import List, Optional, Dict, Any, Generic, TypeVar, Type
from datetime import datetime

from sqlalchemy import select, delete, update, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..database.base import Base

logger = logging.getLogger(__name__)

# Generic type for model classes
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository class with common database operations and tenant filtering."""
    
    def __init__(self, model: Type[ModelType]):
        """Initialize the repository with a model class.
        
        Args:
            model: The SQLAlchemy model class
        """
        self.model = model
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Check if model has tenant_id field for automatic filtering
        self.is_tenant_aware = hasattr(model, 'tenant_id')
        if self.is_tenant_aware:
            self.logger.debug(f"{self.model.__name__} is tenant-aware")
    
    def _add_tenant_filter(self, stmt, tenant_id: Optional[str]):
        """Add tenant filter to query if model is tenant-aware and tenant_id is provided.
        
        Args:
            stmt: SQLAlchemy statement
            tenant_id: Tenant ID to filter by
            
        Returns:
            Modified statement with tenant filter if applicable
        """
        if self.is_tenant_aware and tenant_id:
            return stmt.where(self.model.tenant_id == tenant_id)
        return stmt
    
    def get_by_id(self, session: Session, id: str, tenant_id: Optional[str] = None) -> Optional[ModelType]:
        """Get a record by ID with optional tenant filtering.
        
        Args:
            session: Database session
            id: Record ID
            tenant_id: Tenant ID for filtering (required for tenant-aware models)
            
        Returns:
            Model instance or None if not found
        """
        try:
            if self.is_tenant_aware and tenant_id:
                stmt = select(self.model).where(
                    and_(self.model.id == id, self.model.tenant_id == tenant_id)
                )
                result = session.execute(stmt)
                return result.scalar_one_or_none()
            else:
                return session.get(self.model, id)
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting {self.model.__name__} by ID {id}: {e}")
            raise
    
    def get_all(self, session: Session, tenant_id: Optional[str] = None, limit: Optional[int] = None) -> List[ModelType]:
        """Get all records with optional tenant filtering.
        
        Args:
            session: Database session
            tenant_id: Tenant ID for filtering (required for tenant-aware models)
            limit: Optional limit
            
        Returns:
            List of model instances
        """
        try:
            stmt = select(self.model)
            stmt = self._add_tenant_filter(stmt, tenant_id)
            
            if limit:
                stmt = stmt.limit(limit)
            
            result = session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting all {self.model.__name__}: {e}")
            raise
    
    def create(self, session: Session, tenant_id: Optional[str] = None, **kwargs) -> ModelType:
        """Create a new record with automatic tenant_id injection.
        
        Args:
            session: Database session
            tenant_id: Tenant ID (required for tenant-aware models)
            **kwargs: Model field values
            
        Returns:
            Created model instance
        """
        try:
            # Automatically inject tenant_id for tenant-aware models
            if self.is_tenant_aware and tenant_id:
                kwargs['tenant_id'] = tenant_id
            elif self.is_tenant_aware and not tenant_id:
                raise ValueError(f"tenant_id is required for tenant-aware model {self.model.__name__}")
                
            instance = self.model(**kwargs)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating {self.model.__name__}: {e}")
            session.rollback()
            raise
    
    def update(self, session: Session, id: str, tenant_id: Optional[str] = None, **kwargs) -> Optional[ModelType]:
        """Update a record by ID with tenant filtering.
        
        Args:
            session: Database session
            id: Record ID
            tenant_id: Tenant ID for filtering (required for tenant-aware models)
            **kwargs: Fields to update
            
        Returns:
            Updated model instance or None if not found
        """
        try:
            instance = self.get_by_id(session, id, tenant_id)
            if not instance:
                return None
            
            # Prevent tenant_id changes
            if 'tenant_id' in kwargs:
                self.logger.warning(f"Attempted to change tenant_id for {self.model.__name__} {id}")
                kwargs.pop('tenant_id')
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            if hasattr(instance, 'updated_at'):
                instance.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating {self.model.__name__} {id}: {e}")
            session.rollback()
            raise
    
    def delete(self, session: Session, id: str, tenant_id: Optional[str] = None) -> bool:
        """Delete a record by ID with tenant filtering.
        
        Args:
            session: Database session
            id: Record ID
            tenant_id: Tenant ID for filtering (required for tenant-aware models)
            
        Returns:
            True if deleted, False if not found
        """
        try:
            instance = self.get_by_id(session, id, tenant_id)
            if not instance:
                return False
            
            session.delete(instance)
            session.commit()
            return True
        except SQLAlchemyError as e:
            self.logger.error(f"Error deleting {self.model.__name__} {id}: {e}")
            session.rollback()
            raise