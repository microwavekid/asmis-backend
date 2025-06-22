# Database Setup Guide

## Overview
ASMIS uses SQLAlchemy with Alembic for database management. The system supports both SQLite (development) and PostgreSQL (production) databases.

## Quick Start

### 1. Environment Configuration
Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```bash
# Development (default)
ASMIS_ENVIRONMENT=development
ASMIS_DB_DATABASE_URL=sqlite:///./asmis.db

# Production
ASMIS_ENVIRONMENT=production
ASMIS_DB_DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/asmis_prod
```

### 2. Initialize Database
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Test the setup
python test_database.py
```

## Environment Variables

### Required Variables
- `ASMIS_ENVIRONMENT`: Environment name (`development`, `staging`, `production`)
- `ASMIS_DB_DATABASE_URL`: Database connection URL

### Optional Variables
- `ASMIS_DB_DATABASE_POOL_SIZE`: Connection pool size (default: 20)
- `ASMIS_DB_DATABASE_POOL_MAX_OVERFLOW`: Max overflow connections (default: 10)
- `ASMIS_DB_DATABASE_POOL_TIMEOUT`: Connection timeout in seconds (default: 30)
- `ASMIS_DB_DATABASE_ECHO`: Enable SQL logging (default: false)

## Database Schema

### Core Tables
1. **prompt_templates**: AI prompt templates with versioning
2. **prompt_versions**: Version history for templates
3. **agent_configurations**: Agent-specific settings
4. **processing_sessions**: Execution tracking and analytics

### Key Features
- **UUID Primary Keys**: For distributed system compatibility
- **Automatic Timestamps**: Created/updated tracking
- **Soft Deletion**: Preserve data integrity
- **JSON Metadata**: Flexible configuration storage
- **Proper Indexing**: Optimized query performance

## Development Workflow

### Database Changes
1. Modify models in `app/database/models.py`
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Review the generated migration file
4. Apply migration: `alembic upgrade head`

### Testing
```bash
# Run database tests
python test_database.py

# Test specific functionality
python -c "from app.database.repository import prompt_template_repo; print('Repository loaded')"
```

## Production Deployment

### Security Checklist
- [ ] Never commit `.env` files
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set `ASMIS_ENVIRONMENT=production`
- [ ] Use proper secrets management
- [ ] Validate environment variables on startup

### Database Setup
1. Create PostgreSQL database
2. Set connection URL in environment
3. Run migrations: `alembic upgrade head`
4. Verify connectivity

## Repository Pattern

### Usage Example
```python
from app.database.connection import db_manager
from app.database.repository import prompt_template_repo

# Initialize connection
db_manager.initialize()

# Use repository
with db_manager.get_session() as session:
    template = prompt_template_repo.create(
        session,
        name="My Template",
        content="Template content...",
        agent_type="meddpic"
    )
    print(f"Created template: {template.id}")
```

### Available Repositories
- `prompt_template_repo`: Prompt template operations
- `prompt_version_repo`: Version management
- `agent_config_repo`: Agent configuration
- `processing_session_repo`: Session tracking

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure all dependencies are installed
2. **Migration conflicts**: Check for model changes without migrations
3. **Connection errors**: Verify database URL and credentials
4. **Permission errors**: Ensure database user has proper permissions

### Error Messages
- `Database engine not initialized`: Call `db_manager.initialize()` first
- `UNIQUE constraint failed`: Duplicate data violates constraints
- `Validation failed`: Check environment variables

## Future Enhancements
- [ ] Async SQLAlchemy support
- [ ] Connection pooling optimization
- [ ] Performance monitoring
- [ ] Automated backup strategies