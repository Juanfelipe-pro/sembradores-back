from pydantic import BaseModel
import uuid

class PlanResponse(BaseModel):
    id: uuid.UUID
    nombre: str
    tipo: str
    precio: int
    descripcion: str
    duracion_dias: int
    activo: bool
    
    class Config:
        from_attributes = True
