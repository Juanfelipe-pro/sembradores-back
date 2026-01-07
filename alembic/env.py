from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import asyncio, os, sys

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.core.database import Base

# Importar explícitamente todos los modelos para que Alembic los detecte
from app.models.user import User
from app.models.devocional import Devocional
from app.models.favorito import Favorito
from app.models.progreso import ProgresoLectura
from app.models.plan import Plan
from app.models.pago import Pago
from app.models.push_subscription import PushSubscription

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
config.set_main_option("sqlalchemy.url", url)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(lambda c: context.configure(connection=c, target_metadata=target_metadata))
        async with connection.begin():
            await connection.run_sync(lambda c: context.run_migrations())
    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()