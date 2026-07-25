"""Add locations table

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-22 16:03:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0003'
down_revision: Union[str, None] = '0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('locations',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('project_id', sa.BigInteger(), nullable=True),
    sa.Column('address_line1', sa.String(length=255), nullable=True),
    sa.Column('address_line2', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('state_or_region', sa.String(length=100), nullable=True),
    sa.Column('postal_code', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_by', sa.BigInteger(), nullable=True),
    sa.Column('updated_by', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_locations_client_id'), 'locations', ['client_id'], unique=False)
    op.create_index(op.f('ix_locations_project_id'), 'locations', ['project_id'], unique=False)
    op.create_index(op.f('ix_locations_deleted_at'), 'locations', ['deleted_at'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_locations_deleted_at'), table_name='locations')
    op.drop_index(op.f('ix_locations_project_id'), table_name='locations')
    op.drop_index(op.f('ix_locations_client_id'), table_name='locations')
    op.drop_table('locations')
