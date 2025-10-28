# 🎨 Revenge POS - Frontend

Sistema de punto de venta moderno y completo desarrollado con HTML5, CSS3 y JavaScript vanilla.

## 🚀 Características

- ✅ **Login** con autenticación JWT
- 📊 **Dashboard** con estadísticas en tiempo real
- 🛒 **Punto de Venta** (POS) con carrito dinámico
- 📦 **Gestión de Productos** (CRUD completo)
- 🏷️ **Categorías** de productos
- 💰 **Historial de Ventas** con vista detallada
- 🚚 **Registro de Compras** a proveedores
- 👥 **Gestión de Usuarios** (Admin)
- 🏢 **Gestión de Proveedores** (Admin)
- 📈 **Reportes en PDF** (Ventas, Inventario, Compras)
- 🎯 **Control de acceso basado en roles** (Administrador, Cajero, Almacenista)

## 🎨 Diseño

- **Colores corporativos**: Amarillo (#FFD200) y Azul (#0048A0)
- **Responsive**: Compatible con desktop, tablet y móvil
- **UI/UX moderna**: Font Awesome 6.4.0 para iconos
- **Sin frameworks**: JavaScript vanilla puro

## 📁 Estructura del Proyecto

```
revenge_frontend/
│
├── index.html              # Página de login
├── dashboard.html          # Dashboard principal
├── punto-venta.html        # Punto de Venta (POS)
├── productos.html          # Gestión de productos
├── categorias.html         # Gestión de categorías
├── ventas.html             # Historial de ventas
├── compras.html            # Registro de compras
├── usuarios.html           # Gestión de usuarios
├── proveedores.html        # Gestión de proveedores
├── reportes.html           # Generación de reportes
│
├── css/
│   ├── styles.css          # Estilos globales (400+ líneas)
│   └── punto-venta.css     # Estilos específicos del POS
│
├── js/
│   ├── config.js           # Configuración y constantes
│   ├── auth.js             # Autenticación y sesión
│   ├── api.js              # Wrapper para API calls
│   ├── menu.js             # Menú lateral compartido
│   ├── dashboard.js        # Lógica del dashboard
│   ├── punto-venta.js      # Lógica del POS
│   ├── productos.js        # Lógica de productos
│   ├── ventas.js           # Lógica de ventas
│   └── reportes.js         # Generación de PDFs
│
└── assets/                 # (Carpeta para imágenes/logos)
```

## ⚙️ Configuración

### 1. Configurar el Backend

Edita `js/config.js` para apuntar a tu backend:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### 2. Abrir en Navegador

Simplemente abre `index.html` en tu navegador web favorito.

**Nota**: Para desarrollo local, se recomienda usar un servidor web:

```bash
# Con Python
python -m http.server 8000

# Con Node.js (npx)
npx http-server -p 8000

# Con PHP
php -S localhost:8000
```

Luego accede a: `http://localhost:8000`

## 🔐 Usuarios de Prueba

El sistema viene con usuarios precargados:

| Email | Password | Rol |
|-------|----------|-----|
| admin@revenge.com | 123456 | Administrador |
| cajero@revenge.com | 123456 | Cajero |
| almacenista@revenge.com | 123456 | Almacenista |

## 🎯 Roles y Permisos

### Administrador
- ✅ Acceso total a todos los módulos
- ✅ Gestión de usuarios
- ✅ Reportes
- ✅ Configuración del sistema

### Cajero
- ✅ Punto de Venta
- ✅ Historial de ventas
- ❌ No puede gestionar productos o usuarios

### Almacenista
- ✅ Gestión de productos
- ✅ Registro de compras
- ✅ Control de inventario
- ❌ No puede realizar ventas

## 📱 Funcionalidades Destacadas

### Punto de Venta
- Búsqueda de productos por código de barras
- Carrito de compras dinámico
- Cálculo automático de subtotal, IVA (16%) y total
- Validación de stock en tiempo real
- Selección de método de pago (Efectivo, Tarjeta, Transferencia)
- Generación de ticket de venta
- Atajo F2 para enfocar búsqueda

### Productos
- CRUD completo (Crear, Leer, Actualizar, Desactivar)
- Búsqueda y filtros avanzados
- Alertas de stock bajo
- Gestión de precios de compra y venta
- Asociación con categorías y proveedores

### Reportes PDF
- **Ventas**: Por período, método de pago, productos más vendidos
- **Inventario**: Estado actual, stock bajo, valorización
- **Compras**: Por período, por proveedor
- Vista previa antes de generar PDF
- Librería jsPDF con autoTable

## 🛠️ Tecnologías Utilizadas

- **HTML5**: Estructura semántica
- **CSS3**: Grid, Flexbox, Variables CSS, Animaciones
- **JavaScript ES6+**: Async/Await, Modules, Arrow Functions
- **Font Awesome 6.4.0**: Iconos
- **jsPDF 2.5.1**: Generación de PDFs
- **jsPDF-AutoTable 3.5.31**: Tablas en PDFs
- **Fetch API**: Comunicación con backend
- **SessionStorage**: Gestión de sesión

## 📞 API Backend

El frontend consume una API REST en:
- **Base URL**: `http://localhost:5000/api`
- **Autenticación**: JWT (Bearer Token)
- **Formato**: JSON

### Endpoints Principales

```
POST   /api/auth/login
GET    /api/productos/
GET    /api/productos/buscar?codigo=XXX
POST   /api/ventas/
GET    /api/ventas/
GET    /api/reportes/ventas
GET    /api/reportes/inventario
GET    /api/reportes/compras
```

Ver documentación completa en `revenge_backend/ENDPOINTS.md`

## 🔧 Personalización

### Cambiar Colores

Edita las variables CSS en `css/styles.css`:

```css
:root {
  --primary-color: #FFD200;    /* Amarillo */
  --secondary-color: #0048A0;  /* Azul */
  --success-color: #10b981;    /* Verde */
  --danger-color: #ef4444;     /* Rojo */
  --warning-color: #f59e0b;    /* Naranja */
}
```

### Agregar Nuevo Módulo

1. Crea `nuevo-modulo.html` basado en la estructura existente
2. Crea `js/nuevo-modulo.js` con la lógica
3. Agrega el enlace al menú en `js/menu.js`
4. Define los endpoints en `js/config.js`

## 🚨 Manejo de Errores

El sistema incluye:
- ✅ Validación de formularios en cliente
- ✅ Mensajes toast informativos
- ✅ Redirección automática en errores de autenticación
- ✅ Confirmaciones para acciones destructivas
- ✅ Manejo de errores de red

## 📦 Dependencias Externas

Solo se requiere conexión a internet para:
- Font Awesome CDN
- jsPDF y jsPDF-AutoTable (solo en reportes)

Opcionalmente puedes descargar y hospedar localmente.

## 🎓 Integración con Scanner de Código de Barras

El sistema está preparado para integrar un scanner de cámara. La función `buscarProducto(codigo)` en `punto-venta.js` puede ser llamada desde cualquier librería de escaneo de códigos de barras.

### Ejemplo de Integración

```javascript
// Tu código de scanner
function onBarcodeScanned(barcode) {
  buscarProducto(barcode);
}
```

## 📝 Notas de Desarrollo

- **Sin Build Step**: No requiere Webpack, Vite ni ningún bundler
- **Compatible**: Chrome, Firefox, Safari, Edge (últimas versiones)
- **Tamaño ligero**: ~50KB total (sin contar imágenes)
- **Performance**: Carga instantánea, sin frameworks pesados

## 🐛 Debugging

Abre las DevTools del navegador (F12) para:
- Ver logs de la consola
- Inspeccionar llamadas API en la pestaña Network
- Revisar SessionStorage en Application > Storage

## 📄 Licencia

Proyecto desarrollado para Revenge POS © 2025

---

**Desarrollado con ⚡ por el equipo de Revenge**
