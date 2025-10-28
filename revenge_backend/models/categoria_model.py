"""
Modelo Categoría
Estructura: Árbol (para soportar categorías jerárquicas en el futuro)
"""

from config.database import Database


class CategoriaModel:
    """Modelo para manejar categorías con estructura de árbol"""
    
    # Cache en memoria como árbol
    _arbol_categorias = {}
    _categorias_dict = {}  # Hash map para búsqueda rápida
    
    @staticmethod
    def crear(nombre, descripcion=None, created_by=None, parent_id=None):
        """Crea una nueva categoría"""
        query = """
            INSERT INTO categorias (nombre, descripcion, created_by, estado_id)
            VALUES (%s, %s, %s, 1)
        """
        params = (nombre, descripcion, created_by)
        
        try:
            categoria_id = Database.execute_query(query, params, commit=True)
            CategoriaModel._cargar_arbol()  # Recargar árbol
            return categoria_id
        except Exception as e:
            print(f"Error creando categoría: {e}")
            raise
    
    @staticmethod
    def obtener_por_id(categoria_id):
        """Obtiene una categoría por ID - Búsqueda O(1) usando hash map"""
        # Primero busca en cache
        if categoria_id in CategoriaModel._categorias_dict:
            return CategoriaModel._categorias_dict[categoria_id]
        
        query = """
            SELECT c.*, e.nombre as estado_nombre,
                   u.nombre as creado_por_nombre
            FROM categorias c
            INNER JOIN estados e ON c.estado_id = e.id
            LEFT JOIN usuarios u ON c.created_by = u.id
            WHERE c.id = %s AND c.deleted_at IS NULL
        """
        categoria = Database.execute_query(query, (categoria_id,), fetch_one=True)
        
        # Guardar en cache
        if categoria:
            CategoriaModel._categorias_dict[categoria_id] = categoria
        
        return categoria
    
    @staticmethod
    def obtener_por_nombre(nombre):
        """Busca categoría por nombre"""
        query = """
            SELECT * FROM categorias
            WHERE nombre = %s AND deleted_at IS NULL
        """
        return Database.execute_query(query, (nombre,), fetch_one=True)
    
    @staticmethod
    def obtener_todas(incluir_inactivas=False):
        """Obtiene todas las categorías"""
        query = """
            SELECT c.id, c.nombre, c.descripcion, c.estado_id,
                   e.nombre as estado_nombre,
                   u.nombre as creado_por,
                   c.created_at, c.updated_at
            FROM categorias c
            INNER JOIN estados e ON c.estado_id = e.id
            LEFT JOIN usuarios u ON c.created_by = u.id
            WHERE c.deleted_at IS NULL
        """
        
        if not incluir_inactivas:
            query += " AND c.estado_id = 1"
        
        query += " ORDER BY c.nombre ASC"
        
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def actualizar(categoria_id, **kwargs):
        """Actualiza una categoría"""
        campos_permitidos = ['nombre', 'descripcion', 'estado_id']
        campos = []
        valores = []
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                campos.append(f"{campo} = %s")
                valores.append(valor)
        
        if not campos:
            return False
        
        valores.append(categoria_id)
        query = f"UPDATE categorias SET {', '.join(campos)}, updated_at = NOW() WHERE id = %s"
        
        try:
            filas_afectadas = Database.execute_query(query, tuple(valores), commit=True)
            
            # Limpiar cache
            if categoria_id in CategoriaModel._categorias_dict:
                del CategoriaModel._categorias_dict[categoria_id]
            CategoriaModel._cargar_arbol()
            
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error actualizando categoría: {e}")
            raise
    
    @staticmethod
    def eliminar_logico(categoria_id):
        """Elimina lógicamente una categoría"""
        # Verificar que no tenga productos asociados
        query_check = "SELECT COUNT(*) as total FROM productos WHERE categoria_id = %s AND deleted_at IS NULL"
        resultado = Database.execute_query(query_check, (categoria_id,), fetch_one=True)
        
        if resultado['total'] > 0:
            raise Exception("No se puede eliminar: tiene productos asociados")
        
        query = "UPDATE categorias SET deleted_at = NOW(), estado_id = 2 WHERE id = %s"
        
        try:
            filas_afectadas = Database.execute_query(query, (categoria_id,), commit=True)
            
            # Limpiar cache
            if categoria_id in CategoriaModel._categorias_dict:
                del CategoriaModel._categorias_dict[categoria_id]
            
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error eliminando categoría: {e}")
            raise
    
    @staticmethod
    def verificar_nombre_existe(nombre, excluir_id=None):
        """Verifica si un nombre de categoría ya existe"""
        query = "SELECT id FROM categorias WHERE nombre = %s AND deleted_at IS NULL"
        params = [nombre]
        
        if excluir_id:
            query += " AND id != %s"
            params.append(excluir_id)
        
        resultado = Database.execute_query(query, tuple(params), fetch_one=True)
        return resultado is not None
    
    @staticmethod
    def obtener_con_productos():
        """Obtiene categorías con conteo de productos"""
        query = """
            SELECT c.id, c.nombre, c.descripcion, c.estado_id,
                   COUNT(p.id) as total_productos
            FROM categorias c
            LEFT JOIN productos p ON c.id = p.categoria_id AND p.deleted_at IS NULL
            WHERE c.deleted_at IS NULL AND c.estado_id = 1
            GROUP BY c.id, c.nombre, c.descripcion, c.estado_id
            ORDER BY c.nombre
        """
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def _cargar_arbol():
        """Carga las categorías en estructura de árbol (preparado para jerarquías)"""
        categorias = CategoriaModel.obtener_todas()
        
        CategoriaModel._arbol_categorias = {}
        CategoriaModel._categorias_dict = {}
        
        for cat in categorias:
            CategoriaModel._categorias_dict[cat['id']] = cat
            # Por ahora solo un nivel, preparado para expandir
            CategoriaModel._arbol_categorias[cat['id']] = {
                'data': cat,
                'hijos': []
            }
    
    @staticmethod
    def obtener_arbol():
        """Retorna el árbol de categorías"""
        if not CategoriaModel._arbol_categorias:
            CategoriaModel._cargar_arbol()
        return CategoriaModel._arbol_categorias
