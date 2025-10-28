"""
Modelo Usuario
Estructura: Diccionario (hash map) para usuarios activos en memoria
"""

from config.database import Database
from datetime import datetime


class UsuarioModel:
    """Modelo para manejar usuarios - Principio Single Responsibility"""
    
    # Cache en memoria para usuarios activos (Diccionario/Hash Map)
    _usuarios_activos = {}
    
    @staticmethod
    def crear(nombre, email, password_hash, rol_id, created_by=None):
        """Crea un nuevo usuario"""
        query = """
            INSERT INTO usuarios (nombre, email, password_hash, rol_id, created_by, estado_id)
            VALUES (%s, %s, %s, %s, %s, 1)
        """
        params = (nombre, email, password_hash, rol_id, created_by)
        
        try:
            usuario_id = Database.execute_query(query, params, commit=True)
            return usuario_id
        except Exception as e:
            print(f"Error creando usuario: {e}")
            raise
    
    @staticmethod
    def obtener_por_id(usuario_id):
        """Obtiene un usuario por ID"""
        # Primero busca en cache
        if usuario_id in UsuarioModel._usuarios_activos:
            return UsuarioModel._usuarios_activos[usuario_id]
        
        query = """
            SELECT u.*, r.nombre as rol_nombre, e.nombre as estado_nombre
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            INNER JOIN estados e ON u.estado_id = e.id
            WHERE u.id = %s AND u.deleted_at IS NULL
        """
        usuario = Database.execute_query(query, (usuario_id,), fetch_one=True)
        
        # Guardar en cache si está activo
        if usuario and usuario['estado_id'] == 1:
            UsuarioModel._usuarios_activos[usuario_id] = usuario
        
        return usuario
    
    @staticmethod
    def obtener_por_email(email):
        """Obtiene un usuario por email"""
        query = """
            SELECT u.*, r.nombre as rol_nombre, e.nombre as estado_nombre
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            INNER JOIN estados e ON u.estado_id = e.id
            WHERE u.email = %s AND u.deleted_at IS NULL
        """
        return Database.execute_query(query, (email,), fetch_one=True)
    
    @staticmethod
    def obtener_todos(incluir_inactivos=False):
        """Obtiene todos los usuarios"""
        query = """
            SELECT u.id, u.nombre, u.email, u.rol_id, u.estado_id,
                   r.nombre as rol_nombre, e.nombre as estado_nombre,
                   u.created_at, u.updated_at
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            INNER JOIN estados e ON u.estado_id = e.id
            WHERE u.deleted_at IS NULL
        """
        
        if not incluir_inactivos:
            query += " AND u.estado_id = 1"
        
        query += " ORDER BY u.created_at DESC"
        
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def actualizar(usuario_id, **kwargs):
        """Actualiza un usuario"""
        campos_permitidos = ['nombre', 'email', 'rol_id', 'estado_id']
        campos = []
        valores = []
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                campos.append(f"{campo} = %s")
                valores.append(valor)
        
        if not campos:
            return False
        
        valores.append(usuario_id)
        query = f"UPDATE usuarios SET {', '.join(campos)}, updated_at = NOW() WHERE id = %s"
        
        try:
            filas_afectadas = Database.execute_query(query, tuple(valores), commit=True)
            
            # Limpiar del cache
            if usuario_id in UsuarioModel._usuarios_activos:
                del UsuarioModel._usuarios_activos[usuario_id]
            
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error actualizando usuario: {e}")
            raise
    
    @staticmethod
    def eliminar_logico(usuario_id):
        """Elimina lógicamente un usuario"""
        query = "UPDATE usuarios SET deleted_at = NOW(), estado_id = 2 WHERE id = %s"
        
        try:
            filas_afectadas = Database.execute_query(query, (usuario_id,), commit=True)
            
            # Limpiar del cache
            if usuario_id in UsuarioModel._usuarios_activos:
                del UsuarioModel._usuarios_activos[usuario_id]
            
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error eliminando usuario: {e}")
            raise
    
    @staticmethod
    def verificar_email_existe(email, excluir_id=None):
        """Verifica si un email ya existe"""
        query = "SELECT id FROM usuarios WHERE email = %s AND deleted_at IS NULL"
        params = [email]
        
        if excluir_id:
            query += " AND id != %s"
            params.append(excluir_id)
        
        resultado = Database.execute_query(query, tuple(params), fetch_one=True)
        return resultado is not None
    
    @staticmethod
    def obtener_por_rol(rol_id):
        """Obtiene todos los usuarios de un rol específico"""
        query = """
            SELECT u.*, r.nombre as rol_nombre
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.id
            WHERE u.rol_id = %s AND u.deleted_at IS NULL AND u.estado_id = 1
            ORDER BY u.nombre
        """
        return Database.execute_query(query, (rol_id,), fetch_all=True)
    
    @staticmethod
    def agregar_a_cache(usuario_id, usuario_data):
        """Agrega un usuario al cache de usuarios activos"""
        UsuarioModel._usuarios_activos[usuario_id] = usuario_data
    
    @staticmethod
    def limpiar_cache():
        """Limpia el cache de usuarios activos"""
        UsuarioModel._usuarios_activos.clear()
    
    @staticmethod
    def obtener_cache():
        """Retorna el diccionario de usuarios activos en cache"""
        return UsuarioModel._usuarios_activos
