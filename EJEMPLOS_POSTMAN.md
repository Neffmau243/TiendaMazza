# EJEMPLOS PARA POSTMAN - REVENGE BACKEND

## 📌 Configuración Base
URL Base: `http://localhost:5000`

---

## 🔑 AUTENTICACIÓN

### 1. Login
```
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "admin@revenge.com",
  "password": "123456"
}
```

**Respuesta esperada:**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "id": 1,
    "nombre": "Administrador",
    "email": "admin@revenge.com",
    "rol_id": 1,
    "rol_nombre": "administrador",
    "estado": "activo"
  }
}
```

### 2. Registrar Nuevo Usuario
```
POST http://localhost:5000/api/auth/registrar
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "email": "juan@revenge.com",
  "password": "123456",
  "rol_id": 2,
  "created_by": 1
}
```

---

## 📦 PRODUCTOS

### 3. Listar Todos los Productos
```
GET http://localhost:5000/api/productos
```

### 4. Buscar Producto por Código
```
GET http://localhost:5000/api/productos/buscar?codigo=7501234567890
```

### 5. Buscar Producto por Nombre
```
GET http://localhost:5000/api/productos/buscar?nombre=Coca
```

### 6. Crear Producto
```
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

### 7. Actualizar Producto
```
PUT http://localhost:5000/api/productos/1
Content-Type: application/json

{
  "precio_venta": 13.50,
  "stock_minimo": 15
}
```

### 8. Productos con Stock Bajo
```
GET http://localhost:5000/api/productos/stock-bajo
```

### 9. Ajustar Stock
```
POST http://localhost:5000/api/productos/1/ajustar-stock
Content-Type: application/json

{
  "cantidad": 50,
  "tipo_ajuste": "entrada",
  "motivo": "Reposición de inventario",
  "usuario_id": 1
}
```

---

## 📑 CATEGORÍAS

### 10. Listar Categorías
```
GET http://localhost:5000/api/categorias
```

### 11. Crear Categoría
```
POST http://localhost:5000/api/categorias
Content-Type: application/json

{
  "nombre": "Bebidas",
  "descripcion": "Bebidas frías y calientes",
  "created_by": 1
}
```

### 12. Actualizar Categoría
```
PUT http://localhost:5000/api/categorias/1
Content-Type: application/json

{
  "nombre": "Bebidas Refrescantes",
  "descripcion": "Todo tipo de bebidas"
}
```

---

## 💰 VENTAS

### 13. Crear Venta Simple (1 producto)
```
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

### 14. Crear Venta Múltiple (varios productos)
```
POST http://localhost:5000/api/ventas
Content-Type: application/json

{
  "cajero_id": 1,
  "metodo_pago_id": 1,
  "items": [
    {
      "producto_id": 1,
      "cantidad": 3,
      "precio_unitario": 12.00,
      "descuento_unitario": 0
    },
    {
      "producto_id": 2,
      "cantidad": 5,
      "precio_unitario": 8.00,
      "descuento_unitario": 0.50
    },
    {
      "producto_id": 3,
      "cantidad": 2,
      "precio_unitario": 25.00,
      "descuento_unitario": 0
    }
  ],
  "descuento": 5.00,
  "impuestos": 0,
  "observaciones": "Venta con descuento general"
}
```

### 15. Listar Ventas
```
GET http://localhost:5000/api/ventas?limite=50&offset=0
```

### 16. Obtener Venta por ID
```
GET http://localhost:5000/api/ventas/1
```

### 17. Ventas por Rango de Fechas
```
GET http://localhost:5000/api/ventas/por-fecha?fecha_inicio=2024-01-01&fecha_fin=2024-12-31
```

### 18. Resumen del Día
```
GET http://localhost:5000/api/ventas/resumen-dia
```

### 19. Resumen de Fecha Específica
```
GET http://localhost:5000/api/ventas/resumen-dia?fecha=2024-10-13
```

### 20. Productos Más Vendidos
```
GET http://localhost:5000/api/ventas/productos-mas-vendidos?limite=10
```

---

## 🛒 COMPRAS

### 21. Crear Compra
```
POST http://localhost:5000/api/compras
Content-Type: application/json

{
  "numero_factura": "F001-00001",
  "proveedor_id": 1,
  "usuario_id": 1,
  "items": [
    {
      "producto_id": 1,
      "cantidad": 50,
      "precio_unitario": 8.50
    },
    {
      "producto_id": 2,
      "cantidad": 30,
      "precio_unitario": 6.00
    }
  ],
  "impuestos": 0,
  "observaciones": "Compra de reposición"
}
```

### 22. Listar Compras
```
GET http://localhost:5000/api/compras?limite=50&offset=0
```

### 23. Obtener Compra por ID
```
GET http://localhost:5000/api/compras/1
```

---

## 🏢 PROVEEDORES

### 24. Listar Proveedores
```
GET http://localhost:5000/api/proveedores
```

### 25. Crear Proveedor
```
POST http://localhost:5000/api/proveedores
Content-Type: application/json

{
  "ruc": "20123456789",
  "nombre": "Distribuidora ABC S.A.C.",
  "telefono": "999888777",
  "direccion": "Av. Principal 123, Lima",
  "email": "ventas@abc.com",
  "contacto": "María García",
  "created_by": 1
}
```

### 26. Actualizar Proveedor
```
PUT http://localhost:5000/api/proveedores/1
Content-Type: application/json

{
  "telefono": "999777666",
  "contacto": "Juan López"
}
```

---

## 👥 USUARIOS

### 27. Listar Usuarios
```
GET http://localhost:5000/api/usuarios
```

### 28. Listar Usuarios (incluir inactivos)
```
GET http://localhost:5000/api/usuarios?incluir_inactivos=true
```

### 29. Obtener Usuario por ID
```
GET http://localhost:5000/api/usuarios/1
```

### 30. Actualizar Usuario
```
PUT http://localhost:5000/api/usuarios/1
Content-Type: application/json

{
  "nombre": "Administrador Principal",
  "rol_id": 1
}
```

---

## 🧪 HEALTH CHECK

### 31. Verificar Estado del Servidor
```
GET http://localhost:5000/health
```

### 32. Información del API
```
GET http://localhost:5000/
```

---

## 📊 RESPUESTAS ESTÁNDAR

### Respuesta Exitosa
```json
{
  "success": true,
  "message": "Operación exitosa",
  "data": { ... }
}
```

### Respuesta de Error
```json
{
  "error": true,
  "message": "Descripción del error",
  "status_code": 400
}
```

---

## 🎯 CASOS DE USO COMPLETOS

### CASO 1: Flujo Completo de Venta

1. Buscar producto: `GET /api/productos/buscar?codigo=XXX`
2. Verificar stock disponible
3. Crear venta: `POST /api/ventas` (el stock se actualiza automáticamente)
4. Ver resumen del día: `GET /api/ventas/resumen-dia`

### CASO 2: Flujo de Compra a Proveedor

1. Crear/Buscar proveedor: `POST /api/proveedores`
2. Crear compra: `POST /api/compras` (el stock se incrementa automáticamente)
3. Verificar productos actualizados: `GET /api/productos`

### CASO 3: Gestión de Inventario

1. Ver productos con stock bajo: `GET /api/productos/stock-bajo`
2. Ajustar stock: `POST /api/productos/{id}/ajustar-stock`
3. Ver movimientos: (implementar endpoint si necesario)

---

## 💡 TIPS PARA POSTMAN

1. **Crear Colección**: Organiza todos estos endpoints en una colección
2. **Variables de Entorno**: 
   - URL: `{{base_url}}` = `http://localhost:5000`
   - Token: `{{token}}` (cuando implementes JWT)
3. **Tests**: Agrega scripts de validación en Postman
4. **Pre-request Scripts**: Para tokens automáticos

---

## ⚠️ NOTAS IMPORTANTES

- El **cajero_id** y **usuario_id** deben existir en la base de datos
- Los **producto_id** deben existir antes de crear ventas/compras
- La **categoria_id** debe existir antes de crear productos
- El **proveedor_id** debe existir antes de crear compras
- Al crear ventas, el stock se **descuenta automáticamente**
- Al crear compras, el stock se **incrementa automáticamente**
- Todos los endpoints retornan JSON
- Los códigos HTTP son estándar: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found), 500 (Server Error)

---

## 🚀 ¡LISTO PARA PROBAR!

Copia estos ejemplos directamente en Postman y comienza a probar tu API.

¡Éxito! 🎉
