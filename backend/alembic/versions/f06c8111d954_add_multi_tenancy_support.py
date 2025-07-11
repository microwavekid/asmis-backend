"""add multi tenancy support

Revision ID: f06c8111d954
Revises: af7e9cfdae04
Create Date: 2025-07-11 10:14:02.316775

"""
from typing import Sequence, Union
from datetime import datetime
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f06c8111d954'
down_revision: Union[str, None] = 'af7e9cfdae04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if tenants table exists, create only if needed  
    # (tables already exist from previous model definitions)
    
    # Create tenant_users junction table if it doesn't exist
    try:
        op.create_table('tenant_users',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('tenant_id', sa.String(36), nullable=False),
            sa.Column('user_id', sa.String(36), nullable=False),
            sa.Column('role', sa.String(50), nullable=False, server_default='member'),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
            sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
            sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('tenant_id', 'user_id')
        )
        op.create_index('ix_tenant_user_tenant_id', 'tenant_users', ['tenant_id'])
        op.create_index('ix_tenant_user_user_id', 'tenant_users', ['user_id'])
    except Exception:
        # Table already exists, skip creation
        pass
    
    # Create default tenant for migration
    default_tenant_id = str(uuid.uuid4())
    op.execute(
        sa.text(
            "INSERT INTO tenants (id, name, domain, created_at, updated_at, is_active) "
            "VALUES (:id, :name, :domain, :created_at, :updated_at, :is_active)"
        ).bindparams(
            id=default_tenant_id,
            name='Default Tenant',
            domain='default.local',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )
    )
    
    # Add tenant_id to all business models that exist
    # High priority models
    potential_tables = [
        'deals',
        'accounts', 
        'stakeholders',
        'meddpicc_analyses',
        'meddpicc_evidence',
        'smart_capture_notes',
        'transcripts',
        # Medium priority models
        'documents',
        'intelligence_evidence',
        'tasks'
    ]
    
    # Check which tables actually exist
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()
    
    tables_to_add_tenant = [table for table in potential_tables if table in existing_tables]
    
    for table_name in tables_to_add_tenant:
        # Use batch mode for SQLite compatibility
        with op.batch_alter_table(table_name) as batch_op:
            # Add tenant_id column (nullable first for existing data)
            batch_op.add_column(sa.Column('tenant_id', sa.String(36), nullable=True))
        
        # Update existing rows to use default tenant
        op.execute(
            sa.text(f"UPDATE {table_name} SET tenant_id = :tenant_id WHERE tenant_id IS NULL").bindparams(
                tenant_id=default_tenant_id
            )
        )
        
        # Use batch mode to make tenant_id NOT NULL and add constraints
        with op.batch_alter_table(table_name) as batch_op:
            # Make tenant_id NOT NULL after populating
            batch_op.alter_column('tenant_id', nullable=False)
            
            # Add foreign key constraint
            batch_op.create_foreign_key(
                f'fk_{table_name}_tenant_id',
                'tenants',
                ['tenant_id'],
                ['id']
            )
            
            # Add index for performance
            batch_op.create_index(f'ix_{table_name}_tenant_id', ['tenant_id'])


def downgrade() -> None:
    # Remove tenant_id from all tables (in reverse order)
    potential_tables = [
        'tasks',
        'intelligence_evidence',
        'documents',
        'transcripts',
        'smart_capture_notes',
        'meddpicc_evidence',
        'meddpicc_analyses',
        'stakeholders',
        'accounts',
        'deals'
    ]
    
    # Check which tables actually exist
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()
    
    tables_to_remove_tenant = [table for table in potential_tables if table in existing_tables]
    
    for table_name in tables_to_remove_tenant:
        # Use batch mode for SQLite compatibility
        with op.batch_alter_table(table_name) as batch_op:
            # Drop index
            batch_op.drop_index(f'ix_{table_name}_tenant_id')
            
            # Drop foreign key
            batch_op.drop_constraint(f'fk_{table_name}_tenant_id', type_='foreignkey')
            
            # Drop column
            batch_op.drop_column('tenant_id')
    
    # Drop tenant_users junction table only (leave tenants and users tables as they're part of core models)
    try:
        op.drop_index('ix_tenant_user_user_id', 'tenant_users')
        op.drop_index('ix_tenant_user_tenant_id', 'tenant_users')
        op.drop_table('tenant_users')
    except Exception:
        # Table doesn't exist, skip
        pass