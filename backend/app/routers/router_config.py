"""
Router configuration for switching between stub and real implementations.

TODO: This configuration enables testing multi-tenancy with stubs.
Remove or update for production use.
"""

import os
from typing import Optional


def use_stub_routers() -> bool:
    """
    Determine whether to use stub routers for testing.
    
    TODO: Replace with proper configuration management.
    """
    # Check environment variable
    return os.getenv("USE_STUB_ROUTERS", "false").lower() == "true"


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


# Helper for logging which mode is active
def get_router_mode() -> str:
    """Get current router mode for logging."""
    return "STUB" if use_stub_routers() else "REAL"