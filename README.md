# 📘 API Punto de Venta

## 📌 Descripción

La **API RESTful para el Sistema de Punto de Venta** permite gestionar operaciones comerciales clave como autenticación de usuarios, administración de productos y categorías, registro de ventas, cierres de caja y generación de pagos a través de QR con Mercado Pago.

### ✨ Características principales

- 🔐 Seguridad mediante **JWT**
- 🛒 CRUD de productos y categorías
- 📦 Verificación de stock automático
- 🔎 Filtros avanzados por nombre, precio, fecha y más
- 💳 Integración con Mercado Pago para generar pagos QR
- 🧾 Registro de ventas y cierres diarios

### 🧱 Modelos principales

- **Producto**
- **Categoria**
- **Venta**
- **Pago**
- **RendicionDiaria**

---

## 🛠️ Tecnologías utilizadas

- Django 5.2
- Django REST Framework
- JWT (djangorestframework-simplejwt)
- SQLite
- Mercado Pago SDK

---

## 🧩 Requisitos

- Python 3.11 o superior
- Django 5.2 o superiror

**Dependencias principales:**

- Django 5.2  
- django-environ 0.12.0  
- djangorestframework 3.16.0  
- django-filter 25.1  
- djangorestframework-simplejwt 5.5.0  
- mercadopago 2.3.0   

Instalar todas las dependencias con:

```bash
pip install -r requirements.txt
```

---

## 📮 Colección Postman

Podés probar todos los endpoints y explorar ejemplos importando la colección desde la documentación pública:  
👉 [Ver documentación en Postman](https://documenter.getpostman.com/view/42563303/2sB2qf9e5x)
