"""
Configuración de conexión a MySQL
Implementa pool de conexiones para mejor rendimiento
"""

import pymysql
from pymysql import cursors
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """Configuración de la base de datos siguiendo el principio Single Responsibility"""
    
    HOST = os.getenv('DB_HOST', 'localhost')
    PORT = int(os.getenv('DB_PORT', 3306))
    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE = os.getenv('DB_NAME', 'mazza')
    CHARSET = 'utf8mb4'
    
    # Configuración del pool
    MAX_CONNECTIONS = 10
    CONNECT_TIMEOUT = 10


class Database:
    """Clase para manejar la conexión a MySQL con patrón Singleton"""
    
    _instance = None
    _connection_pool = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    @staticmethod
    def get_connection():
        """Obtiene una conexión a la base de datos"""
        try:
            connection = pymysql.connect(
                host=DatabaseConfig.HOST,
                port=DatabaseConfig.PORT,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                database=DatabaseConfig.DATABASE,
                charset=DatabaseConfig.CHARSET,
                cursorclass=cursors.DictCursor,
                autocommit=False
            )
            return connection
        except pymysql.Error as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            raise
    
    @staticmethod
    @contextmanager
    def get_cursor(commit=False):
        """
        Context manager para manejar cursores de manera segura
        
        Args:
            commit (bool): Si True, hace commit automáticamente al finalizar
            
        Usage:
            with Database.get_cursor(commit=True) as cursor:
                cursor.execute("INSERT INTO ...")
        """
        connection = None
        cursor = None
        try:
            connection = Database.get_connection()
            cursor = connection.cursor()
            yield cursor
            
            if commit:
                connection.commit()
                
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error en la operación de BD: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
        """
        Ejecuta una query de manera simple
        
        Args:
            query (str): Query SQL
            params (tuple): Parámetros de la query
            fetch_one (bool): Retorna un solo resultado
            fetch_all (bool): Retorna todos los resultados (por defecto si no es commit)
            commit (bool): Hace commit de la transacción
            
        Returns:
            dict, list, int: Dependiendo del tipo de query
        """
        with Database.get_cursor(commit=commit) as cursor:
            cursor.execute(query, params or ())
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all or (not commit and not fetch_one):
                # Por defecto, si no es commit ni fetch_one, retorna todos
                return cursor.fetchall()
            else:
                return cursor.lastrowid if commit else cursor.rowcount
    
    @staticmethod
    def test_connection():
        """Prueba la conexión a la base de datos"""
        try:
            with Database.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return True if result else False
        except Exception as e:
            print(f"❌ Test de conexión fallido: {e}")
            return False


# Instancia global
db = Database()


if __name__ == '__main__':
    # Test de conexión
    print("🔍 Probando conexión a la base de datos...")
    if db.test_connection():
        print("✅ Conexión exitosa!")
    else:
        print("❌ Conexión fallida!")
