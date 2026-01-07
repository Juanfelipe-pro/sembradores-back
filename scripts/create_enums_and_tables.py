"""
Script para crear los tipos ENUM y luego las tablas.
Este script maneja correctamente la creación de tipos ENUM en PostgreSQL.
"""
import asyncio
import sys
from pathlib import Path

# Agregar backend al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from app.core.database import engine, Base

# Importar TODOS los modelos
from app.models.user import User
from app.models.devocional import Devocional
from app.models.favorito import Favorito
from app.models.progreso import ProgresoLectura
from app.models.plan import Plan
from app.models.pago import Pago
from app.models.push_subscription import PushSubscription

async def create_enums_and_tables():
    """Crea los tipos ENUM y luego todas las tablas"""
    print("🚀 Creando tipos ENUM y tablas...")
    
    async with engine.begin() as conn:
        # Crear tipos ENUM si no existen
        print("\n📝 Creando tipos ENUM...")
        try:
            await conn.execute(text("""
                DO $$ BEGIN
                    CREATE TYPE tipoplan AS ENUM ('BASICO', 'PREMIUM', 'PREMIUM_ANUAL');
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            """))
            print("   ✅ Tipo 'tipoplan' creado o ya existe")
        except Exception as e:
            print(f"   ⚠️  Error con tipoplan: {e}")
        
        try:
            await conn.execute(text("""
                DO $$ BEGIN
                    CREATE TYPE estadopago AS ENUM ('PENDIENTE', 'APROBADO', 'RECHAZADO', 'CANCELADO');
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            """))
            print("   ✅ Tipo 'estadopago' creado o ya existe")
        except Exception as e:
            print(f"   ⚠️  Error con estadopago: {e}")
        
        # Crear todas las tablas
        print("\n📊 Creando tablas...")
        await conn.run_sync(Base.metadata.create_all)
    
    print("\n✅ Proceso completado!")
    print("📋 Las siguientes tablas deberían estar creadas:")
    print("   - users")
    print("   - devocionales")
    print("   - favoritos")
    print("   - progreso_lectura")
    print("   - planes")
    print("   - pagos")
    print("   - push_subscriptions")

if __name__ == "__main__":
    asyncio.run(create_enums_and_tables())

