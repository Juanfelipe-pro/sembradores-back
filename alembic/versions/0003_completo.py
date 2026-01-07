"""Agregar tablas planes, pagos y push_subscriptions

Revision ID: 0003
Revises: 0002
Create Date: 2025-01-05
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade():
    # Tabla planes
    op.create_table('planes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('tipo', sa.Enum('basico', 'premium', 'premium_anual', name='tipoplan'), nullable=False, unique=True),
        sa.Column('precio', sa.Integer(), nullable=False),
        sa.Column('descripcion', sa.String()),
        sa.Column('duracion_dias', sa.Integer(), default=30),
        sa.Column('activo', sa.Boolean(), default=True),
    )
    
    # Tabla pagos
    op.create_table('pagos',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('mp_payment_id', sa.String()),
        sa.Column('mp_preference_id', sa.String()),
        sa.Column('monto', sa.Integer(), nullable=False),
        sa.Column('estado', sa.Enum('pendiente', 'aprobado', 'rechazado', 'cancelado', name='estadopago'), default='pendiente'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['plan_id'], ['planes.id']),
    )
    
    # Tabla push_subscriptions
    op.create_table('push_subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('endpoint', sa.String(), nullable=False, unique=True),
        sa.Column('p256dh', sa.Text(), nullable=False),
        sa.Column('auth', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

def downgrade():
    op.drop_table('push_subscriptions')
    op.drop_table('pagos')
    op.drop_table('planes')
    op.execute('DROP TYPE estadopago')
    op.execute('DROP TYPE tipoplan')
