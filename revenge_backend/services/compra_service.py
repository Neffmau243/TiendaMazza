"""
Servicio de Compras
Aplica SOLID con cola para pedidos pendientes
"""

from models.compra_model import CompraModel
from models.detalle_compra_model import DetalleCompraModel
from models.producto_model import ProductoModel
from models.proveedor_model import ProveedorModel
from config.database import Database


class CompraService:
    """
    Servicio para lógica de negocio de compras
    Usa cola (FIFO) para pedidos pendientes
    """
    
    @staticmethod
    def crear_compra(numero_factura, proveedor_id, usuario_id, items,
                    impuestos=0, observaciones=None):
        """
        Crea una compra completa con sus detalles
        
        Args:
            items: Lista de diccionarios con los productos
        """
        
        # Validar proveedor
        proveedor = ProveedorModel.obtener_por_id(proveedor_id)
        if not proveedor:
            raise ValueError("Proveedor no encontrado")
        
        # Validar items
        if not items or len(items) == 0:
            raise ValueError("La compra debe tener al menos un producto")
        
        # Calcular totales
        subtotal = 0
        items_validados = []
        
        for item in items:
            producto_id = item['producto_id']
            cantidad = item['cantidad']
            precio_unitario = item['precio_unitario']
            
            # Obtener producto
            producto = ProductoModel.obtener_por_id(producto_id)
            if not producto:
                raise ValueError(f"Producto ID {producto_id} no encontrado")
            
            # Calcular subtotal del item
            item_subtotal = cantidad * precio_unitario
            subtotal += item_subtotal
            
            items_validados.append({
                'producto_id': producto_id,
                'cantidad': cantidad,
                'precio_unitario': precio_unitario,
                'producto': producto
            })
        
        # Calcular total
        total = subtotal + impuestos
        
        if total <= 0:
            raise ValueError("El total de la compra debe ser mayor a 0")
        
        # Crear compra en una transacción
        try:
            with Database.get_cursor(commit=True) as cursor:
                # 1. Crear cabecera de compra
                query_compra = """
                    INSERT INTO compras (numero_factura, proveedor_id, usuario_id,
                                       subtotal, impuestos, total, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_compra, (
                    numero_factura, proveedor_id, usuario_id,
                    subtotal, impuestos, total, observaciones
                ))
                compra_id = cursor.lastrowid
                
                # 2. Crear detalles y actualizar stock
                query_detalle = """
                    INSERT INTO detalle_compra (compra_id, producto_id, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                """
                
                query_update_stock = """
                    UPDATE productos SET stock = stock + %s, updated_at = NOW()
                    WHERE id = %s
                """
                
                # También actualizar precio de compra si es mayor
                query_update_precio = """
                    UPDATE productos SET precio_compra = %s, updated_at = NOW()
                    WHERE id = %s AND precio_compra < %s
                """
                
                query_movimiento = """
                    INSERT INTO movimientos_inventario 
                    (producto_id, tipo, cantidad, stock_anterior, stock_nuevo,
                     referencia_id, referencia_tipo, motivo, usuario_id)
                    VALUES (%s, 'entrada', %s, %s, %s, %s, 'compra', 'Compra a proveedor', %s)
                """
                
                for item in items_validados:
                    # Crear detalle
                    cursor.execute(query_detalle, (
                        compra_id,
                        item['producto_id'],
                        item['cantidad'],
                        item['precio_unitario']
                    ))
                    
                    # Actualizar stock
                    cursor.execute(query_update_stock, (
                        item['cantidad'],
                        item['producto_id']
                    ))
                    
                    # Actualizar precio de compra si es mayor
                    cursor.execute(query_update_precio, (
                        item['precio_unitario'],
                        item['producto_id'],
                        item['precio_unitario']
                    ))
                    
                    # Registrar movimiento
                    stock_anterior = item['producto']['stock']
                    stock_nuevo = stock_anterior + item['cantidad']
                    
                    cursor.execute(query_movimiento, (
                        item['producto_id'],
                        item['cantidad'],
                        stock_anterior,
                        stock_nuevo,
                        compra_id,
                        usuario_id
                    ))
            
            # Limpiar cache de productos afectados
            for item in items_validados:
                if item['producto_id'] in ProductoModel._productos_por_id:
                    del ProductoModel._productos_por_id[item['producto_id']]
            
            return {
                'compra_id': compra_id,
                'numero_factura': numero_factura,
                'total': total,
                'items': len(items_validados)
            }
            
        except Exception as e:

            raise
    
    @staticmethod
    def obtener_compra(compra_id):
        """Obtiene una compra completa"""
        return CompraModel.obtener_por_id(compra_id)
    
    @staticmethod
    def listar_compras(limite=100, offset=0):
        """Lista compras con paginación"""
        return CompraModel.obtener_todas(limite, offset)
    
    @staticmethod
    def obtener_compras_proveedor(proveedor_id):
        """Obtiene compras de un proveedor"""
        return CompraModel.obtener_por_proveedor(proveedor_id)
    
    @staticmethod
    def obtener_compras_por_fecha(fecha_inicio, fecha_fin):
        """Obtiene compras por rango de fechas"""
        return CompraModel.obtener_por_fecha(fecha_inicio, fecha_fin)
    
    @staticmethod
    def obtener_resumen_mes(año=None, mes=None):
        """Obtiene resumen de compras del mes"""
        return CompraModel.obtener_resumen_mes(año, mes)
    
    @staticmethod
    def agregar_pedido_pendiente(compra_id):
        """Agrega una compra a la cola de pedidos pendientes"""
        CompraModel.agregar_a_cola_pendientes(compra_id)
    
    @staticmethod
    def procesar_siguiente_pedido():
        """Procesa el siguiente pedido de la cola (FIFO)"""
        return CompraModel.obtener_siguiente_pendiente()
    
    @staticmethod
    def obtener_cola_pendientes():
        """Obtiene la cola de pedidos pendientes"""
        return CompraModel.obtener_cola_pendientes()
