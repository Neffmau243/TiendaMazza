-- ================================================================================
-- 🧪 CONSULTAS SQL DE PRUEBA PARA REPORTES
-- ================================================================================
-- Ejecuta estas consultas directamente en MySQL para verificar que funcionan
-- correctamente con tu base de datos "mazza"
-- ================================================================================

USE mazza;

-- ================================================================================
-- 1️⃣  PRUEBA: RESUMEN DE VENTAS
-- ================================================================================

-- Obtener resumen general de ventas (últimos 7 días)
SELECT 
    COUNT(*) as total_ventas,
    COALESCE(SUM(total), 0) as monto_total,
    COALESCE(AVG(total), 0) as promedio_venta,
    COALESCE(MIN(total), 0) as venta_minima,
    COALESCE(MAX(total), 0) as venta_maxima
FROM ventas
WHERE DATE(fecha) BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE();

-- Ventas por día
SELECT 
    DATE(fecha) as fecha,
    COUNT(*) as cantidad,
    COALESCE(SUM(total), 0) as total
FROM ventas
WHERE DATE(fecha) BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
GROUP BY DATE(fecha)
ORDER BY fecha;

-- ================================================================================
-- 2️⃣  PRUEBA: PRODUCTOS MÁS VENDIDOS
-- ================================================================================

SELECT 
    p.nombre as producto,
    p.codigo_barras,
    SUM(dv.cantidad) as cantidad_vendida,
    COALESCE(SUM(dv.subtotal), 0) as total_vendido
FROM detalle_venta dv
INNER JOIN productos p ON dv.producto_id = p.id
INNER JOIN ventas v ON dv.venta_id = v.id
WHERE DATE(v.fecha) BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
GROUP BY p.id, p.nombre, p.codigo_barras
ORDER BY cantidad_vendida DESC
LIMIT 10;

-- ================================================================================
-- 3️⃣  PRUEBA: VENTAS POR MÉTODO DE PAGO
-- ================================================================================

SELECT 
    mp.nombre as metodo_pago,
    mp.id,
    COUNT(*) as cantidad,
    COALESCE(SUM(v.total), 0) as total
FROM ventas v
INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id
WHERE DATE(v.fecha) BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
GROUP BY mp.id, mp.nombre
ORDER BY total DESC;

-- ================================================================================
-- 4️⃣  PRUEBA: VENTAS POR CAJERO
-- ================================================================================

SELECT 
    u.nombre as cajero,
    u.id,
    COUNT(*) as cantidad_ventas,
    COALESCE(SUM(v.total), 0) as total_vendido
FROM ventas v
INNER JOIN usuarios u ON v.cajero_id = u.id  -- ⚠️  Nota: cajero_id
WHERE DATE(v.fecha) BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
GROUP BY u.id, u.nombre
ORDER BY total_vendido DESC;

-- ================================================================================
-- 5️⃣  PRUEBA: INVENTARIO - RESUMEN GENERAL
-- ================================================================================

SELECT 
    COUNT(*) as total_productos,
    COALESCE(SUM(stock * precio_compra), 0) as valor_inventario,
    COALESCE(SUM(stock * precio_venta), 0) as valor_venta_potencial,
    SUM(CASE WHEN stock <= stock_minimo THEN 1 ELSE 0 END) as productos_stock_bajo,
    SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) as productos_sin_stock
FROM productos
WHERE deleted_at IS NULL;

-- ================================================================================
-- 6️⃣  PRUEBA: PRODUCTOS POR CATEGORÍA
-- ================================================================================

SELECT 
    c.nombre as categoria,
    c.id,
    COUNT(p.id) as cantidad_productos,
    COALESCE(SUM(p.stock), 0) as stock_total,
    COALESCE(SUM(p.stock * p.precio_compra), 0) as valor_inventario
FROM categorias c
LEFT JOIN productos p ON c.id = p.categoria_id AND p.deleted_at IS NULL
WHERE c.deleted_at IS NULL
GROUP BY c.id, c.nombre
ORDER BY cantidad_productos DESC;

-- ================================================================================
-- 7️⃣  PRUEBA: PRODUCTOS CON STOCK BAJO
-- ================================================================================

SELECT 
    p.id as producto_id,
    p.codigo_barras,
    p.nombre,
    p.stock as stock_actual,
    p.stock_minimo,
    c.nombre as categoria,
    (p.stock - p.stock_minimo) as diferencia
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id
WHERE p.stock <= p.stock_minimo
AND p.deleted_at IS NULL
ORDER BY (p.stock - p.stock_minimo) ASC
LIMIT 10;

-- ================================================================================
-- 8️⃣  PRUEBA: PRODUCTOS SIN STOCK
-- ================================================================================

SELECT 
    p.id as producto_id,
    p.codigo_barras,
    p.nombre,
    c.nombre as categoria
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id
WHERE p.stock = 0
AND p.deleted_at IS NULL
ORDER BY p.nombre;

-- ================================================================================
-- 9️⃣  PRUEBA: RESUMEN DE COMPRAS
-- ================================================================================

SELECT 
    COUNT(*) as total_compras,
    COALESCE(SUM(total), 0) as monto_total,
    COALESCE(AVG(total), 0) as promedio_compra
FROM compras
WHERE DATE(fecha) BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE();

-- ================================================================================
-- 🔟 PRUEBA: COMPRAS POR PROVEEDOR
-- ================================================================================

SELECT 
    pr.nombre as proveedor,
    pr.ruc,
    pr.id,
    COUNT(*) as cantidad_compras,
    COALESCE(SUM(c.total), 0) as total_comprado
FROM compras c
INNER JOIN proveedores pr ON c.proveedor_id = pr.id
WHERE DATE(c.fecha) BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
GROUP BY pr.id, pr.nombre, pr.ruc
ORDER BY total_comprado DESC;

-- ================================================================================
-- 1️⃣1️⃣  PRUEBA: PRODUCTOS MÁS COMPRADOS
-- ================================================================================

SELECT 
    p.nombre as producto,
    p.codigo_barras,
    SUM(dc.cantidad) as cantidad_comprada,
    COALESCE(SUM(dc.subtotal), 0) as total_gastado
FROM detalle_compra dc
INNER JOIN productos p ON dc.producto_id = p.id
INNER JOIN compras c ON dc.compra_id = c.id
WHERE DATE(c.fecha) BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
GROUP BY p.id, p.nombre, p.codigo_barras
ORDER BY cantidad_comprada DESC
LIMIT 10;

-- ================================================================================
-- 🔍 VERIFICACIÓN: ESTRUCTURA DE TABLAS
-- ================================================================================

-- Verificar estructura de ventas (debe tener cajero_id)
DESCRIBE ventas;

-- Verificar estructura de productos (debe tener stock, no stock_actual)
DESCRIBE productos;

-- Verificar estructura de detalle_venta (debe tener subtotal GENERATED)
DESCRIBE detalle_venta;

-- Verificar estructura de detalle_compra (debe tener subtotal GENERATED)
DESCRIBE detalle_compra;

-- ================================================================================
-- 🧮 VERIFICACIÓN: COLUMNAS GENERADAS
-- ================================================================================

-- Probar que subtotal se calcula automáticamente en detalle_venta
SELECT 
    dv.id,
    dv.cantidad,
    dv.precio_unitario,
    dv.descuento_unitario,
    dv.subtotal,  -- Esta columna es GENERATED ALWAYS
    (dv.cantidad * (dv.precio_unitario - dv.descuento_unitario)) as calculo_manual
FROM detalle_venta dv
LIMIT 5;

-- Probar que subtotal se calcula automáticamente en detalle_compra
SELECT 
    dc.id,
    dc.cantidad,
    dc.precio_unitario,
    dc.subtotal,  -- Esta columna es GENERATED ALWAYS
    (dc.cantidad * dc.precio_unitario) as calculo_manual
FROM detalle_compra dc
LIMIT 5;

-- ================================================================================
-- 📊 CONSULTAS DE DATOS DE EJEMPLO
-- ================================================================================

-- Ver todas las ventas
SELECT 
    v.id,
    v.numero_boleta,
    v.fecha,
    u.nombre as cajero,
    mp.nombre as metodo_pago,
    v.total
FROM ventas v
INNER JOIN usuarios u ON v.cajero_id = u.id
INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id
ORDER BY v.fecha DESC
LIMIT 10;

-- Ver todos los productos con su stock
SELECT 
    p.id,
    p.codigo_barras,
    p.nombre,
    c.nombre as categoria,
    p.stock,
    p.stock_minimo,
    p.precio_compra,
    p.precio_venta,
    CASE 
        WHEN p.stock = 0 THEN '🚨 SIN STOCK'
        WHEN p.stock <= p.stock_minimo THEN '⚠️  STOCK BAJO'
        ELSE '✅ OK'
    END as estado_stock
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id
WHERE p.deleted_at IS NULL
ORDER BY p.stock ASC;

-- Ver todas las compras
SELECT 
    c.id,
    c.numero_factura,
    c.fecha,
    pr.nombre as proveedor,
    u.nombre as usuario,
    c.total
FROM compras c
INNER JOIN proveedores pr ON c.proveedor_id = pr.id
INNER JOIN usuarios u ON c.usuario_id = u.id
ORDER BY c.fecha DESC
LIMIT 10;

-- ================================================================================
-- ✅ CHECKLIST DE VALIDACIÓN
-- ================================================================================
-- 
-- Ejecuta cada sección y verifica:
-- 
-- ✅ Las consultas se ejecutan sin errores
-- ✅ Los resultados tienen sentido (no hay valores NULL inesperados)
-- ✅ Las columnas calculadas (subtotal) funcionan correctamente
-- ✅ Los JOINs encuentran las relaciones correctamente
-- ✅ Los filtros de fecha funcionan
-- ✅ Los filtros deleted_at IS NULL funcionan
-- 
-- Si todo funciona aquí, entonces los reportes en Python también funcionarán ✅
-- ================================================================================
