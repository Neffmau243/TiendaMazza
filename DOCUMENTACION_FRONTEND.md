# 📘 Revenge POS - Documentación Frontend

> Sistema de Punto de Venta - Frontend con Vue.js 3 + Vite

![Vue.js](https://img.shields.io/badge/Vue.js-3.5.22-4FC08D?logo=vue.js&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7.1.7-646CFF?logo=vite&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-3.0.3-FFD700?logo=pinia&logoColor=black)

## 📋 Tabla de Contenidos

- [Información General](#-información-general)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías y Dependencias](#-tecnologías-y-dependencias)
- [Sistema de Diseño](#-sistema-de-diseño)
- [Componentes Principales](#-componentes-principales)
- [Vistas Principales](#-vistas-principales)
- [Stores (Pinia)](#-stores-pinia)
- [Servicios API](#-servicios-api)
- [Rutas y Navegación](#-rutas-y-navegación)
- [Composables](#-composables)
- [Configuración](#-configuración)
- [Instalación y Ejecución](#-instalación-y-ejecución)

## 📋 Información General

| Atributo | Valor |
|----------|-------|
| **Nombre del Proyecto** | Revenge POS Frontend |
| **Tecnología Principal** | Vue.js 3 (Composition API) |
| **Build Tool** | Vite 7.1.7 |
| **Gestión de Estado** | Pinia 3.0.3 |
| **Enrutamiento** | Vue Router 4.6.3 |
| **Puerto Desarrollo** | 5173 |
| **Versión** | 0.0.0 |

## 📁 Estructura del Proyecto

```
revenge-pos-vue/
├── public/                      # Archivos públicos estáticos
│   └── favicon.ico
│
├── src/
│   ├── assets/                  # Recursos estáticos
│   │   ├── images/              # Imágenes
│   │   └── styles/              # Estilos CSS
│   │       ├── main.css         # Variables y estilos globales
│   │       ├── components.css   # Estilos de componentes
│   │       ├── variables.css    # Variables CSS
│   │       └── responsive.css   # Estilos responsive
│   │
│   ├── components/              # Componentes reutilizables
│   │   ├── categorias/          # Componentes de categorías
│   │   ├── common/              # Componentes comunes
│   │   │   ├── BaseButton.vue
│   │   │   ├── BaseCard.vue
│   │   │   ├── BaseInput.vue
│   │   │   ├── BaseModal.vue
│   │   │   ├── BaseTable.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   ├── Toast.vue
│   │   │   └── ToastContainer.vue
│   │   ├── compras/             # Componentes de compras
│   │   ├── dashboard/           # Componentes del dashboard
│   │   │   └── MetricCard.vue
│   │   ├── layout/              # Componentes de layout
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   └── AppFooter.vue
│   │   ├── productos/           # Componentes de productos
│   │   ├── proveedores/         # Componentes de proveedores
│   │   ├── usuarios/            # Componentes de usuarios
│   │   └── ventas/              # Componentes de ventas
│   │       └── CarritoItem.vue
│   │
│   ├── composables/             # Composables (lógica reutilizable)
│   │   ├── useAuth.js           # Lógica de autenticación
│   │   ├── useDebounce.js       # Debounce para búsquedas
│   │   ├── useForm.js           # Manejo de formularios
│   │   ├── useModal.js          # Control de modales
│   │   ├── usePagination.js     # Paginación
│   │   └── useToast.js          # Sistema de notificaciones
│   │
│   ├── layouts/                 # Layouts de página
│   │   ├── AuthLayout.vue       # Layout para login
│   │   └── DefaultLayout.vue    # Layout principal con sidebar
│   │
│   ├── router/                  # Configuración de rutas
│   │   └── index.js             # Definición de rutas y guards
│   │
│   ├── services/                # Servicios API
│   │   ├── api.js               # Cliente HTTP base (Axios)
│   │   ├── authService.js       # Servicio de autenticación
│   │   ├── categoriasService.js # Servicio de categorías
│   │   ├── comprasService.js    # Servicio de compras
│   │   ├── productosService.js  # Servicio de productos
│   │   ├── proveedoresService.js# Servicio de proveedores
│   │   ├── reportesService.js   # Servicio de reportes
│   │   ├── usuariosService.js   # Servicio de usuarios
│   │   └── ventasService.js     # Servicio de ventas
│   │
│   ├── stores/                  # Pinia Stores (Estado global)
│   │   ├── auth.js              # Store de autenticación
│   │   ├── cart.js              # Store del carrito de compras
│   │   ├── categorias.js        # Store de categorías
│   │   ├── compras.js           # Store de compras
│   │   ├── productos.js         # Store de productos
│   │   ├── proveedores.js       # Store de proveedores
│   │   ├── ui.js                # Store de UI (modales, loading)
│   │   ├── usuarios.js          # Store de usuarios
│   │   └── ventas.js            # Store de ventas
│   │
│   ├── utils/                   # Utilidades
│   │   ├── constants.js         # Constantes de la aplicación
│   │   ├── formatters.js        # Funciones de formato (moneda, fecha)
│   │   ├── helpers.js           # Funciones auxiliares
│   │   └── validators.js        # Funciones de validación
│   │
│   ├── views/                   # Vistas/Páginas
│   │   ├── CategoriasView.vue   # Vista de categorías
│   │   ├── ComprasView.vue      # Vista de compras
│   │   ├── DashboardView.vue    # Vista del dashboard
│   │   ├── LoginView.vue        # Vista de login
│   │   ├── NotFoundView.vue     # Vista 404
│   │   ├── ProductosView.vue    # Vista de productos
│   │   ├── ProveedoresView.vue  # Vista de proveedores
│   │   ├── PuntoVentaView.vue   # Vista de punto de venta
│   │   ├── ReportesView.vue     # Vista de reportes
│   │   ├── UsuariosView.vue     # Vista de usuarios
│   │   └── VentasView.vue       # Vista de historial de ventas
│   │
│   ├── App.vue                  # Componente raíz
│   ├── main.js                  # Punto de entrada
│   └── style.css                # Estilos base
│
├── .env                         # Variables de entorno (desarrollo)
├── .env.example                 # Ejemplo de variables de entorno
├── .env.production              # Variables de entorno (producción)
├── .gitignore                   # Archivos ignorados por git
├── index.html                   # HTML principal
├── jsconfig.json                # Configuración de JavaScript
├── package.json                 # Dependencias y scripts
├── vite.config.js               # Configuración de Vite
├── README.md                    # Documentación del proyecto
└── PROYECTO_FINALIZADO.md       # Estado del proyecto
```

## 🔧 Tecnologías y Dependencias

### Dependencias Principales

```json
{
  "vue": "^3.5.22",                       // Framework progresivo
  "vue-router": "^4.6.3",                  // Enrutamiento SPA
  "pinia": "^3.0.3",                       // Gestión de estado
  "axios": "^1.13.1",                      // Cliente HTTP
  "jspdf": "^3.0.3",                       // Generación de PDFs
  "jspdf-autotable": "^5.0.2",             // Tablas en PDFs
  "@fortawesome/fontawesome-free": "^7.1.0" // Iconos
}
```

### Dependencias de Desarrollo

```json
{
  "@vitejs/plugin-vue": "^6.0.1",          // Plugin Vue para Vite
  "vite": "^7.1.7"                         // Build tool ultra rápido
}
```

### Instalación

```bash
cd revenge-pos-vue
npm install
```

## 🎨 Sistema de Diseño

### Paleta de Colores

#### Colores Primarios
```css
--primary: #007bff;        /* Azul Principal */
--primary-hover: #0056b3;  /* Azul Hover */
--primary-light: #e7f3ff;  /* Azul Claro */
```

#### Estados
```css
--success: #28a745;        /* Verde Éxito */
--danger: #dc3545;         /* Rojo Peligro */
--warning: #ffc107;        /* Naranja Advertencia */
--info: #17a2b8;           /* Celeste Información */
--purple: #6f42c1;         /* Morado */
```

#### Neutrales
```css
--dark: #333;              /* Gris Oscuro */
--gray: #666;              /* Gris Medio */
--light: #f8f9fa;          /* Gris Claro */
--border: #dee2e6;         /* Borde */
--background: #f5f5f5;     /* Fondo */
--white: #ffffff;          /* Blanco */
```

### Tipografía

```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;

/* Tamaños */
--font-xs: 0.75rem;        /* 12px */
--font-sm: 0.875rem;       /* 14px */
--font-md: 1rem;           /* 16px */
--font-lg: 1.125rem;       /* 18px */
--font-xl: 1.25rem;        /* 20px */
--font-2xl: 1.5rem;        /* 24px */
```

### Espaciado

```css
--spacing-xs: 0.25rem;     /* 4px */
--spacing-sm: 0.5rem;      /* 8px */
--spacing-md: 1rem;        /* 16px */
--spacing-lg: 1.5rem;      /* 24px */
--spacing-xl: 2rem;        /* 32px */
```

### Bordes

```css
--radius: 8px;             /* Radio estándar */
--radius-sm: 4px;          /* Radio pequeño */
--radius-lg: 12px;         /* Radio grande */
```

### Sombras

```css
--shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
--shadow-md: 0 4px 6px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 25px rgba(0,0,0,0.1);
```

## 🧩 Componentes Principales

### Componentes Comunes

#### 1. BaseButton.vue
Botón reutilizable con múltiples variantes.

**Props:**
- `variant`: string - primary, secondary, success, danger, warning
- `size`: string - sm, md, lg
- `disabled`: boolean
- `loading`: boolean

**Ejemplo:**
```vue
<BaseButton variant="primary" size="md" @click="handleClick">
  Guardar
</BaseButton>
```

#### 2. BaseInput.vue
Input con validación y mensajes de error.

**Props:**
- `modelValue`: any
- `type`: string - text, email, password, number, date
- `label`: string
- `error`: string
- `required`: boolean

**Ejemplo:**
```vue
<BaseInput
  v-model="form.email"
  type="email"
  label="Email"
  :error="errors.email"
  required
/>
```

#### 3. BaseModal.vue
Modal reutilizable con slots.

**Props:**
- `show`: boolean
- `title`: string
- `size`: string - sm, md, lg, xl

**Slots:**
- `header` - Encabezado personalizado
- `default` - Contenido principal
- `footer` - Footer personalizado

**Eventos:**
- `close` - Al cerrar modal
- `confirm` - Al confirmar

**Ejemplo:**
```vue
<BaseModal :show="showModal" title="Nuevo Producto" @close="closeModal">
  <template #default>
    <ProductForm />
  </template>
  <template #footer>
    <BaseButton @click="saveProduct">Guardar</BaseButton>
  </template>
</BaseModal>
```

#### 4. BaseTable.vue
Tabla con paginación y ordenamiento.

**Props:**
- `columns`: array - Definición de columnas
- `data`: array - Datos a mostrar
- `loading`: boolean

**Slots:**
- `acciones` - Acciones personalizadas por fila

**Eventos:**
- `sort` - Al ordenar por columna
- `page-change` - Al cambiar de página

#### 5. Toast.vue / ToastContainer.vue
Sistema de notificaciones.

**Tipos:**
- `success` - Verde
- `error` - Rojo
- `warning` - Amarillo
- `info` - Azul

**Uso:**
```javascript
import { useToast } from '@/composables/useToast'

const toast = useToast()
toast.success('Producto guardado correctamente')
toast.error('Error al guardar producto')
```

#### 6. LoadingSpinner.vue
Spinner de carga.

**Props:**
- `size`: string - sm, md, lg
- `color`: string

### Componentes de Layout

#### 1. AppHeader.vue
Encabezado con logo y menú de usuario.

**Características:**
- Muestra nombre de usuario y rol
- Botón de logout
- Responsive

#### 2. AppSidebar.vue
Menú lateral con navegación.

**Características:**
- Rutas filtradas por rol
- Indicador de ruta activa
- Colapsable en móvil
- Iconos Font Awesome

### Componentes Específicos

#### 1. MetricCard.vue (Dashboard)
Tarjeta de métricas con icono.

**Props:**
- `title`: string
- `value`: string | number
- `icon`: string
- `color`: string
- `trend`: string

#### 2. CarritoItem.vue (Punto de Venta)
Item del carrito con cantidad y precio.

**Características:**
- Botones para aumentar/disminuir cantidad
- Botón para eliminar
- Cálculo automático de subtotal

## 📱 Vistas Principales

### 1. LoginView.vue
**Ruta:** `/login`

**Características:**
- Formulario de login con validación
- Manejo de errores
- Redirección automática si ya está autenticado
- Diseño moderno y responsive

### 2. DashboardView.vue
**Ruta:** `/dashboard`

**Características:**
- Métricas principales (ventas, productos, usuarios)
- Últimas ventas realizadas
- Productos con stock bajo
- Accesos rápidos

### 3. PuntoVentaView.vue
**Ruta:** `/punto-venta`

**Características:**
- Búsqueda de productos por código de barras
- Lista de productos disponibles
- Carrito de compras interactivo
- Cálculo automático de totales e IVA (18%)
- Selección de método de pago
- Generación de boleta
- Impresión de ticket

**Flujo de uso:**
1. Buscar producto por código de barras
2. Agregar al carrito
3. Modificar cantidades si es necesario
4. Seleccionar método de pago
5. Procesar venta
6. Generar e imprimir boleta

### 4. ProductosView.vue
**Ruta:** `/productos`

**Características:**
- Listado de productos con búsqueda
- Filtros por categoría y estado
- CRUD completo (crear, editar, eliminar)
- Modal de formulario
- Indicador de stock bajo
- Paginación

### 5. VentasView.vue
**Ruta:** `/ventas`

**Características:**
- Historial de ventas
- Filtros por fecha y cajero
- Detalle de cada venta
- Búsqueda por número de boleta
- Estadísticas de ventas
- Exportación a PDF

### 6. UsuariosView.vue
**Ruta:** `/usuarios`

**Características:**
- Listado de usuarios
- CRUD completo
- Asignación de roles (Administrador, Cajero, Almacenista)
- Cambio de estado (activo/inactivo)
- Validación de email único

### 7. CategoriasView.vue
**Ruta:** `/categorias`

**Características:**
- Listado de categorías
- CRUD completo
- Contador de productos por categoría

### 8. ComprasView.vue
**Ruta:** `/compras`

**Características:**
- Registro de compras
- Selección de proveedor
- Agregar productos con cantidad y precio
- Cálculo de totales
- Historial de compras

### 9. ProveedoresView.vue
**Ruta:** `/proveedores`

**Características:**
- Listado de proveedores
- CRUD completo
- Validación de RUC
- Información de contacto

### 10. ReportesView.vue
**Ruta:** `/reportes`

**Características:**
- Reporte de ventas (PDF/Excel)
- Reporte de inventario (PDF/Excel)
- Reporte de compras
- Filtros por fecha
- Gráficos y estadísticas

## 🔄 Stores (Pinia)

### 1. auth.js
**Estado:**
```javascript
{
  user: null,
  token: null,
  isAuthenticated: false
}
```

**Acciones:**
- `login(credentials)` - Iniciar sesión
- `logout()` - Cerrar sesión
- `checkAuth()` - Verificar autenticación
- `updateUser(userData)` - Actualizar datos de usuario

**Getters:**
- `userRole` - Rol del usuario
- `userName` - Nombre del usuario
- `isAdmin` - Si es administrador

### 2. cart.js
**Estado:**
```javascript
{
  items: [],
  subtotal: 0,
  descuento: 0,
  impuestos: 0,
  total: 0
}
```

**Acciones:**
- `addItem(product, quantity)` - Agregar al carrito
- `removeItem(productId)` - Eliminar del carrito
- `updateQuantity(productId, quantity)` - Actualizar cantidad
- `clear()` - Limpiar carrito

**Getters:**
- `itemCount` - Total de items
- `totalAmount` - Monto total

### 3. productos.js
**Estado:**
```javascript
{
  productos: [],
  loading: false,
  error: null
}
```

**Acciones:**
- `fetchProductos()` - Obtener todos los productos
- `createProducto(producto)` - Crear producto
- `updateProducto(id, producto)` - Actualizar producto
- `deleteProducto(id)` - Eliminar producto

**Getters:**
- `productosPorCategoria` - Productos agrupados por categoría
- `productosStockBajo` - Productos con stock bajo

### 4. ventas.js
**Estado:**
```javascript
{
  ventas: [],
  ventaActual: null,
  loading: false
}
```

**Acciones:**
- `fetchVentas(params)` - Obtener ventas
- `createVenta(venta)` - Crear venta
- `fetchVentaById(id)` - Obtener detalle de venta

**Getters:**
- `ventasDelDia` - Ventas del día actual
- `totalVentas` - Total en ventas

## 🔌 Servicios API

### Configuración Base (api.js)

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor de request - Agregar token JWT
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor de response - Manejo de errores
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Logout automático en token inválido
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

### Servicios Disponibles

#### authService.js
```javascript
login(email, password)
logout()
getCurrentUser()
```

#### productosService.js
```javascript
getAll()
getById(id)
getByCodigoBarras(codigo)
search(query)
getStockBajo()
create(producto)
update(id, producto)
delete(id)
```

#### ventasService.js
```javascript
getAll(params)
getById(id)
getByBoleta(numero)
getByCajero(cajeroId, params)
getResumenDia(fecha)
create(venta)
```

## 🛣️ Rutas y Navegación

### Rutas Públicas

```javascript
{
  path: '/login',
  component: LoginView
}
```

### Rutas Protegidas

| Ruta | Vista | Acceso |
|------|-------|--------|
| `/` | Redirect a /dashboard | Todos |
| `/dashboard` | DashboardView | Todos |
| `/punto-venta` | PuntoVentaView | Admin, Cajero |
| `/productos` | ProductosView | Todos |
| `/categorias` | CategoriasView | Admin |
| `/ventas` | VentasView | Admin, Cajero |
| `/compras` | ComprasView | Admin, Almacenista |
| `/proveedores` | ProveedoresView | Admin |
| `/usuarios` | UsuariosView | Admin |
| `/reportes` | ReportesView | Admin |

### Guards de Navegación

```javascript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})
```

## 🎯 Composables

### useToast.js
Sistema de notificaciones.

```javascript
const toast = useToast()
toast.success('Mensaje de éxito')
toast.error('Mensaje de error')
toast.warning('Mensaje de advertencia')
toast.info('Mensaje de información')
```

### useModal.js
Control de modales.

```javascript
const { isOpen, open, close, toggle } = useModal()
```

### useForm.js
Manejo de formularios con validación.

```javascript
const { form, errors, validate, reset } = useForm(initialValues, rules)
```

## ⚙️ Configuración

### Variables de Entorno (`.env`)

```bash
VITE_API_BASE_URL=http://127.0.0.1:5000/api
VITE_APP_NAME=Revenge POS
VITE_IVA=0.18
```

### Vite Config (`vite.config.js`)

```javascript
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    }
  }
})
```

## 🚀 Instalación y Ejecución

### 1. Instalar Dependencias

```bash
cd revenge-pos-vue
npm install
```

### 2. Configurar Variables de Entorno

```bash
cp .env.example .env
# Editar .env con la URL del backend
```

### 3. Ejecutar en Desarrollo

```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

### 4. Compilar para Producción

```bash
npm run build
```

Output en: `dist/`

### 5. Preview del Build

```bash
npm run preview
```

## 🔑 Usuarios de Prueba

```
Administrador:
Email: admin@revenge.com
Password: 123456

Cajero:
Email: cajero@revenge.com
Password: 123456

Almacenista:
Email: almacen@revenge.com
Password: 123456
```

## 📊 Características Implementadas

✅ Autenticación completa con JWT  
✅ Dashboard con métricas en tiempo real  
✅ Punto de venta funcional  
✅ Gestión de productos con CRUD  
✅ Gestión de categorías  
✅ Historial de ventas  
✅ Gestión de compras  
✅ Gestión de proveedores  
✅ Gestión de usuarios  
✅ Sistema de reportes (PDF/Excel)  
✅ Sistema de notificaciones toast  
✅ Diseño responsive  
✅ Validación de formularios  
✅ Manejo de errores  
✅ Loading states  
✅ Protección de rutas por rol  

---

**Documentación actualizada:** 2024-11-24  
**Versión Frontend:** 0.0.0
