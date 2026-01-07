#!/bin/bash
# Script de inicio para Railway
# Lee la variable de entorno PORT y la usa para uvicorn

PORT=${PORT:-8000}

# Ejecutar migraciones si DATABASE_URL está configurado
if [ -n "$DATABASE_URL" ] && [ "$DATABASE_URL" != "postgresql://postgres:postgres@localhost:5432/sembradores_fe" ]; then
    echo "Ejecutando migraciones de base de datos..."
    alembic upgrade head || echo "Advertencia: Error al ejecutar migraciones"
fi

# Iniciar servidor
uvicorn app.main:app --host 0.0.0.0 --port $PORT

