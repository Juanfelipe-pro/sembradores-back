import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import AsyncSessionLocal
from app.models.plan import Plan, TipoPlan
from sqlalchemy import select

async def init_planes():
    async with AsyncSessionLocal() as db:
        # Verificar si ya existen planes
        result = await db.execute(select(Plan))
        if result.scalar_one_or_none():
            print("Planes ya existentes")
            return
        
        planes = [
            Plan(
                nombre="Plan Básico",
                tipo=TipoPlan.BASICO,
                precio=0,
                descripcion="Acceso gratuito a devocionales públicos",
                duracion_dias=365,
                activo=True
            ),
            Plan(
                nombre="Plan Premium Mensual",
                tipo=TipoPlan.PREMIUM,
                precio=999,  # $9.99 USD
                descripcion="Acceso completo a todos los devocionales, sin anuncios",
                duracion_dias=30,
                activo=True
            ),
            Plan(
                nombre="Plan Premium Anual",
                tipo=TipoPlan.PREMIUM_ANUAL,
                precio=9999,  # $99.99 USD
                descripcion="Acceso completo por un año con descuento",
                duracion_dias=365,
                activo=True
            ),
        ]
        
        for plan in planes:
            db.add(plan)
        
        await db.commit()
        print(f"✅ {len(planes)} planes creados")

if __name__ == "__main__":
    print("🚀 Inicializando planes...\n")
    asyncio.run(init_planes())