from pydantic import BaseModel
from datetime import datetime
import uuid

class PagoCreate(BaseModel):
    plan_id: uuid.UUID

class PagoResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    plan_id: uuid.UUID
    mp_preference_id: str
    monto: int
    estado: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MPWebhook(BaseModel):
    type: str
    data: dict
