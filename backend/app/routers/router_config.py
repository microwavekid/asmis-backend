"""
Router configuration for switching between stub and real implementations.

This configuration enables switching between stub and real authentication
as well as stub and real routers for testing and production.
"""

import os
from typing import Optional, Callable
from fastapi import Depends

from ..auth.models import AuthContext


def use_stub_routers() -> bool:
    """
    Determine whether to use stub routers for testing.
    """
    return os.getenv("USE_STUB_ROUTERS", "false").lower() == "true"


def use_jwt_auth() -> bool:
    """
    Determine whether to use real JWT authentication or stubs.
    
    Returns:
        True to use real JWT auth, False to use stub auth
    """
    return os.getenv("USE_JWT_AUTH", "false").lower() == "true"


def get_deals_router():
    """
    Get the appropriate deals router based on configuration.
    
    Returns:
        Either the stub router for testing or real router for production.
    """
    if use_stub_routers():
        from .deals_stub import router as deals_stub_router
        return deals_stub_router
    else:
        from .deals import router as deals_router
        return deals_router


def get_auth_dependency() -> Callable:
    """
    Get the appropriate authentication dependency based on configuration.
    
    Returns:
        Either JWT auth dependency or stub auth dependency
    """
    if use_jwt_auth():
        from ..auth.jwt_auth import get_auth_context
        return get_auth_context
    else:
        from ..auth.stubs import get_auth_context_stub
        return get_auth_context_stub


def get_optional_auth_dependency() -> Callable:
    """
    Get the appropriate optional authentication dependency.
    
    Returns:
        Either JWT optional auth or stub optional auth
    """
    if use_jwt_auth():
        from ..auth.jwt_auth import get_auth_context_optional
        return get_auth_context_optional
    else:
        # Stub doesn't have optional, so return regular stub
        from ..auth.stubs import get_auth_context_stub
        return get_auth_context_stub


# Helper for logging which mode is active
def get_router_mode() -> str:
    """Get current router mode for logging."""
    return "STUB" if use_stub_routers() else "REAL"


def get_auth_mode() -> str:
    """Get current authentication mode for logging."""
    return "JWT" if use_jwt_auth() else "STUB"