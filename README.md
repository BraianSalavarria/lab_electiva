# ✅ Test Suite – API Punto de Venta (Django REST Framework)

Este repositorio contiene los **tests automatizados** de la API RESTful para un sistema de punto de venta, desarrollado con **Django** y **Django REST Framework**, autenticado mediante **JWT (SimpleJWT)**.

La rama `tests` incluye:
- Fixtures reutilizables para usuarios, productos, categorías y ventas
- Casos de prueba funcionales para endpoints y reglas de negocio
- Validaciones de permisos, errores, filtros y lógica de stock

---

## 🧪 Tecnologías y dependencias clave

- **Django 5.2**
- **Django REST Framework 3.16**
- **Simple JWT 5.5.0**
- **Pytest 8.4** + **pytest-django 4.11**
- **Freezegun 1.5.2**
- **MercadoPago SDK 2.3.0**
- **qrcode 8.2**
- **django-filter 25.1**
- Base de datos: PostgreSQL (`psycopg2-binary`)

---

## 📦 Estructura general de los tests

```bash
apps/
├── usuario/
│   └── test/
│       ├── fixture_user.py          # Fixtures de usuario y JWT
│       └── test_auth.py             # Login, errores de autenticación
│
├── producto/
│   └── test/
│       ├── fixtures_categoria.py    # Fixtures de categorías
│       ├── fixtures_producto.py     # Fixtures de productos
│       └── test_producto.py         # CRUD, validaciones, filtros
│
├── venta/
│   └── test/
│       ├── fixtures_venta.py        # Fixtures para ventas e items
│       └── test_venta.py            # Reglas de stock, totales, filtros
