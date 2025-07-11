"""
JWT Authentication Stubs for ASMIS Multi-Tenancy Integration Testing.

TODO: This is a STUB implementation for early integration testing.
Real JWT authentication will be implemented in Phase 3 (MIC-68).

Purpose: Enable end-to-end testing of tenant isolation before implementing
real JWT token validation and authentication middleware.
"""

from typing import Dict, Any, Optional
from fastapi import Request, HTTPException
from .models import AuthContext


# Hardcoded test tenants for integration testing
STUB_TENANTS = {
    "acme-corp": "550e8400-e29b-41d4-a716-446655440001",
    "beta-industries": "550e8400-e29b-41d4-a716-446655440002",
    "gamma-solutions": "550e8400-e29b-41d4-a716-446655440003"
}

# Hardcoded test users for integration testing
STUB_USERS = {
    "alice@acme.com": {
        "user_id": "550e8400-e29b-41d4-a716-446655440101",
        "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
        "role": "admin"
    },
    "bob@acme.com": {
        "user_id": "550e8400-e29b-41d4-a716-446655440102", 
        "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
        "role": "member"
    },
    "david@beta.com": {
        "user_id": "550e8400-e29b-41d4-a716-446655440201",
        "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
        "role": "owner"
    },
    "frank@gamma.com": {
        "user_id": "550e8400-e29b-41d4-a716-446655440301",
        "tenant_id": "550e8400-e29b-41d4-a716-446655440003",
        "role": "member"
    }
}


async def get_auth_context_stub(request: Request) -> AuthContext:
    """
    STUB: Extract authentication context from request.
    
    TODO: Replace with real JWT validation in Phase 3.
    
    For testing, this function:
    1. Checks Authorization header for user hint
    2. Returns hardcoded tenant context
    3. Defaults to alice@acme.com if no header
    
    Real implementation will:
    1. Extract JWT from Authorization header
    2. Validate JWT signature and expiration
    3. Return actual user/tenant from token payload
    """
    
    # Extract Authorization header
    auth_header = request.headers.get("Authorization")
    
    # Default to alice@acme.com for testing
    default_email = "alice@acme.com"
    
    # Check for user hint in Authorization header
    # Format: "Bearer stub-token-{email}"
    if auth_header and auth_header.startswith("Bearer stub-token-"):
        email_hint = auth_header.replace("Bearer stub-token-", "")
        if email_hint in STUB_USERS:
            user_data = STUB_USERS[email_hint]
            return AuthContext(
                user_id=user_data["user_id"],
                tenant_id=user_data["tenant_id"],
                email=email_hint,
                role=user_data["role"]
            )
    
    # Return default user for testing
    user_data = STUB_USERS[default_email]
    return AuthContext(
        user_id=user_data["user_id"],
        tenant_id=user_data["tenant_id"],
        email=default_email,
        role=user_data["role"]
    )


def get_stub_tenant_id(tenant_slug: str) -> Optional[str]:
    """
    STUB: Helper function to get tenant ID from slug.
    TODO: Replace with real tenant lookup in Phase 3.
    """
    return STUB_TENANTS.get(tenant_slug)


def get_stub_user_context(email: str) -> Optional[Dict[str, Any]]:
    """
    STUB: Helper function to get user context from email.
    TODO: Replace with real user lookup in Phase 3.
    """
    return STUB_USERS.get(email)