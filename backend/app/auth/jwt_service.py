"""
JWT Token Service for ASMIS Authentication.

This module handles JWT token generation, validation, and management
for the multi-tenant authentication system.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os
from jose import JWTError, jwt
from pydantic import BaseModel

# JWT Configuration from environment
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


class TokenData(BaseModel):
    """JWT Token payload structure."""
    sub: str  # user_id
    email: str
    tenant_id: str
    role: str
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None
    token_type: str = "access"  # "access" or "refresh"


class TokenPair(BaseModel):
    """Access and refresh token pair."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until access token expires


def create_access_token(user_id: str, email: str, tenant_id: str, role: str) -> str:
    """
    Create a JWT access token for authentication.
    
    Args:
        user_id: Unique user identifier
        email: User's email address
        tenant_id: Tenant identifier for multi-tenancy
        role: User's role (admin, owner, member)
    
    Returns:
        Encoded JWT token string
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": user_id,
        "email": email,
        "tenant_id": tenant_id,
        "role": role,
        "exp": expire,
        "iat": now,
        "token_type": "access"
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str, email: str, tenant_id: str, role: str) -> str:
    """
    Create a JWT refresh token for obtaining new access tokens.
    
    Args:
        user_id: Unique user identifier
        email: User's email address
        tenant_id: Tenant identifier for multi-tenancy
        role: User's role (admin, owner, member)
    
    Returns:
        Encoded JWT refresh token string
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub": user_id,
        "email": email,
        "tenant_id": tenant_id,
        "role": role,
        "exp": expire,
        "iat": now,
        "token_type": "refresh"
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_token_pair(user_id: str, email: str, tenant_id: str, role: str) -> TokenPair:
    """
    Create both access and refresh tokens for a user.
    
    Args:
        user_id: Unique user identifier
        email: User's email address
        tenant_id: Tenant identifier for multi-tenancy
        role: User's role (admin, owner, member)
    
    Returns:
        TokenPair containing both tokens and metadata
    """
    access_token = create_access_token(user_id, email, tenant_id, role)
    refresh_token = create_refresh_token(user_id, email, tenant_id, role)
    
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    )


def decode_token(token: str) -> Optional[TokenData]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string to decode
    
    Returns:
        TokenData if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Validate required fields
        if not all(key in payload for key in ["sub", "email", "tenant_id", "role"]):
            return None
        
        return TokenData(
            sub=payload["sub"],
            email=payload["email"],
            tenant_id=payload["tenant_id"],
            role=payload["role"],
            exp=payload.get("exp"),
            iat=payload.get("iat"),
            token_type=payload.get("token_type", "access")
        )
    except JWTError:
        return None


def verify_token(token: str, expected_type: str = "access") -> Optional[TokenData]:
    """
    Verify a token is valid and of the expected type.
    
    Args:
        token: JWT token string to verify
        expected_type: Expected token type ("access" or "refresh")
    
    Returns:
        TokenData if valid and correct type, None otherwise
    """
    token_data = decode_token(token)
    
    if not token_data:
        return None
    
    # Verify token type matches expected
    if token_data.token_type != expected_type:
        return None
    
    return token_data


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Generate a new access token from a valid refresh token.
    
    Args:
        refresh_token: Valid refresh token
    
    Returns:
        New access token if refresh token is valid, None otherwise
    """
    token_data = verify_token(refresh_token, expected_type="refresh")
    
    if not token_data:
        return None
    
    # Create new access token with same user data
    return create_access_token(
        user_id=token_data.sub,
        email=token_data.email,
        tenant_id=token_data.tenant_id,
        role=token_data.role
    )


def get_current_user_id(token: str) -> Optional[str]:
    """
    Extract user ID from a valid access token.
    
    Args:
        token: JWT access token
    
    Returns:
        User ID if token is valid, None otherwise
    """
    token_data = verify_token(token, expected_type="access")
    return token_data.sub if token_data else None