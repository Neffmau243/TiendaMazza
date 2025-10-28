"""
Modelo Detalle de Venta
Estructura: Lista para procesar items de venta
"""

from config.database import Database


class DetalleVentaModel:
    """Modelo para manejar detalles de venta"""
    
    @staticmethod
    def crear(venta_id, producto_id, cantidad, precio_unitario, descuento_unitario=0):
        """Crea un detalle de venta"""
        query = """
            INSERT INTO detalle_venta (venta_id, producto_id, cantidad, 
                                      precio_unitario, descuento_unitario)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (venta_id, producto_id, cantidad, precio_unitario, descuento_unitario)
        
        try:
            detalle_id = Database.execute_query(query, params, commit=True)
            return detalle_id
        except Exception as e:
            print(f"Error creando detalle de venta: {e}")
            raise
    
    @staticmethod
    def crear_multiples(venta_id, detalles_lista):
        """
        Crea múltiples detalles de venta en una transacción
        
        Args:
            detalles_lista: Lista de diccionarios con los detalles
            [
                {
                    'producto_id': 1,
                    'cantidad': 2,
                    'precio_unitario': 10.50,
                    'descuento_unitario': 0
                },
                ...
            ]
        """
        query = """
            INSERT INTO detalle_venta (venta_id, producto_id, cantidad, 
                                      precio_unitario, descuento_unitario)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            with Database.get_cursor(commit=True) as cursor:
                for detalle in detalles_lista:
                    params = (
                        venta_id,
                        detalle['producto_id'],
                        detalle['cantidad'],
                        detalle['precio_unitario'],
                        detalle.get('descuento_unitario', 0)
                    )
                    cursor.execute(query, params)
            
            return True
        except Exception as e:
            print(f"Error creando detalles de venta: {e}")
            raise
    
    @staticmethod
    def obtener_por_venta(venta_id):
        """Obtiene todos los detalles de una venta"""
        query = """
            SELECT dv.*, p.nombre as producto_nombre, p.codigo_barras
            FROM detalle_venta dv
            INNER JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = %s
            ORDER BY dv.id
        """
        return Database.execute_query(query, (venta_id,), fetch_all=True)
    
    @staticmethod
    def obtener_por_producto(producto_id, limite=50):
        """Obtiene las ventas de un producto específico"""
        query = """
            SELECT dv.*, v.numero_boleta, v.fecha, v.cajero_id, u.nombre as cajero_nombre
            FROM detalle_venta dv
            INNER JOIN ventas v ON dv.venta_id = v.id
            INNER JOIN usuarios u ON v.cajero_id = u.id
            WHERE dv.producto_id = %s
            ORDER BY v.fecha DESC
            LIMIT %s
        """
        return Database.execute_query(query, (producto_id, limite), fetch_all=True)
