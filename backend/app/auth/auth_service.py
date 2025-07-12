"""
User Authentication Service for ASMIS.

This module handles user authentication operations including
login, token management, and user verification.
"""

from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone

from ..database.models import User, TenantUser
from .jwt_service import create_token_pair, TokenPair, refresh_access_token
from .password_service import verify_password, hash_password, validate_password_strength
from .models import AuthContext


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class UserNotFoundError(AuthenticationError):
    """Raised when user is not found."""
    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when credentials are invalid."""
    pass


class InactiveUserError(AuthenticationError):
    """Raised when user account is inactive."""
    pass


class NoTenantAssociationError(AuthenticationError):
    """Raised when user has no tenant association."""
    pass


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> Tuple[User, TenantUser]:
    """
    Authenticate a user with email and password.
    
    Args:
        db: Database session
        email: User's email address
        password: Plain text password
    
    Returns:
        Tuple of (User, TenantUser) if authentication succeeds
    
    Raises:
        UserNotFoundError: If user doesn't exist
        InvalidCredentialsError: If password is incorrect
        InactiveUserError: If user account is inactive
        NoTenantAssociationError: If user has no tenant
    """
    # Find user by email
    user = db.query(User).filter(
        User.email == email,
        User.is_active == True
    ).first()
    
    if not user:
        raise UserNotFoundError(f"No user found with email: {email}")
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError("Invalid password")
    
    # Check if user is active
    if not user.is_active:
        raise InactiveUserError("User account is inactive")
    
    # Get tenant association
    tenant_user = db.query(TenantUser).filter(
        TenantUser.user_id == user.id
    ).first()
    
    if not tenant_user:
        raise NoTenantAssociationError("User has no tenant association")
    
    # Update last login timestamp
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    
    return user, tenant_user


def login_user(
    db: Session,
    email: str,
    password: str
) -> Tuple[TokenPair, AuthContext]:
    """
    Authenticate user and generate JWT tokens.
    
    Args:
        db: Database session
        email: User's email address
        password: Plain text password
    
    Returns:
        Tuple of (TokenPair, AuthContext) containing tokens and user info
    
    Raises:
        AuthenticationError: If authentication fails for any reason
    """
    # Authenticate user
    user, tenant_user = authenticate_user(db, email, password)
    
    # Create JWT tokens
    token_pair = create_token_pair(
        user_id=str(user.id),
        email=user.email,
        tenant_id=str(tenant_user.tenant_id),
        role=tenant_user.role
    )
    
    # Create auth context
    auth_context = AuthContext(
        user_id=str(user.id),
        tenant_id=str(tenant_user.tenant_id),
        email=user.email,
        role=tenant_user.role
    )
    
    return token_pair, auth_context


def refresh_user_token(
    db: Session,
    refresh_token: str
) -> Optional[str]:
    """
    Generate new access token from refresh token.
    
    Args:
        db: Database session
        refresh_token: Valid refresh token
    
    Returns:
        New access token if refresh is valid, None otherwise
    """
    # Use jwt_service to handle refresh
    new_access_token = refresh_access_token(refresh_token)
    
    if new_access_token:
        # Could add additional validation here, like checking
        # if user is still active in database
        return new_access_token
    
    return None


def create_user(
    db: Session,
    email: str,
    username: str,
    password: str,
    tenant_id: str,
    role: str = "member"
) -> User:
    """
    Create a new user with tenant association.
    
    This is primarily for admin-provisioned accounts in MVP.
    
    Args:
        db: Database session
        email: User's email address
        username: User's username
        password: Plain text password (will be hashed)
        tenant_id: Tenant to associate user with
        role: User's role in the tenant
    
    Returns:
        Created User object
    
    Raises:
        ValueError: If user already exists or validation fails
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()
    
    if existing_user:
        raise ValueError("User with this email or username already exists")
    
    # Validate password strength
    is_valid, error_msg = validate_password_strength(password)
    if not is_valid:
        raise ValueError(f"Password validation failed: {error_msg}")
    
    # Create user
    user = User(
        email=email,
        username=username,
        hashed_password=hash_password(password),
        is_active=True
    )
    db.add(user)
    db.flush()  # Get user ID
    
    # Create tenant association
    tenant_user = TenantUser(
        user_id=user.id,
        tenant_id=tenant_id,
        role=role
    )
    db.add(tenant_user)
    
    db.commit()
    db.refresh(user)
    
    return user


def change_user_password(
    db: Session,
    user_id: str,
    current_password: str,
    new_password: str
) -> bool:
    """
    Change a user's password.
    
    Args:
        db: Database session
        user_id: User's ID
        current_password: Current password for verification
        new_password: New password to set
    
    Returns:
        True if password changed successfully
    
    Raises:
        UserNotFoundError: If user doesn't exist
        InvalidCredentialsError: If current password is wrong
        ValueError: If new password doesn't meet requirements
    """
    # Get user
    user = db.query(User).filter(
        User.id == user_id,
        User.is_active == True
    ).first()
    
    if not user:
        raise UserNotFoundError("User not found")
    
    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        raise InvalidCredentialsError("Current password is incorrect")
    
    # Validate new password
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        raise ValueError(f"New password validation failed: {error_msg}")
    
    # Update password
    user.hashed_password = hash_password(new_password)
    user.password_changed_at = datetime.now(timezone.utc)
    
    db.commit()
    return True