from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.plan import Plan
from app.schemas.plan import PlanResponse

router = APIRouter()

@router.get("/", response_model=List[PlanResponse])
async def listar_planes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Plan).where(Plan.activo == True))
    return result.scalars().all()
