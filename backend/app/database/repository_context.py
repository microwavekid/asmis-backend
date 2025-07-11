"""
Repository context wrapper for tenant-aware operations.

TODO: This is a STUB wrapper for early integration testing.
Real implementation will get tenant_id from request context in Phase 3.
"""

from typing import Dict, List, Optional, Any, TypeVar, Generic
from sqlalchemy.orm import Session
from .stubs import BaseRepositoryStub


class MockModel:
    """Mock model that converts dict to object with attributes."""
    
    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f"<MockModel({self.__dict__})>"


T = TypeVar("T")


class TenantAwareRepositoryWrapper(Generic[T]):
    """
    STUB: Wrapper that provides BaseRepository-compatible interface.
    Gets tenant_id from auth context instead of method parameters.
    TODO: Replace with real implementation in Phase 3.
    """
    
    def __init__(self, stub_repository: BaseRepositoryStub, tenant_id: str):
        """
        Initialize with a stub repository and tenant context.
        
        Args:
            stub_repository: The underlying stub repository
            tenant_id: The tenant ID from auth context
        """
        self.stub = stub_repository
        self.tenant_id = tenant_id
    
    def get_by_id(self, session: Session, id: str) -> Optional[MockModel]:
        """Get by ID - matches BaseRepository interface."""
        data = self.stub.get_by_id(session, id, self.tenant_id)
        return MockModel(data) if data else None
    
    def get_all(self, session: Session, limit: Optional[int] = None) -> List[MockModel]:
        """Get all - matches BaseRepository interface."""
        data_list = self.stub.get_all(session, self.tenant_id, limit)
        return [MockModel(data) for data in data_list]
    
    def create(self, session: Session, **kwargs) -> MockModel:
        """Create - matches BaseRepository interface."""
        data = self.stub.create(session, self.tenant_id, **kwargs)
        return MockModel(data)
    
    def update(self, session: Session, id: str, **kwargs) -> Optional[MockModel]:
        """Update - matches BaseRepository interface."""
        data = self.stub.update(session, id, self.tenant_id, **kwargs)
        return MockModel(data) if data else None
    
    def delete(self, session: Session, id: str) -> bool:
        """Delete - matches BaseRepository interface."""
        return self.stub.delete(session, id, self.tenant_id)


def get_repository_for_tenant(stub_repository: BaseRepositoryStub, tenant_id: str) -> TenantAwareRepositoryWrapper:
    """
    Factory function to create tenant-aware repository wrapper.
    
    TODO: In real implementation, get tenant_id from request context.
    """
    return TenantAwareRepositoryWrapper(stub_repository, tenant_id)