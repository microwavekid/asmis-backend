"""
Authentication module for ASMIS backend.

This module supports both stub and real JWT authentication,
controlled by the USE_JWT_AUTH environment variable.
"""

from .models import AuthContext
from .stubs import get_auth_context_stub

# JWT authentication exports (available when USE_JWT_AUTH=true)
try:
    from .jwt_auth import (
        get_auth_context,
        get_auth_context_optional,
        get_current_user,
        require_role,
        require_admin,
        require_admin_or_owner,
        require_any_role
    )
    from .jwt_service import (
        create_token_pair,
        create_access_token,
        create_refresh_token,
        decode_token,
        verify_token,
        refresh_access_token,
        TokenPair,
        TokenData
    )
    from .auth_service import (
        authenticate_user,
        login_user,
        refresh_user_token,
        create_user,
        change_user_password,
        AuthenticationError,
        UserNotFoundError,
        InvalidCredentialsError,
        InactiveUserError,
        NoTenantAssociationError
    )
    from .password_service import (
        hash_password,
        verify_password,
        validate_password_strength,
        generate_temp_password
    )
    
    __all__ = [
        # Core models
        "AuthContext",
        
        # Stub auth (for testing)
        "get_auth_context_stub",
        
        # JWT auth dependencies
        "get_auth_context",
        "get_auth_context_optional",
        "get_current_user",
        "require_role",
        "require_admin",
        "require_admin_or_owner",
        "require_any_role",
        
        # JWT service
        "create_token_pair",
        "create_access_token",
        "create_refresh_token",
        "decode_token",
        "verify_token",
        "refresh_access_token",
        "TokenPair",
        "TokenData",
        
        # Auth service
        "authenticate_user",
        "login_user",
        "refresh_user_token",
        "create_user",
        "change_user_password",
        "AuthenticationError",
        "UserNotFoundError",
        "InvalidCredentialsError",
        "InactiveUserError",
        "NoTenantAssociationError",
        
        # Password service
        "hash_password",
        "verify_password",
        "validate_password_strength",
        "generate_temp_password"
    ]
except ImportError:
    # If JWT modules aren't available, just export stub functionality
    __all__ = ["AuthContext", "get_auth_context_stub"]