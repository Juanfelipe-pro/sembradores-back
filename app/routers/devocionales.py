from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.dependencies import get_current_admin, get_current_user_optional
from app.models.devocional import Devocional
from app.models.user import User
from app.schemas.devocional import DevocionalCreate, DevocionalUpdate, DevocionalResponse

router = APIRouter()

def check_user_has_active_plan(user: Optional[User]) -> bool:
    """Verifica si el usuario tiene un plan activo"""
    if not user:
        return False
    if user.is_admin:
        return True
    # Por ahora, todos los usuarios autenticados pueden acceder
    return True

@router.get("/", response_model=List[DevocionalResponse])
async def list_devocionales(
    skip: int = 0, 
    limit: int = 20, 
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    # Verificar autenticación
    if not current_user:
        raise HTTPException(
            status_code=401, 
            detail="Debes iniciar sesión para ver los devocionales"
        )
    
    # Verificar plan activo (excepto admins)
    if not check_user_has_active_plan(current_user):
        raise HTTPException(
            status_code=403,
            detail="Necesitas un plan activo para acceder a los devocionales"
        )
    
    result = await db.execute(
        select(Devocional)
        .where(Devocional.is_published == True)
        .order_by(Devocional.created_at.desc())
        .offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.get("/{id}", response_model=DevocionalResponse)
async def get_devocional(
    id: str, 
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    # Verificar autenticación
    if not current_user:
        raise HTTPException(
            status_code=401, 
            detail="Debes iniciar sesión para ver el devocional"
        )
    
    # Verificar plan activo (excepto admins)
    if not check_user_has_active_plan(current_user):
        raise HTTPException(
            status_code=403,
            detail="Necesitas un plan activo para acceder a este devocional"
        )
    
    result = await db.execute(select(Devocional).where(Devocional.id == id))
    dev = result.scalar_one_or_none()
    if not dev:
        raise HTTPException(status_code=404, detail="Not found")
    return dev

@router.post("/", response_model=DevocionalResponse)
async def create_devocional(
    devocional: DevocionalCreate,
    current_user = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    db_dev = Devocional(**devocional.dict())
    db.add(db_dev)
    await db.commit()
    await db.refresh(db_dev)
    return db_dev

@router.put("/{id}", response_model=DevocionalResponse)
async def update_devocional(
    id: str,
    devocional: DevocionalUpdate,
    current_user = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Devocional).where(Devocional.id == id))
    db_dev = result.scalar_one_or_none()
    if not db_dev:
        raise HTTPException(status_code=404, detail="Devocional not found")
    
    update_data = devocional.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_dev, field, value)
    
    await db.commit()
    await db.refresh(db_dev)
    return db_dev

@router.delete("/{id}")
async def delete_devocional(
    id: str,
    current_user = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Devocional).where(Devocional.id == id))
    db_dev = result.scalar_one_or_none()
    if not db_dev:
        raise HTTPException(status_code=404, detail="Devocional not found")
    
    await db.delete(db_dev)
    await db.commit()
    return {"message": "Devocional deleted successfully"}

@router.get("/admin/all", response_model=List[DevocionalResponse])
async def list_all_devocionales(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Lista todos los devocionales (incluyendo no publicados) para admin"""
    result = await db.execute(
        select(Devocional)
        .order_by(Devocional.created_at.desc())
        .offset(skip).limit(limit)
    )
    return result.scalars().all()