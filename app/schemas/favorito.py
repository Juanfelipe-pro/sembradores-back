from pydantic import BaseModel
from datetime import datetime
import uuid

class FavoritoResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    devocional_id: uuid.UUID
    fecha_agregado: datetime
    
    class Config:
        from_attributes = True

class FavoritoConDevocional(BaseModel):
    id: uuid.UUID
    devocional_id: uuid.UUID
    fecha_agregado: datetime
    devocional: dict  # DevocionalResponse simplificado
    
    class Config:
        from_attributes = True
