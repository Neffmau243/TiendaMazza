"""
Modelo Estado
"""

from config.database import Database


class EstadoModel:
    """Modelo para manejar estados"""
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los estados"""
        query = "SELECT * FROM estados ORDER BY id"
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def obtener_por_id(estado_id):
        """Obtiene un estado por ID"""
        query = "SELECT * FROM estados WHERE id = %s"
        return Database.execute_query(query, (estado_id,), fetch_one=True)
    
    @staticmethod
    def obtener_por_nombre(nombre):
        """Obtiene un estado por nombre"""
        query = "SELECT * FROM estados WHERE nombre = %s"
        return Database.execute_query(query, (nombre,), fetch_one=True)
