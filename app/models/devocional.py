from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Devocional(Base):
    __tablename__ = "devocionales"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String, nullable=False)
    contenido = Column(Text, nullable=False)
    descripcion_corta = Column(String(500))
    categoria = Column(String, default="reflexion")
    youtube_video_id = Column(String)
    imagen_url = Column(String)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())