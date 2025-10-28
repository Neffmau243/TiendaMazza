# 🔧 SOLUCIÓN A PROBLEMAS DE CONEXIÓN

## ❌ Error Actual
```
Access denied for user 'root'@'localhost' (using password: NO)
```

Este error significa que:
1. MySQL está intentando conectarse pero la contraseña no está configurada
2. O MySQL no está corriendo
3. O las credenciales son incorrectas

---

## ✅ SOLUCIONES PASO A PASO

### PASO 1: Verificar si MySQL está instalado y corriendo

#### Opción A: Buscar MySQL en Servicios de Windows
1. Presiona `Win + R`
2. Escribe: `services.msc`
3. Busca "MySQL" o "MySQL80" en la lista
4. Si está, verifica que esté "Iniciado"
5. Si no está iniciado, clic derecho → Iniciar

#### Opción B: Usar XAMPP, WAMP o similar
Si usas XAMPP:
1. Abre el Panel de Control de XAMPP
2. Inicia "MySQL"
3. La contraseña por defecto suele ser vacía o "root"

---

### PASO 2: Configurar el archivo .env

Abre el archivo `.env` en la carpeta `revenge_backend` y modifica según tu configuración:

#### Si usas MySQL nativo (instalación directa):
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña_aqui    # ← Pon tu contraseña de MySQL
DB_NAME=mazza
```

#### Si usas XAMPP/WAMP (contraseña vacía):
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=                       # ← Dejar vacío si no tiene contraseña
DB_NAME=mazza
```

#### Si usas XAMPP con puerto diferente:
```env
DB_HOST=localhost
DB_PORT=3307                       # ← A veces XAMPP usa 3307
DB_USER=root
DB_PASSWORD=
DB_NAME=mazza
```

---

### PASO 3: Crear la base de datos

Abre tu cliente MySQL (phpMyAdmin, MySQL Workbench, o terminal) y ejecuta:

```sql
CREATE DATABASE IF NOT EXISTS mazza CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mazza;

-- Luego ejecuta todo el script SQL que te di para crear las tablas
```

---

### PASO 4: Probar la conexión

En PowerShell:
```powershell
cd c:\Users\Neff_PM\Documents\ChambitasUwU\TiendaFinal\revenge_backend
C:/Users/Neff_PM/AppData/Local/Programs/Python/Python313/python.exe test_connection.py
```

---

## 🔍 DIAGNÓSTICO RÁPIDO

### ¿No tienes MySQL instalado?

#### Opción 1: Instalar XAMPP (Más fácil)
1. Descarga: https://www.apachefriends.org/download.html
2. Instala y abre el Panel de Control
3. Inicia MySQL
4. Usa phpMyAdmin para crear la BD
5. Configuración:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=          # Vacío por defecto
   DB_NAME=mazza
   ```

#### Opción 2: Instalar MySQL Server
1. Descarga: https://dev.mysql.com/downloads/mysql/
2. Durante instalación, configura contraseña de root
3. Anota tu contraseña
4. Úsala en el .env

---

## 📋 CHECKLIST

- [ ] MySQL está instalado
- [ ] MySQL está corriendo (en servicios o XAMPP)
- [ ] Configuraste el archivo .env con las credenciales correctas
- [ ] Creaste la base de datos "mazza"
- [ ] Ejecutaste el script SQL con todas las tablas
- [ ] El test_connection.py pasa exitosamente

---

## 💡 ALTERNATIVA: Usar SQLite temporalmente

Si quieres probar sin MySQL, puedo modificar el código para usar SQLite (no requiere instalación).
Solo dime y ajusto la configuración.

---

## 📞 SIGUIENTE PASO

Una vez que:
1. MySQL esté corriendo
2. El .env esté configurado correctamente
3. La base de datos "mazza" esté creada

Ejecuta:
```powershell
python test_connection.py
```

Deberías ver:
```
✅ Conexión exitosa!
   - Estados en BD: 5
   - Roles en BD: 3
   - Usuarios en BD: 1
   - Métodos de pago en BD: 4
```

Entonces podrás iniciar el servidor:
```powershell
python app.py
```

---

¿Qué necesitas hacer primero? ¿Instalar MySQL o configurar el que ya tienes?
