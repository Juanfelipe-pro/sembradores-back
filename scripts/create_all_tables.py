import asyncio
import sys
from pathlib import Path

# Agregar backend al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import engine, Base

# Importar TODOS los modelos
from app.models.user import User
from app.models.devocional import Devocional
from app.models.favorito import Favorito
from app.models.progreso import ProgresoLectura
from app.models.plan import Plan
from app.models.pago import Pago
from app.models.push_subscription import PushSubscription

async def create_all_tables():
    print("🚀 Creando todas las tablas...")
    
    async with engine.begin() as conn:
        # Crear todas las tablas
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Todas las tablas creadas correctamente:")
    print("   - users")
    print("   - devocionales")
    print("   - favoritos")
    print("   - progreso_lectura")
    print("   - planes")
    print("   - pagos")
    print("   - push_subscriptions")

if __name__ == "__main__":
    asyncio.run(create_all_tables())