"""
Tenant-aware repository class with automatic authentication context integration.
"""

import logging
from typing import List, Optional, Type, TypeVar
from sqlalchemy.orm import Session

from .base_repository import BaseRepository, ModelType
from ..auth.models import AuthContext
from ..database.base import Base

logger = logging.getLogger(__name__)


class TenantRepository(BaseRepository[ModelType]):
    """Repository with automatic tenant filtering based on authentication context."""
    
    def __init__(self, model: Type[ModelType]):
        """Initialize tenant-aware repository.
        
        Args:
            model: The SQLAlchemy model class
        """
        super().__init__(model)
        
        if not self.is_tenant_aware:
            logger.warning(f"Model {self.model.__name__} is not tenant-aware but using TenantRepository")
    
    def get_by_id_with_auth(self, session: Session, id: str, auth: AuthContext) -> Optional[ModelType]:
        """Get a record by ID using authentication context.
        
        Args:
            session: Database session
            id: Record ID
            auth: Authentication context containing tenant_id
            
        Returns:
            Model instance or None if not found
        """
        return self.get_by_id(session, id, auth.tenant_id)
    
    def get_all_with_auth(self, session: Session, auth: AuthContext, limit: Optional[int] = None) -> List[ModelType]:
        """Get all records using authentication context.
        
        Args:
            session: Database session
            auth: Authentication context containing tenant_id
            limit: Optional limit
            
        Returns:
            List of model instances for the authenticated tenant
        """
        return self.get_all(session, auth.tenant_id, limit)
    
    def create_with_auth(self, session: Session, auth: AuthContext, **kwargs) -> ModelType:
        """Create a new record using authentication context.
        
        Args:
            session: Database session
            auth: Authentication context containing tenant_id
            **kwargs: Model field values
            
        Returns:
            Created model instance
        """
        return self.create(session, auth.tenant_id, **kwargs)
    
    def update_with_auth(self, session: Session, id: str, auth: AuthContext, **kwargs) -> Optional[ModelType]:
        """Update a record using authentication context.
        
        Args:
            session: Database session
            id: Record ID
            auth: Authentication context containing tenant_id
            **kwargs: Fields to update
            
        Returns:
            Updated model instance or None if not found
        """
        return self.update(session, id, auth.tenant_id, **kwargs)
    
    def delete_with_auth(self, session: Session, id: str, auth: AuthContext) -> bool:
        """Delete a record using authentication context.
        
        Args:
            session: Database session
            id: Record ID
            auth: Authentication context containing tenant_id
            
        Returns:
            True if deleted, False if not found
        """
        return self.delete(session, id, auth.tenant_id)
    
    def ensure_tenant_access(self, session: Session, id: str, auth: AuthContext) -> bool:
        """Verify that a record exists and belongs to the authenticated tenant.
        
        Args:
            session: Database session
            id: Record ID
            auth: Authentication context containing tenant_id
            
        Returns:
            True if record exists and belongs to tenant, False otherwise
        """
        instance = self.get_by_id(session, id, auth.tenant_id)
        return instance is not None