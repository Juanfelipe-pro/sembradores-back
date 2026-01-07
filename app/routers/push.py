from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.models.push_subscription import PushSubscription
from app.schemas.push import PushSubscriptionCreate, PushSubscriptionResponse, NotificacionCreate
from app.services.push_notifications import push_service

router = APIRouter()

@router.get("/vapid-key")
async def get_vapid_key():
    """Obtener la clave pública VAPID"""
    from app.core.config import settings
    return {"publicKey": settings.VAPID_PUBLIC_KEY}

@router.post("/subscribe", response_model=PushSubscriptionResponse)
async def subscribe_push(
    sub_data: PushSubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verificar si ya existe
    result = await db.execute(
        select(PushSubscription).where(PushSubscription.endpoint == sub_data.endpoint)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return existing
    
    # Crear nueva suscripción
    subscription = PushSubscription(
        user_id=current_user.id,
        endpoint=sub_data.endpoint,
        p256dh=sub_data.keys.get("p256dh"),
        auth=sub_data.keys.get("auth")
    )
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    
    return subscription

@router.post("/test")
async def test_notification(
    notif: NotificacionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Obtener suscripciones del usuario
    result = await db.execute(
        select(PushSubscription).where(PushSubscription.user_id == current_user.id)
    )
    subscriptions = result.scalars().all()
    
    if not subscriptions:
        raise HTTPException(status_code=404, detail="No subscriptions found")
    
    # Enviar notificación
    sent_count = 0
    for sub in subscriptions:
        subscription_info = {
            "endpoint": sub.endpoint,
            "keys": {
                "p256dh": sub.p256dh,
                "auth": sub.auth
            }
        }
        
        if push_service.send_notification(subscription_info, {
            "title": notif.titulo,
            "body": notif.mensaje,
            "url": notif.url
        }):
            sent_count += 1
    
    return {"sent": sent_count, "total": len(subscriptions)}

@router.post("/broadcast")
async def broadcast_notification(
    notif: NotificacionCreate,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Enviar notificación a todos los usuarios suscritos (solo admin)"""
    
    # Obtener todas las suscripciones activas
    result = await db.execute(select(PushSubscription))
    subscriptions = result.scalars().all()
    
    if not subscriptions:
        return {"sent": 0, "total": 0, "message": "No subscriptions found"}
    
    # Enviar notificación a todos
    sent_count = 0
    failed_count = 0
    
    for sub in subscriptions:
        subscription_info = {
            "endpoint": sub.endpoint,
            "keys": {
                "p256dh": sub.p256dh,
                "auth": sub.auth
            }
        }
        
        if push_service.send_notification(subscription_info, {
            "title": notif.titulo,
            "body": notif.mensaje,
            "url": notif.url or "/index.html"
        }):
            sent_count += 1
        else:
            failed_count += 1
    
    return {
        "sent": sent_count,
        "failed": failed_count,
        "total": len(subscriptions),
        "message": f"Notificación enviada a {sent_count} de {len(subscriptions)} suscripciones"
    }
