"""
Modelo Proveedor
"""

from config.database import Database


class ProveedorModel:
    """Modelo para manejar proveedores"""
    
    @staticmethod
    def crear(nombre, ruc=None, telefono=None, direccion=None, 
              email=None, contacto=None, created_by=None):
        """Crea un nuevo proveedor"""
        query = """
            INSERT INTO proveedores (ruc, nombre, telefono, direccion, 
                                    email, contacto, created_by, estado_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
        """
        params = (ruc, nombre, telefono, direccion, email, contacto, created_by)
        
        try:
            proveedor_id = Database.execute_query(query, params, commit=True)
            return proveedor_id
        except Exception as e:
            print(f"Error creando proveedor: {e}")
            raise
    
    @staticmethod
    def obtener_por_id(proveedor_id):
        """Obtiene un proveedor por ID"""
        query = """
            SELECT p.*, e.nombre as estado_nombre
            FROM proveedores p
            INNER JOIN estados e ON p.estado_id = e.id
            WHERE p.id = %s AND p.deleted_at IS NULL
        """
        return Database.execute_query(query, (proveedor_id,), fetch_one=True)
    
    @staticmethod
    def obtener_por_ruc(ruc):
        """Obtiene un proveedor por RUC"""
        query = """
            SELECT * FROM proveedores
            WHERE ruc = %s AND deleted_at IS NULL
        """
        return Database.execute_query(query, (ruc,), fetch_one=True)
    
    @staticmethod
    def obtener_todos(incluir_inactivos=False):
        """Obtiene todos los proveedores"""
        query = """
            SELECT p.*, e.nombre as estado_nombre
            FROM proveedores p
            INNER JOIN estados e ON p.estado_id = e.id
            WHERE p.deleted_at IS NULL
        """
        
        if not incluir_inactivos:
            query += " AND p.estado_id = 1"
        
        query += " ORDER BY p.nombre ASC"
        
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def buscar_por_nombre(nombre):
        """Busca proveedores por nombre"""
        query = """
            SELECT p.*, e.nombre as estado_nombre
            FROM proveedores p
            INNER JOIN estados e ON p.estado_id = e.id
            WHERE p.nombre LIKE %s AND p.deleted_at IS NULL
            ORDER BY p.nombre
        """
        return Database.execute_query(query, (f"%{nombre}%",), fetch_all=True)
    
    @staticmethod
    def actualizar(proveedor_id, **kwargs):
        """Actualiza un proveedor"""
        campos_permitidos = ['ruc', 'nombre', 'telefono', 'direccion', 
                            'email', 'contacto', 'estado_id']
        campos = []
        valores = []
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                campos.append(f"{campo} = %s")
                valores.append(valor)
        
        if not campos:
            return False
        
        valores.append(proveedor_id)
        query = f"UPDATE proveedores SET {', '.join(campos)}, updated_at = NOW() WHERE id = %s"
        
        try:
            filas_afectadas = Database.execute_query(query, tuple(valores), commit=True)
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error actualizando proveedor: {e}")
            raise
    
    @staticmethod
    def eliminar_logico(proveedor_id):
        """Elimina lógicamente un proveedor"""
        # Verificar que no tenga compras asociadas
        query_check = "SELECT COUNT(*) as total FROM compras WHERE proveedor_id = %s"
        resultado = Database.execute_query(query_check, (proveedor_id,), fetch_one=True)
        
        if resultado['total'] > 0:
            raise Exception("No se puede eliminar: tiene compras asociadas")
        
        query = "UPDATE proveedores SET deleted_at = NOW(), estado_id = 2 WHERE id = %s"
        
        try:
            filas_afectadas = Database.execute_query(query, (proveedor_id,), commit=True)
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error eliminando proveedor: {e}")
            raise
    
    @staticmethod
    def verificar_ruc_existe(ruc, excluir_id=None):
        """Verifica si un RUC ya existe"""
        if not ruc:
            return False
        
        query = "SELECT id FROM proveedores WHERE ruc = %s AND deleted_at IS NULL"
        params = [ruc]
        
        if excluir_id:
            query += " AND id != %s"
            params.append(excluir_id)
        
        resultado = Database.execute_query(query, tuple(params), fetch_one=True)
        return resultado is not None
