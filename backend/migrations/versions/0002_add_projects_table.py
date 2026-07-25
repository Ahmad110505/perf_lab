"""Add projects table

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-22 16:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('projects',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('active', 'on_hold', 'completed', 'cancelled', name='projectstatus'), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_by', sa.BigInteger(), nullable=True),
    sa.Column('updated_by', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_client_id'), 'projects', ['client_id'], unique=False)
    op.create_index(op.f('ix_projects_deleted_at'), 'projects', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_projects_status'), 'projects', ['status'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_projects_status'), table_name='projects')
    op.drop_index(op.f('ix_projects_deleted_at'), table_name='projects')
    op.drop_index(op.f('ix_projects_client_id'), table_name='projects')
    op.drop_table('projects')
