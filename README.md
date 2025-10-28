# Revenge Backend - Sistema de Gestión de Tienda

Backend API RESTful para sistema de punto de venta (POS) desarrollado con Flask, MySQL y arquitectura modular aplicando principios SOLID.

## 🚀 Características

- ✅ Arquitectura modular (Models, Services, Controllers, Routes)
- ✅ Principios SOLID aplicados
- ✅ Estructuras de datos optimizadas (Hash Maps, Árboles, Listas, Colas)
- ✅ Sistema de roles (Administrador, Cajero, Trabajador)
- ✅ Gestión de productos con inventario
- ✅ Sistema de ventas y compras
- ✅ Manejo de proveedores y categorías
- ✅ Movimientos de inventario rastreables
- ✅ API RESTful documentada

## 📋 Requisitos

- Python 3.8+
- MySQL 8.0+
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
cd revenge_backend
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Ejecuta el script SQL de tu base de datos `mazza` en MySQL.

### 5. Configurar variables de entorno

Copia `.env.example` a `.env` y configura:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=mazza

FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta
```

### 6. Ejecutar el servidor
```bash
python app.py
```

El servidor estará corriendo en `http://localhost:5000`

## 📚 Estructura del Proyecto

```
revenge_backend/
│
├── app.py                     # Punto de entrada principal
│
├── config/
│   ├── __init__.py
│   └── database.py            # Conexión a MySQL con pool
│
├── models/                    # Modelos de datos (acceso a BD)
│   ├── usuario_model.py       # Cache con diccionario
│   ├── producto_model.py      # Hash maps para búsqueda O(1)
│   ├── categoria_model.py     # Estructura de árbol
│   ├── venta_model.py         # Listas para detalles
│   ├── compra_model.py        # Cola FIFO para pedidos
│   └── ...
│
├── services/                  # Lógica de negocio (SOLID)
│   ├── auth_service.py        # Autenticación y autorización
│   ├── venta_service.py       # Lógica de ventas
│   ├── compra_service.py      # Lógica de compras
│   ├── producto_service.py    # Gestión de productos
│   └── usuario_service.py
│
├── controllers/               # Controladores HTTP
│   ├── auth_controller.py
│   ├── venta_controller.py
│   ├── producto_controller.py
│   └── ...
│
├── routes/                    # Definición de rutas
│   ├── auth_routes.py
│   ├── venta_routes.py
│   ├── producto_routes.py
│   └── ...
│
├── utils/                     # Utilidades
│   ├── error_handler.py       # Manejo de errores HTTP
│   ├── jwt_helper.py          # Tokens JWT (preparado)
│   ├── password_helper.py     # Hash de contraseñas (preparado)
│   └── decorators.py          # Middlewares y decoradores
│
└── requirements.txt           # Dependencias
```

## 🌐 Endpoints Principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/registrar` - Registrar usuario
- `POST /api/auth/logout` - Cerrar sesión

### Productos
- `GET /api/productos` - Listar productos
- `GET /api/productos/<id>` - Obtener producto
- `GET /api/productos/buscar?codigo=XXX` - Buscar por código
- `POST /api/productos` - Crear producto
- `PUT /api/productos/<id>` - Actualizar producto
- `DELETE /api/productos/<id>` - Eliminar producto
- `GET /api/productos/stock-bajo` - Productos con stock bajo
- `POST /api/productos/<id>/ajustar-stock` - Ajustar stock

### Categorías
- `GET /api/categorias` - Listar categorías
- `POST /api/categorias` - Crear categoría
- `PUT /api/categorias/<id>` - Actualizar categoría
- `DELETE /api/categorias/<id>` - Eliminar categoría

### Ventas
- `GET /api/ventas` - Listar ventas
- `GET /api/ventas/<id>` - Obtener venta
- `POST /api/ventas` - Registrar venta
- `GET /api/ventas/resumen-dia` - Resumen del día
- `GET /api/ventas/productos-mas-vendidos` - Top productos

### Compras
- `GET /api/compras` - Listar compras
- `GET /api/compras/<id>` - Obtener compra
- `POST /api/compras` - Registrar compra

### Usuarios
- `GET /api/usuarios` - Listar usuarios
- `GET /api/usuarios/<id>` - Obtener usuario
- `PUT /api/usuarios/<id>` - Actualizar usuario
- `DELETE /api/usuarios/<id>` - Eliminar usuario

### Proveedores
- `GET /api/proveedores` - Listar proveedores
- `POST /api/proveedores` - Crear proveedor
- `PUT /api/proveedores/<id>` - Actualizar proveedor

## 🔐 Roles y Permisos

### Administrador (rol_id = 1)
- Acceso completo al sistema
- Gestión de usuarios
- Realizar ventas
- Gestión de productos, categorías, proveedores
- Ver reportes y estadísticas

### Cajero (rol_id = 2)
- Realizar ventas
- Ver productos y categorías
- Ver su historial de ventas

### Trabajador (rol_id = 3)
- Gestión de inventario
- Registrar compras
- Gestión de productos y proveedores
- Ver productos y categorías

## 🧪 Probar con Postman

### Login
```http
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "admin@revenge.com",
  "password": "123456"
}
```

### Crear Producto
```http
POST http://localhost:5000/api/productos
Content-Type: application/json

{
  "codigo_barras": "7501234567890",
  "nombre": "Coca Cola 500ml",
  "descripcion": "Refresco carbonatado",
  "categoria_id": 1,
  "precio_compra": 8.50,
  "precio_venta": 12.00,
  "stock": 100,
  "stock_minimo": 20,
  "created_by": 1
}
```

### Registrar Venta
```http
POST http://localhost:5000/api/ventas
Content-Type: application/json

{
  "cajero_id": 1,
  "metodo_pago_id": 1,
  "items": [
    {
      "producto_id": 1,
      "cantidad": 2,
      "precio_unitario": 12.00,
      "descuento_unitario": 0
    }
  ],
  "descuento": 0,
  "impuestos": 0,
  "observaciones": "Venta de prueba"
}
```

## 📊 Estructuras de Datos Implementadas

- **Hash Maps (Diccionarios)**: Productos por código/ID, usuarios activos (O(1))
- **Árboles**: Categorías jerárquicas (preparado para subcategorías)
- **Listas**: Items de venta/compra, procesamiento LIFO
- **Colas (FIFO)**: Pedidos pendientes de procesamiento

## 🔧 Principios SOLID Aplicados

1. **Single Responsibility**: Cada clase tiene una única responsabilidad
2. **Open/Closed**: Extensible sin modificar código existente
3. **Liskov Substitution**: Herencia correcta en error handlers
4. **Interface Segregation**: Servicios específicos y cohesivos
5. **Dependency Inversion**: Dependencias de abstracciones, no implementaciones

## 📝 TODO (Pendiente)

- [ ] Implementar hash de contraseñas con bcrypt
- [ ] Implementar tokens JWT completos
- [ ] Agregar paginación en todos los listados
- [ ] Implementar filtros avanzados
- [ ] Agregar tests unitarios
- [ ] Documentación con Swagger/OpenAPI
- [ ] Rate limiting
- [ ] Logs estructurados

## 🤝 Contribuir

Este es un proyecto educativo. Siéntete libre de mejorarlo.

## 📄 Licencia

Proyecto académico - Uso libre

---

**Desarrollado con ❤️ usando Flask y MySQL**
