"""
Authentication module for ASMIS backend.
TODO: This module currently contains stub implementations for early integration testing.
Real JWT authentication will be implemented in Phase 3.
"""

from .models import AuthContext
from .stubs import get_auth_context_stub

__all__ = ["AuthContext", "get_auth_context_stub"]