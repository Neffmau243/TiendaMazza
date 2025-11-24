# 📖 Guía de Instalación - Revenge POS

> Guía paso a paso para instalar y configurar el sistema completo de Punto de Venta

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

| Software | Versión Mínima | Descarga |
|----------|----------------|----------|
| **Python** | 3.11+ | [python.org](https://python.org) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org) |
| **MySQL** | 8.0+ | [mysql.com](https://mysql.com) |
| **npm** | 9+ | Incluido con Node.js |
| **Git** | 2.0+ | [git-scm.com](https://git-scm.com) |

### Verificar Instalaciones

```bash
# Verificar Python
python --version
# Salida esperada: Python 3.11.x o superior

# Verificar Node.js
node --version
# Salida esperada: v18.x.x o superior

# Verificar npm
npm --version
# Salida esperada: 9.x.x o superior

# Verificar MySQL
mysql --version
# Salida esperada: mysql Ver 8.0.x
```

## 🗂️ Paso 1: Clonar el Repositorio

```bash
# Clonar el repositorio
git clone <repository-url>

# Navegar al directorio
cd TiendaFinal
```

## 🗄️ Paso 2: Configurar Base de Datos

### 2.1. Crear Base de Datos

```bash
# Conectar a MySQL como root
mysql -u root -p

# Ingresar password cuando se solicite
```

```sql
-- Crear base de datos
CREATE DATABASE mazza CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verificar creación
SHOW DATABASES;

-- Salir de MySQL
exit;
```

### 2.2. Ejecutar Script de Tablas

```bash
# Si tienes un archivo SQL con el schema
mysql -u root -p mazza < database/schema.sql
```

O ejecutar manualmente las siguientes tablas:

<details>
<summary><strong>Click para ver Script SQL Completo</strong></summary>

```sql
-- Usar base de datos
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

-- Crear índices para mejor rendimiento
CREATE INDEX idx_productos_codigo ON productos(codigo_barras);
CREATE INDEX idx_ventas_cajero ON ventas(cajero_id);
CREATE INDEX idx_ventas_fecha ON ventas(created_at);
CREATE INDEX idx_usuarios_email ON usuarios(email);
```

</details>

### 2.3. Insertar Datos de Prueba

```sql
-- Usuario Administrador (password: 123456 hasheado con bcrypt)
INSERT INTO usuarios (nombre, email, password, rol_id) VALUES
('Administrador', 'admin@revenge.com', '$2b$12$hashed_password_here', 1),
('Juan Cajero', 'cajero@revenge.com', '$2b$12$hashed_password_here', 2),
('Pedro Almacén', 'almacen@revenge.com', '$2b$12$hashed_password_here', 3);

-- Categorías de ejemplo
INSERT INTO categorias (nombre, descripcion) VALUES
('Bebidas', 'Bebidas gaseosas y jugos'),
('Snacks', 'Galletas, papas fritas, etc'),
('Lácteos', 'Leche, yogurt, queso');

-- Productos de ejemplo
INSERT INTO productos (codigo_barras, nombre, categoria_id, precio_compra, precio_venta, stock) VALUES
('7501234567890', 'Coca Cola 500ml', 1, 1.50, 2.50, 100),
('7501234567891', 'Doritos Nacho', 2, 2.00, 3.50, 50),
('7501234567892', 'Leche Gloria 1L', 3, 3.00, 4.50, 30);

-- Proveedores de ejemplo
INSERT INTO proveedores (ruc, nombre, telefono, email) VALUES
('20123456789', 'Distribuidora Central SAC', '987654321', 'ventas@central.com'),
('20987654321', 'Mayorista del Norte EIRL', '912345678', 'contacto@mnorte.com');
```

## 🐍 Paso 3: Configurar Backend (Python/Flask)

### 3.1. Navegar al directorio del backend

```bash
cd revenge_backend
```

### 3.2. Crear entorno virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3.3. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Salida esperada:**
```
Successfully installed Flask-3.0.0 Flask-CORS-4.0.0 python-dotenv-1.0.0 
mysql-connector-python-8.2.0 reportlab-4.0.7
```

### 3.4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env (usar nano, vim, notepad, etc.)
nano .env
```

**Contenido del `.env`:**
```bash
# Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_de_mysql
DB_NAME=mazza

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta_super_segura_cambiar_en_produccion

# JWT
JWT_SECRET_KEY=tu_jwt_secret_key_cambiar_en_produccion
JWT_EXPIRATION_HOURS=24

# Puerto
PORT=5000
```

### 3.5. Probar conexión a base de datos

```bash
python test_connection.py
```

**Salida esperada:**
```
✅ Conexión exitosa a la base de datos
✅ Base de datos: mazza
✅ Tablas encontradas: 11
```

### 3.6. Volver a la raíz del proyecto

```bash
cd ..
```

## ⚛️ Paso 4: Configurar Frontend (Vue.js)

### 4.1. Navegar al directorio del frontend

```bash
cd revenge-pos-vue
```

### 4.2. Instalar dependencias

```bash
npm install
```

**Proceso esperado:**
```
added 300+ packages in 30s
```

### 4.3. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env
code .env  # o nano .env
```

**Contenido del `.env`:**
```bash
VITE_API_BASE_URL=http://127.0.0.1:5000/api
VITE_APP_NAME=Revenge POS
VITE_IVA=0.18
```

### 4.4. Volver a la raíz del proyecto

```bash
cd ..
```

## 🚀 Paso 5: Ejecutar la Aplicación

### Opción A: Modo Desarrollo (Recomendado para desarrollo)

#### Terminal 1 - Backend
```bash
# Desde la raíz del proyecto
python app.py
```

**Salida esperada:**
```
============================================================
🚀 REVENGE POS - Backend Server
============================================================
🔧 Modo: DESARROLLO (Solo API)
🔌 API Backend: http://localhost:5000
🎨 Frontend Vue: http://localhost:5173

📝 Para iniciar el frontend:
   cd revenge-pos-vue
   npm run dev

💡 Para modo producción: python app.py --production
============================================================

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

#### Terminal 2 - Frontend
```bash
# Abrir nueva terminal
cd revenge-pos-vue
npm run dev
```

**Salida esperada:**
```
  VITE v7.1.7  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Opción B: Modo Producción (Todo en un servidor)

```bash
# 1. Compilar el frontend
cd revenge-pos-vue
npm run build
cd ..

# 2. Ejecutar backend con frontend integrado
python app.py --production
```

**Salida esperada:**
```
============================================================
🚀 REVENGE POS - Backend Server
============================================================
📦 Modo: PRODUCCIÓN (API + Frontend Vue)
🌐 Aplicación completa: http://localhost:5000
⚠️  Asegúrate de haber ejecutado 'npm run build' en revenge-pos-vue/
============================================================
```

## 🔍 Paso 6: Verificación

### 6.1. Verificar Backend

```bash
# Health check
curl http://localhost:5000/health

# Debería retornar:
# {"status":"healthy","mode":"development"}

# Info de API
curl http://localhost:5000/api

# Debería retornar información de la API
```

### 6.2. Verificar Frontend

1. Abrir navegador en `http://localhost:5173` (desarrollo) o `http://localhost:5000` (producción)
2. Debería aparecer la pantalla de login
3. Probar login con:
   - Email: `admin@revenge.com`
   - Password: `123456`

### 6.3. Verificar Integración

1. Iniciar sesión
2. Navegar por las diferentes secciones:
   - Dashboard
   - Productos
   - Punto de Venta
   - Ventas
   - Usuarios (solo Admin)

## 🐛 Solución de Problemas

### Problema: Backend no inicia

**Error:** `mysql.connector.errors.DatabaseError: 2003 Can't connect to MySQL server`

**Solución:**
1. Verificar que MySQL esté corriendo:
   ```bash
   # Windows
   net start MySQL80
   
   # Linux/Mac
   sudo systemctl start mysql
   ```
2. Verificar credenciales en `.env`
3. Verificar puerto MySQL (por defecto 3306)

### Problema: Frontend no conecta al backend

**Error:** `Network Error` en consola del navegador

**Solución:**
1. Verificar que el backend esté corriendo (`http://localhost:5000`)
2. Revisar `VITE_API_BASE_URL` en `revenge-pos-vue/.env`
3. Verificar CORS en el backend
4. Limpiar caché del navegador y localStorage

### Problema: Error de autenticación

**Error:** `Invalid token` o `Unauthorized`

**Solución:**
1. Limpiar localStorage del navegador:
   ```javascript
   // En consola del navegador
   localStorage.clear()
   ```
2. Verificar que `JWT_SECRET_KEY` sea igual en backend y frontend
3. Reiniciar ambos servidores

### Problema: `npm install` falla

**Error:** `EACCES: permission denied`

**Solución:**
```bash
# Opción 1: Usar --force
npm install --force

# Opción 2: Limpiar cache y reinstalar
npm cache clean --force
rm package-lock.json
rm -rf node_modules
npm install
```

### Problema: Puerto ocupado

**Error:** `Port 5000 is already in use`

**Solución:**
```bash
# Cambiar puerto en .env del backend
PORT=5001

# O terminar proceso que usa el puerto
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

## 📝 Siguientes Pasos

Después de la instalación exitosa:

1. **Familiarízate con el sistema:**
   - Explora todas las vistas
   - Crea productos de prueba
   - Realiza ventas de prueba

2. **Personaliza la configuración:**
   - Cambia las claves secretas en producción
   - Ajusta el porcentaje de IVA si es necesario
   - Configura tus propias categorías

3. **Lee la documentación:**
   - [Documentación Backend](DOCUMENTACION_BACKEND.md)
   - [Documentación Frontend](DOCUMENTACION_FRONTEND.md)
   - [Arquitectura del Sistema](ARQUITECTURA.md)

4. **Configura para producción:**
   - Usa variables de entorno seguras
   - Configura HTTPS
   - Establece backups de base de datos
   - Configura logs de producción

## ✅ Checklist de Instalación

- [ ] Python 3.11+ instalado
- [ ] Node.js 18+ instalado
- [ ] MySQL 8.0+ instalado y corriendo
- [ ] Base de datos `mazza` creada
- [ ] Tablas creadas en MySQL
- [ ] Datos de prueba insertados
- [ ] Backend: `requirements.txt` instalado
- [ ] Backend: `.env` configurado
- [ ] Backend: Conexión a BD verificada
- [ ] Frontend: `npm install` completado
- [ ] Frontend: `.env` configurado
- [ ] Backend corriendo en puerto 5000
- [ ] Frontend corriendo en puerto 5173
- [ ] Login exitoso con usuario de prueba

## 🎉 ¡Instalación Completa!

Si completaste todos los pasos, el sistema Revenge POS está listo para usar.

**Accede a:**
- **Desarrollo:** http://localhost:5173
- **Producción:** http://localhost:5000

**Credenciales:**
- Email: `admin@revenge.com`
- Password: `123456`

---

**¿Necesitas ayuda?** Consulta la documentación completa o revisa la sección de solución de problemas.
