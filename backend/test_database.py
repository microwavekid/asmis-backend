"""Test script for database layer functionality."""

import logging
from datetime import datetime

from app.database.connection import db_manager
from app.database.repository import prompt_template_repo, prompt_version_repo
from app.database.models import PromptTemplate, PromptVersion

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_database_connection():
    """Test basic database connection and operations."""
    try:
        # Initialize the database connection
        db_manager.initialize()
        logger.info("✅ Database connection initialized successfully")
        
        # Test creating a prompt template
        with db_manager.get_session() as session:
            # Create a test prompt template
            template = prompt_template_repo.create(
                session,
                name="Test MEDDPICC Template",
                description="A test template for MEDDPICC analysis",
                content="Analyze the following content for MEDDPICC elements: {content}",
                agent_type="meddpic",
                version="1.0.0",
                template_metadata={"test": True},
                variables={"content": "string"}
            )
            logger.info(f"✅ Created template: {template.name} (ID: {template.id})")
            
            # Create a version for the template
            version = prompt_version_repo.create(
                session,
                template_id=template.id,
                version="1.0.0",
                content=template.content,
                change_notes="Initial version",
                is_current=True,
                created_by="test_system"
            )
            logger.info(f"✅ Created version: {version.version} (ID: {version.id})")
            
            # Test querying the template
            retrieved_template = prompt_template_repo.get_by_id(session, template.id)
            assert retrieved_template is not None
            assert retrieved_template.name == "Test MEDDPICC Template"
            logger.info(f"✅ Retrieved template: {retrieved_template.name}")
            
            # Test querying by agent type
            meddpic_templates = prompt_template_repo.get_by_agent_type(session, "meddpic")
            assert len(meddpic_templates) >= 1
            logger.info(f"✅ Found {len(meddpic_templates)} MEDDPICC templates")
            
            # Test getting current version
            current_version = prompt_version_repo.get_current_version(session, template.id)
            assert current_version is not None
            assert current_version.is_current is True
            logger.info(f"✅ Current version: {current_version.version}")
            
            # Test increment usage
            original_count = template.usage_count
            prompt_template_repo.increment_usage(session, template.id)
            session.refresh(template)
            assert template.usage_count == original_count + 1
            logger.info(f"✅ Usage count incremented: {template.usage_count}")
            
        logger.info("✅ All database tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        return False
    finally:
        # Clean up
        db_manager.close()
        logger.info("🔒 Database connection closed")


def test_database_schema():
    """Test database schema and relationships."""
    try:
        db_manager.initialize()
        
        with db_manager.get_session() as session:
            # Test creating related records
            template = prompt_template_repo.create(
                session,
                name="Multi-Version Template",
                description="Template with multiple versions",
                content="Version 1 content",
                agent_type="test",
                version="1.0.0"
            )
            
            # Create multiple versions
            for i in range(1, 4):
                version = prompt_version_repo.create(
                    session,
                    template_id=template.id,
                    version=f"1.{i}.0",
                    content=f"Version 1.{i}.0 content",
                    change_notes=f"Update {i}",
                    is_current=(i == 3),  # Make the last one current
                    created_by="test_system"
                )
            
            # Test getting all versions
            versions = prompt_version_repo.get_by_template_id(session, template.id)
            assert len(versions) == 3
            logger.info(f"✅ Created {len(versions)} versions")
            
            # Test current version selection
            current = prompt_version_repo.get_current_version(session, template.id)
            assert current.version == "1.3.0"
            logger.info(f"✅ Current version correctly set: {current.version}")
            
        logger.info("✅ Schema relationship tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Schema test failed: {e}")
        return False
    finally:
        db_manager.close()


if __name__ == "__main__":
    print("🧪 Testing ASMIS Database Layer")
    print("=" * 50)
    
    # Run tests
    basic_test = test_database_connection()
    schema_test = test_database_schema()
    
    print("=" * 50)
    if basic_test and schema_test:
        print("🎉 All database tests passed!")
        exit(0)
    else:
        print("💥 Some tests failed!")
        exit(1)