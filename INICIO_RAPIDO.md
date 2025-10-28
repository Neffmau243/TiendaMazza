# GUÍA DE INICIO RÁPIDO - Revenge Backend

## 📋 Pasos para ejecutar el proyecto

### 1️⃣ Instalar dependencias
```powershell
# Crear entorno virtual (recomendado)
python -m venv venv
.\venv\Scripts\activate

# Instalar paquetes
pip install -r requirements.txt
```

### 2️⃣ Configurar base de datos

1. Ejecuta el script SQL para crear la base de datos `mazza`
2. Copia `.env.example` a `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
3. Edita `.env` con tus credenciales de MySQL

### 3️⃣ Probar conexión
```powershell
python test_connection.py
```

### 4️⃣ Iniciar servidor
```powershell
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

---

## 🧪 Probar con Postman

### Importar en Postman

Puedes importar estos endpoints directamente:

#### 1. Login
```
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "admin@revenge.com",
  "password": "123456"
}
```

#### 2. Listar Productos
```
GET http://localhost:5000/api/productos
```

#### 3. Crear Producto
```
POST http://localhost:5000/api/productos
Content-Type: application/json

{
  "codigo_barras": "7501234567890",
  "nombre": "Producto Ejemplo",
  "descripcion": "Descripción del producto",
  "categoria_id": 1,
  "precio_compra": 10.00,
  "precio_venta": 15.00,
  "stock": 50,
  "stock_minimo": 10,
  "created_by": 1
}
```

#### 4. Crear Venta
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
      "precio_unitario": 15.00,
      "descuento_unitario": 0
    }
  ],
  "descuento": 0,
  "impuestos": 0
}
```

---

## 📊 Endpoints Disponibles

### Autenticación
- POST `/api/auth/login` - Iniciar sesión
- POST `/api/auth/registrar` - Registrar usuario

### Productos
- GET `/api/productos` - Listar todos
- GET `/api/productos/<id>` - Obtener uno
- GET `/api/productos/buscar?codigo=XXX` - Buscar
- POST `/api/productos` - Crear
- PUT `/api/productos/<id>` - Actualizar
- DELETE `/api/productos/<id>` - Eliminar
- GET `/api/productos/stock-bajo` - Stock bajo

### Categorías
- GET `/api/categorias` - Listar
- POST `/api/categorias` - Crear
- PUT `/api/categorias/<id>` - Actualizar
- DELETE `/api/categorias/<id>` - Eliminar

### Ventas
- GET `/api/ventas` - Listar
- GET `/api/ventas/<id>` - Obtener
- POST `/api/ventas` - Crear venta
- GET `/api/ventas/resumen-dia` - Resumen
- GET `/api/ventas/productos-mas-vendidos` - Top productos

### Compras
- GET `/api/compras` - Listar
- POST `/api/compras` - Crear

### Usuarios
- GET `/api/usuarios` - Listar
- PUT `/api/usuarios/<id>` - Actualizar

### Proveedores
- GET `/api/proveedores` - Listar
- POST `/api/proveedores` - Crear

---

## 🔑 Usuarios de prueba

**Administrador:**
- Email: `admin@revenge.com`
- Password: `123456`
- Rol: Administrador (full access)

---

## ⚠️ Notas Importantes

1. **Hashing de contraseñas**: Por ahora está deshabilitado (contraseñas en texto plano). Implementar bcrypt cuando estés listo.

2. **JWT**: Está preparado pero no implementado completamente. Puedes trabajar sin tokens por ahora.

3. **CORS**: Habilitado para facilitar pruebas.

4. **Roles**:
   - Administrador (1): Acceso completo
   - Cajero (2): Solo ventas
   - Trabajador (3): Inventario y compras

---

## 🐛 Solución de Problemas

### Error de conexión a MySQL
```
Verifica que MySQL esté corriendo:
- En servicios de Windows
- Credenciales correctas en .env
```

### Import errors
```powershell
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Puerto ocupado
```powershell
# Cambiar puerto en .env o terminar proceso
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## 📞 Soporte

Lee el README.md completo para más información.

¡Buena suerte con tu proyecto! 🚀
