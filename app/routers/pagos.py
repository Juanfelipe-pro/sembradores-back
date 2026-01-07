from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.plan import Plan
from app.models.pago import Pago, EstadoPago
from app.schemas.pago import PagoCreate, PagoResponse, MPWebhook
from app.services.mercadopago import mp_service

router = APIRouter()

@router.post("/crear", response_model=PagoResponse)
async def crear_pago(
    pago_data: PagoCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Obtener plan
    result = await db.execute(select(Plan).where(Plan.id == pago_data.plan_id))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Crear preferencia de MercadoPago
    try:
        preference = mp_service.crear_preferencia(
            titulo=f"Plan {plan.nombre}",
            precio=plan.precio,
            user_id=str(current_user.id)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating preference: {str(e)}")
    
    # Crear registro de pago
    pago = Pago(
        user_id=current_user.id,
        plan_id=plan.id,
        mp_preference_id=preference.get("id"),
        monto=plan.precio,
        estado=EstadoPago.PENDIENTE
    )
    db.add(pago)
    await db.commit()
    await db.refresh(pago)
    
    return pago

@router.post("/webhook")
async def webhook_mercadopago(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    data = await request.json()
    
    if data.get("type") == "payment":
        payment_id = data["data"]["id"]
        payment = mp_service.get_payment(str(payment_id))
        
        if payment and payment.get("status") == "approved":
            # Buscar pago
            result = await db.execute(
                select(Pago).where(Pago.mp_preference_id == payment.get("preference_id"))
            )
            pago = result.scalar_one_or_none()
            
            if pago:
                pago.mp_payment_id = str(payment_id)
                pago.estado = EstadoPago.APROBADO
                
                # Pago aprobado - aquí se podría agregar lógica de suscripción en el futuro
                await db.commit()
    
    return {"status": "ok"}
