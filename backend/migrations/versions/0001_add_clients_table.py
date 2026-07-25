"""Add clients table

Revision ID: 0001
Revises: 
Create Date: 2026-07-22 15:55:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('clients',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_by', sa.BigInteger(), nullable=True),
    sa.Column('updated_by', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clients_deleted_at'), 'clients', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_clients_name'), 'clients', ['name'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_clients_name'), table_name='clients')
    op.drop_index(op.f('ix_clients_deleted_at'), table_name='clients')
    op.drop_table('clients')
