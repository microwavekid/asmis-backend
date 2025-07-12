"""
Password Hashing Service for ASMIS Authentication.

This module handles secure password hashing and verification
using bcrypt with proper salt generation.
"""

from passlib.context import CryptContext
from typing import Optional

# Create password context with bcrypt scheme
# Cost factor of 12 provides good security/performance balance
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    Args:
        password: Plain text password to hash
    
    Returns:
        Hashed password string safe for database storage
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database
    
    Returns:
        True if password matches, False otherwise
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Handle any verification errors (e.g., invalid hash format)
        return False


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password meets security requirements.
    
    Requirements:
    - Minimum 12 characters
    - Contains uppercase and lowercase letters
    - Contains at least one number
    - Contains at least one special character
    
    Args:
        password: Password to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "Password must contain at least one special character"
    
    return True, None


def needs_rehash(hashed_password: str) -> bool:
    """
    Check if a hashed password needs to be rehashed.
    
    This is useful when upgrading hashing algorithms or
    increasing cost factors.
    
    Args:
        hashed_password: Current hashed password
    
    Returns:
        True if password should be rehashed, False otherwise
    """
    return pwd_context.needs_update(hashed_password)


def generate_temp_password() -> str:
    """
    Generate a temporary password for initial user setup.
    
    This should only be used for MVP admin-provisioned accounts
    and users should be required to change it on first login.
    
    Returns:
        Temporary password string
    """
    import secrets
    import string
    
    # Generate a secure random password
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(16))
    
    # Ensure it meets our requirements
    # Add guaranteed uppercase, lowercase, digit, and special char
    password = (
        secrets.choice(string.ascii_uppercase) +
        secrets.choice(string.ascii_lowercase) +
        secrets.choice(string.digits) +
        secrets.choice("!@#$%^&*") +
        password[4:]
    )
    
    # Shuffle to avoid predictable pattern
    password_list = list(password)
    for i in range(len(password_list)):
        j = secrets.randbelow(len(password_list))
        password_list[i], password_list[j] = password_list[j], password_list[i]
    
    return ''.join(password_list)