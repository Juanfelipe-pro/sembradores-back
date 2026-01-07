from sqlalchemy import Column, Boolean, DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class ProgresoLectura(Base):
    __tablename__ = "progreso_lectura"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    devocional_id = Column(UUID(as_uuid=True), ForeignKey('devocionales.id', ondelete='CASCADE'), nullable=False)
    
    # Progreso de lectura
    completado = Column(Boolean, default=False)
    tiempo_lectura_segundos = Column(Integer, default=0)
    
    # Progreso de video
    video_visto = Column(Boolean, default=False)
    progreso_video_segundos = Column(Integer, default=0)
    
    # Timestamps
    ultima_visita = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fecha_completado = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('user_id', 'devocional_id', name='unique_user_devocional_progreso'),
    )
    
    def __repr__(self):
        return f"<Progreso user={self.user_id} dev={self.devocional_id} completado={self.completado}>"
