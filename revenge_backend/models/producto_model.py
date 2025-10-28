"""
Modelo Producto
Estructura: Diccionario (hash map) para búsqueda instantánea por código o nombre
"""

from config.database import Database


class ProductoModel:
    """Modelo para manejar productos con búsqueda optimizada"""
    
    # Cache en memoria como hash map
    _productos_por_codigo = {}  # Búsqueda por código de barras O(1)
    _productos_por_id = {}      # Búsqueda por ID O(1)
    
    @staticmethod
    def crear(codigo_barras, nombre, descripcion, categoria_id, precio_compra, 
              precio_venta, stock=0, stock_minimo=5, imagen_url=None, created_by=None):
        """Crea un nuevo producto"""
        query = """
            INSERT INTO productos (codigo_barras, nombre, descripcion, categoria_id,
                                 precio_compra, precio_venta, stock, stock_minimo,
                                 imagen_url, created_by, estado_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
        """
        params = (codigo_barras, nombre, descripcion, categoria_id, precio_compra,
                 precio_venta, stock, stock_minimo, imagen_url, created_by)
        
        try:
            producto_id = Database.execute_query(query, params, commit=True)
            
            # Registrar movimiento de inventario inicial
            if stock > 0:
                ProductoModel._registrar_movimiento(
                    producto_id, 'inicial', stock, 0, stock,
                    None, 'sistema', 'Stock inicial', created_by
                )
            
            return producto_id
        except Exception as e:
            print(f"Error creando producto: {e}")
            raise
    
    @staticmethod
    def obtener_por_id(producto_id):
        """Obtiene un producto por ID - O(1)"""
        # Buscar en cache
        if producto_id in ProductoModel._productos_por_id:
            return ProductoModel._productos_por_id[producto_id]
        
        query = """
            SELECT p.*, c.nombre as categoria_nombre, e.nombre as estado_nombre
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            INNER JOIN estados e ON p.estado_id = e.id
            WHERE p.id = %s AND p.deleted_at IS NULL
        """
        producto = Database.execute_query(query, (producto_id,), fetch_one=True)
        
        # Guardar en cache
        if producto:
            ProductoModel._productos_por_id[producto_id] = producto
            ProductoModel._productos_por_codigo[producto['codigo_barras']] = producto
        
        return producto
    
    @staticmethod
    def obtener_por_codigo(codigo_barras):
        """Obtiene un producto por código de barras - O(1)"""
        # Buscar en cache
        if codigo_barras in ProductoModel._productos_por_codigo:
            return ProductoModel._productos_por_codigo[codigo_barras]
        
        query = """
            SELECT p.*, c.nombre as categoria_nombre, e.nombre as estado_nombre
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            INNER JOIN estados e ON p.estado_id = e.id
            WHERE p.codigo_barras = %s AND p.deleted_at IS NULL
        """
        producto = Database.execute_query(query, (codigo_barras,), fetch_one=True)
        
        # Guardar en cache
        if producto:
            ProductoModel._productos_por_codigo[codigo_barras] = producto
            ProductoModel._productos_por_id[producto['id']] = producto
        
        return producto
    
    @staticmethod
    def buscar_por_nombre(nombre):
        """Busca productos por nombre (búsqueda parcial)"""
        query = """
            SELECT p.*, c.nombre as categoria_nombre, e.nombre as estado_nombre
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            INNER JOIN estados e ON p.estado_id = e.id
            WHERE p.nombre LIKE %s AND p.deleted_at IS NULL
            ORDER BY p.nombre
            LIMIT 50
        """
        return Database.execute_query(query, (f"%{nombre}%",), fetch_all=True)
    
    @staticmethod
    def obtener_todos(incluir_inactivos=False):
        """Obtiene todos los productos"""
        query = """
            SELECT p.id, p.codigo_barras, p.nombre, p.descripcion,
                   p.categoria_id, c.nombre as categoria_nombre,
                   p.precio_compra, p.precio_venta, p.stock, p.stock_minimo,
                   p.imagen_url, p.estado_id, e.nombre as estado_nombre,
                   p.created_at, p.updated_at
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            INNER JOIN estados e ON p.estado_id = e.id
            WHERE p.deleted_at IS NULL
        """
        
        if not incluir_inactivos:
            query += " AND p.estado_id = 1"
        
        query += " ORDER BY p.nombre ASC"
        
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def obtener_por_categoria(categoria_id):
        """Obtiene productos de una categoría"""
        query = """
            SELECT p.*, c.nombre as categoria_nombre
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            WHERE p.categoria_id = %s AND p.deleted_at IS NULL AND p.estado_id = 1
            ORDER BY p.nombre
        """
        return Database.execute_query(query, (categoria_id,), fetch_all=True)
    
    @staticmethod
    def obtener_stock_bajo():
        """Obtiene productos con stock bajo"""
        query = """
            SELECT p.*, c.nombre as categoria_nombre
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            WHERE p.stock <= p.stock_minimo 
                AND p.deleted_at IS NULL 
                AND p.estado_id = 1
            ORDER BY p.stock ASC
        """
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def actualizar(producto_id, **kwargs):
        """Actualiza un producto"""
        campos_permitidos = ['nombre', 'descripcion', 'categoria_id', 'precio_compra',
                            'precio_venta', 'stock', 'stock_minimo', 'imagen_url', 'estado_id']
        campos = []
        valores = []
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                campos.append(f"{campo} = %s")
                valores.append(valor)
        
        if not campos:
            return False
        
        valores.append(producto_id)
        query = f"UPDATE productos SET {', '.join(campos)}, updated_at = NOW() WHERE id = %s"
        
        try:
            filas_afectadas = Database.execute_query(query, tuple(valores), commit=True)
            
            # Limpiar cache
            ProductoModel._limpiar_cache_producto(producto_id)
            
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error actualizando producto: {e}")
            raise
    
    @staticmethod
    def actualizar_stock(producto_id, nueva_cantidad, tipo_movimiento, 
                        referencia_id=None, referencia_tipo=None, 
                        motivo=None, usuario_id=None):
        """
        Actualiza el stock de un producto y registra el movimiento
        
        Args:
            tipo_movimiento: 'entrada', 'salida', 'ajuste'
        """
        # Obtener stock actual
        producto = ProductoModel.obtener_por_id(producto_id)
        if not producto:
            raise Exception("Producto no encontrado")
        
        stock_anterior = producto['stock']
        stock_nuevo = nueva_cantidad
        cantidad_movimiento = stock_nuevo - stock_anterior
        
        # Actualizar stock
        query = "UPDATE productos SET stock = %s, updated_at = NOW() WHERE id = %s"
        
        try:
            with Database.get_cursor(commit=True) as cursor:
                cursor.execute(query, (stock_nuevo, producto_id))
                
                # Registrar movimiento
                ProductoModel._registrar_movimiento(
                    producto_id, tipo_movimiento, cantidad_movimiento,
                    stock_anterior, stock_nuevo, referencia_id,
                    referencia_tipo, motivo, usuario_id, cursor
                )
            
            # Limpiar cache
            ProductoModel._limpiar_cache_producto(producto_id)
            
            return True
        except Exception as e:
            print(f"Error actualizando stock: {e}")
            raise
    
    @staticmethod
    def eliminar_logico(producto_id):
        """Elimina lógicamente un producto"""
        query = "UPDATE productos SET deleted_at = NOW(), estado_id = 2 WHERE id = %s"
        
        try:
            filas_afectadas = Database.execute_query(query, (producto_id,), commit=True)
            ProductoModel._limpiar_cache_producto(producto_id)
            return filas_afectadas > 0
        except Exception as e:
            print(f"Error eliminando producto: {e}")
            raise
    
    @staticmethod
    def verificar_codigo_existe(codigo_barras, excluir_id=None):
        """Verifica si un código de barras ya existe"""
        query = "SELECT id FROM productos WHERE codigo_barras = %s AND deleted_at IS NULL"
        params = [codigo_barras]
        
        if excluir_id:
            query += " AND id != %s"
            params.append(excluir_id)
        
        resultado = Database.execute_query(query, tuple(params), fetch_one=True)
        return resultado is not None
    
    @staticmethod
    def _registrar_movimiento(producto_id, tipo, cantidad, stock_anterior, stock_nuevo,
                             referencia_id, referencia_tipo, motivo, usuario_id, cursor=None):
        """Registra un movimiento de inventario"""
        query = """
            INSERT INTO movimientos_inventario 
            (producto_id, tipo, cantidad, stock_anterior, stock_nuevo,
             referencia_id, referencia_tipo, motivo, usuario_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (producto_id, tipo, cantidad, stock_anterior, stock_nuevo,
                 referencia_id, referencia_tipo, motivo, usuario_id)
        
        if cursor:
            cursor.execute(query, params)
        else:
            Database.execute_query(query, params, commit=True)
    
    @staticmethod
    def obtener_movimientos(producto_id, limite=50):
        """Obtiene el historial de movimientos de un producto"""
        query = """
            SELECT m.*, u.nombre as usuario_nombre
            FROM movimientos_inventario m
            LEFT JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.producto_id = %s
            ORDER BY m.created_at DESC
            LIMIT %s
        """
        return Database.execute_query(query, (producto_id, limite), fetch_all=True)
    
    @staticmethod
    def _limpiar_cache_producto(producto_id):
        """Limpia el cache de un producto específico"""
        if producto_id in ProductoModel._productos_por_id:
            producto = ProductoModel._productos_por_id[producto_id]
            codigo = producto.get('codigo_barras')
            
            del ProductoModel._productos_por_id[producto_id]
            
            if codigo and codigo in ProductoModel._productos_por_codigo:
                del ProductoModel._productos_por_codigo[codigo]
    
    @staticmethod
    def cargar_cache():
        """Carga todos los productos activos en cache"""
        productos = ProductoModel.obtener_todos()
        
        ProductoModel._productos_por_id.clear()
        ProductoModel._productos_por_codigo.clear()
        
        for producto in productos:
            ProductoModel._productos_por_id[producto['id']] = producto
            ProductoModel._productos_por_codigo[producto['codigo_barras']] = producto
    
    @staticmethod
    def obtener_cache():
        """Retorna el cache de productos"""
        return {
            'por_id': ProductoModel._productos_por_id,
            'por_codigo': ProductoModel._productos_por_codigo
        }
