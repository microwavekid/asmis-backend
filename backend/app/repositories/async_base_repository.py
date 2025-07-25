"""Async base repository class for common database operations."""

import logging
from typing import List, Optional, Dict, Any, Generic, TypeVar, Type
from datetime import datetime, UTC

from sqlalchemy import select, delete, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..database.base import Base

logger = logging.getLogger(__name__)

# Generic type for model classes
ModelType = TypeVar("ModelType", bound=Base)


class AsyncBaseRepository(Generic[ModelType]):
    """Async base repository class with common database operations and tenant filtering."""
    
    def __init__(self, model: Type[ModelType]):
        """Initialize the repository with a model class.
        
        Args:
            model: The SQLAlchemy model class
        """
        self.model = model
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Check if model has tenant_id for automatic filtering
        self.is_tenant_aware = hasattr(model, 'tenant_id')
        if not self.is_tenant_aware:
            # Only warn if this is actually used as a TenantRepository (child classes can override)
            if self.__class__.__name__.endswith('TenantRepository'):
                self.logger.warning(f"Model {model.__name__} is not tenant-aware but using AsyncTenantRepository")
    
    def _add_tenant_filter(self, stmt, tenant_id: str):
        """Add tenant filter to query if model is tenant-aware.
        
        Args:
            stmt: SQLAlchemy select statement
            tenant_id: Tenant ID to filter by
            
        Returns:
            Modified statement with tenant filter
        """
        if self.is_tenant_aware and tenant_id:
            return stmt.where(self.model.tenant_id == tenant_id)
        return stmt
    
    def _add_active_filter(self, stmt):
        """Add active filter to exclude soft-deleted records.
        
        Args:
            stmt: SQLAlchemy select statement
            
        Returns:
            Modified statement with active filter
        """
        if hasattr(self.model, 'is_active'):
            return stmt.where(self.model.is_active.is_(True))
        elif hasattr(self.model, 'deleted_at'):
            return stmt.where(self.model.deleted_at.is_(None))
        return stmt
    
    async def get_all(self, session: AsyncSession, tenant_id: Optional[str] = None, limit: Optional[int] = None) -> List[ModelType]:
        """Get all records for a tenant with optional limit.
        
        Args:
            session: Async database session
            tenant_id: Tenant ID for filtering (required for tenant-aware models)
            limit: Optional limit
            
        Returns:
            List of model instances
        """
        try:
            stmt = select(self.model)
            stmt = self._add_tenant_filter(stmt, tenant_id)
            stmt = self._add_active_filter(stmt)
            
            if limit:
                stmt = stmt.limit(limit)
            
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting all {self.model.__name__}: {e}")
            raise
    
    async def create(self, session: AsyncSession, tenant_id: Optional[str] = None, **kwargs) -> ModelType:
        """Create a new record with automatic tenant_id injection.
        
        Args:
            session: Async database session
            tenant_id: Tenant ID (required for tenant-aware models)
            **kwargs: Model field values
            
        Returns:
            Created model instance
        """
        try:
            # Auto-inject tenant_id for tenant-aware models
            if self.is_tenant_aware and tenant_id:
                kwargs['tenant_id'] = tenant_id
            
            # Auto-inject timestamps if available
            now = datetime.now(UTC)
            if hasattr(self.model, 'created_at') and 'created_at' not in kwargs:
                kwargs['created_at'] = now
            if hasattr(self.model, 'updated_at') and 'updated_at' not in kwargs:
                kwargs['updated_at'] = now
            if hasattr(self.model, 'is_active') and 'is_active' not in kwargs:
                kwargs['is_active'] = True
                
            instance = self.model(**kwargs)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            
            self.logger.info(f"Created {self.model.__name__} with id: {instance.id}")
            return instance
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Error creating {self.model.__name__}: {e}")
            raise
    
    async def get_by_id(self, session: AsyncSession, record_id: str, tenant_id: Optional[str] = None) -> Optional[ModelType]:
        """Get a record by ID with optional tenant filtering.
        
        Args:
            session: Async database session
            record_id: Record ID
            tenant_id: Tenant ID for filtering (required for tenant-aware models)
            
        Returns:
            Model instance or None if not found
        """
        try:
            stmt = select(self.model).where(self.model.id == record_id)
            stmt = self._add_tenant_filter(stmt, tenant_id)
            stmt = self._add_active_filter(stmt)
            
            result = await session.execute(stmt)
            return result.scalars().first()
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting {self.model.__name__} by id {record_id}: {e}")
            raise
    
    async def update(self, session: AsyncSession, record_id: str, tenant_id: Optional[str] = None, **kwargs) -> Optional[ModelType]:
        """Update a record by ID.
        
        Args:
            session: Async database session
            record_id: Record ID
            tenant_id: Tenant ID for filtering (required for tenant-aware models)
            **kwargs: Fields to update
            
        Returns:
            Updated model instance or None if not found
        """
        try:
            # Get the record first
            record = await self.get_by_id(session, record_id, tenant_id)
            if not record:
                return None
            
            # Auto-inject updated_at timestamp
            if hasattr(self.model, 'updated_at'):
                kwargs['updated_at'] = datetime.now(UTC)
            
            # Update fields
            for field, value in kwargs.items():
                if hasattr(record, field):
                    setattr(record, field, value)
            
            await session.commit()
            await session.refresh(record)
            
            self.logger.info(f"Updated {self.model.__name__} with id: {record_id}")
            return record
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Error updating {self.model.__name__} {record_id}: {e}")
            raise
    
    async def delete(self, session: AsyncSession, record_id: str, tenant_id: Optional[str] = None, soft_delete: bool = True) -> bool:
        """Delete a record by ID (soft or hard delete).
        
        Args:
            session: Async database session
            record_id: Record ID
            tenant_id: Tenant ID for filtering (required for tenant-aware models)
            soft_delete: Whether to soft delete (default) or hard delete
            
        Returns:
            True if deleted, False if not found
        """
        try:
            record = await self.get_by_id(session, record_id, tenant_id)
            if not record:
                return False
            
            if soft_delete:
                # Soft delete - mark as inactive or set deleted_at
                if hasattr(record, 'is_active'):
                    record.is_active = False
                if hasattr(record, 'deleted_at'):
                    record.deleted_at = datetime.now(UTC)
                if hasattr(record, 'updated_at'):
                    record.updated_at = datetime.now(UTC)
            else:
                # Hard delete
                await session.delete(record)
            
            await session.commit()
            self.logger.info(f"{'Soft' if soft_delete else 'Hard'} deleted {self.model.__name__} with id: {record_id}")
            return True
        except SQLAlchemyError as e:
            await session.rollback()
            self.logger.error(f"Error deleting {self.model.__name__} {record_id}: {e}")
            raise


class AsyncTenantRepository(AsyncBaseRepository[ModelType]):
    """Async repository with tenant isolation enforced."""
    
    def __init__(self, model: Type[ModelType]):
        """Initialize tenant repository.
        
        Args:
            model: The SQLAlchemy model class (must have tenant_id field)
        """
        super().__init__(model)
        
        if not self.is_tenant_aware:
            raise ValueError(f"Model {model.__name__} must have tenant_id field for AsyncTenantRepository")
    
    async def get_all_with_auth(self, session: AsyncSession, auth, limit: Optional[int] = None) -> List[ModelType]:
        """Get all records for the authenticated user's tenant.
        
        Args:
            session: Async database session
            auth: Authentication context with tenant_id
            limit: Optional limit
            
        Returns:
            List of model instances
        """
        return await self.get_all(session, auth.tenant_id, limit)
    
    async def get_by_id_with_auth(self, session: AsyncSession, record_id: str, auth) -> Optional[ModelType]:
        """Get a record by ID for the authenticated user's tenant.
        
        Args:
            session: Async database session
            record_id: Record ID
            auth: Authentication context with tenant_id
            
        Returns:
            Model instance or None if not found
        """
        return await self.get_by_id(session, record_id, auth.tenant_id)
    
    async def create_with_auth(self, session: AsyncSession, auth, **kwargs) -> ModelType:
        """Create a record for the authenticated user's tenant.
        
        Args:
            session: Async database session
            auth: Authentication context with tenant_id
            **kwargs: Model field values
            
        Returns:
            Created model instance
        """
        return await self.create(session, auth.tenant_id, **kwargs)
    
    async def update_with_auth(self, session: AsyncSession, record_id: str, auth, **kwargs) -> Optional[ModelType]:
        """Update a record for the authenticated user's tenant.
        
        Args:
            session: Async database session
            record_id: Record ID
            auth: Authentication context with tenant_id
            **kwargs: Fields to update
            
        Returns:
            Updated model instance or None if not found
        """
        return await self.update(session, record_id, auth.tenant_id, **kwargs)
    
    async def delete_with_auth(self, session: AsyncSession, record_id: str, auth, soft_delete: bool = True) -> bool:
        """Delete a record for the authenticated user's tenant.
        
        Args:
            session: Async database session
            record_id: Record ID
            auth: Authentication context with tenant_id
            soft_delete: Whether to soft delete (default) or hard delete
            
        Returns:
            True if deleted, False if not found
        """
        return await self.delete(session, record_id, auth.tenant_id, soft_delete)