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
- Base de datos: SQLite

---

## 📦 Estructura general de los tests

```bash
apps/
├── usuario/
│   └── test/
│       ├── fixture_user.py           # Fixtures para usuarios y generación de tokens JWT
│       └── test_token_jwt.py         # Tests relacionados con autenticación JWT
│
├── producto/
│   └── test/
│       ├── fixtures_categoria.py     # Fixtures para categorías de productos
│       ├── fixtures_producto.py      # Fixtures para productos
│       ├── test_categoria.py         # Tests de CRUD, validaciones y filtros para categorías
│       └── test_producto.py          # Tests de CRUD, validaciones y filtros para productos
│
├── venta/
│   └── test/
│       ├── fixtures_venta.py         # Fixtures para ventas e ítems de venta
│       └── test_venta.py             # Tests de reglas de stock, totales y filtros en ventas

