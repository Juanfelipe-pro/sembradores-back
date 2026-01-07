from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import Token, UserResponse
from app.services.google_oauth import google_oauth
from pydantic import BaseModel

router = APIRouter()

class GoogleTokenRequest(BaseModel):
    token: str

@router.post("/google", response_model=Token)
async def google_login(
    token_data: GoogleTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    # Verificar token de Google
    user_info = google_oauth.verify_token(token_data.token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    
    # Buscar o crear usuario
    result = await db.execute(
        select(User).where(User.email == user_info['email'])
    )
    user = result.scalar_one_or_none()
    
    if not user:
        # Crear nuevo usuario
        user = User(
            email=user_info['email'],
            full_name=user_info.get('name'),
            google_id=user_info['google_id'],
            avatar_url=user_info.get('picture'),
            is_active=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    elif not user.google_id:
        # Vincular cuenta existente
        user.google_id = user_info['google_id']
        if not user.avatar_url:
            user.avatar_url = user_info.get('picture')
        await db.commit()
    
    # Crear token JWT
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
