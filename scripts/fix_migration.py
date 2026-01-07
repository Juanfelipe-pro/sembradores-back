"""
Script para corregir el problema de migración donde las tablas no se crearon.
Este script hace downgrade y luego upgrade de la migración inicial.
"""
import asyncio
import sys
import os
from pathlib import Path

# Agregar backend al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from alembic.config import Config
from alembic import command
from app.core.config import settings

def fix_migration():
    """Hace downgrade a base y luego upgrade a head para forzar la creación de tablas"""
    print("🔧 Corrigiendo migración...")
    print(f"📊 Base de datos: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")
    
    # Configurar Alembic
    alembic_cfg = Config(str(backend_dir / "alembic.ini"))
    
    try:
        # Hacer downgrade a base (eliminar todas las migraciones)
        print("\n📉 Haciendo downgrade a base...")
        command.downgrade(alembic_cfg, "base")
        print("✅ Downgrade completado")
        
        # Hacer upgrade a head (aplicar todas las migraciones)
        print("\n📈 Haciendo upgrade a head...")
        command.upgrade(alembic_cfg, "head")
        print("✅ Upgrade completado")
        
        print("\n🎉 ¡Migración corregida exitosamente!")
        print("📋 Las siguientes tablas deberían estar creadas:")
        print("   - users")
        print("   - devocionales")
        print("   - favoritos")
        print("   - progreso_lectura")
        print("   - planes")
        print("   - pagos")
        print("   - push_subscriptions")
        
    except Exception as e:
        print(f"\n❌ Error al corregir la migración: {e}")
        print("\n💡 Alternativa: Ejecuta el script create_all_tables.py directamente")
        raise

if __name__ == "__main__":
    fix_migration()

