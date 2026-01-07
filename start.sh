#!/bin/bash
# Script de inicio para Railway
# Lee la variable de entorno PORT y la usa para uvicorn

PORT=${PORT:-8000}

uvicorn app.main:app --host 0.0.0.0 --port $PORT

