# Documentación de Base de Datos — TourPack Manager

## Motor de base de datos
PostgreSQL 16

---

## Tablas y descripción

### `locations_country` — Países
| Campo | Tipo | Restricciones |
|-------|------|--------------|
| id | BIGINT | PK, AUTO |
| code | VARCHAR(5) | UNIQUE, NOT NULL |
| name | VARCHAR(100) | UNIQUE, NOT NULL |
| is_active | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMPTZ | AUTO |
| updated_at | TIMESTAMPTZ | AUTO |

**Índices:** `code`, `name`  
**Reglas:** El código debe ser de 2-5 caracteres en mayúsculas (EC, PE, CO, etc.).

---

### `locations_city` — Ciudades
| Campo | Tipo | Restricciones |
|-------|------|--------------|
| id | BIGINT | PK, AUTO |
| country_id | BIGINT | FK → locations_country |
| name | VARCHAR(100) | NOT NULL |
| phone_prefix | VARCHAR(10) | NULLABLE |
| postal_code | VARCHAR(15) | NULLABLE |
| region_zone | VARCHAR(100) | NULLABLE |
| is_active | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMPTZ | AUTO |
| updated_at | TIMESTAMPTZ | AUTO |

**Relaciones:** `country_id` → `locations_country.id` (PROTECT)  
**Índices:** `name`

---

### `accounts_user` — Usuarios
| Campo | Tipo | Restricciones |
|-------|------|--------------|
| id | BIGINT | PK, AUTO |
| public_code | VARCHAR(20) | UNIQUE, formato USR-001 |
| username | VARCHAR(150) | UNIQUE |
| first_name | VARCHAR(150) | NOT NULL |
| last_name | VARCHAR(150) | NOT NULL |
| email | VARCHAR(254) | UNIQUE, NOT NULL |
| phone | VARCHAR(20) | NULLABLE |
| city_id | BIGINT | FK → locations_city, NULLABLE |
| role | VARCHAR(10) | ADMIN \| CLIENT |
| status | VARCHAR(15) | ACTIVE \| INACTIVE \| SUSPENDED |
| password | VARCHAR(128) | HASHED (Django PBKDF2) |
| created_at | TIMESTAMPTZ | AUTO |
| updated_at | TIMESTAMPTZ | AUTO |

**Seguridad:** Las contraseñas se almacenan con PBKDF2 + SHA256 usando el sistema de Django. Nunca en texto plano.

---

### `destinations_destination` — Destinos
| Campo | Tipo | Restricciones |
|-------|------|--------------|
| id | BIGINT | PK, AUTO |
| public_code | VARCHAR(20) | UNIQUE, formato DST-001 |
| city_id | BIGINT | FK → locations_city |
| name | VARCHAR(200) | NOT NULL |
| description | TEXT | NOT NULL |
| attractions | TEXT | NULLABLE |
| climate | VARCHAR(100) | NULLABLE |
| season | VARCHAR(100) | NULLABLE |
| difficulty | VARCHAR(10) | EASY \| MODERATE \| HIGH |
| image | VARCHAR(255) | NULLABLE (ruta archivo) |
| is_active | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMPTZ | AUTO |
| updated_at | TIMESTAMPTZ | AUTO |

**Índices:** `name`, `difficulty`

---

### `packages_tourpackage` — Paquetes Turísticos
| Campo | Tipo | Restricciones |
|-------|------|--------------|
| id | BIGINT | PK, AUTO |
| public_code | VARCHAR(20) | UNIQUE, formato PKG-001 |
| name | VARCHAR(200) | NOT NULL |
| description | TEXT | NOT NULL |
| days | INTEGER | > 0 |
| nights | INTEGER | >= 0 |
| price | DECIMAL(10,2) | > 0.01 |
| category | VARCHAR(15) | STANDARD\|PREMIUM\|ADVENTURE\|LUXURY\|ECOLOGICAL |
| includes | TEXT | NULLABLE |
| stops | TEXT | NULLABLE |
| image | VARCHAR(255) | NULLABLE |
| is_active | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMPTZ | AUTO |
| updated_at | TIMESTAMPTZ | AUTO |

**Índices:** `category`, `price`

---

### `packages_packagedestination` — Destinos por Paquete
| Campo | Tipo | Restricciones |
|-------|------|--------------|
| id | BIGINT | PK, AUTO |
| package_id | BIGINT | FK → packages_tourpackage |
| destination_id | BIGINT | FK → destinations_destination |
| visit_order | INTEGER | >= 1 |

**Restricción única:** `(package_id, destination_id)` — no se puede repetir el mismo destino en el mismo paquete.  
**Semántica:** Define el orden del recorrido dentro de un paquete.

---

### `packages_departure` — Fechas de Salida
| Campo | Tipo | Restricciones |
|-------|------|--------------|
| id | BIGINT | PK, AUTO |
| package_id | BIGINT | FK → packages_tourpackage |
| departure_date | DATE | NOT NULL, >= hoy |
| capacity | INTEGER | > 0 |
| available_slots | INTEGER | >= 0, <= capacity |
| status | VARCHAR(15) | AVAILABLE\|FULL\|CANCELLED\|COMPLETED |
| created_at | TIMESTAMPTZ | AUTO |
| updated_at | TIMESTAMPTZ | AUTO |

**Restricción única:** `(package_id, departure_date)` — no puede haber dos salidas del mismo paquete en la misma fecha.  
**Índices:** `(departure_date, status)`  
**Regla de integridad:** `available_slots` se actualiza atómicamente en cada reserva usando `SELECT FOR UPDATE`.

---

### `reservations_reservation` — Reservas
| Campo | Tipo | Restricciones |
|-------|------|--------------|
| id | BIGINT | PK, AUTO |
| public_code | VARCHAR(20) | UNIQUE, formato RES-1001 |
| user_id | BIGINT | FK → accounts_user |
| departure_id | BIGINT | FK → packages_departure |
| reservation_date | TIMESTAMPTZ | AUTO |
| number_of_people | INTEGER | >= 1 |
| unit_price | DECIMAL(10,2) | copiado del paquete en el momento de reservar |
| total_amount | DECIMAL(12,2) | = unit_price × number_of_people |
| payment_status | VARCHAR(15) | PENDING\|PAID\|REFUNDED\|FAILED |
| status | VARCHAR(15) | PENDING\|CONFIRMED\|IN_PROCESS\|CANCELLED |
| created_at | TIMESTAMPTZ | AUTO |
| updated_at | TIMESTAMPTZ | AUTO |

**Índices:** `status`, `user_id`

---

## Relaciones

```
Country (1) ──── (N) City
City    (1) ──── (N) User
City    (1) ──── (N) Destination
TourPackage (N) ──── (N) Destination  [via PackageDestination]
TourPackage (1) ──── (N) Departure
Departure   (1) ──── (N) Reservation
User        (1) ──── (N) Reservation
```

---

## Normalización

El esquema está en **Tercera Forma Normal (3FN)**:
- Cada tabla tiene una clave primaria.
- No hay dependencias transitivas.
- Los datos no se repiten: el precio del paquete se copia a `unit_price` en la reserva para preservar el valor histórico aunque el paquete cambie de precio.

---

## Integridad referencial

| Relación | ON DELETE |
|----------|-----------|
| City → Country | PROTECT (no se puede borrar un país con ciudades) |
| Destination → City | PROTECT |
| User → City | SET NULL |
| PackageDestination → TourPackage | CASCADE |
| PackageDestination → Destination | PROTECT |
| Departure → TourPackage | PROTECT |
| Reservation → User | PROTECT |
| Reservation → Departure | PROTECT |

---

## Consultas principales

```sql
-- Paquetes activos con próxima salida disponible
SELECT tp.name, tp.price, MIN(d.departure_date) AS proxima_salida
FROM packages_tourpackage tp
JOIN packages_departure d ON d.package_id = tp.id
WHERE tp.is_active = TRUE
  AND d.status = 'AVAILABLE'
  AND d.departure_date >= CURRENT_DATE
GROUP BY tp.id, tp.name, tp.price;

-- Reservas confirmadas con ingresos por paquete
SELECT tp.name, COUNT(r.id) AS reservas, SUM(r.total_amount) AS ingresos
FROM reservations_reservation r
JOIN packages_departure d ON d.id = r.departure_id
JOIN packages_tourpackage tp ON tp.id = d.package_id
WHERE r.status = 'CONFIRMED'
GROUP BY tp.id, tp.name
ORDER BY ingresos DESC;

-- Cupos disponibles por salida futura
SELECT tp.name, d.departure_date, d.capacity, d.available_slots,
       ROUND((d.available_slots::NUMERIC / d.capacity) * 100, 1) AS pct_disponible
FROM packages_departure d
JOIN packages_tourpackage tp ON tp.id = d.package_id
WHERE d.departure_date >= CURRENT_DATE
ORDER BY d.departure_date;
```
