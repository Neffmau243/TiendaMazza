# 🎯 PROMPT PARA GENERAR FRONTEND - Sistema POS Revenge

## Contexto
Necesito crear el frontend para un sistema de Punto de Venta (POS) llamado "Revenge". Ya tengo el backend completamente funcional en Flask con MySQL.

## Requisitos del Frontend

### Tecnologías
- HTML5, CSS3, JavaScript (vanilla o framework moderno)
- Responsive design
- Interfaz moderna y limpia
- Opcional: Bootstrap, Tailwind, o framework CSS de tu elección

### Estructura del Proyecto
```
revenge_frontend/
├── index.html (login)
├── dashboard.html
├── punto-venta.html (⭐ PRINCIPAL)
├── productos.html
├── categorias.html
├── ventas.html
├── compras.html
├── usuarios.html
├── proveedores.html
├── reportes.html (⭐ NUEVO - Reportes)
├── css/
│   └── styles.css
├── js/
│   ├── config.js (configuración API)
│   ├── auth.js (autenticación)
│   ├── api.js (llamadas al backend)
│   └── [módulos por página]
    aqui metere un js para scannear los codifos d barra con mi camara de celular de momento ya lo tengo desarrollado
└── assets/
    └── [imágenes, iconos]
```

## 🔌 Conexión con Backend

### Base URL del API
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### Endpoints Disponibles

#### Autenticación
- **POST** `/api/auth/login` - Login de usuario
  ```json
  Request: { "email": "admin@revenge.com", "password": "123456" }
  Response: { "usuario_id": 1, "nombre": "Admin", "rol_id": 1, "rol_nombre": "Administrador" }
  ```

- **POST** `/api/auth/registrar` - Registrar nuevo usuario

#### Productos
- **GET** `/api/productos/` - Listar todos
- **GET** `/api/productos/buscar?codigo=XXX` - Buscar por código de barras (⭐ IMPORTANTE para punto de venta)
- **POST** `/api/productos/` - Crear producto
- **PUT** `/api/productos/:id` - Actualizar producto
- **DELETE** `/api/productos/:id` - Eliminar producto
- **GET** `/api/productos/stock-bajo` - Productos con stock bajo

#### Ventas (⭐ MÁS IMPORTANTE)
- **POST** `/api/ventas/` - Crear venta
  ```json
  {
    "usuario_id": 1,
    "cliente_nombre": "Juan Pérez",
    "metodo_pago_id": 1,
    "productos": [
      { "producto_id": 1, "cantidad": 2, "precio_unitario": 15.00 }
    ]
  }
  ```
- **GET** `/api/ventas/` - Listar ventas
- **GET** `/api/ventas/:id` - Detalle de venta

#### Categorías
- **GET** `/api/categorias/` - Listar todas
- **POST** `/api/categorias/` - Crear categoría

#### Usuarios
- **GET** `/api/usuarios/` - Listar todos
- **POST** `/api/usuarios/` - Crear usuario
- **PUT** `/api/usuarios/:id` - Actualizar usuario
- **DELETE** `/api/usuarios/:id` - Desactivar usuario

#### Proveedores
- **GET** `/api/proveedores/` - Listar todos
- **POST** `/api/proveedores/` - Crear proveedor

#### Compras
- **GET** `/api/compras/` - Listar todas
- **POST** `/api/compras/` - Registrar compra

#### Reportes (⭐ NUEVO)
- **GET** `/api/reportes/ventas?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD` - Reporte de ventas
  - Si no se especifican fechas, retorna últimos 7 días
  - Retorna: resumen, ventas por día, productos más vendidos, ventas por método de pago, ventas por cajero
  
- **GET** `/api/reportes/inventario` - Reporte de inventario
  - Retorna: resumen, productos por categoría, productos con stock bajo, productos sin stock
  
- **GET** `/api/reportes/compras?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD` - Reporte de compras
  - Si no se especifican fechas, retorna últimos 30 días
  - Retorna: resumen, compras por proveedor, productos más comprados

### Datos de Referencia
```javascript
const ROLES = {
  ADMINISTRADOR: 1,
  CAJERO: 2,
  ALMACENISTA: 3
};

const METODOS_PAGO = {
  EFECTIVO: 1,
  TARJETA_CREDITO: 2,
  TARJETA_DEBITO: 3,
  TRANSFERENCIA: 4
};

const ESTADOS = {
  ACTIVO: 1,
  INACTIVO: 2
};
```

## 📱 Pantallas/Vistas Requeridas

### 1. Login (index.html) - PÚBLICO
**Elementos:**
- Logo de "Revenge"
- Input email
- Input password (type="password")
- Botón "Iniciar Sesión"
- Mensaje de error si credenciales incorrectas

**Funcionalidad:**
- Llamar a POST `/api/auth/login`
- Guardar usuario en `localStorage` o `sessionStorage`
- Redirigir a dashboard según el rol

**Credenciales de prueba:**
- Email: `admin@revenge.com`
- Password: `123456`

---

### 2. Dashboard - TODOS LOS ROLES
**Elementos:**
- Navbar con nombre del usuario y rol
- Menú lateral con opciones según rol:
  - **Administrador:** Punto de Venta, Productos, Categorías, Ventas, Compras, Usuarios, Proveedores, **Reportes**
  - **Cajero:** Punto de Venta, Ventas
  - **Almacenista:** Productos, Compras
- Cards con:
  - Total ventas del día
  - Productos con stock bajo
  - Total productos
  - Última venta
- Botón "Cerrar Sesión"

**Funcionalidad:**
- Verificar autenticación (si no hay usuario, redirigir a login)
- Cargar datos desde:
  - GET `/api/ventas/` (filtrar hoy)
  - GET `/api/productos/stock-bajo`
  - GET `/api/productos/`

---

### 3. Punto de Venta (punto-venta.html) - ⭐ PRINCIPAL
**Roles permitidos:** Administrador, Cajero

**Layout:**
```
┌─────────────────────┬──────────────────────┐
│   BUSCAR PRODUCTO   │   CARRITO DE VENTA   │
│                     │                      │
│  [Input Código]     │  Producto 1 x2 $30   │
│  [Buscar]           │  Producto 2 x1 $25   │
│                     │  ─────────────────   │
│  Resultado:         │  Subtotal:    $55    │
│  ┌──────────────┐   │  IVA (16%):   $8.80  │
│  │ Coca Cola    │   │  ─────────────────   │
│  │ $15.00       │   │  TOTAL:       $63.80 │
│  │ [+ Agregar]  │   │                      │
│  └──────────────┘   │  [Método de Pago ▼]  │
│                     │  [Cliente (opc)]     │
│                     │  [🛒 FINALIZAR VENTA]│
└─────────────────────┴──────────────────────┘
```

**Elementos:**
- Input para código de barras (autofocus)
- Botón "Buscar Producto"
- Área de resultados de búsqueda
- Tabla/Lista de productos en carrito con:
  - Nombre, cantidad, precio unitario, subtotal
  - Botón eliminar item
  - Botón +/- cantidad
- Cálculo automático de:
  - Subtotal
  - IVA (16%)
  - Total
- Select "Método de Pago" (Efectivo, Tarjeta Crédito, Tarjeta Débito, Transferencia)
- Input opcional "Nombre del Cliente"
- Botón grande "FINALIZAR VENTA"
- Botón "Cancelar/Limpiar Carrito"

**Funcionalidad:**
1. Al escribir código de barras → GET `/api/productos/buscar?codigo=XXX`
2. Mostrar producto encontrado
3. Botón "Agregar" → Agregar al carrito (array en memoria)
4. Actualizar totales en tiempo real
5. Al hacer clic "FINALIZAR VENTA":
   - Validar que haya productos
   - Validar método de pago
   - POST `/api/ventas/` con estructura:
     ```json
     {
       "usuario_id": [del localStorage],
       "cliente_nombre": "Juan Pérez",
       "metodo_pago_id": 1,
       "productos": [
         { "producto_id": 1, "cantidad": 2, "precio_unitario": 15.00 }
       ]
     }
     ```
   - Si éxito → Mostrar mensaje, limpiar carrito, opción de imprimir ticket
   - Si error → Mostrar mensaje de error

**Importante:**
- El input de código debe tener `autofocus` y limpiarse después de cada búsqueda
- Soportar escáner de código de barras (simula un Enter después del código)
- Validar stock antes de agregar (mostrar si no hay suficiente)

---

### 4. Productos (productos.html) - Administrador, Almacenista
**Elementos:**
- Tabla con columnas: Código, Nombre, Categoría, Precio Venta, Stock, Acciones
- Botón "Nuevo Producto"
- Filtros: Por categoría, por nombre
- Indicador visual si stock < stock_minimo (texto rojo o badge)

**Modal/Form "Nuevo Producto":**
- Código de barras
- Nombre
- Descripción
- Precio compra
- Precio venta
- Stock actual
- Stock mínimo
- Categoría (select desde GET `/api/categorias/`)
- Botón "Guardar"

**Funcionalidad:**
- Listar: GET `/api/productos/`
- Crear: POST `/api/productos/`
- Editar: PUT `/api/productos/:id`
- Eliminar: DELETE `/api/productos/:id` (con confirmación)

---

### 5. Categorías (categorias.html) - Administrador
**Elementos:**
- Tabla simple: ID, Nombre, Descripción, Acciones
- Botón "Nueva Categoría"
- Modal/Form con: Nombre, Descripción

**Funcionalidad:**
- Listar: GET `/api/categorias/`
- Crear: POST `/api/categorias/`
- Editar: PUT `/api/categorias/:id`
- Eliminar: DELETE `/api/categorias/:id`

---

### 6. Ventas/Historial (ventas.html) - Administrador, Cajero
**Elementos:**
- Tabla: Folio, Fecha, Total, Cliente, Cajero, Método Pago, Acciones
- Filtros: Por fecha, por cajero
- Botón "Ver Detalle" → Modal con productos de la venta
- Botón "Cancelar Venta" (solo Admin, con confirmación)

**Funcionalidad:**
- Listar: GET `/api/ventas/`
- Detalle: GET `/api/ventas/:id`
- Cancelar: DELETE `/api/ventas/:id`

---

### 7. Compras (compras.html) - Administrador, Almacenista
**Elementos:**
- Tabla: Folio, Fecha, Proveedor, Total, Acciones
- Botón "Nueva Compra"
- Form con:
  - Select Proveedor
  - Agregar productos (similar a punto de venta pero con precio de compra)
  - Total

**Funcionalidad:**
- Listar: GET `/api/compras/`
- Crear: POST `/api/compras/`

---

### 8. Usuarios (usuarios.html) - SOLO Administrador
**Elementos:**
- Tabla: Nombre, Email, Rol, Teléfono, Estado, Acciones
- Botón "Nuevo Usuario"
- Form con: Nombre, Email, Password, Rol (select), Teléfono

**Funcionalidad:**
- Listar: GET `/api/usuarios/`
- Crear: POST `/api/usuarios/`
- Editar: PUT `/api/usuarios/:id`
- Desactivar: DELETE `/api/usuarios/:id`

---

### 9. Proveedores (proveedores.html) - Administrador
**Elementos:**
- Tabla: Nombre, Contacto, Teléfono, Email, Acciones
- Botón "Nuevo Proveedor"
- Form con: Nombre, Contacto, Teléfono, Email, Dirección

**Funcionalidad:**
- Listar: GET `/api/proveedores/`
- Crear: POST `/api/proveedores/`
- Editar: PUT `/api/proveedores/:id`
- Eliminar: DELETE `/api/proveedores/:id`

---

## 🎨 Estilo y UX

### Paleta de colores sugerida:
Fondo	Amarillo brillante y saturado (parecido al color del logo)	#FFD200	rgb(255, 210, 0)
Texto/Símbolo	Azul intenso y eléctrico (para el texto)	#0048A0	rgb(0, 72, 160)

### Navbar:
- Logo "Revenge POS"
- Nombre del usuario y rol
- Botón "Cerrar Sesión"

### Menú Lateral (Sidebar):
- Iconos para cada opción
- Resaltar opción activa
- Responsive (colapsable en móvil)

### Tablas:
- Paginación si >10 items
- Hover en filas
- Botones de acción (Editar, Eliminar) con iconos

### Formularios:
- Validación en frontend
- Mensajes de error claros
- Feedback visual al guardar

### Mensajes:
- Toast/Alert para éxito/error
- Confirmación antes de eliminar
- Loading spinner en peticiones

---

### 10. Reportes (reportes.html) - Administrador
**Elementos:**
- Tabs o secciones para 3 tipos de reportes:
  1. **Reporte de Ventas**
  2. **Reporte de Inventario**
  3. **Reporte de Compras**

#### Reporte de Ventas
**Form:**
- Input fecha inicio
- Input fecha fin
- Botón "Generar Reporte"
- Botón "Descargar PDF"

**Secciones del reporte:**
- **Resumen:** Total ventas, monto total, promedio, venta mínima/máxima
- **Gráfica:** Ventas por día (Chart.js recomendado)
- **Tabla:** Top 10 productos más vendidos
- **Gráfica de pastel:** Ventas por método de pago
- **Tabla:** Ventas por cajero

**Funcionalidad:**
- GET `/api/reportes/ventas?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD`
- Mostrar datos en cards, tablas y gráficas
- Botón PDF: Usar **jsPDF** o **pdfmake** para generar PDF con:
  - Header con logo y título "Reporte de Ventas"
  - Rango de fechas
  - Todas las tablas y resúmenes
  - Footer con fecha de generación

#### Reporte de Inventario
**Elementos:**
- Botón "Generar Reporte"
- Botón "Descargar PDF"

**Secciones del reporte:**
- **Resumen:** Total productos, valor inventario, valor venta potencial, productos con stock bajo/sin stock
- **Tabla:** Productos por categoría
- **Tabla con alerta:** Productos con stock bajo (texto rojo)
- **Tabla:** Productos sin stock

**Funcionalidad:**
- GET `/api/reportes/inventario`
- Mostrar datos con indicadores visuales (rojo para alertas)
- Generar PDF con toda la información

#### Reporte de Compras
**Form:**
- Input fecha inicio (default: hace 30 días)
- Input fecha fin (default: hoy)
- Botón "Generar Reporte"
- Botón "Descargar PDF"

**Secciones del reporte:**
- **Resumen:** Total compras, monto total, promedio
- **Tabla:** Compras por proveedor
- **Tabla:** Top 10 productos más comprados

**Funcionalidad:**
- GET `/api/reportes/compras?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD`
- Mostrar datos en tablas
- Generar PDF

**Librería recomendada para PDF:**
```javascript
// Usando jsPDF
import { jsPDF } from "jspdf";
import "jspdf-autotable";

function generarPDFVentas(data) {
  const doc = new jsPDF();
  
  // Header
  doc.setFontSize(18);
  doc.text("Reporte de Ventas", 14, 20);
  doc.setFontSize(11);
  doc.text(`Periodo: ${data.fecha_inicio} a ${data.fecha_fin}`, 14, 30);
  
  // Resumen
  doc.text(`Total Ventas: ${data.resumen.total_ventas}`, 14, 40);
  doc.text(`Monto Total: $${data.resumen.monto_total}`, 14, 46);
  
  // Tabla de productos
  doc.autoTable({
    startY: 55,
    head: [['Producto', 'Cantidad', 'Total']],
    body: data.productos_mas_vendidos.map(p => [p.producto, p.cantidad, `$${p.total}`])
  });
  
  // Guardar
  doc.save(`reporte-ventas-${Date.now()}.pdf`);
}
```

---

## 📋 Funcionalidades Extra (Opcionales pero Recomendadas)

1. **Impresión de Ticket:**
   - Después de una venta, botón "Imprimir Ticket"
   - Abrir ventana con formato de ticket
   - CSS para impresión (@media print)



3. **Búsqueda Inteligente:**
   - Autocompletar en búsqueda de productos
   - Buscar por nombre, código, o categoría

4. **Dashboard Mejorado:**
   - Gráficas de ventas (Chart.js o similar)
   - Top 5 productos más vendidos

5. **Validaciones:**
   - No permitir stock negativo
   - Validar formato de email
   - Validar precios > 0

---

## 🔒 Seguridad Frontend

- Validar autenticación en cada página (redirect a login si no hay sesión)
- Validar rol del usuario (ocultar opciones no permitidas)
- Limpiar sesión al cerrar sesión
- No exponer información sensible en localStorage

---

## 📝 Notas Técnicas

- **CORS:** Ya está habilitado en el backend
- **Content-Type:** Todas las peticiones POST/PUT deben incluir `Content-Type: application/json`
- **Manejo de errores:** El backend devuelve:
  ```json
  { "error": true, "message": "Descripción", "status_code": 400 }
  ```
- **Stock:** Se actualiza automáticamente al registrar ventas/compras

---

## 🚀 Entregables

Por favor genera:

1. **Todos los archivos HTML** mencionados
2. **CSS** organizado y responsive
3. **JavaScript modular** con:
   - `config.js` - Configuración del API
   - `auth.js` - Funciones de autenticación
   - `api.js` - Funciones para llamadas al backend
   - Scripts específicos por página
4. **README.md** con instrucciones de uso
5. **Estructura de carpetas** limpia y organizada

---

## ✅ Orden de Prioridad de Desarrollo

1. **Login** (sin esto no hay nada)
2. **Dashboard** (navegación)
3. **Punto de Venta** ⭐ (funcionalidad principal)
4. **Productos** (necesario para el punto de venta)
5. **Ventas** (historial)
6. **Categorías, Usuarios, Proveedores, Compras**
7. **Reportes** 📊 (para análisis y toma de decisiones)

---

¿Puedes generar el frontend completo siguiendo estas especificaciones?
