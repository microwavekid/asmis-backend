"""
JWT Authentication Dependency for FastAPI.

This module provides the authentication dependency that extracts
and validates JWT tokens from requests, returning AuthContext.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..database.connection import get_db_session
from ..database.models import User, TenantUser
from .models import AuthContext
from .jwt_service import verify_token, TokenData


# HTTP Bearer authentication scheme
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db_session)
) -> Optional[User]:
    """
    Get current user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials containing JWT token
        db: Database session
    
    Returns:
        User model if token is valid, None otherwise
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from Bearer scheme
    token = credentials.credentials
    
    # Verify and decode token
    token_data = verify_token(token, expected_type="access")
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = db.query(User).filter(
        User.id == token_data.sub,
        User.is_active == True,
        User.is_deleted == False
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_auth_context(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db_session)
) -> AuthContext:
    """
    Get authentication context from JWT token.
    
    This is the main authentication dependency that replaces
    get_auth_context_stub for production use.
    
    Args:
        credentials: HTTP Bearer credentials containing JWT token
        db: Database session
    
    Returns:
        AuthContext with user and tenant information
    
    Raises:
        HTTPException: If authentication fails
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from Bearer scheme
    token = credentials.credentials
    
    # Verify and decode token
    token_data = verify_token(token, expected_type="access")
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # For MVP, we trust the token data since we control user creation
    # In production, we might want to verify against database
    return AuthContext(
        user_id=token_data.sub,
        tenant_id=token_data.tenant_id,
        email=token_data.email,
        role=token_data.role
    )


async def get_auth_context_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db_session)
) -> Optional[AuthContext]:
    """
    Get authentication context if provided, None otherwise.
    
    This is useful for endpoints that work with or without authentication.
    
    Args:
        credentials: HTTP Bearer credentials containing JWT token
        db: Database session
    
    Returns:
        AuthContext if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    try:
        return await get_auth_context(credentials, db)
    except HTTPException:
        return None


def require_role(allowed_roles: list[str]):
    """
    Create a dependency that requires specific roles.
    
    Args:
        allowed_roles: List of roles that are allowed access
    
    Returns:
        Dependency function that validates role
    """
    async def role_checker(auth: AuthContext = Depends(get_auth_context)) -> AuthContext:
        if auth.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{auth.role}' not authorized. Required roles: {allowed_roles}"
            )
        return auth
    
    return role_checker


# Pre-configured role dependencies for common use cases
require_admin = require_role(["admin"])
require_admin_or_owner = require_role(["admin", "owner"])
require_any_role = require_role(["admin", "owner", "member"])