# TourPack Manager

Sistema web de gestión turística para agencias. Permite administrar países, ciudades, destinos, paquetes turísticos, fechas de salida, reservas y reportes.

---

## Tecnologías

- Python 3.12 / Django 5.0
- Django REST Framework
- MySQL 8 (MySQL Workbench / servidor local)
- Bootstrap 5 + HTML + CSS + JS
- pytest + pytest-django

---

## Estructura del proyecto

```
tourpack_manager/
└── backend/                  ← Aplicación Django
    ├── manage.py
    ├── config/               ← Configuración Django
    ├── apps/
    │   ├── accounts/         ← Usuarios, autenticación
    │   ├── locations/        ← Países y ciudades
    │   ├── destinations/     ← Destinos turísticos
    │   ├── packages/         ← Paquetes y fechas de salida
    │   ├── reservations/     ← Reservas (con services.py)
    │   └── reports/          ← Dashboard y reportes
    ├── templates/            ← HTML con Django Templates
    ├── static/               ← CSS, JS
    ├── docs/                 ← Documentación
    └── tests/                ← Pruebas pytest
```

---

## Requisitos previos

- Python 3.12+
- MySQL Server 8 (o XAMPP con MySQL activo)
- MySQL Workbench (recomendado)
- pip

---

## Instalación y configuración

### 1. Entrar al backend

```bash
cd tourpack_manager/backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos en MySQL

En MySQL Workbench ejecutar:

```sql
CREATE DATABASE IF NOT EXISTS tourpack_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'tourpack_user'@'127.0.0.1' IDENTIFIED BY 'tourpack_pass';
GRANT ALL PRIVILEGES ON tourpack_db.* TO 'tourpack_user'@'127.0.0.1';
FLUSH PRIVILEGES;
```

### 5. Configurar variables de entorno

```bash
cp .env.example .env
```

Contenido de `.env`:

```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=tourpack_db
DB_USER=tourpack_user
DB_PASSWORD=tourpack_pass
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 6. Aplicar migraciones

```bash
python manage.py migrate
```

### 7. Cargar datos iniciales

```bash
python manage.py seed_data
```

### 8. Verificar configuración

```bash
python manage.py check
```

### 9. Iniciar el servidor

```bash
python manage.py runserver 8000
```

El sistema estará disponible en: http://127.0.0.1:8000

---

## Credenciales ficticias

| Rol | Email | Contraseña |
|-----|-------|------------|
| Administrador | admin@tourpack.com | Admin123* |
| Cliente | cliente@tourpack.com | Cliente123* |

---

## URLs principales

| URL | Descripción |
|-----|-------------|
| `/` | Redirección según rol |
| `/auth/login/` | Inicio de sesión |
| `/auth/registro/` | Registro de clientes |
| `/administracion/` | Dashboard del administrador |
| `/administracion/paises/` | Gestión de países |
| `/administracion/ciudades/` | Gestión de ciudades |
| `/administracion/destinos/` | Gestión de destinos |
| `/administracion/paquetes/` | Gestión de paquetes |
| `/administracion/salidas/` | Fechas de salida |
| `/administracion/reservas/` | Gestión de reservas |
| `/cliente/paquetes/` | Catálogo de paquetes |
| `/cliente/reservas/` | Mis reservas |
| `/cliente/perfil/` | Perfil del cliente |
| `/django-admin/` | Panel Django Admin |

---

## API REST

Base URL: `/api/`

| Endpoint | Descripción |
|----------|-------------|
| `POST /api/auth/login/` | Iniciar sesión |
| `POST /api/auth/register/` | Registrar cliente |
| `GET /api/auth/me/` | Usuario actual |
| `GET/POST /api/countries/` | Países |
| `GET/POST /api/cities/` | Ciudades |
| `GET/POST /api/destinations/` | Destinos |
| `GET/POST /api/packages/` | Paquetes |
| `GET/POST /api/departures/` | Fechas de salida |
| `GET/POST /api/reservations/` | Reservas |
| `POST /api/reservations/{id}/confirm/` | Confirmar reserva |
| `POST /api/reservations/{id}/cancel/` | Cancelar reserva |
| `GET /api/reports/` | Métricas del dashboard |

---

## Ejecutar pruebas

```bash
pytest
```

---

## Variables de entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DEBUG` | Modo debug | `True` |
| `SECRET_KEY` | Clave secreta Django | (cambiar en producción) |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `DB_ENGINE` | Motor de BD | `django.db.backends.mysql` |
| `DB_NAME` | Nombre de la BD | `tourpack_db` |
| `DB_USER` | Usuario MySQL | `tourpack_user` |
| `DB_PASSWORD` | Contraseña MySQL | `tourpack_pass` |
| `DB_HOST` | Host MySQL | `127.0.0.1` |
| `DB_PORT` | Puerto MySQL | `3306` |

---

## Comandos útiles

```bash
python manage.py createsuperuser
python manage.py makemigrations
python manage.py makemigrations --check
python manage.py seed_data
python manage.py collectstatic
```

---

## Seguridad de contraseñas

Todas las contraseñas se almacenan con el sistema PBKDF2+SHA256 de Django. El comando `seed_data` usa `set_password()` — nunca guarda contraseñas en texto plano.
