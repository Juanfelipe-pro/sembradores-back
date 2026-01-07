"""Agregar tablas favoritos y progreso

Revision ID: 0002
Revises: 0001
Create Date: 2025-01-05

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers
revision = '0002'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Tabla favoritos
    op.create_table('favoritos',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('devocional_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('fecha_agregado', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['devocional_id'], ['devocionales.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'devocional_id', name='unique_user_devocional_favorito')
    )
    op.create_index('ix_favoritos_user_id', 'favoritos', ['user_id'])
    op.create_index('ix_favoritos_devocional_id', 'favoritos', ['devocional_id'])
    
    # Tabla progreso_lectura
    op.create_table('progreso_lectura',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('devocional_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('completado', sa.Boolean(), default=False, nullable=False),
        sa.Column('tiempo_lectura_segundos', sa.Integer(), default=0, nullable=False),
        sa.Column('video_visto', sa.Boolean(), default=False, nullable=False),
        sa.Column('progreso_video_segundos', sa.Integer(), default=0, nullable=False),
        sa.Column('ultima_visita', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('fecha_completado', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['devocional_id'], ['devocionales.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'devocional_id', name='unique_user_devocional_progreso')
    )
    op.create_index('ix_progreso_user_id', 'progreso_lectura', ['user_id'])
    op.create_index('ix_progreso_devocional_id', 'progreso_lectura', ['devocional_id'])

def downgrade():
    op.drop_table('progreso_lectura')
    op.drop_table('favoritos')
