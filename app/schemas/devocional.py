from pydantic import BaseModel
from datetime import datetime
import uuid

class DevocionalCreate(BaseModel):
    titulo: str
    contenido: str
    descripcion_corta: str = None
    categoria: str = "reflexion"
    youtube_video_id: str = None
    imagen_url: str = None
    is_published: bool = True

class DevocionalUpdate(BaseModel):
    titulo: str = None
    contenido: str = None
    descripcion_corta: str = None
    categoria: str = None
    youtube_video_id: str = None
    imagen_url: str = None
    is_published: bool = None

class DevocionalResponse(BaseModel):
    id: uuid.UUID
    titulo: str
    contenido: str
    descripcion_corta: str
    categoria: str
    youtube_video_id: str
    imagen_url: str
    is_published: bool
    created_at: datetime
    class Config:
        from_attributes = True