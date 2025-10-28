# 🚀 Endpoints API - Revenge Backend

**Base URL:** `http://localhost:5000/api`

---

## 🔐 AUTENTICACIÓN (`/api/auth`)

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@revenge.com",
  "password": "123456"
}

✅ Response 200:
{
  "usuario_id": 1,
  "nombre": "Admin",
  "email": "admin@revenge.com",
  "rol_id": 1,
  "rol_nombre": "Administrador",
  "estado_id": 1
}
```

### Registrar Usuario
```http
POST /api/auth/registrar
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "password": "123456",
  "rol_id": 2,
  "telefono": "5551234567"
}

✅ Response 201:
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "data": {
    "usuario_id": 5,
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com"
  }
}
```

---

## 🛍️ PRODUCTOS (`/api/productos`)

### Listar Todos los Productos
```http
GET /api/productos/

✅ Response 200:
{
  "success": true,
  "data": [
    {
      "producto_id": 1,
      "codigo_barras": "7501234567890",
      "nombre": "Coca Cola 600ml",
      "descripcion": "Refresco de cola",
      "precio_compra": 10.00,
      "precio_venta": 15.00,
      "stock_actual": 100,
      "stock_minimo": 10,
      "categoria_id": 1,
      "categoria_nombre": "Bebidas"
    }
  ]
}
```

### Buscar Producto por Código de Barras
```http
GET /api/productos/buscar?codigo=7501234567890

✅ Response 200:
{
  "success": true,
  "data": {
    "producto_id": 1,
    "codigo_barras": "7501234567890",
    "nombre": "Coca Cola 600ml",
    "precio_venta": 15.00,
    "stock_actual": 100
  }
}
```

### Obtener Producto por ID
```http
GET /api/productos/1

✅ Response 200:
{
  "success": true,
  "data": {
    "producto_id": 1,
    "codigo_barras": "7501234567890",
    "nombre": "Coca Cola 600ml",
    "precio_venta": 15.00,
    "stock_actual": 100
  }
}
```

### Crear Producto
```http
POST /api/productos/
Content-Type: application/json

{
  "codigo_barras": "7501234567890",
  "nombre": "Coca Cola 600ml",
  "descripcion": "Refresco de cola",
  "precio_compra": 10.00,
  "precio_venta": 15.00,
  "stock_actual": 100,
  "stock_minimo": 10,
  "categoria_id": 1
}

✅ Response 201:
{
  "success": true,
  "message": "Producto creado exitosamente",
  "data": {
    "producto_id": 1,
    "codigo_barras": "7501234567890",
    "nombre": "Coca Cola 600ml"
  }
}
```

### Actualizar Producto
```http
PUT /api/productos/1
Content-Type: application/json

{
  "precio_venta": 16.50,
  "stock_minimo": 15
}

✅ Response 200:
{
  "success": true,
  "message": "Producto actualizado exitosamente"
}
```

### Eliminar Producto
```http
DELETE /api/productos/1

✅ Response 200:
{
  "success": true,
  "message": "Producto eliminado exitosamente"
}
```

### Productos con Stock Bajo
```http
GET /api/productos/stock-bajo

✅ Response 200:
{
  "success": true,
  "data": [
    {
      "producto_id": 1,
      "nombre": "Coca Cola 600ml",
      "stock_actual": 5,
      "stock_minimo": 10
    }
  ]
}
```

### Ajustar Stock
```http
POST /api/productos/1/ajustar-stock
Content-Type: application/json

{
  "cantidad": 50,
  "tipo": "entrada",  // "entrada" o "salida"
  "motivo": "Inventario físico"
}

✅ Response 200:
{
  "success": true,
  "message": "Stock ajustado correctamente"
}
```

---

## 📦 CATEGORÍAS (`/api/categorias`)

### Listar Todas las Categorías
```http
GET /api/categorias/

✅ Response 200:
{
  "success": true,
  "data": [
    {
      "categoria_id": 1,
      "nombre": "Bebidas",
      "descripcion": "Refrescos y bebidas",
      "estado_id": 1
    }
  ]
}
```

### Crear Categoría
```http
POST /api/categorias/
Content-Type: application/json

{
  "nombre": "Bebidas",
  "descripcion": "Refrescos y bebidas"
}

✅ Response 201:
{
  "success": true,
  "message": "Categoría creada exitosamente",
  "data": {
    "categoria_id": 1,
    "nombre": "Bebidas"
  }
}
```

### Actualizar Categoría
```http
PUT /api/categorias/1
Content-Type: application/json

{
  "nombre": "Bebidas Frías",
  "descripcion": "Refrescos y bebidas frías"
}

✅ Response 200:
{
  "success": true,
  "message": "Categoría actualizada exitosamente"
}
```

### Eliminar Categoría
```http
DELETE /api/categorias/1

✅ Response 200:
{
  "success": true,
  "message": "Categoría eliminada exitosamente"
}
```

---

## 💰 VENTAS (`/api/ventas`)

### Crear Venta (⭐ PRINCIPAL)
```http
POST /api/ventas/
Content-Type: application/json

{
  "usuario_id": 1,
  "cliente_nombre": "Juan Pérez",
  "metodo_pago_id": 1,
  "productos": [
    {
      "producto_id": 1,
      "cantidad": 2,
      "precio_unitario": 15.00
    },
    {
      "producto_id": 2,
      "cantidad": 1,
      "precio_unitario": 25.50
    }
  ]
}

✅ Response 201:
{
  "success": true,
  "message": "Venta registrada exitosamente",
  "data": {
    "venta_id": 1,
    "folio": "V-000001",
    "total": 55.50,
    "fecha": "2025-10-13 12:30:45"
  }
}
```

### Listar Todas las Ventas
```http
GET /api/ventas/

✅ Response 200:
{
  "success": true,
  "data": [
    {
      "venta_id": 1,
      "folio": "V-000001",
      "fecha": "2025-10-13",
      "total": 55.50,
      "usuario_nombre": "Admin",
      "cliente_nombre": "Juan Pérez",
      "metodo_pago": "Efectivo"
    }
  ]
}
```

### Obtener Detalle de Venta
```http
GET /api/ventas/1

✅ Response 200:
{
  "success": true,
  "data": {
    "venta_id": 1,
    "folio": "V-000001",
    "fecha": "2025-10-13 12:30:45",
    "total": 55.50,
    "cliente_nombre": "Juan Pérez",
    "productos": [
      {
        "producto_nombre": "Coca Cola 600ml",
        "cantidad": 2,
        "precio_unitario": 15.00,
        "subtotal": 30.00
      }
    ]
  }
}
```

### Cancelar Venta
```http
DELETE /api/ventas/1

✅ Response 200:
{
  "success": true,
  "message": "Venta cancelada exitosamente"
}
```

---

## 📥 COMPRAS (`/api/compras`)

### Crear Compra
```http
POST /api/compras/
Content-Type: application/json

{
  "proveedor_id": 1,
  "usuario_id": 1,
  "productos": [
    {
      "producto_id": 1,
      "cantidad": 50,
      "precio_unitario": 10.00
    }
  ]
}

✅ Response 201:
{
  "success": true,
  "message": "Compra registrada exitosamente",
  "data": {
    "compra_id": 1,
    "folio": "C-000001",
    "total": 500.00
  }
}
```

### Listar Todas las Compras
```http
GET /api/compras/

✅ Response 200:
{
  "success": true,
  "data": [
    {
      "compra_id": 1,
      "folio": "C-000001",
      "fecha": "2025-10-13",
      "total": 500.00,
      "proveedor_nombre": "Coca Cola FEMSA"
    }
  ]
}
```

### Obtener Detalle de Compra
```http
GET /api/compras/1

✅ Response 200:
{
  "success": true,
  "data": {
    "compra_id": 1,
    "folio": "C-000001",
    "fecha": "2025-10-13",
    "total": 500.00,
    "proveedor_nombre": "Coca Cola FEMSA",
    "productos": [
      {
        "producto_nombre": "Coca Cola 600ml",
        "cantidad": 50,
        "precio_unitario": 10.00,
        "subtotal": 500.00
      }
    ]
  }
}
```

---

## 👥 USUARIOS (`/api/usuarios`)

### Listar Todos los Usuarios
```http
GET /api/usuarios/

✅ Response 200:
{
  "success": true,
  "data": [
    {
      "usuario_id": 1,
      "nombre": "Admin",
      "email": "admin@revenge.com",
      "rol_nombre": "Administrador",
      "telefono": "5551234567",
      "estado_nombre": "Activo"
    }
  ]
}
```

### Obtener Usuario por ID
```http
GET /api/usuarios/1

✅ Response 200:
{
  "success": true,
  "data": {
    "usuario_id": 1,
    "nombre": "Admin",
    "email": "admin@revenge.com",
    "rol_id": 1,
    "rol_nombre": "Administrador"
  }
}
```

### Crear Usuario
```http
POST /api/usuarios/
Content-Type: application/json

{
  "nombre": "Carlos López",
  "email": "carlos@revenge.com",
  "password": "123456",
  "rol_id": 2,
  "telefono": "5551234567"
}

✅ Response 201:
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "usuario_id": 5,
    "nombre": "Carlos López"
  }
}
```

### Actualizar Usuario
```http
PUT /api/usuarios/1
Content-Type: application/json

{
  "nombre": "Carlos López Actualizado",
  "telefono": "5559876543"
}

✅ Response 200:
{
  "success": true,
  "message": "Usuario actualizado exitosamente"
}
```

### Eliminar Usuario (Desactivar)
```http
DELETE /api/usuarios/1

✅ Response 200:
{
  "success": true,
  "message": "Usuario desactivado exitosamente"
}
```

---

## 🏢 PROVEEDORES (`/api/proveedores`)

### Listar Todos los Proveedores
```http
GET /api/proveedores/

✅ Response 200:
{
  "success": true,
  "data": [
    {
      "proveedor_id": 1,
      "nombre": "Coca Cola FEMSA",
      "contacto": "Juan Pérez",
      "telefono": "5551234567",
      "email": "ventas@cocacola.com"
    }
  ]
}
```

### Crear Proveedor
```http
POST /api/proveedores/
Content-Type: application/json

{
  "nombre": "Coca Cola FEMSA",
  "contacto": "Juan Pérez",
  "telefono": "5551234567",
  "email": "ventas@cocacola.com",
  "direccion": "Av. Principal #123"
}

✅ Response 201:
{
  "success": true,
  "message": "Proveedor creado exitosamente",
  "data": {
    "proveedor_id": 1,
    "nombre": "Coca Cola FEMSA"
  }
}
```

### Actualizar Proveedor
```http
PUT /api/proveedores/1
Content-Type: application/json

{
  "telefono": "5559876543",
  "email": "nuevo@cocacola.com"
}

✅ Response 200:
{
  "success": true,
  "message": "Proveedor actualizado exitosamente"
}
```

### Eliminar Proveedor
```http
DELETE /api/proveedores/1

✅ Response 200:
{
  "success": true,
  "message": "Proveedor eliminado exitosamente"
}
```

---

## 📊 REPORTES (`/api/reportes`)

### Reporte de Ventas
```http
GET /api/reportes/ventas?fecha_inicio=2025-10-06&fecha_fin=2025-10-13

✅ Response 200:
{
  "success": true,
  "data": {
    "fecha_inicio": "2025-10-06",
    "fecha_fin": "2025-10-13",
    "resumen": {
      "total_ventas": 50,
      "monto_total": 5500.00,
      "promedio_venta": 110.00,
      "venta_minima": 50.00,
      "venta_maxima": 250.00
    },
    "ventas_por_dia": [
      {
        "fecha": "2025-10-06",
        "cantidad": 8,
        "total": 880.00
      },
      {
        "fecha": "2025-10-07",
        "cantidad": 10,
        "total": 1100.00
      }
    ],
    "productos_mas_vendidos": [
      {
        "producto": "Coca Cola 600ml",
        "cantidad": 50,
        "total": 750.00
      }
    ],
    "ventas_por_metodo_pago": [
      {
        "metodo": "Efectivo",
        "cantidad": 30,
        "total": 3300.00
      },
      {
        "metodo": "Tarjeta de Crédito",
        "cantidad": 20,
        "total": 2200.00
      }
    ],
    "ventas_por_cajero": [
      {
        "cajero": "Juan Pérez",
        "cantidad": 20,
        "total": 2200.00
      },
      {
        "cajero": "María López",
        "cantidad": 30,
        "total": 3300.00
      }
    ]
  }
}
```

### Reporte de Inventario
```http
GET /api/reportes/inventario

✅ Response 200:
{
  "success": true,
  "data": {
    "resumen": {
      "total_productos": 150,
      "valor_inventario": 15000.00,
      "valor_venta_potencial": 22500.00,
      "productos_stock_bajo": 5,
      "productos_sin_stock": 2
    },
    "productos_por_categoria": [
      {
        "categoria": "Bebidas",
        "cantidad": 50,
        "stock_total": 500,
        "valor": 7500.00
      },
      {
        "categoria": "Snacks",
        "cantidad": 30,
        "stock_total": 300,
        "valor": 4500.00
      }
    ],
    "productos_stock_bajo": [
      {
        "producto_id": 1,
        "codigo_barras": "7501234567890",
        "nombre": "Coca Cola 600ml",
        "stock_actual": 5,
        "stock_minimo": 10,
        "categoria": "Bebidas"
      }
    ],
    "productos_sin_stock": [
      {
        "producto_id": 5,
        "codigo_barras": "7501234567894",
        "nombre": "Producto agotado",
        "categoria": "Snacks"
      }
    ]
  }
}
```

### Reporte de Compras
```http
GET /api/reportes/compras?fecha_inicio=2025-09-01&fecha_fin=2025-10-13

✅ Response 200:
{
  "success": true,
  "data": {
    "fecha_inicio": "2025-09-01",
    "fecha_fin": "2025-10-13",
    "resumen": {
      "total_compras": 20,
      "monto_total": 10000.00,
      "promedio_compra": 500.00
    },
    "compras_por_proveedor": [
      {
        "proveedor": "Coca Cola FEMSA",
        "cantidad": 10,
        "total": 5000.00
      },
      {
        "proveedor": "Sabritas",
        "cantidad": 10,
        "total": 5000.00
      }
    ],
    "productos_mas_comprados": [
      {
        "producto": "Coca Cola 600ml",
        "cantidad": 200,
        "total": 2000.00
      }
    ]
  }
}
```

**Nota:** Si no se especifican fechas:
- **Ventas:** Últimos 7 días
- **Compras:** Últimos 30 días

---

## 📊 DATOS DE REFERENCIA

### Roles Disponibles:
- `1` - Administrador (acceso total)
- `2` - Cajero (ventas principalmente)
- `3` - Almacenista (inventario)

### Métodos de Pago:
- `1` - Efectivo
- `2` - Tarjeta de Crédito
- `3` - Tarjeta de Débito
- `4` - Transferencia

### Estados:
- `1` - Activo
- `2` - Inactivo

---

## 🔧 Configuración para Frontend

### JavaScript/TypeScript
```javascript
// config/api.js
const API_BASE_URL = 'http://localhost:5000/api';

export const endpoints = {
  auth: {
    login: `${API_BASE_URL}/auth/login`,
    register: `${API_BASE_URL}/auth/registrar`,
  },
  productos: {
    list: `${API_BASE_URL}/productos/`,
    search: `${API_BASE_URL}/productos/buscar`,
    stockBajo: `${API_BASE_URL}/productos/stock-bajo`,
    create: `${API_BASE_URL}/productos/`,
    update: (id) => `${API_BASE_URL}/productos/${id}`,
    delete: (id) => `${API_BASE_URL}/productos/${id}`,
  },
  ventas: {
    list: `${API_BASE_URL}/ventas/`,
    create: `${API_BASE_URL}/ventas/`,
    detail: (id) => `${API_BASE_URL}/ventas/${id}`,
  },
  categorias: {
    list: `${API_BASE_URL}/categorias/`,
    create: `${API_BASE_URL}/categorias/`,
  },
  usuarios: {
    list: `${API_BASE_URL}/usuarios/`,
    create: `${API_BASE_URL}/usuarios/`,
  },
  proveedores: {
    list: `${API_BASE_URL}/proveedores/`,
    create: `${API_BASE_URL}/proveedores/`,
  },
  compras: {
    list: `${API_BASE_URL}/compras/`,
    create: `${API_BASE_URL}/compras/`,
  },
  reportes: {
    ventas: `${API_BASE_URL}/reportes/ventas`,
    inventario: `${API_BASE_URL}/reportes/inventario`,
    compras: `${API_BASE_URL}/reportes/compras`,
  },
};

// Función helper para fetch
export const apiCall = async (url, options = {}) => {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });
  return response.json();
};
```

### Ejemplo de uso:
```javascript
// Login
const login = async (email, password) => {
  const response = await apiCall(endpoints.auth.login, {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  return response;
};

// Crear venta
const crearVenta = async (ventaData) => {
  const response = await apiCall(endpoints.ventas.create, {
    method: 'POST',
    body: JSON.stringify(ventaData),
  });
  return response;
};
```

---

## ⚠️ Notas Importantes

1. **CORS está habilitado** - Puedes hacer peticiones desde cualquier origen
2. **Todos los endpoints usan JSON** - Asegúrate de incluir `Content-Type: application/json`
3. **Las ventas actualizan el stock automáticamente** - No necesitas hacer peticiones adicionales
4. **Los errores devuelven formato estándar:**
   ```json
   {
     "error": true,
     "message": "Descripción del error",
     "status_code": 400
   }
   ```

---

✅ **Backend completamente funcional y listo para conectar con cualquier frontend**
