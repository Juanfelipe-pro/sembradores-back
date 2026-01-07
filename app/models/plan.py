from sqlalchemy import Column, String, Integer, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from app.core.database import Base

class TipoPlan(str, enum.Enum):
    BASICO = "basico"
    PREMIUM = "premium"
    PREMIUM_ANUAL = "premium_anual"

class Plan(Base):
    __tablename__ = "planes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    tipo = Column(SQLEnum(TipoPlan), nullable=False, unique=True)
    precio = Column(Integer, nullable=False)  # En centavos
    descripcion = Column(String)
    duracion_dias = Column(Integer, default=30)
    activo = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Plan {self.nombre}>"
