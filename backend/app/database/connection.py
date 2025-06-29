"""Database connection management for ASMIS backend."""

import logging
from contextlib import contextmanager, asynccontextmanager
from typing import Generator, Optional, AsyncGenerator

from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
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


class AsyncDatabaseConnectionManager:
    """Async database connection manager for FastAPI."""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize the async connection manager."""
        self.database_url = database_url or db_settings.database_url
        # Convert sync URL to async URL
        if self.database_url.startswith("sqlite"):
            self.async_database_url = self.database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
        elif self.database_url.startswith("postgresql"):
            self.async_database_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://")
        else:
            self.async_database_url = self.database_url
            
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None
        
    def initialize(self) -> None:
        """Initialize the async database engine and session factory."""
        try:
            # Configure async engine
            if self.async_database_url.startswith("sqlite"):
                # SQLite async configuration
                self._engine = create_async_engine(
                    self.async_database_url,
                    echo=db_settings.database_echo,
                    poolclass=StaticPool,
                    connect_args={"check_same_thread": False},
                )
            else:
                # PostgreSQL async configuration
                self._engine = create_async_engine(
                    self.async_database_url,
                    echo=db_settings.database_echo,
                    pool_size=db_settings.database_pool_size,
                    max_overflow=db_settings.database_pool_max_overflow,
                    pool_timeout=db_settings.database_pool_timeout,
                    pool_pre_ping=True,
                )
            
            # Create async session factory
            self._session_factory = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            
            logger.info(f"Async database engine initialized for {self.async_database_url}")
        except Exception as e:
            logger.error(f"Failed to initialize async database engine: {e}")
            raise
    
    async def close(self) -> None:
        """Close the async database engine."""
        if self._engine:
            await self._engine.dispose()
            logger.info("Async database engine closed")
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get an async database session with automatic cleanup."""
        if not self._session_factory:
            raise RuntimeError("Async database engine not initialized")
        
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    
    @property
    def engine(self) -> AsyncEngine:
        """Get the async database engine."""
        if not self._engine:
            raise RuntimeError("Async database engine not initialized")
        return self._engine


# Create singleton instances for the application
db_manager = DatabaseConnectionManager()
async_db_manager = AsyncDatabaseConnectionManager()


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


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session for FastAPI dependencies.
    
    Yields:
        AsyncSession: Async database session
    """
    async with async_db_manager.get_session() as session:
        yield session