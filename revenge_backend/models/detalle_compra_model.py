"""
Modelo Detalle de Compra
"""

from config.database import Database


class DetalleCompraModel:
    """Modelo para manejar detalles de compra"""
    
    @staticmethod
    def crear(compra_id, producto_id, cantidad, precio_unitario):
        """Crea un detalle de compra"""
        query = """
            INSERT INTO detalle_compra (compra_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        params = (compra_id, producto_id, cantidad, precio_unitario)
        
        try:
            detalle_id = Database.execute_query(query, params, commit=True)
            return detalle_id
        except Exception as e:
            print(f"Error creando detalle de compra: {e}")
            raise
    
    @staticmethod
    def crear_multiples(compra_id, detalles_lista):
        """
        Crea múltiples detalles de compra en una transacción
        
        Args:
            detalles_lista: Lista de diccionarios con los detalles
        """
        query = """
            INSERT INTO detalle_compra (compra_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            with Database.get_cursor(commit=True) as cursor:
                for detalle in detalles_lista:
                    params = (
                        compra_id,
                        detalle['producto_id'],
                        detalle['cantidad'],
                        detalle['precio_unitario']
                    )
                    cursor.execute(query, params)
            
            return True
        except Exception as e:
            print(f"Error creando detalles de compra: {e}")
            raise
    
    @staticmethod
    def obtener_por_compra(compra_id):
        """Obtiene todos los detalles de una compra"""
        query = """
            SELECT dc.*, p.nombre as producto_nombre, p.codigo_barras
            FROM detalle_compra dc
            INNER JOIN productos p ON dc.producto_id = p.id
            WHERE dc.compra_id = %s
            ORDER BY dc.id
        """
        return Database.execute_query(query, (compra_id,), fetch_all=True)
