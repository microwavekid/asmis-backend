"""
Repository Stubs for ASMIS Multi-Tenancy Integration Testing.

TODO: This is a STUB implementation for early integration testing.
Real repository implementations will be updated in Phase 3 (MIC-69).

Purpose: Test tenant filtering and data isolation concepts before implementing
real database schema changes and migrations.
"""

from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from datetime import datetime


class BaseRepositoryStub:
    """
    STUB: Base repository with tenant filtering for integration testing.
    TODO: Replace with real BaseRepository updates in Phase 3.
    """
    
    def __init__(self, mock_data: Dict[str, List[Dict[str, Any]]]):
        """Initialize with mock data organized by tenant."""
        self.mock_data = mock_data
    
    def get_by_id(self, session: Session, id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """
        STUB: Get entity by ID with tenant filtering.
        TODO: Replace with real SQLAlchemy query in Phase 3.
        """
        tenant_data = self.mock_data.get(self._tenant_id_to_slug(tenant_id), [])
        for item in tenant_data:
            if item["id"] == id:
                return item
        return None
    
    def get_all(self, session: Session, tenant_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        STUB: Get all entities for tenant.
        TODO: Replace with real SQLAlchemy query in Phase 3.
        """
        tenant_data = self.mock_data.get(self._tenant_id_to_slug(tenant_id), [])
        if limit:
            return tenant_data[:limit]
        return tenant_data
    
    def create(self, session: Session, tenant_id: str, **kwargs) -> Dict[str, Any]:
        """
        STUB: Create new entity with tenant_id.
        TODO: Replace with real SQLAlchemy creation in Phase 3.
        """
        # Generate mock ID
        mock_id = f"mock-{len(self.mock_data.get(self._tenant_id_to_slug(tenant_id), []))}"
        
        new_item = {
            "id": mock_id,
            "tenant_id": tenant_id,
            "created_at": datetime.utcnow().isoformat(),
            **kwargs
        }
        
        tenant_slug = self._tenant_id_to_slug(tenant_id)
        if tenant_slug not in self.mock_data:
            self.mock_data[tenant_slug] = []
        
        self.mock_data[tenant_slug].append(new_item)
        return new_item
    
    def update(self, session: Session, id: str, tenant_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        STUB: Update entity with tenant filtering.
        TODO: Replace with real SQLAlchemy update in Phase 3.
        """
        tenant_data = self.mock_data.get(self._tenant_id_to_slug(tenant_id), [])
        for item in tenant_data:
            if item["id"] == id:
                item.update(kwargs)
                item["updated_at"] = datetime.utcnow().isoformat()
                return item
        return None
    
    def delete(self, session: Session, id: str, tenant_id: str) -> bool:
        """
        STUB: Delete entity with tenant filtering.
        TODO: Replace with real SQLAlchemy delete in Phase 3.
        """
        tenant_slug = self._tenant_id_to_slug(tenant_id)
        tenant_data = self.mock_data.get(tenant_slug, [])
        
        for i, item in enumerate(tenant_data):
            if item["id"] == id:
                del tenant_data[i]
                return True
        return False
    
    def _tenant_id_to_slug(self, tenant_id: str) -> str:
        """Helper to convert tenant UUID to slug for mock data lookup."""
        tenant_map = {
            "550e8400-e29b-41d4-a716-446655440001": "acme-corp",
            "550e8400-e29b-41d4-a716-446655440002": "beta-industries", 
            "550e8400-e29b-41d4-a716-446655440003": "gamma-solutions"
        }
        return tenant_map.get(tenant_id, "unknown")