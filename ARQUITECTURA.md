# 🏗️ Arquitectura del Sistema - Revenge POS

> Documentación técnica de la arquitectura y diseño del sistema

## 📋 Tabla de Contenidos

- [Visión General](#-visión-general)
- [Arquitectura de Alto Nivel](#-arquitectura-de-alto-nivel)
- [Stack Tecnológico](#-stack-tecnológico)
- [Arquitectura del Backend](#-arquitectura-del-backend)
- [Arquitectura del Frontend](#-arquitectura-del-frontend)
- [Flujo de Datos](#-flujo-de-datos)
- [Patrones de Diseño](#-patrones-de-diseño)
- [Base de Datos](#-base-de-datos)
- [Seguridad](#-seguridad)
- [Escalabilidad](#-escalabilidad)

## 🎯 Visión General

Revenge POS es un sistema de punto de venta moderno construido con arquitectura cliente-servidor, separando claramente el frontend (Vue.js) del backend (Flask), comunicándose mediante una API RESTful.

### Características Arquitectónicas

- ✅ **Arquitectura en Capas** - Separación clara de responsabilidades
- ✅ **API RESTful** - Comunicación estándar HTTP/JSON
- ✅ **SPA (Single Page Application)** - Frontend reactivo
- ✅ **Stateless Backend** - Escalabilidad horizontal
- ✅ **JWT Authentication** - Autenticación sin estado
- ✅ **Responsive Design** - Compatible con todos los dispositivos

## 🏛️ Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENTE                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │           Navegador Web (Chrome, Firefox, etc)          ││
│  │                                                          ││
│  │  ┌──────────────────────────────────────────────────┐  ││
│  │  │         Vue.js 3 SPA                             │  ││
│  │  │  - Components                                     │  ││
│  │  │  - Views                                          │  ││
│  │  │  - Pinia Stores (Estado)                          │  ││
│  │  │  - Vue Router (Rutas)                             │  ││
│  │  └──────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/JSON (REST API)
                        │ JWT Token
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                        SERVIDOR                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Flask Backend (Python)                      ││
│  │                                                          ││
│  │  ┌─────────┐  ┌────────────┐  ┌──────────┐            ││
│  │  │ Routes  │─▶│Controllers │─▶│ Services │            ││
│  │  └─────────┘  └────────────┘  └──────────┘            ││
│  │                                     │                   ││
│  │                                     ▼                   ││
│  │                              ┌──────────┐              ││
│  │                              │  Models  │              ││
│  │                              └──────────┘              ││
│  │                                     │                   ││
│  └─────────────────────────────────────┼──────────────────┘│
└─────────────────────────────────────────┼───────────────────┘
                                          │ MySQL Protocol
                                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       BASE DE DATOS                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   MySQL 8.0+                             ││
│  │                                                          ││
│  │  - usuarios          - productos       - ventas         ││
│  │  - categorias        - proveedores     - compras        ││
│  │  - detalle_ventas    - detalle_compras - roles          ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Stack Tecnológico

### Frontend

| Componente | Tecnología | Versión | Propósito |
|------------|-----------|---------|-----------|
| **Framework** | Vue.js | 3.5.22 | Framework UI reactivo |
| **Estado** | Pinia | 3.0.3 | Gestión de estado global |
| **Rutas** | Vue Router | 4.6.3 | Navegación SPA |
| **HTTP Client** | Axios | 1.13.1 | Peticiones HTTP |
| **Build** | Vite | 7.1.7 | Build y bundling |
| **PDF** | jsPDF | 3.0.3 | Generación de PDFs |
| **Iconos** | Font Awesome | 7.1.0 | Librería de iconos |

### Backend

| Componente | Tecnología | Versión | Propósito |
|------------|-----------|---------|-----------|
| **Framework** | Flask | 3.0.0 | Framework web |
| **Lenguaje** | Python | 3.11+ | Lenguaje de programación |
| **Base de Datos** | MySQL | 8.0+ | Base de datos relacional |
| **Conector DB** | mysql-connector | 8.2.0 | Driver de MySQL |
| **PDF** | ReportLab | 4.0.7 | Generación de PDFs |
| **CORS** | Flask-CORS | 4.0.0 | Manejo de CORS |
| **Env** | python-dotenv | 1.0.0 | Variables de entorno |

## 🔧 Arquitectura del Backend

### Patrón MVC + Service Layer

```
app.py (Aplicación Flask Principal)
    │
    ├── Routes (Rutas HTTP)
    │   ├── auth_routes.py
    │   ├── producto_routes.py
    │   ├── venta_routes.py
    │   └── ...
    │
    ├── Controllers (Manejo de Requests)
    │   ├── auth_controller.py
    │   ├── producto_controller.py
    │   ├── venta_controller.py
    │   └── ...
    │
    ├── Services (Lógica de Negocio)
    │   ├── auth_service.py
    │   ├── producto_service.py
    │   ├── venta_service.py
    │   └── ...
    │
    ├── Models (Acceso a Datos)
    │   ├── producto_model.py
    │   ├── venta_model.py
    │   ├── usuario_model.py
    │   └── ...
    │
    └── Utils (Utilidades)
        ├── jwt_helper.py
        ├── password_helper.py
        ├── pdf_generator.py
        └── error_handler.py
```

### Flujo de Petición Backend

```
1. HTTP Request
   │
   ▼
2. Route (@app.route)
   │
   ▼
3. Controller (Validación básica, extracción de datos)
   │
   ▼
4. Service (Lógica de negocio, validaciones complejas)
   │
   ▼
5. Model (Consultas SQL, acceso a BD)
   │
   ▼
6. Database (MySQL)
   │
   ▼
7. Model (Retorna datos)
   │
   ▼
8. Service (Procesa resultados)
   │
   ▼
9. Controller (Formatea respuesta)
   │
   ▼
10. HTTP Response (JSON)
```

### Ejemplo de Flujo Completo

**Endpoint:** `POST /api/ventas`

```
1. cliente.post('/api/ventas', datos)
   ↓
2. venta_routes.py → @venta_bp.route('/', methods=['POST'])
   ↓
3. venta_controller.create_venta()
   - Extrae datos del request
   - Valida JSON
   ↓
4. venta_service.create_venta(data)
   - Valida datos de negocio
   - Calcula totales
   - Inicia transacción
   ↓
5. venta_model.create(venta_data)
   - INSERT INTO ventas
   - INSERT INTO detalle_ventas
   - UPDATE productos (stock)
   - COMMIT transacción
   ↓
6. MySQL ejecuta queries
   ↓
7. venta_model retorna ID de venta
   ↓
8. venta_service genera número de boleta
   ↓
9. venta_controller retorna JSON
   {
     "venta_id": 123,
     "numero_boleta": "B001-00123"
   }
```

## ⚛️ Arquitectura del Frontend

### Estructura de Componentes Vue

```
App.vue (Raíz)
    │
    ├── Router (Vue Router)
    │   │
    │   ├── DefaultLayout.vue (Con sidebar)
    │   │   ├── AppHeader
    │   │   ├── AppSidebar
    │   │   └── <router-view> (Vista actual)
    │   │
    │   └── AuthLayout.vue (Sin sidebar)
    │       └── <router-view> (LoginView)
    │
    ├── Views (Páginas)
    │   ├── DashboardView
    │   ├── PuntoVentaView
    │   ├── ProductosView
    │   └── ...
    │
    ├── Components (Reutilizables)
    │   ├── common/
    │   │   ├── BaseButton
    │   │   ├── BaseModal
    │   │   └── BaseTable
    │   │
    │   └── specific/
    │       ├── MetricCard
    │       └── CarritoItem
    │
    └── Pinia Stores (Estado Global)
        ├── auth
        ├── productos
        ├── ventas
        └── cart
```

### Flujo de Datos Frontend

```
1. Usuario Interacción
   │
   ▼
2. Componente Vue (View/Component)
   │
   ▼
3. Pinia Store Action
   │
   ▼
4. Service API (Axios)
   │
   ▼
5. HTTP Request → Backend
   │
   ▼
6. HTTP Response ← Backend
   │
   ▼
7. Service retorna datos
   │
   ▼
8. Store actualiza estado
   │
   ▼
9. Componente re-renderiza (reactivo)
```

### Ejemplo de Flujo Completo

**Acción:** Agregar producto al carrito

```
1. Usuario hace click en "Agregar al carrito"
   ↓
2. PuntoVentaView.vue
   <BaseButton @click="addToCart(product)">
   ↓
3. methods: {
     addToCart(product) {
       cartStore.addItem(product, quantity)
     }
   }
   ↓
4. cart.js (Pinia Store)
   addItem(product, quantity) {
     // Validar stock
     // Calcular subtotal
     // Actualizar items[]
     // Recalcular totales
   }
   ↓
5. Estado actualizado reactivamente
   ↓
6. Componente CarritoItem se actualiza
   Muestra nuevo producto en la lista
```

## 🔄 Flujo de Datos Completo

### Caso de Uso: Realizar una Venta

```
┌──────────┐  1. Usuario agrega productos  ┌──────────────┐
│ Usuario  │─────────────────────────────▶│ PuntoVenta   │
│          │                               │ View         │
└──────────┘                               └──────┬───────┘
                                                  │
                                     2. addItem() │
                                                  ▼
                                          ┌───────────────┐
                                          │  Cart Store   │
                                          │  (Pinia)      │
                                          └───────┬───────┘
                                                  │
                             3. Click "Procesar" │
                                                  ▼
                                          ┌───────────────┐
                                          │ Ventas Store  │
                                          └───────┬───────┘
                                                  │
                                4. createVenta()  │
                                                  ▼
                                          ┌───────────────┐
                                          │ventasService  │
                                          │  (Axios)      │
                                          └───────┬───────┘
                                                  │
                           5. POST /api/ventas   │
                                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND                                  │
│                                                             │
│  venta_routes → venta_controller → venta_service           │
│         ↓              ↓                 ↓                  │
│  venta_model ────────────────────▶ MySQL Database          │
│                                                             │
│  Response: { venta_id, numero_boleta }                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
         6. Response JSON │
                          ▼
                  ┌───────────────┐
                  │ventasService  │
                  └───────┬───────┘
                          │
         7. Success       │
                          ▼
                  ┌───────────────┐
                  │ Ventas Store  │
                  │ - Update list │
                  └───────┬───────┘
                          │
         8. Show toast    │
                          ▼
                  ┌───────────────┐
                  │  PuntoVenta   │
                  │  - Clear cart │
                  │  - Show PDF   │
                  └───────────────┘
```

## 🎨 Patrones de Diseño

### Backend

#### 1. Factory Pattern
```python
# app.py
def create_app(serve_frontend=False):
    app = Flask(__name__)
    # Configuración
    # Registro de blueprints
    return app

app = create_app()
```

#### 2. Repository Pattern
```python
# producto_model.py
class ProductoModel:
    @staticmethod
    def get_all():
        # Acceso a datos
        pass
    
    @staticmethod
    def get_by_id(id):
        # Acceso a datos
        pass
```

#### 3. Service Layer Pattern
```python
# producto_service.py
class ProductoService:
    def create_producto(self, data):
        # Validación de negocio
        if not self.validate_stock(data['stock']):
            raise ValueError()
        
        # Llamar al modelo
        return ProductoModel.create(data)
```

#### 4. Singleton (Database)
```python
# database.py
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Frontend

#### 1. Composition API
```javascript
// useProductos.js
export function useProductos() {
  const productos = ref([])
  const loading = ref(false)
  
  async function fetchProductos() {
    loading.value = true
    productos.value = await productosService.getAll()
    loading.value = false
  }
  
  return { productos, loading, fetchProductos }
}
```

#### 2. Store Pattern (Pinia)
```javascript
// productos.js
export const useProductosStore = defineStore('productos', {
  state: () => ({
    items: [],
    loading: false
  }),
  
  actions: {
    async fetchAll() {
      this.loading = true
      this.items = await productosService.getAll()
      this.loading = false
    }
  }
})
```

#### 3. Provider Pattern
```javascript
// main.js
createApp(App)
  .use(pinia)
  .use(router)
  .mount('#app')
```

## 🗄️ Base de Datos

### Modelo Entidad-Relación

```
┌─────────────┐       ┌──────────────┐       ┌────────────┐
│   usuarios  │       │    ventas    │       │  productos │
├─────────────┤       ├──────────────┤       ├────────────┤
│ id (PK)     │◀─────┤ cajero_id(FK)│       │ id (PK)    │
│ nombre      │       │ numero_boleta│       │ nombre     │
│ email       │       │ total        │       │ precio     │
│ password    │       │ created_at   │       │ stock      │
│ rol_id (FK) │       │ metodo_pago  │       └────────────┘
└─────────────┘       └──────────────┘              ▲
       │                     │                      │
       │                     ▼                      │
       │             ┌───────────────┐             │
       │             │detalle_ventas │             │
       │             ├───────────────┤             │
       │             │ id (PK)       │             │
       │             │ venta_id (FK) │─────────────┘
       │             │ producto_id   │
       │             │ cantidad      │
       │             │ precio        │
       │             └───────────────┘
       │
       ▼
┌─────────────┐
│    roles    │
├─────────────┤
│ id (PK)     │
│ nombre      │
└─────────────┘
```

### Índices y Optimización

```sql
-- Índices para mejor rendimiento
CREATE INDEX idx_productos_codigo ON productos(codigo_barras);
CREATE INDEX idx_ventas_cajero ON ventas(cajero_id);
CREATE INDEX idx_ventas_fecha ON ventas(created_at);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_productos_stock ON productos(stock);
```

## 🔐 Seguridad

### Autenticación JWT

```
1. Usuario hace login
   ↓
2. Backend valida credenciales
   ↓
3. Backend genera token JWT
   {
     "user_id": 1,
     "rol_id": 1,
     "exp": timestamp + 24h
   }
   ↓
4. Frontend guarda token en localStorage
   ↓
5. Cada request incluye token en header
   Authorization: Bearer <token>
   ↓
6. Backend verifica token en cada request
```

### Capas de Seguridad

| Capa | Implementación |
|------|----------------|
| **Frontend** | Vue Router Guards, Validación de inputs |
| **Red** | HTTPS (producción), CORS configurado |
| **Backend** | JWT verification, Input validation |
| **Base de Datos** | Prepared statements, Password hashing |

### Hashing de Contraseñas

```python
# Backend - password_helper.py
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
```

## 📈 Escalabilidad

### Escalabilidad Horizontal

```
       Load Balancer
            │
  ┌─────────┼─────────┐
  │         │         │
  ▼         ▼         ▼
Flask 1  Flask 2  Flask 3  (Stateless)
  │         │         │
  └─────────┼─────────┘
            │
            ▼
        MySQL Master
            │
     ┌──────┴──────┐
     ▼             ▼
  Replica 1   Replica 2
```

### Optimizaciones Implementadas

#### Backend
- ✅ Pool de conexiones MySQL
- ✅ Cache en memoria para productos activos
- ✅ Paginación en listados grandes
- ✅ Índices en tablas críticas
- ✅ Lazy loading de módulos

#### Frontend
- ✅ Lazy loading de rutas
- ✅ Code splitting (Vite)
- ✅ Debounce en búsquedas
- ✅ Virtualización de listas largas
- ✅ Minificación y compresión

### Performance

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| **Time to First Byte** | < 200ms | ~150ms |
| **First Contentful Paint** | < 1s | ~800ms |
| **API Response Time** | < 100ms | ~50ms |
| **Bundle Size** | < 500KB | ~400KB |

## 🚀 Modos de Despliegue

### Desarrollo

```
Frontend (Vite Dev Server)  ←→  Backend (Flask Debug)
   localhost:5173                localhost:5000
```

### Producción

```
Flask Static Server
   localhost:5000
      │
      ├─ /api/* → Backend API
      └─ /* → Frontend build (dist/)
```

## 📊 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTACIÓN                         │
├─────────────────────────────────────────────────────────┤
│  Vue Components │ Views │ Router │ Composables          │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│                 GESTIÓN DE ESTADO                        │
├─────────────────────────────────────────────────────────┤
│  Pinia Stores (auth, productos, ventas, cart, etc.)     │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│              SERVICIOS / API CLIENT                      │
├─────────────────────────────────────────────────────────┤
│  Axios │ Services │ Interceptors │ Error Handling       │
└────────────┬────────────────────────────────────────────┘
             │ HTTP/REST
┌────────────▼────────────────────────────────────────────┐
│                    BACKEND API                           │
├─────────────────────────────────────────────────────────┤
│  Routes │ Controllers │ Services │ Models               │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│                  BASE DE DATOS                           │
├─────────────────────────────────────────────────────────┤
│  MySQL 8.0+ │ Tables │ Indexes │ Relationships          │
└─────────────────────────────────────────────────────────┘
```

---

**Última actualización:** 2024-11-24  
**Versión del Sistema:** 2.0.0
