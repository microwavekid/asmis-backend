"""Database configuration for ASMIS backend."""

import os
import sys
import logging
from pydantic_settings import BaseSettings
from typing import Optional

logger = logging.getLogger(__name__)


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    # Database connection settings
    database_url: str = "sqlite:///./asmis.db"
    database_pool_size: int = 20
    database_pool_max_overflow: int = 10
    database_pool_timeout: int = 30
    database_echo: bool = False
    
    # Test database settings
    test_database_url: Optional[str] = "sqlite:///./test_asmis.db"
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        # Prefix for environment variables
        env_prefix = "ASMIS_DB_"


def validate_env_vars() -> None:
    """Validate required environment variables and database configuration.
    
    Raises:
        ValueError: If required environment variables are missing or invalid
        SystemExit: If validation fails in production environment
    """
    errors = []
    
    # Check if we're in production
    environment = os.getenv("ASMIS_ENVIRONMENT", "development").lower()
    
    if environment == "production":
        # In production, require explicit database URL
        database_url = os.getenv("ASMIS_DB_DATABASE_URL")
        if not database_url:
            errors.append("ASMIS_DB_DATABASE_URL is required in production")
        elif database_url.startswith("sqlite"):
            errors.append("SQLite is not recommended for production. Use PostgreSQL.")
        
        # Validate PostgreSQL URL format
        if database_url and not any(db in database_url for db in ["postgresql", "postgres"]):
            errors.append("Production database must be PostgreSQL")
    
    # Check for security issues
    database_url = os.getenv("ASMIS_DB_DATABASE_URL", "sqlite:///./asmis.db")
    if "password" in database_url.lower() or ":" in database_url.split("@")[0] if "@" in database_url else False:
        logger.warning("Database URL may contain credentials. Ensure secrets are properly managed.")
    
    # Validate pool settings
    try:
        pool_size = int(os.getenv("ASMIS_DB_DATABASE_POOL_SIZE", "20"))
        if pool_size < 1 or pool_size > 100:
            errors.append("Database pool size must be between 1 and 100")
    except ValueError:
        errors.append("ASMIS_DB_DATABASE_POOL_SIZE must be a valid integer")
    
    try:
        max_overflow = int(os.getenv("ASMIS_DB_DATABASE_POOL_MAX_OVERFLOW", "10"))
        if max_overflow < 0 or max_overflow > 50:
            errors.append("Database pool max overflow must be between 0 and 50")
    except ValueError:
        errors.append("ASMIS_DB_DATABASE_POOL_MAX_OVERFLOW must be a valid integer")
    
    # Report errors
    if errors:
        error_msg = "Database configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
        logger.error(error_msg)
        
        if environment == "production":
            # Fail fast in production
            print(f"FATAL: {error_msg}", file=sys.stderr)
            sys.exit(1)
        else:
            # Warn in development
            logger.warning("Continuing with default values in development mode")
            raise ValueError(error_msg)
    
    logger.info(f"Database configuration validated for {environment} environment")


def get_database_settings() -> DatabaseSettings:
    """Get validated database settings.
    
    Returns:
        DatabaseSettings: Validated database configuration
    """
    # Validate environment first
    validate_env_vars()
    
    # Return settings
    return DatabaseSettings()


# Create a singleton instance with validation
db_settings = get_database_settings()