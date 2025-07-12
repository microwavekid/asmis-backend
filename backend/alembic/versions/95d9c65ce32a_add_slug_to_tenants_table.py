"""Add slug to tenants table

Revision ID: 95d9c65ce32a
Revises: f06c8111d954
Create Date: 2025-07-11 16:27:34.179962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95d9c65ce32a'
down_revision: Union[str, None] = 'f06c8111d954'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add slug column to tenants table
    with op.batch_alter_table('tenants') as batch_op:
        batch_op.add_column(sa.Column('slug', sa.String(100), nullable=True))
        batch_op.create_unique_constraint('uq_tenant_slug', ['slug'])
    
    # Update existing tenants with a default slug based on their name
    # This is safe for SQLite
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id, name FROM tenants"))
    for row in result:
        tenant_id = row[0]
        name = row[1]
        # Create slug from name (lowercase, replace spaces with hyphens)
        slug = name.lower().replace(' ', '-').replace('_', '-')
        conn.execute(
            sa.text("UPDATE tenants SET slug = :slug WHERE id = :id"),
            {"slug": slug, "id": tenant_id}
        )
    
    # Make slug non-nullable after populating
    with op.batch_alter_table('tenants') as batch_op:
        batch_op.alter_column('slug', nullable=False)


def downgrade() -> None:
    # Remove slug column from tenants table
    with op.batch_alter_table('tenants') as batch_op:
        batch_op.drop_constraint('uq_tenant_slug', type_='unique')
        batch_op.drop_column('slug')
