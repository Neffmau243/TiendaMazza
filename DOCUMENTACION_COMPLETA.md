# 📚 REVENGE POS - Documentación Completa del Sistema

**Sistema de Punto de Venta Moderno y Completo**  
Versión: 2.0.0  
Fecha: Noviembre 2024

---

## 📑 Tabla de Contenidos

1. [Información General](#información-general)
2. [Guía de Inicio Rápido](#guía-de-inicio-rápido)
3. [Documentación del Frontend](#documentación-del-frontend)
4. [Documentación del Backend](#documentación-del-backend)
5. [Arquitectura del Sistema](#arquitectura-del-sistema)
6. [Características Completas](#características-completas)
7. [Guías de Desarrollo](#guías-de-desarrollo)
8. [API Reference](#api-reference)
9. [Seguridad y Roles](#seguridad-y-roles)
10. [Deployment](#deployment)

---

# 📋 Información General

## Descripción del Proyecto

**Revenge POS** es un sistema completo de punto de venta desarrollado con tecnologías modernas, diseñado específicamente para tiendas, bodegas y comercios minoristas. Ofrece una interfaz intuitiva, gestión completa de inventario, procesamiento rápido de ventas, sistema de reportes avanzado y arquitectura escalable.

### Características Principales

✅ **Punto de Venta Avanzado** - Sistema POS rápido con búsqueda por código de barras  
✅ **Gestión de Inventario** - Control completo de productos, categorías y stock  
✅ **Sistema de Ventas** - Múltiples métodos de pago y generación de boletas  
✅ **Reportes Completos** - PDF y Excel con análisis detallado  
✅ **Dashboard en Tiempo Real** - Métricas y estadísticas actualizadas  
✅ **Multi-usuario y Roles** - Administrador, Cajero y Almacenista  

### Stack Tecnológico

**Frontend:**
- Vue.js 3 (Composition API)
- Pinia (Estado global)
- Vue Router (Navegación)
- Axios (HTTP Client)
- Vite (Build tool)

**Backend:**
- Flask 3.0 (Python)
- MySQL 8.0+
- JWT (Autenticación)
- ReportLab (PDFs)

---

# 🚀 Guía de Inicio Rápido

## Requisitos Previos

- Node.js 18+ y npm 9+
- Python 3.8+
- MySQL 8.0+
- Navegador moderno

## Instalación en 5 Pasos

### 1. Configurar Base de Datos

```sql
CREATE DATABASE mazza CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Ejecutar script SQL de tablas
```

### 2. Configurar Backend

```bash
cd revenge_backend
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar credenciales DB

# Probar conexión
python test_connection.py

# Iniciar servidor
python app.py
```

Backend disponible en: **http://localhost:5000**

### 3. Configurar Frontend

```bash
cd revenge-pos-vue
npm install

# Variables de entorno ya configuradas en .env
npm run dev
```

Frontend disponible en: **http://localhost:5173**

### 4. Usuarios de Prueba

**Administrador:**
- Email: `admin@revenge.com`
- Password: `123456`

**Cajero:**
- Email: `cajero@revenge.com`  
- Password: `123456`

**Almacenista:**
- Email: `almacen@revenge.com`
- Password: `123456`

### 5. Acceder al Sistema

Abrir navegador en `http://localhost:5173` e iniciar sesión.

---

# 💻 Documentación del Frontend

## Información General

**Nombre:** Revenge POS Frontend  
**Tecnología:** Vue.js 3 con Composition API  
**Build Tool:** Vite  
**Puerto:** 5173  
**Versión:** 0.0.0

## Estructura del Proyecto

```
revenge-pos-vue/
├── public/
├── src/
│   ├── assets/
│   │   ├── images/
│   │   └── styles/
│   │       ├── variables.css      # Variables CSS (colores, fuentes)
│   │       ├── main.css           # Estilos globales y resets
│   │       ├── components.css     # Estilos de componentes
│   │       └── responsive.css     # Breakpoints responsive
│   │
│   ├── components/
│   │   ├── common/                # 8 componentes base
│   │   │   ├── BaseButton.vue
│   │   │   ├── BaseInput.vue
│   │   │   ├── BaseModal.vue
│   │   │   ├── BaseTable.vue
│   │   │   ├── BaseCard.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   ├── Toast.vue
│   │   │   └── ToastContainer.vue
│   │   │
│   │   ├── layout/                # 4 componentes de layout
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   ├── AppFooter.vue
│   │   │   └── MobileMenu.vue
│   │   │
│   │   ├── dashboard/
│   │   │   └── MetricCard.vue
│   │   │
│   │   └── ventas/
│   │       └── CarritoItem.vue
│   │
│   ├── views/                     # 11 vistas
│   │   ├── DashboardView.vue
│   │   ├── LoginView.vue
│   │   ├── PuntoVentaView.vue
│   │   ├── ProductosView.vue
│   │   ├── VentasView.vue
│   │   ├── UsuariosView.vue
│   │   ├── CategoriasView.vue
│   │   ├── ComprasView.vue
│   │   ├── ProveedoresView.vue
│   │   ├── ReportesView.vue
│   │   └── NotFoundView.vue
│   │
│   ├── stores/                    # 9 Pinia stores
│   │   ├── auth.js
│   │   ├── cart.js
│   │   ├── productos.js
│   │   ├── ventas.js
│   │   ├── usuarios.js
│   │   ├── categorias.js
│   │   ├── proveedores.js
│   │   ├── compras.js
│   │   └── ui.js
│   │
│   ├── services/                  # 9 servicios API
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── productosService.js
│   │   ├── ventasService.js
│   │   ├── usuariosService.js
│   │   ├── categoriasService.js
│   │   ├── proveedoresService.js
│   │   ├── comprasService.js
│   │   └── reportesService.js
│   │
│   ├── composables/               # 6 composables
│   │   ├── useAuth.js
│   │   ├── useForm.js
│   │   ├── useModal.js
│   │   ├── useToast.js
│   │   ├── usePagination.js
│   │   └── useDebounce.js
│   │
│   ├── utils/                     # 4 utilidades
│   │   ├── formatters.js
│   │   ├── validators.js
│   │   ├── helpers.js
│   │   └── constants.js
│   │
│   ├── layouts/                   # 2 layouts
│   │   ├── AuthLayout.vue
│   │   └── DefaultLayout.vue
│   │
│   ├── router/
│   │   └── index.js
│   │
│   ├── App.vue
│   └── main.js
│
├── .env
├── package.json
├── vite.config.js
└── index.html
```

## Dependencias Principales

```json
{
  "vue": "^3.5.22",
  "vue-router": "^4.6.3",
  "pinia": "^3.0.3",
  "axios": "^1.13.1",
  "jspdf": "^3.0.3",
  "jspdf-autotable": "^5.0.2",
  "@fortawesome/fontawesome-free": "^7.1.0",
  "@vitejs/plugin-vue": "^6.0.1",
  "vite": "^7.1.7"
}
```

## Sistema de Diseño

### Paleta de Colores

```css
/* Colores Primarios */
--primary-orange: #FF6B00;    /* Naranja Plaza Vea */
--primary-blue: #007bff;      /* Azul principal */

/* Estados */
--success: #28a745;           /* Verde éxito */
--danger: #dc3545;            /* Rojo peligro */
--warning: #ffc107;           /* Amarillo advertencia */

/* Neutrales */
--dark-text: #333;
--light-bg: #f8f9fa;
--border-color: #dee2e6;
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

## Vistas Principales

### 1. LoginView.vue
- Formulario de autenticación
- Validación de campos
- Manejo de errores
- Redirección automática

### 2. DashboardView.vue
- Métricas en tiempo real
- Ventas del día
- Productos con stock bajo
- Últimas ventas
- Accesos rápidos

### 3. PuntoVentaView.vue
- Búsqueda por código de barras
- Búsqueda por nombre
- Carrito de compras
- Cálculo automático (subtotal, IVA, total)
- Métodos de pago
- Generación de boletas

### 4. ProductosView.vue
- Listado con paginación
- Búsqueda y filtros
- CRUD completo
- Control de stock
- Alertas de stock bajo
- Categorización

### 5. VentasView.vue
- Historial de ventas
- Filtros por fecha y cajero
- Detalle de ventas
- Estadísticas
- Búsqueda por boleta

### 6. UsuariosView.vue
- CRUD de usuarios
- Asignación de roles
- Estados activo/inactivo
- Validación de email

### 7. CategoriasView.vue
- CRUD de categorías
- Contador de productos

### 8. ComprasView.vue
- Registro de compras
- Selección de proveedor
- Detalle de productos
- Actualización de stock

### 9. ProveedoresView.vue
- CRUD de proveedores
- Validación de RUC
- Información de contacto

### 10. ReportesView.vue (25KB - Completa)
- Reportes de ventas
- Reportes de inventario
- Reportes de compras
- Exportación PDF/Excel
- Gráficos y visualizaciones
- Filtros personalizables

### 11. NotFoundView.vue
- Página 404 personalizada

## Stores (Pinia)

### auth.js
```javascript
// Estado: user, token, isAuthenticated
// Acciones: login, logout, checkAuth
// Getters: userRole, userName, isAdmin
```

### cart.js
```javascript
// Estado: items, subtotal, descuento, total
// Acciones: addItem, removeItem, updateQuantity, clear
// Getters: itemCount, totalAmount
```

### productos.js
```javascript
// Estado: productos, loading, error
// Acciones: fetchProductos, createProducto, updateProducto
// Getters: productosPorCategoria, productosStockBajo
```

### ventas.js
```javascript
// Estado: ventas, ventaActual, loading
// Acciones: fetchVentas, createVenta
// Getters: ventasDelDia, totalVentas
```

## Servicios API

### Configuración Base (api.js)

```javascript
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para agregar token JWT
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Servicios Disponibles

| Servicio | Métodos Principales |
|----------|-------------------|
| **authService** | login, logout, getCurrentUser |
| **productosService** | getAll, getById, create, update, delete |
| **ventasService** | getAll, create, getById, getResumenDia |
| **usuariosService** | getAll, create, update, delete |
| **categoriasService** | getAll, create, update, delete |
| **proveedoresService** | getAll, create, update, delete |
| **comprasService** | getAll, create |
| **reportesService** | getVentas, getInventario, downloadPDF |

## Rutas y Navegación

### Rutas Públicas
- `/login` - Vista de login

### Rutas Protegidas

| Ruta | Vista | Roles Permitidos |
|------|-------|-----------------|
| `/` | Redirect a /dashboard | Todos |
| `/dashboard` | Dashboard | Todos |
| `/punto-venta` | Punto de Venta | Admin, Cajero |
| `/productos` | Productos | Todos |
| `/categorias` | Categorías | Admin |
| `/ventas` | Historial Ventas | Admin, Cajero |
| `/compras` | Compras | Admin, Almacenista |
| `/proveedores` | Proveedores | Admin |
| `/usuarios` | Usuarios | Admin |
| `/reportes` | Reportes | Admin |

## Variables de Entorno

```env
VITE_API_BASE_URL=http://127.0.0.1:5000/api
VITE_APP_NAME=Revenge POS
VITE_IVA=0.18
```

## Scripts NPM

```bash
npm run dev      # Desarrollo (http://localhost:5173)
npm run build    # Producción (output: dist/)
npm run preview  # Preview del build
```

---

# ⚙️ Documentación del Backend

## Información General

**Nombre:** Revenge POS Backend  
**Tecnología:** Flask (Python)  
**Base de Datos:** MySQL  
**Arquitectura:** MVC + Services  
**Puerto:** 5000  
**Versión:** 2.0.0

## Estructura del Proyecto

```
revenge_backend/
├── config/
│   ├── __init__.py
│   └── database.py              # Pool de conexiones MySQL
│
├── controllers/                 # 9 controladores
│   ├── auth_controller.py
│   ├── categoria_controller.py
│   ├── compra_controller.py
│   ├── producto_controller.py
│   ├── proveedor_controller.py
│   ├── reporte_controller.py
│   ├── usuario_controller.py
│   └── venta_controller.py
│
├── models/                      # 12 modelos
│   ├── categoria_model.py
│   ├── compra_model.py
│   ├── detalle_compra_model.py
│   ├── detalle_venta_model.py
│   ├── estado_model.py
│   ├── metodo_pago_model.py
│   ├── producto_model.py
│   ├── proveedor_model.py
│   ├── reporte_model.py
│   ├── usuario_model.py
│   └── venta_model.py
│
├── routes/                      # 9 rutas
│   ├── auth_routes.py
│   ├── categoria_routes.py
│   ├── compra_routes.py
│   ├── producto_routes.py
│   ├── proveedor_routes.py
│   ├── reporte_routes.py
│   ├── usuario_routes.py
│   └── venta_routes.py
│
├── services/                    # 7 servicios
│   ├── auth_service.py
│   ├── compra_service.py
│   ├── producto_service.py
│   ├── reporte_service.py
│   ├── usuario_service.py
│   └── venta_service.py
│
├── utils/                       # 7 utilidades
│   ├── decorators.py
│   ├── error_handler.py
│   ├── excel_generator.py
│   ├── jwt_helper.py
│   ├── password_helper.py
│   └── pdf_generator.py
│
├── .env
├── .env.example
├── requirements.txt
└── test_connection.py
```

## Dependencias

```txt
Flask==3.0.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
mysql-connector-python==8.2.0
reportlab==4.0.7
PyJWT==2.8.0
bcrypt==4.1.0
```

## Base de Datos

### Configuración

```
Nombre: mazza
Motor: MySQL 8.0+
Charset: utf8mb4
Collation: utf8mb4_unicode_ci
```

### Tablas Principales

#### 1. usuarios
```sql
id, nombre, email, password, rol_id, estado_id
created_at, updated_at, deleted_at
```

#### 2. roles
```sql
id, nombre
-- 1: Administrador
-- 2: Cajero
-- 3: Almacenista
```

#### 3. productos
```sql
id, codigo_barras, nombre, descripcion, categoria_id
precio_compra, precio_venta, stock, stock_minimo
imagen_url, estado_id
created_at, updated_at, deleted_at
```

#### 4. ventas
```sql
id, numero_boleta, cajero_id
subtotal, descuento, impuestos, total
metodo_pago_id, observaciones
created_at
```

#### 5. detalle_ventas
```sql
id, venta_id, producto_id
cantidad, precio_unitario
subtotal, descuento, total
```

#### 6. compras
```sql
id, numero_factura, proveedor_id, usuario_id
subtotal, impuestos, total
observaciones, fecha_compra, created_at
```

#### 7. detalle_compras
```sql
id, compra_id, producto_id
cantidad, precio_unitario
subtotal, total
```

#### 8. proveedores
```sql
id, ruc, nombre, telefono
direccion, email, contacto, estado_id
created_at, updated_at, deleted_at
```

#### 9. categorias
```sql
id, nombre, descripcion, estado_id
created_at, updated_at, deleted_at
```

#### 10. metodos_pago
```sql
id, nombre, estado_id
-- 1: Efectivo
-- 2: Tarjeta
-- 3: Transferencia
```

#### 11. estados
```sql
id, nombre
-- 1: Activo
-- 2: Inactivo
```

## Autenticación y Seguridad

### JWT (JSON Web Tokens)
- Algoritmo: HS256
- Expiración: 24 horas (configurable)
- Header: `Authorization: Bearer <token>`

### Passwords
- Hash: bcrypt
- Rounds: 12

### CORS
- Origen permitido: `http://localhost:5173`
- Métodos: GET, POST, PUT, DELETE
- Headers: Content-Type, Authorization

### Roles y Permisos

**Administrador (rol_id: 1)**
- Acceso completo al sistema
- Gestión de usuarios
- Reportes completos
- Configuración

**Cajero (rol_id: 2)**
- Punto de venta
- Consulta de productos
- Historial de ventas propias
- Dashboard básico

**Almacenista (rol_id: 3)**
- Gestión de productos
- Gestión de compras
- Control de inventario
- Reportes de stock

## Variables de Entorno (.env)

```env
# Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=mazza

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta_super_segura

# JWT
JWT_SECRET_KEY=tu_jwt_secret_key
JWT_EXPIRATION_HOURS=24
```

## Instalación y Ejecución

### 1. Instalar Dependencias
```bash
cd revenge_backend
pip install -r requirements.txt
```

### 2. Configurar Base de Datos
```bash
# Crear database en MySQL
CREATE DATABASE mazza;

# Ejecutar script SQL de tablas
# Configurar .env con credenciales
```

### 3. Probar Conexión
```bash
python test_connection.py
```

### 4. Ejecutar Servidor
```bash
# Desarrollo
python app.py

# Servidor: http://localhost:5000
# API: http://localhost:5000/api
```

---

# 📡 API Reference

## Autenticación

### POST /api/auth/login
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

### POST /api/auth/logout
```
Headers: Authorization: Bearer <token>
Response: { "message": "Sesión cerrada" }
```

### GET /api/auth/me
```
Headers: Authorization: Bearer <token>
Response: { "user": {...} }
```

## Productos

### GET /api/productos
```
Query: ?incluir_inactivos=true
Response: [{ "id": 1, "nombre": "...", ... }]
```

### GET /api/productos/:id
```
Response: { "id": 1, "codigo_barras": "...", ... }
```

### GET /api/productos/codigo/:codigo_barras
```
Response: { "id": 1, "nombre": "...", ... }
```

### GET /api/productos/buscar?q=nombre
```
Response: [productos...]
```

### GET /api/productos/stock-bajo
```
Response: [productos con stock < stock_minimo]
```

### POST /api/productos
```json
{
  "codigo_barras": "7501234567890",
  "nombre": "Producto",
  "categoria_id": 1,
  "precio_compra": 10.00,
  "precio_venta": 15.00,
  "stock": 100,
  "stock_minimo": 10
}
```

### PUT /api/productos/:id
### DELETE /api/productos/:id

## Ventas

### GET /api/ventas
```
Query: ?limite=100&offset=0
Response: [ventas...]
```

### GET /api/ventas/:id
```
Response: {
  "venta": {...},
  "detalles": [...]
}
```

### GET /api/ventas/resumen-dia?fecha=2024-11-24
```
Response: {
  "total_ventas": 1500.00,
  "cantidad": 25,
  "efectivo": 800.00,
  "tarjeta": 700.00
}
```

### POST /api/ventas
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

## Usuarios

### GET /api/usuarios
### POST /api/usuarios
### GET /api/usuarios/:id
### PUT /api/usuarios/:id
### DELETE /api/usuarios/:id

## Categorías

### GET /api/categorias
### POST /api/categorias
### GET /api/categorias/:id
### PUT /api/categorias/:id
### DELETE /api/categorias/:id

## Proveedores

### GET /api/proveedores
### POST /api/proveedores
### GET /api/proveedores/:id
### PUT /api/proveedores/:id
### DELETE /api/proveedores/:id

## Compras

### GET /api/compras
### POST /api/compras
### GET /api/compras/:id
### GET /api/compras/proveedor/:proveedor_id

## Reportes

### GET /api/reportes/ventas
```
Query: ?fecha_inicio=2024-01-01&fecha_fin=2024-12-31&formato=pdf
Response: PDF o JSON
```

### GET /api/reportes/inventario
```
Query: ?formato=excel
Response: Excel o JSON
```

### GET /api/reportes/compras
```
Query: ?fecha_inicio=2024-01-01&fecha_fin=2024-12-31
Response: JSON
```

---

# 🏗️ Arquitectura del Sistema

## Patrones de Diseño

### Backend
- **MVC** (Model-View-Controller)
- **Repository Pattern** (Models)
- **Service Layer** (Business Logic)
- **Factory Pattern** (app.py)
- **Singleton** (Database)
- **Decorator Pattern** (Validaciones)

### Frontend
- **Component-Based** (Vue Components)
- **Composition API** (Vue 3)
- **Store Pattern** (Pinia)
- **Service Layer** (API Services)
- **Composables** (Reusable Logic)

## Flujos Principales

### Flujo de Login
1. Usuario ingresa credenciales
2. Frontend valida campos
3. POST a `/api/auth/login`
4. Backend valida usuario y password
5. Backend genera token JWT
6. Token guardado en localStorage
7. Store de auth actualizado
8. Redirección a /dashboard

### Flujo de Venta
1. Cajero accede a Punto de Venta
2. Busca productos (código/nombre)
3. Agrega productos al carrito (store)
4. Modifica cantidades
5. Revisa totales calculados
6. Selecciona método de pago
7. POST a `/api/ventas`
8. Backend:
   - Crea registro de venta
   - Crea detalles de venta
   - Actualiza stock de productos
   - Genera número de boleta
9. Frontend muestra boleta
10. Carrito limpiado

### Flujo de Compra
1. Usuario accede a Compras
2. Selecciona proveedor
3. Agrega productos con cantidad y precio
4. POST a `/api/compras`
5. Backend:
   - Crea registro de compra
   - Crea detalles
   - Actualiza stock (aumenta)
6. Confirmación exitosa

---

# ✨ Características Completas

## 1. Sistema de Autenticación
- ✅ Login con email y password
- ✅ Tokens JWT persistentes
- ✅ Logout automático si token inválido
- ✅ Protección de rutas por rol
- ✅ Passwords hash con bcrypt

## 2. Dashboard en Tiempo Real
- ✅ Métricas actualizadas
- ✅ Ventas del día
- ✅ Productos con stock bajo
- ✅ Últimas ventas
- ✅ Accesos rápidos por rol

## 3. Punto de Venta (POS)
- ✅ Búsqueda por código de barras
- ✅ Búsqueda por nombre
- ✅ Carrito interactivo
- ✅ Cálculo automático (subtotal, IVA, total)
- ✅ Múltiples métodos de pago
- ✅ Generación de boletas
- ✅ Actualización automática de stock

## 4. Gestión de Productos
- ✅ CRUD completo
- ✅ Búsqueda y filtrado
- ✅ Categorización
- ✅ Control de stock
- ✅ Alertas de stock bajo
- ✅ Imágenes de productos
- ✅ Cache en memoria

## 5. Historial de Ventas
- ✅ Listado con paginación
- ✅ Filtros por fecha y cajero
- ✅ Detalle de cada venta
- ✅ Búsqueda por boleta
- ✅ Estadísticas
- ✅ Exportación de datos

## 6. Gestión de Usuarios
- ✅ CRUD de usuarios
- ✅ Asignación de roles
- ✅ Estados activo/inactivo
- ✅ Validación de email único
- ✅ Control de acceso

## 7. Gestión de Compras y Proveedores
- ✅ CRUD de proveedores
- ✅ Validación de RUC
- ✅ Registro de compras
- ✅ Asociación compra-proveedor
- ✅ Actualización automática de inventario

## 8. Sistema de Reportes Avanzado
- ✅ Reporte de ventas (PDF/Excel)
- ✅ Reporte de inventario (PDF/Excel)
- ✅ Reporte de compras
- ✅ Gráficos y visualizaciones
- ✅ Filtros personalizables
- ✅ Productos más vendidos

## 9. Gestión de Categorías
- ✅ CRUD completo
- ✅ Contador de productos
- ✅ Filtrado por categoría

## 10. Sistema de Estilos Modular
- ✅ Variables CSS centralizadas
- ✅ 4 archivos CSS organizados
- ✅ Responsive design
- ✅ Tema consistente (Plaza Vea)

## 11. Componentes Reutilizables
- ✅ Sistema de diseño consistente
- ✅ 8 componentes base
- ✅ 4 componentes de layout
- ✅ Sistema de notificaciones
- ✅ Validación de formularios

---

# 👨‍💻 Guías de Desarrollo

## Crear un Nuevo Componente

```vue
<template>
  <div class="mi-componente">
    {{ mensaje }}
  </div>
</template>

<script setup>
import { ref } from 'vue';

const mensaje = ref('Hola Mundo');
</script>

<style scoped>
.mi-componente {
  padding: 1rem;
}
</style>
```

## Crear un Nuevo Store

```javascript
// stores/miStore.js
import { defineStore } from 'pinia';

export const useMiStore = defineStore('miStore', {
  state: () => ({
    items: []
  }),
  
  getters: {
    itemCount: (state) => state.items.length
  },
  
  actions: {
    async fetchItems() {
      // Lógica
    }
  }
});
```

## Crear un Nuevo Servicio

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
  }
};
```

## Crear un Endpoint en Backend

```python
# routes/mi_routes.py
from flask import Blueprint, request, jsonify
from controllers.mi_controller import MiController

mi_bp = Blueprint('mi', __name__)

@mi_bp.route('/api/mi-recurso', methods=['GET'])
def get_all():
    return MiController.get_all()
```

## Debugging

### Frontend
```javascript
// En cualquier componente
console.log('Estado:', JSON.stringify(state, null, 2));

// En Pinia store
console.log('Store:', this.$state);
```

### Backend
```python
# En cualquier función
print(f"Debug: {variable}")

# En Flask
from flask import current_app
current_app.logger.info('Mensaje de log')
```

---

# 🔒 Seguridad y Roles

## Seguridad

### Frontend
- Tokens JWT en localStorage
- Expiración automática
- Guards de navegación
- Validación de inputs
- Sanitización de datos

### Backend
- Passwords hasheados (bcrypt)
- Tokens JWT con expiración
- Validación de inputs
- SQL injection prevention
- CORS configurado
- Eliminación lógica (soft delete)

## Roles y Permisos

### Administrador
| Módulo | Permisos |
|--------|----------|
| Usuarios | CRUD completo |
| Productos | CRUD completo |
| Categorías | CRUD completo |
| Proveedores | CRUD completo |
| Ventas | Ver todas, crear |
| Compras | CRUD completo |
| Reportes | Todos los reportes |
| Dashboard | Vista completa |

### Cajero
| Módulo | Permisos |
|--------|----------|
| Punto de Venta | Acceso completo |
| Productos | Solo lectura |
| Ventas | Ver propias, crear |
| Dashboard | Vista básica |

### Almacenista
| Módulo | Permisos |
|--------|----------|
| Productos | CRUD completo |
| Compras | CRUD completo |
| Inventario | Control completo |
| Reportes | Solo inventario |
| Dashboard | Vista básica |

---

# 🚀 Deployment

## Desarrollo

### Frontend
```bash
cd revenge-pos-vue
npm run dev
# http://localhost:5173
```

### Backend
```bash
cd revenge_backend
python app.py
# http://localhost:5000
```

## Producción

### 1. Build del Frontend
```bash
cd revenge-pos-vue
npm run build
# Output en /dist
```

### 2. Configurar Backend para Servir Frontend
```python
# app.py
from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('../revenge-pos-vue/dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../revenge-pos-vue/dist', path)
```

### 3. Ejecutar en Producción
```bash
python app.py --production
# Todo en http://localhost:5000
```

## Variables de Entorno Producción

### Frontend (.env.production)
```env
VITE_API_BASE_URL=http://tu-servidor.com/api
VITE_APP_NAME=Revenge POS
VITE_IVA=0.18
```

### Backend (.env)
```env
FLASK_ENV=production
FLASK_DEBUG=False
DB_HOST=tu-servidor-mysql
DB_USER=usuario_produccion
JWT_EXPIRATION_HOURS=24
```

---

# 📞 Soporte y Mantenimiento

## Estructura de Respuestas API

### Éxito
```json
{
  "message": "Operación exitosa",
  "data": {...}
}
```

### Error
```json
{
  "error": "Descripción del error",
  "details": "Detalles adicionales"
}
```

## Códigos HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

## Logs

### Frontend
- Consola del navegador (desarrollo)
- Sentry/LogRocket (producción)

### Backend
- Consola Python (desarrollo)
- Archivos de log (producción)
- `/logs/app.log`

## Backup Base de Datos

```bash
# Backup
mysqldump -u root -p mazza > backup_$(date +%Y%m%d).sql

# Restore
mysql -u root -p mazza < backup_20241124.sql
```

---

# 📚 Recursos Adicionales

## Enlaces Útiles

- **Vue.js 3:** https://vuejs.org/
- **Pinia:** https://pinia.vuejs.org/
- **Vue Router:** https://router.vuejs.org/
- **Vite:** https://vitejs.dev/
- **Flask:** https://flask.palletsprojects.com/
- **MySQL:** https://dev.mysql.com/doc/

## Herramientas de Desarrollo

- **Vue DevTools** - Inspector de componentes
- **Pinia DevTools** - Inspector de estado
- **Postman** - Testing de API
- **MySQL Workbench** - Gestión de base de datos

---

## 📝 Notas Finales

1. El sistema usa eliminación lógica (soft delete) con campo `deleted_at`
2. Todos los precios se manejan como `DECIMAL(10,2)`
3. El IVA por defecto es 18% (configurable)
4. Los números de boleta se generan automáticamente
5. El stock se actualiza automáticamente en ventas y compras
6. Los tokens JWT expiran en 24 horas
7. Las contraseñas se hashean con bcrypt
8. El sistema soporta múltiples métodos de pago
9. Los reportes se pueden generar en PDF o Excel
10. El sistema tiene cache para productos y usuarios activos

---

**Revenge POS** - Sistema completo de punto de venta  
**Versión:** 2.0.0  
**Última actualización:** Noviembre 2024

¡Gracias por usar Revenge POS! 🎉
