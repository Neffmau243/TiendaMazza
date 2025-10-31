"""
Modelo de Reportes
Consultas especializadas para generación de reportes
"""

from config.database import Database
from datetime import datetime, timedelta


class ReporteModel:
    """Modelo para consultas de reportes"""
    
    @staticmethod
    def reporte_ventas(fecha_inicio=None, fecha_fin=None):
        """
        Obtiene reporte completo de ventas en un rango de fechas
        
        Args:
            fecha_inicio (str): Fecha inicio YYYY-MM-DD
            fecha_fin (str): Fecha fin YYYY-MM-DD
            
        Returns:
            dict: Datos del reporte de ventas
        """
        # Si no hay fechas, últimos 7 días
        if not fecha_inicio:
            fecha_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        if not fecha_fin:
            fecha_fin = datetime.now().strftime('%Y-%m-%d')
        
        # Resumen general
        query_resumen = """
            SELECT 
                COUNT(*) as total_ventas,
                COALESCE(SUM(total), 0) as monto_total,
                COALESCE(AVG(total), 0) as promedio_venta,
                COALESCE(MIN(total), 0) as venta_minima,
                COALESCE(MAX(total), 0) as venta_maxima
            FROM ventas
            WHERE DATE(fecha) BETWEEN %s AND %s
        """
        resumen = Database.execute_query(query_resumen, (fecha_inicio, fecha_fin), fetch_one=True)
        
        # Ventas por día
        query_por_dia = """
            SELECT 
                DATE(fecha) as fecha,
                COUNT(*) as cantidad,
                COALESCE(SUM(total), 0) as total
            FROM ventas
            WHERE DATE(fecha) BETWEEN %s AND %s
            GROUP BY DATE(fecha)
            ORDER BY fecha
        """
        ventas_por_dia = Database.execute_query(query_por_dia, (fecha_inicio, fecha_fin))
        
        # Productos más vendidos (con más detalles)
        query_productos = """
            SELECT 
                p.codigo_barras,
                p.nombre as producto,
                c.nombre as categoria,
                SUM(dv.cantidad) as cantidad_vendida,
                dv.precio_unitario,
                COALESCE(SUM(dv.subtotal), 0) as total_vendido
            FROM detalle_venta dv
            INNER JOIN productos p ON dv.producto_id = p.id
            INNER JOIN categorias c ON p.categoria_id = c.id
            INNER JOIN ventas v ON dv.venta_id = v.id
            WHERE DATE(v.fecha) BETWEEN %s AND %s
            GROUP BY p.id, p.codigo_barras, p.nombre, c.nombre, dv.precio_unitario
            ORDER BY cantidad_vendida DESC
            LIMIT 10
        """
        productos_mas_vendidos = Database.execute_query(query_productos, (fecha_inicio, fecha_fin))
        
        # Calcular total general para porcentajes
        total_general = float(resumen['monto_total']) if resumen else 0.0
        
        # Ventas por método de pago
        query_metodos = """
            SELECT 
                mp.nombre as metodo_pago,
                COUNT(*) as cantidad,
                COALESCE(SUM(v.total), 0) as total
            FROM ventas v
            INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id
            WHERE DATE(v.fecha) BETWEEN %s AND %s
            GROUP BY mp.id, mp.nombre
            ORDER BY total DESC
        """
        ventas_por_metodo = Database.execute_query(query_metodos, (fecha_inicio, fecha_fin))
        
        # Ventas por cajero
        query_cajeros = """
            SELECT 
                u.nombre as cajero,
                COUNT(*) as cantidad_ventas,
                COALESCE(SUM(v.total), 0) as total_vendido
            FROM ventas v
            INNER JOIN usuarios u ON v.cajero_id = u.id
            WHERE DATE(v.fecha) BETWEEN %s AND %s
            GROUP BY u.id, u.nombre
            ORDER BY total_vendido DESC
        """
        ventas_por_cajero = Database.execute_query(query_cajeros, (fecha_inicio, fecha_fin))
        
        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'resumen': {
                'total_ventas': resumen['total_ventas'] if resumen else 0,
                'monto_total': float(resumen['monto_total']) if resumen else 0.0,
                'promedio_venta': float(resumen['promedio_venta']) if resumen else 0.0,
                'venta_minima': float(resumen['venta_minima']) if resumen else 0.0,
                'venta_maxima': float(resumen['venta_maxima']) if resumen else 0.0
            },
            'ventas_por_dia': [
                {
                    'fecha': str(item['fecha']),
                    'cantidad': item['cantidad'],
                    'total': float(item['total'])
                } for item in ventas_por_dia
            ],
            'productos_mas_vendidos': [
                {
                    'codigo': item['codigo_barras'],
                    'producto': item['producto'],
                    'categoria': item['categoria'],
                    'cantidad': item['cantidad_vendida'],
                    'precio_unitario': float(item['precio_unitario']),
                    'total': float(item['total_vendido']),
                    'porcentaje': round((float(item['total_vendido']) / total_general * 100), 2) if total_general > 0 else 0
                } for item in productos_mas_vendidos
            ],
            'ventas_por_metodo_pago': [
                {
                    'metodo': item['metodo_pago'],
                    'cantidad': item['cantidad'],
                    'total': float(item['total']),
                    'porcentaje': round((float(item['total']) / total_general * 100), 2) if total_general > 0 else 0
                } for item in ventas_por_metodo
            ],
            'ventas_por_cajero': [
                {
                    'cajero': item['cajero'],
                    'cantidad': item['cantidad_ventas'],
                    'total': float(item['total_vendido']),
                    'ticket_promedio': round(float(item['total_vendido']) / item['cantidad_ventas'], 2) if item['cantidad_ventas'] > 0 else 0,
                    'porcentaje': round((float(item['total_vendido']) / total_general * 100), 2) if total_general > 0 else 0
                } for item in ventas_por_cajero
            ]
        }
    
    @staticmethod
    def reporte_inventario():
        """
        Obtiene reporte del estado del inventario
        
        Returns:
            dict: Datos del reporte de inventario
        """
        # Resumen general
        query_resumen = """
            SELECT 
                COUNT(*) as total_productos,
                COALESCE(SUM(stock * precio_compra), 0) as valor_inventario,
                COALESCE(SUM(stock * precio_venta), 0) as valor_venta,
                SUM(CASE WHEN stock <= stock_minimo THEN 1 ELSE 0 END) as productos_stock_bajo,
                SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) as productos_sin_stock
            FROM productos
            WHERE deleted_at IS NULL
        """
        resumen = Database.execute_query(query_resumen, fetch_one=True)
        
        # Productos por categoría
        query_categorias = """
            SELECT 
                c.nombre as categoria,
                COUNT(p.id) as cantidad_productos,
                COALESCE(SUM(p.stock), 0) as stock_total,
                COALESCE(SUM(p.stock * p.precio_compra), 0) as valor_inventario
            FROM categorias c
            LEFT JOIN productos p ON c.id = p.categoria_id AND p.deleted_at IS NULL
            WHERE c.deleted_at IS NULL
            GROUP BY c.id, c.nombre
            ORDER BY cantidad_productos DESC
        """
        productos_por_categoria = Database.execute_query(query_categorias)
        
        # Productos con stock bajo
        query_stock_bajo = """
            SELECT 
                p.id as producto_id,
                p.codigo_barras,
                p.nombre,
                p.stock as stock_actual,
                p.stock_minimo,
                c.nombre as categoria
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            WHERE p.stock <= p.stock_minimo
            AND p.deleted_at IS NULL
            ORDER BY (p.stock - p.stock_minimo) ASC
        """
        productos_stock_bajo = Database.execute_query(query_stock_bajo)
        
        # Productos sin stock
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
        productos_sin_stock = Database.execute_query(query_sin_stock)
        
        return {
            'resumen': {
                'total_productos': resumen['total_productos'] if resumen else 0,
                'valor_inventario': float(resumen['valor_inventario']) if resumen else 0.0,
                'valor_venta_potencial': float(resumen['valor_venta']) if resumen else 0.0,
                'productos_stock_bajo': resumen['productos_stock_bajo'] if resumen else 0,
                'productos_sin_stock': resumen['productos_sin_stock'] if resumen else 0
            },
            'productos_por_categoria': [
                {
                    'categoria': item['categoria'],
                    'cantidad': item['cantidad_productos'],
                    'stock_total': item['stock_total'],
                    'valor': float(item['valor_inventario'])
                } for item in productos_por_categoria
            ],
            'productos_stock_bajo': [
                {
                    'producto_id': item['producto_id'],
                    'codigo_barras': item['codigo_barras'],
                    'nombre': item['nombre'],
                    'stock_actual': item['stock_actual'],
                    'stock_minimo': item['stock_minimo'],
                    'categoria': item['categoria']
                } for item in productos_stock_bajo
            ],
            'productos_sin_stock': [
                {
                    'producto_id': item['producto_id'],
                    'codigo_barras': item['codigo_barras'],
                    'nombre': item['nombre'],
                    'categoria': item['categoria']
                } for item in productos_sin_stock
            ]
        }
    
    @staticmethod
    def reporte_compras(fecha_inicio=None, fecha_fin=None):
        """
        Obtiene reporte de compras en un rango de fechas
        
        Args:
            fecha_inicio (str): Fecha inicio YYYY-MM-DD
            fecha_fin (str): Fecha fin YYYY-MM-DD
            
        Returns:
            dict: Datos del reporte de compras
        """
        # Si no hay fechas, últimos 30 días
        if not fecha_inicio:
            fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not fecha_fin:
            fecha_fin = datetime.now().strftime('%Y-%m-%d')
        
        # Resumen general
        query_resumen = """
            SELECT 
                COUNT(*) as total_compras,
                COALESCE(SUM(total), 0) as monto_total,
                COALESCE(AVG(total), 0) as promedio_compra
            FROM compras
            WHERE DATE(fecha) BETWEEN %s AND %s
        """
        resumen = Database.execute_query(query_resumen, (fecha_inicio, fecha_fin), fetch_one=True)
        
        # Compras por proveedor
        query_proveedores = """
            SELECT 
                pr.nombre as proveedor,
                COUNT(*) as cantidad_compras,
                COALESCE(SUM(c.total), 0) as total_comprado
            FROM compras c
            INNER JOIN proveedores pr ON c.proveedor_id = pr.id
            WHERE DATE(c.fecha) BETWEEN %s AND %s
            GROUP BY pr.id, pr.nombre
            ORDER BY total_comprado DESC
        """
        compras_por_proveedor = Database.execute_query(query_proveedores, (fecha_inicio, fecha_fin))
        
        # Productos más comprados (con más detalles)
        query_productos = """
            SELECT 
                p.codigo_barras,
                p.nombre as producto,
                c.nombre as categoria,
                SUM(dc.cantidad) as cantidad_comprada,
                dc.precio_unitario,
                COALESCE(SUM(dc.subtotal), 0) as total_gastado
            FROM detalle_compra dc
            INNER JOIN productos p ON dc.producto_id = p.id
            INNER JOIN categorias c ON p.categoria_id = c.id
            INNER JOIN compras co ON dc.compra_id = co.id
            WHERE DATE(co.fecha) BETWEEN %s AND %s
            GROUP BY p.id, p.codigo_barras, p.nombre, c.nombre, dc.precio_unitario
            ORDER BY cantidad_comprada DESC
            LIMIT 10
        """
        productos_mas_comprados = Database.execute_query(query_productos, (fecha_inicio, fecha_fin))
        
        # Compras por día
        query_por_dia = """
            SELECT 
                DATE(fecha) as fecha,
                COUNT(*) as cantidad,
                COALESCE(SUM(total), 0) as total
            FROM compras
            WHERE DATE(fecha) BETWEEN %s AND %s
            GROUP BY DATE(fecha)
            ORDER BY fecha
        """
        compras_por_dia = Database.execute_query(query_por_dia, (fecha_inicio, fecha_fin))
        
        # Calcular total general para porcentajes
        total_general = float(resumen['monto_total']) if resumen else 0.0
        
        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'resumen': {
                'total_compras': resumen['total_compras'] if resumen else 0,
                'monto_total': float(resumen['monto_total']) if resumen else 0.0,
                'promedio_compra': float(resumen['promedio_compra']) if resumen else 0.0
            },
            'compras_por_proveedor': [
                {
                    'proveedor': item['proveedor'],
                    'cantidad': item['cantidad_compras'],
                    'total': float(item['total_comprado']),
                    'porcentaje': round((float(item['total_comprado']) / total_general * 100), 2) if total_general > 0 else 0
                } for item in compras_por_proveedor
            ],
            'productos_mas_comprados': [
                {
                    'codigo': item['codigo_barras'],
                    'producto': item['producto'],
                    'categoria': item['categoria'],
                    'cantidad': item['cantidad_comprada'],
                    'precio_unitario': float(item['precio_unitario']),
                    'total': float(item['total_gastado']),
                    'porcentaje': round((float(item['total_gastado']) / total_general * 100), 2) if total_general > 0 else 0
                } for item in productos_mas_comprados
            ],
            'compras_por_dia': [
                {
                    'fecha': str(item['fecha']),
                    'cantidad': item['cantidad'],
                    'total': float(item['total'])
                } for item in compras_por_dia
            ]
        }
