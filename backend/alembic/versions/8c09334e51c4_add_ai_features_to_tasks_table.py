"""add_ai_features_to_tasks_table

Revision ID: 8c09334e51c4
Revises: 95d9c65ce32a
Create Date: 2025-07-23 22:48:25.312033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '8c09334e51c4'
down_revision: Union[str, None] = '95d9c65ce32a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use batch mode for SQLite compatibility when altering the tasks table
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        # Add new columns with server defaults for NOT NULL fields
        batch_op.add_column(sa.Column('user_id', sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column('assigned_to', sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column('task_type', sa.String(length=50), nullable=False, server_default='manual'))
        batch_op.add_column(sa.Column('execution_mode', sa.String(length=50), nullable=False, server_default='manual'))
        batch_op.add_column(sa.Column('ai_confidence', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('ai_rationale', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('source', sa.String(length=50), nullable=False, server_default='manual'))
        batch_op.add_column(sa.Column('estimated_credits', sa.Integer(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('actual_credits_used', sa.Integer(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('complexity_tier', sa.String(length=20), nullable=False, server_default='simple'))
        batch_op.add_column(sa.Column('smart_capture_id', sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column('transcript_segments', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('execution_status', sa.String(length=50), nullable=False, server_default='not_started'))
        batch_op.add_column(sa.Column('execution_method', sa.String(length=50), nullable=False, server_default='manual'))
        batch_op.add_column(sa.Column('execution_steps', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('execution_context', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('completed_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('requires_approval', sa.Boolean(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('approval_status', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('approved_by', sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column('approved_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('template_id', sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column('template_parameters', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('outcome_status', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('outcome_metrics', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('outcome_notes', sa.Text(), nullable=True))
        
        # Alter priority to be NOT NULL with default
        batch_op.alter_column('priority', nullable=False, server_default='medium')
        
        # Create indexes
        batch_op.create_index('ix_task_account', ['account_id'])
        batch_op.create_index('ix_task_deal', ['deal_id'])
        batch_op.create_index('ix_task_execution_mode', ['execution_mode'])
        batch_op.create_index('ix_task_priority_due', ['priority', 'due_date'])
        batch_op.create_index('ix_task_stakeholder', ['stakeholder_id'])
        batch_op.create_index('ix_task_task_type', ['task_type'])
        batch_op.create_index('ix_task_template', ['template_id'])
        batch_op.create_index('ix_task_tenant_assignee', ['tenant_id', 'assigned_to'])
        batch_op.create_index('ix_task_tenant_due_date', ['tenant_id', 'due_date'])
        batch_op.create_index('ix_task_tenant_status', ['tenant_id', 'status'])
    
    # Update existing tasks to have valid user_id values (set to a placeholder)
    # This would need to be customized based on your actual user setup
    op.execute("UPDATE tasks SET user_id = 'system-migration' WHERE user_id IS NULL")
    
    # Create missing indexes on task_templates if they don't exist
    try:
        op.create_index('ix_template_usage', 'task_templates', ['usage_count'], unique=False)
    except:
        pass  # Index might already exist
        
    try:
        op.create_index('ix_template_visibility', 'task_templates', ['visibility'], unique=False)
    except:
        pass  # Index might already exist


def downgrade() -> None:
    # Drop task template indexes if they exist
    try:
        op.drop_index('ix_template_visibility', table_name='task_templates')
    except:
        pass
        
    try:
        op.drop_index('ix_template_usage', table_name='task_templates')
    except:
        pass
    
    # Use batch mode to revert tasks table changes
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        # Drop indexes
        batch_op.drop_index('ix_task_tenant_status')
        batch_op.drop_index('ix_task_tenant_due_date')
        batch_op.drop_index('ix_task_tenant_assignee')
        batch_op.drop_index('ix_task_template')
        batch_op.drop_index('ix_task_task_type')
        batch_op.drop_index('ix_task_stakeholder')
        batch_op.drop_index('ix_task_priority_due')
        batch_op.drop_index('ix_task_execution_mode')
        batch_op.drop_index('ix_task_deal')
        batch_op.drop_index('ix_task_account')
        
        # Revert priority column
        batch_op.alter_column('priority', nullable=True, server_default=None)
        
        # Drop columns
        batch_op.drop_column('outcome_notes')
        batch_op.drop_column('outcome_metrics')
        batch_op.drop_column('outcome_status')
        batch_op.drop_column('template_parameters')
        batch_op.drop_column('template_id')
        batch_op.drop_column('approved_at')
        batch_op.drop_column('approved_by')
        batch_op.drop_column('approval_status')
        batch_op.drop_column('requires_approval')
        batch_op.drop_column('completed_at')
        batch_op.drop_column('execution_context')
        batch_op.drop_column('execution_steps')
        batch_op.drop_column('execution_method')
        batch_op.drop_column('execution_status')
        batch_op.drop_column('transcript_segments')
        batch_op.drop_column('smart_capture_id')
        batch_op.drop_column('complexity_tier')
        batch_op.drop_column('actual_credits_used')
        batch_op.drop_column('estimated_credits')
        batch_op.drop_column('source')
        batch_op.drop_column('ai_rationale')
        batch_op.drop_column('ai_confidence')
        batch_op.drop_column('execution_mode')
        batch_op.drop_column('task_type')
        batch_op.drop_column('assigned_to')
        batch_op.drop_column('user_id')
