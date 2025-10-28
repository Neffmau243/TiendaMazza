# 🔧 REPORTE DE CORRECCIÓN - BACKEND DE REPORTES

## 📋 PROBLEMAS ENCONTRADOS

### 1. **Nombres de Columnas Incorrectos**

Tu base de datos usa **`id`** como nombre de columna en todas las tablas, pero el código buscaba nombres específicos como:

#### ❌ Lo que el código buscaba (INCORRECTO):
```sql
-- Columnas que NO existen en tu BD:
producto_id
venta_id
usuario_id
categoria_id
compra_id
proveedor_id
metodo_pago_id
```

#### ✅ Lo que tu BD realmente tiene (CORRECTO):
```sql
-- Todas las tablas usan simplemente:
id
```

---

### 2. **Columna `stock_actual` No Existe**

#### ❌ Código anterior:
```sql
SELECT stock_actual FROM productos
```

#### ✅ Tu BD tiene:
```sql
SELECT stock FROM productos
```

---

### 3. **Columna `estado_id` en Ventas/Compras**

Tu base de datos **NO tiene** columna `estado_id` en las tablas `ventas` y `compras`.

#### ❌ Código anterior:
```sql
WHERE v.estado_id = 1
```

#### ✅ Código corregido:
```sql
-- Se eliminó la condición estado_id
WHERE DATE(v.fecha) BETWEEN %s AND %s
```

---

### 4. **Usuario vs Cajero en Ventas**

Tu tabla `ventas` tiene `cajero_id`, no `usuario_id`.

#### ❌ Código anterior:
```sql
INNER JOIN usuarios u ON v.usuario_id = u.usuario_id
```

#### ✅ Código corregido:
```sql
INNER JOIN usuarios u ON v.cajero_id = u.id
```

---

### 5. **Soft Deletes con `deleted_at`**

Tu BD usa `deleted_at IS NULL` para verificar registros activos, no `estado_id = 1`.

#### ❌ Código anterior:
```sql
WHERE p.estado_id = 1
```

#### ✅ Código corregido:
```sql
WHERE p.deleted_at IS NULL
```

---

## ✅ CORRECCIONES APLICADAS

### **Archivo: `reporte_model.py`**

### 1️⃣ **Reporte de Ventas** (`reporte_ventas`)

#### **Cambios realizados:**

```python
# ✅ Productos más vendidos
query_productos = """
    SELECT 
        p.nombre as producto,
        SUM(dv.cantidad) as cantidad_vendida,
        COALESCE(SUM(dv.subtotal), 0) as total_vendido  # Usa subtotal calculado
    FROM detalle_venta dv
    INNER JOIN productos p ON dv.producto_id = p.id    # id en lugar de producto_id
    INNER JOIN ventas v ON dv.venta_id = v.id          # id en lugar de venta_id
    WHERE DATE(v.fecha) BETWEEN %s AND %s
    # ❌ Se eliminó: AND v.estado_id = 1
    GROUP BY p.id, p.nombre
    ORDER BY cantidad_vendida DESC
    LIMIT 10
"""

# ✅ Ventas por método de pago
query_metodos = """
    SELECT 
        mp.nombre as metodo_pago,
        COUNT(*) as cantidad,
        COALESCE(SUM(v.total), 0) as total
    FROM ventas v
    INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id  # id
    WHERE DATE(v.fecha) BETWEEN %s AND %s
    # ❌ Se eliminó: AND v.estado_id = 1
    GROUP BY mp.id, mp.nombre
    ORDER BY total DESC
"""

# ✅ Ventas por cajero
query_cajeros = """
    SELECT 
        u.nombre as cajero,
        COUNT(*) as cantidad_ventas,
        COALESCE(SUM(v.total), 0) as total_vendido
    FROM ventas v
    INNER JOIN usuarios u ON v.cajero_id = u.id  # cajero_id y u.id
    WHERE DATE(v.fecha) BETWEEN %s AND %s
    # ❌ Se eliminó: AND v.estado_id = 1
    GROUP BY u.id, u.nombre
    ORDER BY total_vendido DESC
"""
```

---

### 2️⃣ **Reporte de Inventario** (`reporte_inventario`)

#### **Cambios realizados:**

```python
# ✅ Resumen general
query_resumen = """
    SELECT 
        COUNT(*) as total_productos,
        COALESCE(SUM(stock * precio_compra), 0) as valor_inventario,      # stock
        COALESCE(SUM(stock * precio_venta), 0) as valor_venta,            # stock
        SUM(CASE WHEN stock <= stock_minimo THEN 1 ELSE 0 END) as productos_stock_bajo,
        SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) as productos_sin_stock
    FROM productos
    WHERE deleted_at IS NULL  # En lugar de estado_id = 1
"""

# ✅ Productos por categoría
query_categorias = """
    SELECT 
        c.nombre as categoria,
        COUNT(p.id) as cantidad_productos,                           # p.id
        COALESCE(SUM(p.stock), 0) as stock_total,                   # stock
        COALESCE(SUM(p.stock * p.precio_compra), 0) as valor_inventario
    FROM categorias c
    LEFT JOIN productos p ON c.id = p.categoria_id AND p.deleted_at IS NULL
    WHERE c.deleted_at IS NULL
    GROUP BY c.id, c.nombre
    ORDER BY cantidad_productos DESC
"""

# ✅ Productos con stock bajo
query_stock_bajo = """
    SELECT 
        p.id as producto_id,
        p.codigo_barras,
        p.nombre,
        p.stock as stock_actual,      # Alias stock_actual para mantener API
        p.stock_minimo,
        c.nombre as categoria
    FROM productos p
    INNER JOIN categorias c ON p.categoria_id = c.id
    WHERE p.stock <= p.stock_minimo
    AND p.deleted_at IS NULL
    ORDER BY (p.stock - p.stock_minimo) ASC
"""

# ✅ Productos sin stock
query_sin_stock = """
    SELECT 
        p.id as producto_id,
        p.codigo_barras,
        p.nombre,
        c.nombre as categoria
    FROM productos p
    INNER JOIN categorias c ON p.categoria_id = c.id
    WHERE p.stock = 0
    AND p.deleted_at IS NULL
    ORDER BY p.nombre
"""
```

---

### 3️⃣ **Reporte de Compras** (`reporte_compras`)

#### **Cambios realizados:**

```python
# ✅ Compras por proveedor
query_proveedores = """
    SELECT 
        pr.nombre as proveedor,
        COUNT(*) as cantidad_compras,
        COALESCE(SUM(c.total), 0) as total_comprado
    FROM compras c
    INNER JOIN proveedores pr ON c.proveedor_id = pr.id  # pr.id
    WHERE DATE(c.fecha) BETWEEN %s AND %s
    # ❌ Se eliminó: AND c.estado_id = 1
    GROUP BY pr.id, pr.nombre
    ORDER BY total_comprado DESC
"""

# ✅ Productos más comprados
query_productos = """
    SELECT 
        p.nombre as producto,
        SUM(dc.cantidad) as cantidad_comprada,
        COALESCE(SUM(dc.subtotal), 0) as total_gastado  # Usa subtotal calculado
    FROM detalle_compra dc
    INNER JOIN productos p ON dc.producto_id = p.id
    INNER JOIN compras c ON dc.compra_id = c.id
    WHERE DATE(c.fecha) BETWEEN %s AND %s
    # ❌ Se eliminó: AND c.estado_id = 1
    GROUP BY p.id, p.nombre
    ORDER BY cantidad_comprada DESC
    LIMIT 10
"""
```

---

## 📊 RESUMEN DE CAMBIOS

| Cambio | Antes | Después |
|--------|-------|---------|
| IDs de tablas | `producto_id`, `venta_id`, etc. | `id` |
| Stock | `stock_actual` | `stock` |
| Relación ventas-usuario | `v.usuario_id` | `v.cajero_id` |
| Filtro de activos | `estado_id = 1` | `deleted_at IS NULL` |
| Cálculo subtotales | `cantidad * precio` | Usa columnas `subtotal` calculadas |

---

## 🎯 ESTRUCTURA CORRECTA DE TU BASE DE DATOS

```sql
-- Todas las tablas principales:
usuarios (id, nombre, email, password_hash, rol_id, estado_id, created_by, ...)
categorias (id, nombre, descripcion, estado_id, created_by, ...)
productos (id, codigo_barras, nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, ...)
ventas (id, numero_boleta, cajero_id, fecha, subtotal, descuento, impuestos, total, metodo_pago_id, ...)
detalle_venta (id, venta_id, producto_id, cantidad, precio_unitario, descuento_unitario, subtotal GENERATED)
compras (id, numero_factura, proveedor_id, usuario_id, fecha, subtotal, impuestos, total, ...)
detalle_compra (id, compra_id, producto_id, cantidad, precio_unitario, subtotal GENERATED)
proveedores (id, ruc, nombre, telefono, direccion, email, ...)
metodos_pago (id, nombre, descripcion, estado_id, ...)
```

---

## ✅ PRUEBAS RECOMENDADAS

### 1. **Probar Reporte de Ventas:**
```bash
GET /api/reportes/ventas?fecha_inicio=2025-01-01&fecha_fin=2025-12-31
```

### 2. **Probar Reporte de Inventario:**
```bash
GET /api/reportes/inventario
```

### 3. **Probar Reporte de Compras:**
```bash
GET /api/reportes/compras?fecha_inicio=2025-01-01&fecha_fin=2025-12-31
```

---

## 🚨 ADVERTENCIAS

1. **Otros modelos también pueden tener el mismo problema**: Revisa `producto_model.py`, `venta_model.py`, `compra_model.py`, etc.

2. **Verifica las columnas GENERATED**: Las columnas `subtotal` en `detalle_venta` y `detalle_compra` son calculadas automáticamente, no necesitas insertarlas.

3. **Soft Deletes**: Siempre usa `deleted_at IS NULL` en lugar de `estado_id = 1` para productos, categorías, proveedores y usuarios.

---

## 📝 PRÓXIMOS PASOS

1. ✅ **Ya corregido**: `reporte_model.py`
2. ⚠️ **Pendiente revisar**: Otros modelos (producto, venta, compra, etc.)
3. ⚠️ **Pendiente revisar**: Servicios que usen los modelos
4. 🧪 **Pendiente**: Pruebas con datos reales

---

**Estado**: ✅ **REPORTES CORREGIDOS Y LISTOS PARA PRUEBAS**
