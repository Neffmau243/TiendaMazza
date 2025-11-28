# 📚 REVENGE POS - Sistema de Punto de Venta Completo

**Sistema de Punto de Venta Moderno y Escalable**  
Versión: 2.0.0 | Fecha: Noviembre 2024

![Vue.js](https://img.shields.io/badge/Vue.js-3.5.22-4FC08D?logo=vue.js&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7.1.7-646CFF?logo=vite&logoColor=white)

---

## 📑 Tabla de Contenidos

1. [Descripción General](#-descripción-general)
2. [Características](#-características)
3. [Stack Tecnológico](#-stack-tecnológico)
4. [Arquitectura](#-arquitectura)
5. [Guía de Instalación](#-guía-de-instalación)
6. [Estructura del Proyecto](#-estructura-del-proyecto)
7. [API Reference](#-api-reference)
8. [Seguridad y Roles](#-seguridad-y-roles)
9. [Guías de Desarrollo](#-guías-de-desarrollo)
10. [Deployment](#-deployment)
11. [Solución de Problemas](#-solución-de-problemas)

---

## 📋 Descripción General

**Revenge POS** es un sistema completo de punto de venta desarrollado con tecnologías modernas, diseñado específicamente para tiendas, bodegas y comercios minoristas. Ofrece una interfaz intuitiva, gestión completa de inventario, procesamiento rápido de ventas, sistema de reportes avanzado y arquitectura escalable.

### ¿Qué hace este sistema?

- 🛒 **Procesar ventas** rápidamente con búsqueda por código de barras
- 📦 **Gestionar inventario** con control de stock y alertas automáticas
- 📊 **Generar reportes** detallados en PDF y Excel
- 👥 **Administrar usuarios** con diferentes roles y permisos
- 💰 **Controlar compras** y proveedores
- 📈 **Visualizar métricas** en tiempo real en el dashboard

---

## ✨ Características

### Sistema de Punto de Venta (POS)
- ✅ Búsqueda rápida por código de barras
- ✅ Búsqueda por nombre de producto
- ✅ Carrito de compras interactivo
- ✅ Cálculo automático (subtotal, IVA 18%, total)
- ✅ Múltiples métodos de pago (Efectivo, Tarjeta, Transferencia)
- ✅ Generación automática de boletas
- ✅ Actualización automática de stock

### Gestión de Inventario
- ✅ CRUD completo de productos
- ✅ Categorización de productos
- ✅ Control de stock con alertas de stock bajo
- ✅ Gestión de precios (compra y venta)
- ✅ Soporte para imágenes de productos
- ✅ Búsqueda y filtros avanzados

### Sistema de Reportes
- ✅ Reporte de ventas (PDF/Excel)
- ✅ Reporte de inventario (PDF/Excel)
- ✅ Reporte de compras
- ✅ Productos más vendidos
- ✅ Filtros por fecha y periodo
- ✅ Gráficos y visualizaciones

### Dashboard en Tiempo Real
- ✅ Métricas actualizadas del día
- ✅ Total de ventas
- ✅ Productos con stock bajo
- ✅ Últimas ventas realizadas
- ✅ Accesos rápidos por rol

### Gestión de Usuarios
- ✅ CRUD de usuarios
- ✅ Tres roles: Administrador, Cajero, Almacenista
- ✅ Control de acceso basado en roles
- ✅ Estados activo/inactivo
- ✅ Validación de emails únicos

### Gestión de Compras y Proveedores
- ✅ CRUD de proveedores
- ✅ Registro de compras
- ✅ Asociación compra-proveedor
- ✅ Actualización automática de inventario
- ✅ Validación de RUC

### Seguridad
- ✅ Autenticación con JWT
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Tokens con expiración
- ✅ Protección de rutas por rol
- ✅ Validación de datos

---

## 🛠️ Stack Tecnológico

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Vue.js** | 3.5.22 | Framework progresivo reactivo |
| **Pinia** | 3.0.3 | Gestión de estado global |
| **Vue Router** | 4.6.3 | Enrutamiento SPA |
| **Axios** | 1.13.1 | Cliente HTTP |
| **Vite** | 7.1.7 | Build tool ultra rápido |
| **jsPDF** | 3.0.3 | Generación de PDFs |
| **Font Awesome** | 7.1.0 | Iconos |

### Backend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Flask** | 3.0.0 | Framework web Python |
| **Python** | 3.11+ | Lenguaje de programación |
| **MySQL** | 8.0+ | Base de datos relacional |
| **mysql-connector** | 8.2.0 | Driver de MySQL |
| **ReportLab** | 4.0.7 | Generación de PDFs |
| **PyJWT** | 2.8.0 | JSON Web Tokens |
| **bcrypt** | 4.1.0 | Hashing de contraseñas |
| **Flask-CORS** | 4.0.0 | Manejo de CORS |

---

## 🏗️ Arquitectura

### Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENTE (Navegador)                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │          Vue.js 3 SPA                             │  │
│  │  • Components & Views                             │  │
│  │  • Pinia Stores (Estado)                          │  │
│  │  • Vue Router (Navegación)                        │  │
│  └───────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP/REST (JSON)
                        │ JWT Token
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    SERVIDOR (Flask)                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Routes → Controllers → Services → Models         │  │
│  └───────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────┘
                        │ MySQL Protocol
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  BASE DE DATOS (MySQL)                   │
│  • usuarios  • productos  • ventas  • compras           │
│  • categorías  • proveedores  • reportes                │
└─────────────────────────────────────────────────────────┘
```

### Patrones de Diseño Implementados

**Backend:**
- MVC (Model-View-Controller)
- Repository Pattern
- Service Layer
- Factory Pattern
- Singleton (Database)

**Frontend:**
- Component-Based Architecture
- Composition API
- Store Pattern (Pinia)
- Service Layer
- Composables (Lógica reutilizable)

---

## 🚀 Guía de Instalación

### Requisitos Previos

| Software | Versión Mínima | Descarga |
|----------|----------------|----------|
| **Python** | 3.11+ | [python.org](https://python.org) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org) |
| **MySQL** | 8.0+ | [mysql.com](https://mysql.com) |
| **npm** | 9+ | Incluido con Node.js |

### Verificar Instalaciones

```bash
python --version    # Python 3.11.x o superior
node --version      # v18.x.x o superior
npm --version       # 9.x.x o superior
mysql --version     # mysql Ver 8.0.x
```

### Instalación Paso a Paso

#### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd TiendaFinal
```

#### 2. Configurar Base de Datos

```bash
# Conectar a MySQL
mysql -u root -p
```

```sql
-- Crear base de datos
CREATE DATABASE mazza CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verificar
SHOW DATABASES;
exit;
```

**Ejecutar script de tablas** (ver sección [Base de Datos](#base-de-datos) para el script completo)

#### 3. Configurar Backend

```bash
cd revenge_backend

# Crear entorno virtual (Recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de MySQL
```

**Contenido de `.env`:**
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=mazza

FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta_super_segura

JWT_SECRET_KEY=tu_jwt_secret_key
JWT_EXPIRATION_HOURS=24
PORT=5000
```

```bash
# Probar conexión
python test_connection.py

# Volver a la raíz
cd ..
```

#### 4. Configurar Frontend

```bash
cd revenge-pos-vue

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
```

**Contenido de `.env`:**
```env
VITE_API_BASE_URL=http://127.0.0.1:5000/api
VITE_APP_NAME=Revenge POS
VITE_IVA=0.18
```

```bash
# Volver a la raíz
cd ..
```

#### 5. Ejecutar la Aplicación

**Opción A: Modo Desarrollo** (Recomendado)

```bash
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend
cd revenge-pos-vue
npm run dev
```

**Acceder a:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000/api

**Opción B: Modo Producción**

```bash
# 1. Compilar frontend
cd revenge-pos-vue
npm run build
cd ..

# 2. Ejecutar backend con frontend integrado
python app.py --production
```

**Acceder a:** http://localhost:5000

### Usuarios de Prueba

| Rol | Email | Password |
|-----|-------|----------|
| **Administrador** | admin@revenge.com | 123456 |
| **Cajero** | cajero@revenge.com | 123456 |
| **Almacenista** | almacen@revenge.com | 123456 |

---

## 📁 Estructura del Proyecto

```
TiendaFinal/
├── revenge_backend/                 # Backend Flask
│   ├── config/
│   │   ├── __init__.py
│   │   └── database.py              # Conexión MySQL
│   │
│   ├── controllers/                 # 9 Controladores
│   │   ├── auth_controller.py
│   │   ├── categoria_controller.py
│   │   ├── compra_controller.py
│   │   ├── producto_controller.py
│   │   ├── proveedor_controller.py
│   │   ├── reporte_controller.py
│   │   ├── usuario_controller.py
│   │   └── venta_controller.py
│   │
│   ├── models/                      # 12 Modelos
│   │   ├── categoria_model.py
│   │   ├── compra_model.py
│   │   ├── producto_model.py
│   │   ├── usuario_model.py
│   │   ├── venta_model.py
│   │   └── ...
│   │
│   ├── routes/                      # 9 Rutas
│   │   ├── auth_routes.py
│   │   ├── producto_routes.py
│   │   ├── venta_routes.py
│   │   └── ...
│   │
│   ├── services/                    # 7 Servicios
│   │   ├── auth_service.py
│   │   ├── producto_service.py
│   │   ├── venta_service.py
│   │   └── ...
│   │
│   ├── utils/                       # 7 Utilidades
│   │   ├── decorators.py
│   │   ├── jwt_helper.py
│   │   ├── password_helper.py
│   │   ├── pdf_generator.py
│   │   └── ...
│   │
│   ├── requirements.txt
│   ├── .env
│   └── test_connection.py
│
├── revenge-pos-vue/                 # Frontend Vue.js
│   ├── src/
│   │   ├── assets/
│   │   │   ├── images/
│   │   │   └── styles/
│   │   │       ├── main.css
│   │   │       ├── variables.css
│   │   │       ├── components.css
│   │   │       └── responsive.css
│   │   │
│   │   ├── components/
│   │   │   ├── common/              # 8 Componentes base
│   │   │   │   ├── BaseButton.vue
│   │   │   │   ├── BaseInput.vue
│   │   │   │   ├── BaseModal.vue
│   │   │   │   ├── BaseTable.vue
│   │   │   │   ├── BaseCard.vue
│   │   │   │   ├── LoadingSpinner.vue
│   │   │   │   ├── Toast.vue
│   │   │   │   └── ToastContainer.vue
│   │   │   │
│   │   │   ├── layout/              # Componentes de layout
│   │   │   │   ├── AppHeader.vue
│   │   │   │   ├── AppSidebar.vue
│   │   │   │   └── AppFooter.vue
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   └── MetricCard.vue
│   │   │   │
│   │   │   └── ventas/
│   │   │       └── CarritoItem.vue
│   │   │
│   │   ├── views/                   # 11 Vistas
│   │   │   ├── DashboardView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── PuntoVentaView.vue
│   │   │   ├── ProductosView.vue
│   │   │   ├── VentasView.vue
│   │   │   ├── UsuariosView.vue
│   │   │   ├── CategoriasView.vue
│   │   │   ├── ComprasView.vue
│   │   │   ├── ProveedoresView.vue
│   │   │   ├── ReportesView.vue
│   │   │   └── NotFoundView.vue
│   │   │
│   │   ├── stores/                  # 9 Pinia Stores
│   │   │   ├── auth.js
│   │   │   ├── cart.js
│   │   │   ├── productos.js
│   │   │   ├── ventas.js
│   │   │   ├── usuarios.js
│   │   │   ├── categorias.js
│   │   │   ├── proveedores.js
│   │   │   ├── compras.js
│   │   │   └── ui.js
│   │   │
│   │   ├── services/                # 9 Servicios API
│   │   │   ├── api.js
│   │   │   ├── authService.js
│   │   │   ├── productosService.js
│   │   │   ├── ventasService.js
│   │   │   ├── usuariosService.js
│   │   │   ├── categoriasService.js
│   │   │   ├── proveedoresService.js
│   │   │   ├── comprasService.js
│   │   │   └── reportesService.js
│   │   │
│   │   ├── composables/             # 6 Composables
│   │   │   ├── useAuth.js
│   │   │   ├── useToast.js
│   │   │   ├── useModal.js
│   │   │   ├── useForm.js
│   │   │   ├── usePagination.js
│   │   │   └── useDebounce.js
│   │   │
│   │   ├── utils/                   # Utilidades
│   │   │   ├── formatters.js
│   │   │   ├── validators.js
│   │   │   ├── helpers.js
│   │   │   └── constants.js
│   │   │
│   │   ├── layouts/
│   │   │   ├── AuthLayout.vue
│   │   │   └── DefaultLayout.vue
│   │   │
│   │   ├── router/
│   │   │   └── index.js
│   │   │
│   │   ├── App.vue
│   │   └── main.js
│   │
│   ├── package.json
│   ├── vite.config.js
│   ├── .env
│   └── index.html
│
├── app.py                           # Punto de entrada principal
└── README.md                        # Esta documentación
```

---

## 🗄️ Base de Datos

### Configuración

```
Nombre: mazza
Motor: MySQL 8.0+
Charset: utf8mb4
Collation: utf8mb4_unicode_ci
```

### Script SQL Completo

```sql
USE mazza;

-- Tabla de estados
CREATE TABLE estados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL
);

INSERT INTO estados (nombre) VALUES ('Activo'), ('Inactivo');

-- Tabla de roles
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL
);

INSERT INTO roles (nombre) VALUES ('Administrador'), ('Cajero'), ('Almacenista');

-- Tabla de métodos de pago
CREATE TABLE metodos_pago (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    estado_id INT DEFAULT 1,
    FOREIGN KEY (estado_id) REFERENCES estados(id)
);

INSERT INTO metodos_pago (nombre) VALUES ('Efectivo'), ('Tarjeta'), ('Transferencia');

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    estado_id INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (rol_id) REFERENCES roles(id),
    FOREIGN KEY (estado_id) REFERENCES estados(id)
);

-- Tabla de categorías
CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado_id INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (estado_id) REFERENCES estados(id)
);

-- Tabla de productos
CREATE TABLE productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo_barras VARCHAR(50) UNIQUE,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria_id INT,
    precio_compra DECIMAL(10,2) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    stock_minimo INT DEFAULT 5,
    imagen_url VARCHAR(255),
    estado_id INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (estado_id) REFERENCES estados(id)
);

-- Tabla de proveedores
CREATE TABLE proveedores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ruc VARCHAR(20) UNIQUE,
    nombre VARCHAR(200) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    email VARCHAR(100),
    contacto VARCHAR(100),
    estado_id INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (estado_id) REFERENCES estados(id)
);

-- Tabla de ventas
CREATE TABLE ventas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero_boleta VARCHAR(50) UNIQUE NOT NULL,
    cajero_id INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    impuestos DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    metodo_pago_id INT NOT NULL,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cajero_id) REFERENCES usuarios(id),
    FOREIGN KEY (metodo_pago_id) REFERENCES metodos_pago(id)
);

-- Tabla de detalle de ventas
CREATE TABLE detalle_ventas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla de compras
CREATE TABLE compras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero_factura VARCHAR(50),
    proveedor_id INT NOT NULL,
    usuario_id INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    impuestos DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    observaciones TEXT,
    fecha_compra DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de detalle de compras
CREATE TABLE detalle_compras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    compra_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Índices para mejor rendimiento
CREATE INDEX idx_productos_codigo ON productos(codigo_barras);
CREATE INDEX idx_ventas_cajero ON ventas(cajero_id);
CREATE INDEX idx_ventas_fecha ON ventas(created_at);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_productos_stock ON productos(stock);
```

### Modelo Entidad-Relación

```
usuarios ──────┐
   │           │
   │ (cajero)  │ (usuario)
   ↓           ↓
ventas      compras
   │           │
   │           │
   ↓           ↓
detalle_    detalle_
ventas      compras
   │           │
   └───────────┴──────→ productos ←── categorias
                           │
                           │
                      proveedores
```

---

## 📡 API Reference

### Autenticación

#### POST /api/auth/login
```json
Request:
{
  "email": "admin@revenge.com",
  "password": "123456"
}

Response:
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "nombre": "Administrador",
    "email": "admin@revenge.com",
    "rol": "Administrador"
  }
}
```

#### POST /api/auth/logout
```
Headers: Authorization: Bearer <token>
Response: { "message": "Sesión cerrada" }
```

#### GET /api/auth/me
```
Headers: Authorization: Bearer <token>
Response: { "user": {...} }
```

### Productos

#### GET /api/productos
```
Query: ?incluir_inactivos=true
Response: [{ "id": 1, "nombre": "...", ... }]
```

#### GET /api/productos/:id
```
Response: { "id": 1, "codigo_barras": "...", ... }
```

#### GET /api/productos/codigo/:codigo_barras
```
Response: { "id": 1, "nombre": "...", ... }
```

#### GET /api/productos/buscar?q=nombre
```
Response: [productos...]
```

#### GET /api/productos/stock-bajo
```
Response: [productos con stock < stock_minimo]
```

#### POST /api/productos
```json
{
  "codigo_barras": "7501234567890",
  "nombre": "Producto Ejemplo",
  "categoria_id": 1,
  "precio_compra": 10.00,
  "precio_venta": 15.00,
  "stock": 100,
  "stock_minimo": 10
}
```

#### PUT /api/productos/:id
#### DELETE /api/productos/:id

### Ventas

#### GET /api/ventas
```
Query: ?limite=100&offset=0
Response: [ventas...]
```

#### GET /api/ventas/:id
```
Response: {
  "venta": {...},
  "detalles": [...]
}
```

#### POST /api/ventas
```json
{
  "cajero_id": 2,
  "metodo_pago_id": 1,
  "subtotal": 100.00,
  "descuento": 0.00,
  "impuestos": 18.00,
  "total": 118.00,
  "detalles": [
    {
      "producto_id": 1,
      "cantidad": 2,
      "precio_unitario": 50.00,
      "subtotal": 100.00,
      "total": 100.00
    }
  ]
}
```

### Categorías

#### GET /api/categorias
#### POST /api/categorias
#### PUT /api/categorias/:id
#### DELETE /api/categorias/:id

### Usuarios

#### GET /api/usuarios
#### POST /api/usuarios
#### PUT /api/usuarios/:id
#### DELETE /api/usuarios/:id

### Proveedores

#### GET /api/proveedores
#### POST /api/proveedores
#### PUT /api/proveedores/:id
#### DELETE /api/proveedores/:id

### Compras

#### GET /api/compras
#### POST /api/compras
#### GET /api/compras/:id

### Reportes

#### GET /api/reportes/ventas
```
Query: ?fecha_inicio=2024-01-01&fecha_fin=2024-12-31&formato=pdf
Response: PDF o JSON
```

#### GET /api/reportes/inventario
```
Query: ?formato=excel
Response: Excel o JSON
```

---

## 🔒 Seguridad y Roles

### Autenticación JWT

- **Algoritmo:** HS256
- **Expiración:** 24 horas (configurable)
- **Header:** `Authorization: Bearer <token>`

### Contraseñas

- **Hash:** bcrypt
- **Rounds:** 12

### CORS

- **Origen permitido:** http://localhost:5173
- **Métodos:** GET, POST, PUT, DELETE
- **Headers:** Content-Type, Authorization

### Roles y Permisos

#### Administrador (rol_id: 1)
| Módulo | Permisos |
|--------|----------|
| Usuarios | CRUD completo |
| Productos | CRUD completo |
| Categorías | CRUD completo |
| Proveedores | CRUD completo |
| Ventas | Ver todas, crear |
| Compras | CRUD completo |
| Reportes | Todos |
| Dashboard | Vista completa |

#### Cajero (rol_id: 2)
| Módulo | Permisos |
|--------|----------|
| Punto de Venta | Acceso completo |
| Productos | Solo lectura |
| Ventas | Ver propias, crear |
| Dashboard | Vista básica |

#### Almacenista (rol_id: 3)
| Módulo | Permisos |
|--------|----------|
| Productos | CRUD completo |
| Compras | CRUD completo |
| Inventario | Control completo |
| Reportes | Solo inventario |
| Dashboard | Vista básica |

---

## 👨‍💻 Guías de Desarrollo

### Crear un Nuevo Componente Vue

```vue
<template>
  <div class="mi-componente">
    <h2>{{ titulo }}</h2>
    <p>{{ mensaje }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const titulo = ref('Mi Componente');
const mensaje = ref('Hola Mundo');
</script>

<style scoped>
.mi-componente {
  padding: 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
}
</style>
```

### Crear un Nuevo Store (Pinia)

```javascript
// stores/miStore.js
import { defineStore } from 'pinia';

export const useMiStore = defineStore('miStore', {
  state: () => ({
    items: [],
    loading: false
  }),
  
  getters: {
    itemCount: (state) => state.items.length
  },
  
  actions: {
    async fetchItems() {
      this.loading = true;
      try {
        // Lógica para obtener datos
        this.items = await api.get('/items');
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    }
  }
});
```

### Crear un Nuevo Servicio API

```javascript
// services/miService.js
import api from './api';

export default {
  getAll() {
    return api.get('/mi-recurso');
  },
  
  getById(id) {
    return api.get(`/mi-recurso/${id}`);
  },
  
  create(data) {
    return api.post('/mi-recurso', data);
  },
  
  update(id, data) {
    return api.put(`/mi-recurso/${id}`, data);
  },
  
  delete(id) {
    return api.delete(`/mi-recurso/${id}`);
  }
};
```

### Crear un Endpoint en Backend

```python
# routes/mi_routes.py
from flask import Blueprint, request, jsonify
from controllers.mi_controller import MiController

mi_bp = Blueprint('mi', __name__)

@mi_bp.route('/api/mi-recurso', methods=['GET'])
def get_all():
    return MiController.get_all()

@mi_bp.route('/api/mi-recurso/<int:id>', methods=['GET'])
def get_by_id(id):
    return MiController.get_by_id(id)

@mi_bp.route('/api/mi-recurso', methods=['POST'])
def create():
    data = request.get_json()
    return MiController.create(data)
```

### Debugging

#### Frontend
```javascript
// En cualquier componente
console.log('Estado:', JSON.stringify(state, null, 2));

// En Pinia store
console.log('Store:', this.$state);
```

#### Backend
```python
# En cualquier función
print(f"Debug: {variable}")

# En Flask
from flask import current_app
current_app.logger.info('Mensaje de log')
```

---

## 🚀 Deployment

### Desarrollo

#### Backend
```bash
cd revenge_backend
python app.py
# http://localhost:5000
```

#### Frontend
```bash
cd revenge-pos-vue
npm run dev
# http://localhost:5173
```

### Producción

#### 1. Build del Frontend
```bash
cd revenge-pos-vue
npm run build
# Output en /dist
cd ..
```

#### 2. Ejecutar en Modo Producción
```bash
python app.py --production
# Todo en http://localhost:5000
```

### Variables de Entorno Producción

#### Frontend (.env.production)
```env
VITE_API_BASE_URL=http://tu-servidor.com/api
VITE_APP_NAME=Revenge POS
VITE_IVA=0.18
```

#### Backend (.env)
```env
FLASK_ENV=production
FLASK_DEBUG=False
DB_HOST=tu-servidor-mysql
DB_USER=usuario_produccion
DB_PASSWORD=password_seguro
JWT_EXPIRATION_HOURS=24
```

### Checklist de Deployment

- [ ] Variables de entorno configuradas
- [ ] Base de datos en producción creada
- [ ] Frontend compilado (`npm run build`)
- [ ] Cambiar claves secretas
- [ ] Configurar HTTPS
- [ ] Configurar backups de BD
- [ ] Configurar logs
- [ ] Probar todas las funcionalidades

---

## 🐛 Solución de Problemas

### Backend no inicia

**Error:** `Can't connect to MySQL server`

**Solución:**
1. Verificar que MySQL esté corriendo
2. Revisar credenciales en `.env`
3. Verificar puerto MySQL (3306)

```bash
# Windows
net start MySQL80

# Linux/Mac
sudo systemctl start mysql
```

### Frontend no conecta al backend

**Error:** `Network Error`

**Solución:**
1. Verificar que backend esté corriendo
2. Revisar `VITE_API_BASE_URL` en `.env`
3. Verificar CORS en backend
4. Limpiar caché del navegador

```javascript
// En consola del navegador
localStorage.clear()
```

### Error de autenticación

**Error:** `Invalid token` o `Unauthorized`

**Solución:**
1. Limpiar localStorage
2. Verificar `JWT_SECRET_KEY`
3. Reiniciar servidores

### Puerto ocupado

**Error:** `Port 5000 is already in use`

**Solución:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9

# O cambiar puerto en .env
PORT=5001
```

### npm install falla

**Solución:**
```bash
npm cache clean --force
rm package-lock.json
rm -rf node_modules
npm install
```

---

## 📊 Sistema de Diseño

### Paleta de Colores

```css
/* Colores Primarios */
--primary: #007bff;
--primary-hover: #0056b3;
--primary-light: #e7f3ff;

/* Estados */
--success: #28a745;
--danger: #dc3545;
--warning: #ffc107;
--info: #17a2b8;

/* Neutrales */
--dark: #333;
--gray: #666;
--light: #f8f9fa;
--border: #dee2e6;
--background: #f5f5f5;
--white: #ffffff;
```

### Breakpoints Responsive

```css
/* Móviles */
@media (max-width: 576px) { }

/* Tablets */
@media (max-width: 768px) { }

/* Desktop pequeño */
@media (max-width: 992px) { }

/* Desktop grande */
@media (max-width: 1200px) { }
```

---

## 📚 Recursos Adicionales

### Enlaces Útiles

- **Vue.js 3:** https://vuejs.org/
- **Pinia:** https://pinia.vuejs.org/
- **Vue Router:** https://router.vuejs.org/
- **Vite:** https://vitejs.dev/
- **Flask:** https://flask.palletsprojects.com/
- **MySQL:** https://dev.mysql.com/doc/

### Herramientas de Desarrollo

- **Vue DevTools** - Inspector de componentes
- **Pinia DevTools** - Inspector de estado
- **Postman** - Testing de API
- **MySQL Workbench** - Gestión de base de datos

---

## 📝 Backup Base de Datos

```bash
# Crear backup
mysqldump -u root -p mazza > backup_$(date +%Y%m%d).sql

# Restaurar backup
mysql -u root -p mazza < backup_20241126.sql
```

---

## 🎉 ¡Listo para Usar!

Si completaste todos los pasos de instalación, el sistema Revenge POS está listo.

**Acceder a:**
- **Desarrollo:** http://localhost:5173
- **Producción:** http://localhost:5000

**Credenciales de prueba:**
- Email: `admin@revenge.com`
- Password: `123456`

---

## 📞 Soporte

Para más información, consulta los archivos de documentación individuales o revisa la sección de solución de problemas.

---

**Revenge POS** - Sistema Completo de Punto de Venta  
**Versión:** 2.0.0  
**Última actualización:** Noviembre 2024

¡Gracias por usar Revenge POS! 🚀
