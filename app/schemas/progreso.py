from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class ProgresoCreate(BaseModel):
    devocional_id: uuid.UUID
    tiempo_lectura_segundos: Optional[int] = 0
    progreso_video_segundos: Optional[int] = 0
    completado: Optional[bool] = False
    video_visto: Optional[bool] = False

class ProgresoUpdate(BaseModel):
    tiempo_lectura_segundos: Optional[int] = None
    progreso_video_segundos: Optional[int] = None
    completado: Optional[bool] = None
    video_visto: Optional[bool] = None

class ProgresoResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    devocional_id: uuid.UUID
    completado: bool
    tiempo_lectura_segundos: int
    video_visto: bool
    progreso_video_segundos: int
    ultima_visita: datetime
    fecha_completado: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class EstadisticasProgreso(BaseModel):
    total_devocionales: int
    devocionales_leidos: int
    devocionales_completados: int
    videos_vistos: int
    tiempo_total_lectura_minutos: int
    racha_dias: int
    ultima_lectura: Optional[datetime]
    promedio_tiempo_lectura: int
    porcentaje_completado: float
