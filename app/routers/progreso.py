from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.progreso import ProgresoLectura
from app.models.devocional import Devocional
from app.models.user import User
from app.schemas.progreso import ProgresoCreate, ProgresoUpdate, ProgresoResponse, EstadisticasProgreso

router = APIRouter()

@router.post("/", response_model=ProgresoResponse, status_code=status.HTTP_201_CREATED)
async def crear_progreso(
    progreso_data: ProgresoCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verificar que el devocional existe
    result = await db.execute(select(Devocional).where(Devocional.id == progreso_data.devocional_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Devocional not found")
    
    # Buscar progreso existente
    result = await db.execute(
        select(ProgresoLectura).where(
            ProgresoLectura.user_id == current_user.id,
            ProgresoLectura.devocional_id == progreso_data.devocional_id
        )
    )
    progreso = result.scalar_one_or_none()
    
    if progreso:
        # Actualizar existente
        progreso.tiempo_lectura_segundos += progreso_data.tiempo_lectura_segundos
        progreso.progreso_video_segundos = progreso_data.progreso_video_segundos
        progreso.completado = progreso_data.completado
        progreso.video_visto = progreso_data.video_visto
        if progreso_data.completado and not progreso.fecha_completado:
            progreso.fecha_completado = datetime.utcnow()
    else:
        # Crear nuevo
        progreso = ProgresoLectura(
            user_id=current_user.id,
            devocional_id=progreso_data.devocional_id,
            tiempo_lectura_segundos=progreso_data.tiempo_lectura_segundos,
            progreso_video_segundos=progreso_data.progreso_video_segundos,
            completado=progreso_data.completado,
            video_visto=progreso_data.video_visto,
            fecha_completado=datetime.utcnow() if progreso_data.completado else None
        )
        db.add(progreso)
    
    await db.commit()
    await db.refresh(progreso)
    return progreso

@router.get("/stats", response_model=EstadisticasProgreso)
async def obtener_estadisticas(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Total devocionales
    result = await db.execute(select(func.count(Devocional.id)))
    total_devocionales = result.scalar()
    
    # Progreso del usuario
    result = await db.execute(
        select(ProgresoLectura).where(ProgresoLectura.user_id == current_user.id)
    )
    progresos = result.scalars().all()
    
    devocionales_leidos = len(progresos)
    devocionales_completados = sum(1 for p in progresos if p.completado)
    videos_vistos = sum(1 for p in progresos if p.video_visto)
    tiempo_total_minutos = sum(p.tiempo_lectura_segundos for p in progresos) // 60
    
    # Calcular racha
    if progresos:
        progresos_ordenados = sorted(progresos, key=lambda x: x.ultima_visita, reverse=True)
        racha = 1
        fecha_actual = progresos_ordenados[0].ultima_visita.date()
        
        for progreso in progresos_ordenados[1:]:
            fecha_progreso = progreso.ultima_visita.date()
            diferencia = (fecha_actual - fecha_progreso).days
            
            if diferencia == 1:
                racha += 1
                fecha_actual = fecha_progreso
            elif diferencia > 1:
                break
    else:
        racha = 0
    
    ultima_lectura = progresos_ordenados[0].ultima_visita if progresos else None
    promedio_tiempo = tiempo_total_minutos // devocionales_leidos if devocionales_leidos > 0 else 0
    porcentaje = (devocionales_completados / total_devocionales * 100) if total_devocionales > 0 else 0
    
    return EstadisticasProgreso(
        total_devocionales=total_devocionales,
        devocionales_leidos=devocionales_leidos,
        devocionales_completados=devocionales_completados,
        videos_vistos=videos_vistos,
        tiempo_total_lectura_minutos=tiempo_total_minutos,
        racha_dias=racha,
        ultima_lectura=ultima_lectura,
        promedio_tiempo_lectura=promedio_tiempo,
        porcentaje_completado=round(porcentaje, 1)
    )

@router.get("/historial", response_model=List[ProgresoResponse])
async def obtener_historial(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProgresoLectura)
        .where(ProgresoLectura.user_id == current_user.id)
        .order_by(ProgresoLectura.ultima_visita.desc())
    )
    return result.scalars().all()

@router.get("/{devocional_id}", response_model=ProgresoResponse)
async def obtener_progreso(
    devocional_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProgresoLectura).where(
            ProgresoLectura.user_id == current_user.id,
            ProgresoLectura.devocional_id == devocional_id
        )
    )
    progreso = result.scalar_one_or_none()
    
    if not progreso:
        raise HTTPException(status_code=404, detail="Progreso not found")
    
    return progreso
