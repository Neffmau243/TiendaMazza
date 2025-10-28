"""
Modelo Método de Pago
"""

from config.database import Database


class MetodoPagoModel:
    """Modelo para manejar métodos de pago"""
    
    @staticmethod
    def obtener_todos(incluir_inactivos=False):
        """Obtiene todos los métodos de pago"""
        query = """
            SELECT mp.*, e.nombre as estado_nombre
            FROM metodos_pago mp
            INNER JOIN estados e ON mp.estado_id = e.id
        """
        
        if not incluir_inactivos:
            query += " WHERE mp.estado_id = 1"
        
        query += " ORDER BY mp.nombre ASC"
        
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def obtener_por_id(metodo_pago_id):
        """Obtiene un método de pago por ID"""
        query = """
            SELECT mp.*, e.nombre as estado_nombre
            FROM metodos_pago mp
            INNER JOIN estados e ON mp.estado_id = e.id
            WHERE mp.id = %s
        """
        return Database.execute_query(query, (metodo_pago_id,), fetch_one=True)
