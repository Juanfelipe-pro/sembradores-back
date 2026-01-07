from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Favorito(Base):
    __tablename__ = "favoritos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    devocional_id = Column(UUID(as_uuid=True), ForeignKey('devocionales.id', ondelete='CASCADE'), nullable=False)
    fecha_agregado = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('user_id', 'devocional_id', name='unique_user_devocional_favorito'),
    )
    
    def __repr__(self):
        return f"<Favorito user={self.user_id} dev={self.devocional_id}>"
