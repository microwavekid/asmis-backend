# Architectural Patterns

> Part of the ASMIS Project Intelligence System
> Last Updated: 2024-12-17
> These patterns are discovered and proven solutions from the ASMIS project

## Database Access Pattern
**Problem**: Need consistent database access across all services with proper connection management, error handling, and type safety
**Solution**: Repository pattern with connection pooling, comprehensive error handling, and structured data models
**When to use**: All database operations, especially when dealing with multiple entity types or complex queries

### Core Pattern Structure

```python
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import asyncpg
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@dataclass
class Prompt:
    """Data model for prompt entities."""
    id: str
    name: str
    content: str
    version: str
    agent_type: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]
    is_active: bool = True

class DatabaseConnectionPool:
    """Manages database connection pool with proper lifecycle management."""
    
    def __init__(self, database_url: str, min_size: int = 5, max_size: int = 20):
        self.database_url = database_url
        self.min_size = min_size
        self.max_size = max_size
        self._pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize the connection pool."""
        try:
            self._pool = await asyncpg.create_pool(
                self.database_url,
                min_size=self.min_size,
                max_size=self.max_size,
                command_timeout=30,
                server_settings={
                    'application_name': 'asmis_backend'
                }
            )
            logger.info(f"Database pool initialized with {self.min_size}-{self.max_size} connections")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def close(self):
        """Close the connection pool."""
        if self._pool:
            await self._pool.close()
            logger.info("Database pool closed")
    
    @asynccontextmanager
    async def acquire(self):
        """Acquire a connection from the pool with automatic cleanup."""
        if not self._pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self._pool.acquire() as conn:
            try:
                yield conn
            except Exception as e:
                logger.error(f"Database operation failed: {e}")
                raise

class PromptRepository:
    """Repository for prompt data access with comprehensive error handling."""
    
    def __init__(self, db_pool: DatabaseConnectionPool):
        self.db_pool = db_pool
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """
        Retrieve a prompt by ID with proper error handling.
        
        Args:
            prompt_id: Unique identifier for the prompt
            
        Returns:
            Prompt object if found, None otherwise
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT id, name, content, version, agent_type, 
                           created_at, updated_at, metadata, is_active
                    FROM prompts 
                    WHERE id = $1 AND is_active = true
                    """,
                    prompt_id
                )
                
                if row:
                    return Prompt(
                        id=row['id'],
                        name=row['name'],
                        content=row['content'],
                        version=row['version'],
                        agent_type=row['agent_type'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at'],
                        metadata=row['metadata'],
                        is_active=row['is_active']
                    )
                return None
                
        except asyncpg.PostgresError as e:
            self.logger.error(f"Database error retrieving prompt {prompt_id}: {e}")
            raise DatabaseError(f"Failed to retrieve prompt: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error retrieving prompt {prompt_id}: {e}")
            raise DatabaseError(f"Unexpected error: {e}")
    
    async def get_prompts_by_agent_type(self, agent_type: str) -> List[Prompt]:
        """
        Retrieve all active prompts for a specific agent type.
        
        Args:
            agent_type: Type of agent (e.g., 'meddpic', 'stakeholder')
            
        Returns:
            List of Prompt objects
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT id, name, content, version, agent_type, 
                           created_at, updated_at, metadata, is_active
                    FROM prompts 
                    WHERE agent_type = $1 AND is_active = true
                    ORDER BY updated_at DESC
                    """,
                    agent_type
                )
                
                return [
                    Prompt(
                        id=row['id'],
                        name=row['name'],
                        content=row['content'],
                        version=row['version'],
                        agent_type=row['agent_type'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at'],
                        metadata=row['metadata'],
                        is_active=row['is_active']
                    )
                    for row in rows
                ]
                
        except asyncpg.PostgresError as e:
            self.logger.error(f"Database error retrieving prompts for agent {agent_type}: {e}")
            raise DatabaseError(f"Failed to retrieve prompts: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error retrieving prompts for agent {agent_type}: {e}")
            raise DatabaseError(f"Unexpected error: {e}")
    
    async def create_prompt(self, prompt: Prompt) -> Prompt:
        """
        Create a new prompt with validation and error handling.
        
        Args:
            prompt: Prompt object to create
            
        Returns:
            Created Prompt object with generated ID
            
        Raises:
            ValidationError: If prompt data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate required fields
            if not prompt.name or not prompt.content or not prompt.agent_type:
                raise ValidationError("Name, content, and agent_type are required")
            
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    INSERT INTO prompts (name, content, version, agent_type, metadata, is_active)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id, name, content, version, agent_type, 
                              created_at, updated_at, metadata, is_active
                    """,
                    prompt.name,
                    prompt.content,
                    prompt.version,
                    prompt.agent_type,
                    prompt.metadata,
                    prompt.is_active
                )
                
                return Prompt(
                    id=row['id'],
                    name=row['name'],
                    content=row['content'],
                    version=row['version'],
                    agent_type=row['agent_type'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    metadata=row['metadata'],
                    is_active=row['is_active']
                )
                
        except asyncpg.UniqueViolationError as e:
            self.logger.error(f"Duplicate prompt name: {e}")
            raise ValidationError("A prompt with this name already exists")
        except asyncpg.PostgresError as e:
            self.logger.error(f"Database error creating prompt: {e}")
            raise DatabaseError(f"Failed to create prompt: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error creating prompt: {e}")
            raise DatabaseError(f"Unexpected error: {e}")

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

### Usage Example

```python
# Initialize database connection
db_pool = DatabaseConnectionPool(
    database_url="postgresql://user:pass@localhost/asmis",
    min_size=5,
    max_size=20
)

# Initialize repository
prompt_repo = PromptRepository(db_pool)

# Usage in FastAPI endpoint
@app.get("/prompts/{prompt_id}")
async def get_prompt(prompt_id: str):
    try:
        prompt = await prompt_repo.get_prompt(prompt_id)
        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return prompt
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

### Benefits of This Pattern

1. **Connection Pooling**: Efficient database connection management
2. **Error Handling**: Comprehensive error handling with custom exceptions
3. **Type Safety**: Full type hints and data models
4. **Logging**: Proper logging for debugging and monitoring
5. **Context Management**: Automatic connection cleanup
6. **Validation**: Input validation and business rule enforcement
7. **Testability**: Easy to mock and test in isolation

### When to Use This Pattern

- ✅ All database operations in the application
- ✅ When you need consistent error handling
- ✅ When working with multiple entity types
- ✅ When you need connection pooling for performance
- ✅ When you want type-safe database operations

### Related Patterns

- **Unit of Work**: For transaction management across multiple repositories
- **Specification Pattern**: For complex query building
- **Caching Pattern**: For frequently accessed data
- **Migration Pattern**: For database schema evolution

Tags: #database #repository #async #connection-pooling #error-handling #type-safety

---

## Agent Communication Pattern
**Problem**: Need consistent communication between AI agents with proper error handling, retry logic, and result standardization
**Solution**: Base agent class with standardized communication protocol, error handling, and result formatting
**When to use**: All AI agent implementations, especially when agents need to communicate with each other

### Core Pattern Structure

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging
import asyncio
from enum import Enum

logger = logging.getLogger(__name__)

class ProcessingStatus(Enum):
    """Standard processing status values."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class AgentResult:
    """Standardized result format for all agents."""
    status: ProcessingStatus
    data: Dict[str, Any]
    confidence_score: float
    processing_time: float
    timestamp: datetime
    metadata: Dict[str, Any]
    errors: List[str] = None
    warnings: List[str] = None

class BaseAgent(ABC):
    """Base class for all AI agents with standardized communication protocol."""
    
    def __init__(self, api_key: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the base agent.
        
        Args:
            api_key: API key for AI services
            config: Optional configuration overrides
        """
        self.api_key = api_key
        self.config = self._get_default_config()
        if config:
            self.config.update(config)
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self._initialize_client()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for the agent."""
        return {
            "max_retries": 3,
            "retry_delay": 1.0,
            "timeout": 60,
            "confidence_threshold": 0.7,
            "enable_logging": True,
            "model": "claude-3-5-sonnet-20241022"
        }
    
    def _initialize_client(self):
        """Initialize the AI client (to be implemented by subclasses)."""
        try:
            # Initialize client based on configuration
            pass
        except Exception as e:
            self.logger.error(f"Failed to initialize client: {e}")
            raise
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Process input data with standardized error handling and retry logic.
        
        Args:
            input_data: Input data for processing
            
        Returns:
            AgentResult with standardized format
        """
        start_time = datetime.utcnow()
        attempt = 0
        last_error = None
        
        while attempt < self.config["max_retries"]:
            try:
                attempt += 1
                self.logger.info(f"Processing attempt {attempt}/{self.config['max_retries']}")
                
                # Validate input
                self._validate_input(input_data)
                
                # Process with timeout
                result = await asyncio.wait_for(
                    self._process_impl(input_data),
                    timeout=self.config["timeout"]
                )
                
                # Calculate processing time
                processing_time = (datetime.utcnow() - start_time).total_seconds()
                
                # Build result
                return AgentResult(
                    status=ProcessingStatus.COMPLETED,
                    data=result,
                    confidence_score=self._calculate_confidence(result),
                    processing_time=processing_time,
                    timestamp=datetime.utcnow(),
                    metadata={
                        "agent_type": self.__class__.__name__,
                        "attempts": attempt,
                        "config": self.config
                    }
                )
                
            except asyncio.TimeoutError:
                last_error = f"Processing timeout after {self.config['timeout']} seconds"
                self.logger.warning(f"Timeout on attempt {attempt}: {last_error}")
                
            except Exception as e:
                last_error = str(e)
                self.logger.error(f"Error on attempt {attempt}: {e}")
                
            # Wait before retry
            if attempt < self.config["max_retries"]:
                await asyncio.sleep(self.config["retry_delay"] * attempt)
        
        # All attempts failed
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        return AgentResult(
            status=ProcessingStatus.FAILED,
            data={},
            confidence_score=0.0,
            processing_time=processing_time,
            timestamp=datetime.utcnow(),
            metadata={
                "agent_type": self.__class__.__name__,
                "attempts": attempt,
                "config": self.config
            },
            errors=[last_error] if last_error else []
        )
    
    @abstractmethod
    async def _process_impl(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement the actual processing logic.
        
        Args:
            input_data: Input data for processing
            
        Returns:
            Processed result data
        """
        pass
    
    def _validate_input(self, input_data: Dict[str, Any]):
        """Validate input data (can be overridden by subclasses)."""
        if not isinstance(input_data, dict):
            raise ValueError("Input data must be a dictionary")
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score for the result (can be overridden)."""
        # Default confidence calculation
        return 0.8  # Default confidence score
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the agent."""
        try:
            # Basic health check - can be overridden
            return {
                "status": "healthy",
                "agent_type": self.__class__.__name__,
                "config": self.config,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "agent_type": self.__class__.__name__,
                "timestamp": datetime.utcnow().isoformat()
            }
```

### Usage Example

```python
class MEDDPICAgent(BaseAgent):
    """Example implementation of a MEDDPIC analysis agent."""
    
    async def _process_impl(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implement MEDDPIC analysis logic."""
        content = input_data.get("content")
        if not content:
            raise ValueError("Content is required for MEDDPIC analysis")
        
        # Perform MEDDPIC analysis
        analysis_result = await self._analyze_meddpic(content)
        
        return {
            "meddpic_analysis": analysis_result,
            "extraction_method": "claude_analysis",
            "source_type": input_data.get("source_type", "unknown")
        }
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence based on analysis completeness."""
        analysis = result.get("meddpic_analysis", {})
        required_fields = ["metrics", "economic_buyer", "decision_criteria"]
        
        completed_fields = sum(1 for field in required_fields if analysis.get(field))
        return completed_fields / len(required_fields)

# Usage
agent = MEDDPICAgent(api_key="your-api-key")
result = await agent.process({
    "content": "Meeting transcript content...",
    "source_type": "transcript"
})

if result.status == ProcessingStatus.COMPLETED:
    print(f"Analysis completed with {result.confidence_score:.2f} confidence")
else:
    print(f"Analysis failed: {result.errors}")
```

### Benefits of This Pattern

1. **Standardized Communication**: Consistent result format across all agents
2. **Error Handling**: Built-in retry logic and error recovery
3. **Monitoring**: Comprehensive logging and health checks
4. **Configurability**: Flexible configuration for different use cases
5. **Timeout Management**: Prevents hanging operations
6. **Confidence Scoring**: Standardized confidence calculation
7. **Extensibility**: Easy to add new agents following the same pattern

### When to Use This Pattern

- ✅ All AI agent implementations
- ✅ When agents need to communicate with each other
- ✅ When you need consistent error handling
- ✅ When you want standardized result formats
- ✅ When you need retry logic for reliability

Tags: #agent #communication #error-handling #retry-logic #standardization

---

## Caching Pattern
**Problem**: Need to cache expensive operations (AI calls, database queries) to improve performance and reduce costs
**Solution**: Multi-level caching with TTL, invalidation strategies, and cache warming
**When to use**: Expensive operations, frequently accessed data, AI API calls

### Core Pattern Structure

```python
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
import asyncio
import hashlib
import json
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class CacheEntry:
    """Represents a cached item with metadata."""
    
    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.created_at = datetime.utcnow()
        self.ttl_seconds = ttl_seconds
    
    def is_expired(self) -> bool:
        """Check if the cache entry has expired."""
        return (datetime.utcnow() - self.created_at).total_seconds() > self.ttl_seconds
    
    def get_age_seconds(self) -> float:
        """Get the age of the cache entry in seconds."""
        return (datetime.utcnow() - self.created_at).total_seconds()

class MemoryCache:
    """In-memory cache with TTL and size limits."""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheEntry] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if entry.is_expired():
            del self._cache[key]
            return None
        
        return entry.value
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set a value in cache."""
        if len(self._cache) >= self.max_size:
            self._evict_oldest()
        
        ttl = ttl_seconds or self.default_ttl
        self._cache[key] = CacheEntry(value, ttl)
    
    def delete(self, key: str) -> None:
        """Delete a key from cache."""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
    
    def _evict_oldest(self) -> None:
        """Evict the oldest cache entry."""
        if not self._cache:
            return
        
        oldest_key = min(self._cache.keys(), 
                        key=lambda k: self._cache[k].created_at)
        del self._cache[oldest_key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_entries = len(self._cache)
        expired_entries = sum(1 for entry in self._cache.values() 
                            if entry.is_expired())
        
        return {
            "total_entries": total_entries,
            "expired_entries": expired_entries,
            "max_size": self.max_size,
            "utilization": total_entries / self.max_size if self.max_size > 0 else 0
        }

def cache_result(ttl_seconds: int = 300, key_prefix: str = ""):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            
            cache_key = hashlib.md5(
                json.dumps(key_parts, sort_keys=True).encode()
            ).hexdigest()
            
            # Check cache
            cache = getattr(wrapper, '_cache', None)
            if cache is None:
                cache = MemoryCache()
                wrapper._cache = cache
            
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        return wrapper
    return decorator

class CacheManager:
    """Manages multiple cache layers and strategies."""
    
    def __init__(self):
        self.memory_cache = MemoryCache(max_size=1000, default_ttl=300)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def get_or_set(self, key: str, getter_func, ttl_seconds: int = 300) -> Any:
        """
        Get value from cache or compute and store it.
        
        Args:
            key: Cache key
            getter_func: Async function to compute value if not cached
            ttl_seconds: Time to live for the cached value
            
        Returns:
            Cached or computed value
        """
        # Try memory cache first
        cached_value = self.memory_cache.get(key)
        if cached_value is not None:
            return cached_value
        
        # Compute and cache
        try:
            value = await getter_func()
            self.memory_cache.set(key, value, ttl_seconds)
            return value
        except Exception as e:
            self.logger.error(f"Error computing value for key {key}: {e}")
            raise
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching a pattern."""
        keys_to_delete = [key for key in self.memory_cache._cache.keys() 
                         if pattern in key]
        
        for key in keys_to_delete:
            self.memory_cache.delete(key)
        
        return len(keys_to_delete)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        return {
            "memory_cache": self.memory_cache.get_stats(),
            "total_invalidations": 0  # Could track this over time
        }
```

### Usage Example

```python
# Using the cache decorator
@cache_result(ttl_seconds=600, key_prefix="meddpic")
async def analyze_meddpic(content: str, source_type: str) -> Dict[str, Any]:
    """Expensive MEDDPIC analysis with caching."""
    # Expensive AI operation
    result = await ai_client.analyze(content)
    return result

# Using the cache manager
cache_manager = CacheManager()

async def get_prompt_with_cache(prompt_id: str) -> Dict[str, Any]:
    """Get prompt with caching."""
    async def fetch_prompt():
        # Expensive database operation
        return await prompt_repository.get_prompt(prompt_id)
    
    return await cache_manager.get_or_set(
        key=f"prompt:{prompt_id}",
        getter_func=fetch_prompt,
        ttl_seconds=300
    )

# Cache invalidation
cache_manager.invalidate_pattern("prompt:")  # Invalidate all prompts
```

### Benefits of This Pattern

1. **Performance**: Reduces expensive operation costs
2. **Cost Reduction**: Fewer AI API calls
3. **Scalability**: Handles high-traffic scenarios
4. **Flexibility**: Multiple cache layers and strategies
5. **Monitoring**: Cache statistics and hit rates
6. **TTL Management**: Automatic expiration of stale data
7. **Pattern Invalidation**: Bulk cache invalidation

### When to Use This Pattern

- ✅ Expensive AI API calls
- ✅ Database queries with stable results
- ✅ Computationally expensive operations
- ✅ Frequently accessed data
- ✅ When you need to reduce costs

Tags: #caching #performance #cost-optimization #ttl #invalidation