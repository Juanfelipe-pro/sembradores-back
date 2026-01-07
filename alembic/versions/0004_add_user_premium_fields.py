"""Agregar campos is_premium y suscripcion_activa_hasta a users

Revision ID: 0004
Revises: 0003
Create Date: 2026-01-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None

def upgrade():
    # Agregar columna is_premium
    op.add_column('users', 
        sa.Column('is_premium', sa.Boolean(), nullable=False, server_default='false')
    )
    
    # Agregar columna suscripcion_activa_hasta
    op.add_column('users',
        sa.Column('suscripcion_activa_hasta', sa.DateTime(timezone=True), nullable=True)
    )

def downgrade():
    op.drop_column('users', 'suscripcion_activa_hasta')
    op.drop_column('users', 'is_premium')




