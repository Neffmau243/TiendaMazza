"""
Modelo Compra
Estructura: Cola para procesar pedidos pendientes
"""

from config.database import Database
from datetime import datetime


class CompraModel:
    """Modelo para manejar compras"""
    
    # Cola de compras pendientes (FIFO)
    _cola_compras_pendientes = []
    
    @staticmethod
    def crear(numero_factura, proveedor_id, usuario_id, subtotal, 
              impuestos, total, observaciones=None):
        """Crea una nueva compra"""
        query = """
            INSERT INTO compras (numero_factura, proveedor_id, usuario_id,
                               subtotal, impuestos, total, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (numero_factura, proveedor_id, usuario_id, subtotal, 
                 impuestos, total, observaciones)
        
        try:
            compra_id = Database.execute_query(query, params, commit=True)
            return compra_id
        except Exception as e:
            print(f"Error creando compra: {e}")
            raise
    
    @staticmethod
    def obtener_por_id(compra_id):
        """Obtiene una compra con sus detalles"""
        query = """
            SELECT c.*, p.nombre as proveedor_nombre, u.nombre as usuario_nombre
            FROM compras c
            INNER JOIN proveedores p ON c.proveedor_id = p.id
            INNER JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.id = %s
        """
        compra = Database.execute_query(query, (compra_id,), fetch_one=True)
        
        if compra:
            compra['detalles'] = CompraModel.obtener_detalles(compra_id)
        
        return compra
    
    @staticmethod
    def obtener_todas(limite=100, offset=0):
        """Obtiene todas las compras con paginación"""
        query = """
            SELECT c.id, c.numero_factura, c.proveedor_id, p.nombre as proveedor_nombre,
                   c.usuario_id, u.nombre as usuario_nombre,
                   c.fecha, c.subtotal, c.impuestos, c.total
            FROM compras c
            INNER JOIN proveedores p ON c.proveedor_id = p.id
            INNER JOIN usuarios u ON c.usuario_id = u.id
            ORDER BY c.fecha DESC
            LIMIT %s OFFSET %s
        """
        return Database.execute_query(query, (limite, offset), fetch_all=True)
    
    @staticmethod
    def obtener_por_proveedor(proveedor_id):
        """Obtiene compras de un proveedor"""
        query = """
            SELECT c.*, u.nombre as usuario_nombre
            FROM compras c
            INNER JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.proveedor_id = %s
            ORDER BY c.fecha DESC
        """
        return Database.execute_query(query, (proveedor_id,), fetch_all=True)
    
    @staticmethod
    def obtener_por_fecha(fecha_inicio, fecha_fin):
        """Obtiene compras por rango de fechas"""
        query = """
            SELECT c.*, p.nombre as proveedor_nombre, u.nombre as usuario_nombre
            FROM compras c
            INNER JOIN proveedores p ON c.proveedor_id = p.id
            INNER JOIN usuarios u ON c.usuario_id = u.id
            WHERE DATE(c.fecha) BETWEEN %s AND %s
            ORDER BY c.fecha DESC
        """
        return Database.execute_query(query, (fecha_inicio, fecha_fin), fetch_all=True)
    
    @staticmethod
    def obtener_detalles(compra_id):
        """Obtiene los detalles de una compra"""
        query = """
            SELECT dc.*, p.nombre as producto_nombre, p.codigo_barras
            FROM detalle_compra dc
            INNER JOIN productos p ON dc.producto_id = p.id
            WHERE dc.compra_id = %s
            ORDER BY dc.id
        """
        return Database.execute_query(query, (compra_id,), fetch_all=True)
    
    @staticmethod
    def obtener_resumen_mes(año=None, mes=None):
        """Obtiene resumen de compras del mes"""
        if not año or not mes:
            now = datetime.now()
            año = now.year
            mes = now.month
        
        query = """
            SELECT 
                COUNT(*) as total_compras,
                SUM(total) as total_gastado,
                AVG(total) as compra_promedio
            FROM compras
            WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s
        """
        return Database.execute_query(query, (año, mes), fetch_one=True)
    
    @staticmethod
    def agregar_a_cola_pendientes(compra_id):
        """Agrega una compra a la cola de pendientes"""
        compra = CompraModel.obtener_por_id(compra_id)
        if compra:
            CompraModel._cola_compras_pendientes.append(compra)
    
    @staticmethod
    def obtener_siguiente_pendiente():
        """Obtiene y remueve la siguiente compra pendiente (FIFO)"""
        if CompraModel._cola_compras_pendientes:
            return CompraModel._cola_compras_pendientes.pop(0)
        return None
    
    @staticmethod
    def obtener_cola_pendientes():
        """Retorna la cola de compras pendientes"""
        return CompraModel._cola_compras_pendientes.copy()
    
    @staticmethod
    def limpiar_cola_pendientes():
        """Limpia la cola de compras pendientes"""
        CompraModel._cola_compras_pendientes.clear()
