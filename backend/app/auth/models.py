"""
Authentication models for ASMIS backend.
"""

from pydantic import BaseModel


class AuthContext(BaseModel):
    """Authentication context containing user and tenant information."""
    
    user_id: str
    tenant_id: str
    email: str
    role: str = "member"  # Default role for users
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True
        
    def __repr__(self) -> str:
        return f"<AuthContext(user_id='{self.user_id}', tenant_id='{self.tenant_id}', email='{self.email}')>"