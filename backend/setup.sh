#!/bin/bash
echo "============================================"
echo " TourPack Manager - Setup inicial (Linux/Mac)"
echo "============================================"

echo "[1] Creando entorno virtual..."
python3 -m venv venv

echo "[2] Activando entorno virtual..."
source venv/bin/activate

echo "[3] Instalando dependencias..."
pip install -r requirements.txt

echo "[4] Iniciando PostgreSQL con Docker..."
docker-compose up -d

echo "[5] Esperando que PostgreSQL esté listo (10s)..."
sleep 10

echo "[6] Aplicando migraciones..."
python manage.py migrate

echo "[7] Cargando datos iniciales..."
python manage.py seed_data

echo "[8] Verificando configuración..."
python manage.py check

echo ""
echo "============================================"
echo " ✅ Setup completo!"
echo " Inicia el servidor con:"
echo "    source venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo " Admin:  http://127.0.0.1:8000/administracion/"
echo " Email:  admin@tourpack.com"
echo " Pass:   Admin123*"
echo "============================================"
