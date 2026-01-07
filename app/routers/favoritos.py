from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.favorito import Favorito
from app.models.devocional import Devocional
from app.models.user import User
from app.schemas.favorito import FavoritoResponse
from app.schemas.devocional import DevocionalResponse

router = APIRouter()

@router.post("/{devocional_id}", response_model=FavoritoResponse, status_code=status.HTTP_201_CREATED)
async def agregar_favorito(
    devocional_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verificar que el devocional existe
    result = await db.execute(select(Devocional).where(Devocional.id == devocional_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Devocional not found")
    
    # Verificar si ya existe
    result = await db.execute(
        select(Favorito).where(
            Favorito.user_id == current_user.id,
            Favorito.devocional_id == devocional_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing
    
    # Crear favorito
    favorito = Favorito(
        user_id=current_user.id,
        devocional_id=devocional_id
    )
    db.add(favorito)
    await db.commit()
    await db.refresh(favorito)
    return favorito

@router.delete("/{devocional_id}", status_code=status.HTTP_204_NO_CONTENT)
async def quitar_favorito(
    devocional_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        delete(Favorito).where(
            Favorito.user_id == current_user.id,
            Favorito.devocional_id == devocional_id
        )
    )
    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Favorito not found")
    
    return None

@router.get("/", response_model=List[DevocionalResponse])
async def listar_favoritos(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Devocional)
        .join(Favorito, Favorito.devocional_id == Devocional.id)
        .where(Favorito.user_id == current_user.id)
        .order_by(Favorito.fecha_agregado.desc())
    )
    return result.scalars().all()

@router.get("/check/{devocional_id}", response_model=dict)
async def check_favorito(
    devocional_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Favorito).where(
            Favorito.user_id == current_user.id,
            Favorito.devocional_id == devocional_id
        )
    )
    es_favorito = result.scalar_one_or_none() is not None
    return {"es_favorito": es_favorito}
