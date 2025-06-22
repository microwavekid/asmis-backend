"""Database connection management for ASMIS backend."""

import logging
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from .config import db_settings

logger = logging.getLogger(__name__)


class DatabaseConnectionManager:
    """Manages database connections with proper lifecycle management."""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize the connection manager.
        
        Args:
            database_url: Optional database URL override
        """
        self.database_url = database_url or db_settings.database_url
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker[Session]] = None
        
    def initialize(self) -> None:
        """Initialize the database engine and session factory."""
        try:
            # Configure engine based on database type
            if self.database_url.startswith("sqlite"):
                # SQLite-specific configuration
                self._engine = create_engine(
                    self.database_url,
                    echo=db_settings.database_echo,
                    poolclass=StaticPool,
                    connect_args={"check_same_thread": False},
                )
            else:
                # PostgreSQL configuration
                self._engine = create_engine(
                    self.database_url,
                    echo=db_settings.database_echo,
                    pool_size=db_settings.database_pool_size,
                    max_overflow=db_settings.database_pool_max_overflow,
                    pool_timeout=db_settings.database_pool_timeout,
                    pool_pre_ping=True,
                )
            
            # Create session factory
            self._session_factory = sessionmaker(
                self._engine,
                class_=Session,
                expire_on_commit=False,
            )
            
            logger.info(f"Database engine initialized for {self.database_url}")
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise
    
    def close(self) -> None:
        """Close the database engine."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database engine closed")
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session with automatic cleanup.
        
        Yields:
            Session: Database session
            
        Raises:
            RuntimeError: If the engine is not initialized
        """
        if not self._session_factory:
            raise RuntimeError("Database engine not initialized")
        
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    @property
    def engine(self) -> Engine:
        """Get the database engine.
        
        Returns:
            Engine: The database engine
            
        Raises:
            RuntimeError: If the engine is not initialized
        """
        if not self._engine:
            raise RuntimeError("Database engine not initialized")
        return self._engine


# Create a singleton instance for the application
db_manager = DatabaseConnectionManager()


# For testing purposes
def get_test_db_manager(database_url: str) -> DatabaseConnectionManager:
    """Create a test database manager with a custom URL.
    
    Args:
        database_url: Test database URL
        
    Returns:
        DatabaseConnectionManager: Test database manager
    """
    return DatabaseConnectionManager(database_url)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get a database session from the global manager.
    
    This is a convenience function for use in FastAPI dependencies.
    
    Yields:
        Session: Database session
    """
    with db_manager.get_session() as session:
        yield session