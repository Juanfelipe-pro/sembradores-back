import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.core.config import settings
from app.models.user import User
from sqlalchemy import select

async def create_admin():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
        if result.scalar_one_or_none():
            print(f"Admin ya existe: {settings.ADMIN_EMAIL}")
            return
        
        admin = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            full_name="Administrador",
            is_admin=True
        )
        db.add(admin)
        await db.commit()
        print(f"Admin creado: {settings.ADMIN_EMAIL} / {settings.ADMIN_PASSWORD}")

if __name__ == "__main__":
    asyncio.run(create_admin())