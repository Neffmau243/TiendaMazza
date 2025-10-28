"""
Servicio de Productos
Aplica principios SOLID con búsqueda optimizada usando hash maps
"""

from models.producto_model import ProductoModel
from models.categoria_model import CategoriaModel


class ProductoService:
    """
    Servicio para lógica de negocio de productos
    Single Responsibility: Solo maneja operaciones de productos
    """
    
    @staticmethod
    def crear_producto(codigo_barras, nombre, descripcion, categoria_id,
                      precio_compra, precio_venta, stock=0, stock_minimo=5,
                      imagen_url=None, created_by=None):
        """Crea un nuevo producto con validaciones de negocio"""
        
        # Validaciones de negocio
        if precio_compra < 0:
            raise ValueError("El precio de compra no puede ser negativo")
        
        if precio_venta < precio_compra:
            raise ValueError("El precio de venta no puede ser menor al precio de compra")
        
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        # Verificar que la categoría existe
        categoria = CategoriaModel.obtener_por_id(categoria_id)
        if not categoria:
            raise ValueError("La categoría no existe")
        
        # Verificar que el código de barras no existe
        if ProductoModel.verificar_codigo_existe(codigo_barras):
            raise ValueError("El código de barras ya está registrado")
        
        # Crear producto
        producto_id = ProductoModel.crear(
            codigo_barras=codigo_barras,
            nombre=nombre,
            descripcion=descripcion,
            categoria_id=categoria_id,
            precio_compra=float(precio_compra),
            precio_venta=float(precio_venta),
            stock=int(stock),
            stock_minimo=int(stock_minimo),
            imagen_url=imagen_url,
            created_by=created_by
        )
        
        return producto_id
    
    @staticmethod
    def buscar_producto(criterio, valor):
        """
        Búsqueda optimizada de productos usando hash maps
        
        Args:
            criterio: 'id', 'codigo', 'nombre'
            valor: valor a buscar
        """
        if criterio == 'id':
            return ProductoModel.obtener_por_id(valor)
        elif criterio == 'codigo':
            return ProductoModel.obtener_por_codigo(valor)
        elif criterio == 'nombre':
            return ProductoModel.buscar_por_nombre(valor)
        else:
            raise ValueError("Criterio de búsqueda inválido")
    
    @staticmethod
    def listar_productos(filtro=None):
        """Lista productos con filtros opcionales"""
        if filtro == 'stock_bajo':
            return ProductoModel.obtener_stock_bajo()
        elif filtro == 'categoria' and 'categoria_id' in filtro:
            return ProductoModel.obtener_por_categoria(filtro['categoria_id'])
        else:
            return ProductoModel.obtener_todos()
    
    @staticmethod
    def actualizar_producto(producto_id, **datos):
        """Actualiza un producto con validaciones"""
        
        # Verificar que el producto existe
        producto = ProductoModel.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        # Validar precios si se actualizan
        if 'precio_compra' in datos and datos['precio_compra'] < 0:
            raise ValueError("El precio de compra no puede ser negativo")
        
        if 'precio_venta' in datos:
            precio_compra = datos.get('precio_compra', producto['precio_compra'])
            if datos['precio_venta'] < precio_compra:
                raise ValueError("El precio de venta no puede ser menor al precio de compra")
        
        # Validar categoría si se actualiza
        if 'categoria_id' in datos:
            categoria = CategoriaModel.obtener_por_id(datos['categoria_id'])
            if not categoria:
                raise ValueError("La categoría no existe")
        
        # Actualizar
        return ProductoModel.actualizar(producto_id, **datos)
    
    @staticmethod
    def eliminar_producto(producto_id):
        """Elimina lógicamente un producto"""
        producto = ProductoModel.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        return ProductoModel.eliminar_logico(producto_id)
    
    @staticmethod
    def ajustar_stock(producto_id, cantidad, tipo_ajuste, motivo, usuario_id):
        """
        Ajusta el stock de un producto
        
        Args:
            tipo_ajuste: 'entrada', 'salida', 'ajuste'
        """
        producto = ProductoModel.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        stock_actual = producto['stock']
        
        if tipo_ajuste == 'entrada':
            nuevo_stock = stock_actual + abs(cantidad)
        elif tipo_ajuste == 'salida':
            nuevo_stock = stock_actual - abs(cantidad)
            if nuevo_stock < 0:
                raise ValueError("Stock insuficiente")
        elif tipo_ajuste == 'ajuste':
            nuevo_stock = cantidad
        else:
            raise ValueError("Tipo de ajuste inválido")
        
        # Actualizar stock
        return ProductoModel.actualizar_stock(
            producto_id=producto_id,
            nueva_cantidad=nuevo_stock,
            tipo_movimiento=tipo_ajuste,
            motivo=motivo,
            usuario_id=usuario_id
        )
    
    @staticmethod
    def obtener_productos_bajo_stock():
        """Obtiene productos con stock bajo el mínimo"""
        return ProductoModel.obtener_stock_bajo()
    
    @staticmethod
    def obtener_historial_movimientos(producto_id, limite=50):
        """Obtiene el historial de movimientos de un producto"""
        return ProductoModel.obtener_movimientos(producto_id, limite)
    
    @staticmethod
    def verificar_disponibilidad(producto_id, cantidad_requerida):
        """Verifica si hay stock disponible"""
        producto = ProductoModel.obtener_por_id(producto_id)
        if not producto:
            return False
        
        return producto['stock'] >= cantidad_requerida
    
    @staticmethod
    def calcular_valor_inventario():
        """Calcula el valor total del inventario"""
        productos = ProductoModel.obtener_todos()
        
        valor_total = 0
        for producto in productos:
            valor_total += producto['stock'] * producto['precio_compra']
        
        return {
            'valor_total_compra': valor_total,
            'total_productos': len(productos),
            'productos_evaluados': productos
        }
