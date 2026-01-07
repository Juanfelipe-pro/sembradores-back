from pydantic import BaseModel
import uuid

class PushSubscriptionCreate(BaseModel):
    endpoint: str
    keys: dict  # {p256dh, auth}

class PushSubscriptionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    endpoint: str
    
    class Config:
        from_attributes = True

class NotificacionCreate(BaseModel):
    titulo: str
    mensaje: str
    url: str = "/"
