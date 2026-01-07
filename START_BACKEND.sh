#!/bin/bash

echo "🚀 Iniciando Backend Sembradores de Fe..."
echo ""

# Verificar si existe venv
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
fi

# Activar venv
source venv/bin/activate

# Verificar si hay dependencias instaladas
if [ ! -d "venv/lib/python*/site-packages/fastapi" ]; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado!"
    echo "   Copia .env.example a .env y configúralo"
    exit 1
fi

echo "✅ Iniciando servidor..."
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

python app/main.py
