"""
Servicio de Ventas
Aplica SOLID con procesamiento de listas para items de venta
"""

from models.venta_model import VentaModel
from models.detalle_venta_model import DetalleVentaModel
from models.producto_model import ProductoModel
from models.usuario_model import UsuarioModel
from config.database import Database
from datetime import datetime


class VentaService:
    """
    Servicio para lógica de negocio de ventas
    Procesa ventas con estructura de lista (items)
    """
    
    @staticmethod
    def crear_venta(cajero_id, items, metodo_pago_id, descuento_general=0, 
                   impuestos=None, observaciones=None):
        """
        Crea una venta completa con sus detalles
        
        Args:
            items: Lista de diccionarios
            [
                {
                    'producto_id': 1,
                    'cantidad': 2,
                    'precio_unitario': 10.50,
                    'descuento_unitario': 0
                },
                ...
            ]
            impuestos: Si es None, se calcula automáticamente (18% IGV)
        """
        
        # Validar que el cajero existe y puede vender
        cajero = UsuarioModel.obtener_por_id(cajero_id)
        if not cajero:
            raise ValueError("Cajero no encontrado")
        
        # Verificar que el rol permite ventas (admin=1 o cajero=2)
        if cajero['rol_id'] not in [1, 2]:
            raise ValueError("El usuario no tiene permisos para realizar ventas")
        
        # Validar items
        if not items or len(items) == 0:
            raise ValueError("La venta debe tener al menos un producto")
        
        # Calcular totales y validar stock
        subtotal = 0
        items_validados = []
        
        for item in items:
            producto_id = int(item['producto_id'])
            cantidad = int(item['cantidad'])
            precio_unitario = float(item.get('precio_unitario')) if item.get('precio_unitario') is not None else None
            descuento_unitario = float(item.get('descuento_unitario', 0))
            
            # Obtener producto
            producto = ProductoModel.obtener_por_id(producto_id)
            if not producto:
                raise ValueError(f"Producto ID {producto_id} no encontrado")
            
            # Verificar stock
            stock_actual = int(producto['stock']) if isinstance(producto['stock'], str) else producto['stock']
            if stock_actual < cantidad:
                raise ValueError(f"Stock insuficiente para {producto['nombre']}. " +
                               f"Disponible: {stock_actual}, Requerido: {cantidad}")
            
            # Usar precio de venta del producto si no se especifica
            if precio_unitario is None:
                precio_unitario = producto['precio_venta']
            
            # Calcular subtotal del item
            item_subtotal = cantidad * (precio_unitario - descuento_unitario)
            subtotal += item_subtotal
            
            items_validados.append({
                'producto_id': producto_id,
                'cantidad': cantidad,
                'precio_unitario': precio_unitario,
                'descuento_unitario': descuento_unitario,
                'producto': producto
            })
        
        # Calcular IGV automáticamente si no se especifica
        # IGV en Perú = 18%
        if impuestos is None:
            base_imponible = subtotal - descuento_general
            impuestos = round(base_imponible * 0.18, 2)
        
        # Calcular total
        total = subtotal - descuento_general + impuestos
        
        if total <= 0:
            raise ValueError("El total de la venta debe ser mayor a 0")
        
        # Generar número de boleta
        numero_boleta = VentaModel.generar_numero_boleta()
        
        # Crear venta en una transacción
        try:
            with Database.get_cursor(commit=True) as cursor:
                # 1. Crear cabecera de venta
                query_venta = """
                    INSERT INTO ventas (numero_boleta, cajero_id, subtotal, descuento,
                                      impuestos, total, metodo_pago_id, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_venta, (
                    numero_boleta, cajero_id, subtotal, descuento_general,
                    impuestos, total, metodo_pago_id, observaciones
                ))
                venta_id = cursor.lastrowid
                
                # 2. Crear detalles y actualizar stock
                query_detalle = """
                    INSERT INTO detalle_venta (venta_id, producto_id, cantidad,
                                              precio_unitario, descuento_unitario)
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                query_update_stock = """
                    UPDATE productos SET stock = stock - %s, updated_at = NOW()
                    WHERE id = %s
                """
                
                query_movimiento = """
                    INSERT INTO movimientos_inventario 
                    (producto_id, tipo, cantidad, stock_anterior, stock_nuevo,
                     referencia_id, referencia_tipo, motivo, usuario_id)
                    VALUES (%s, 'salida', %s, %s, %s, %s, 'venta', 'Venta realizada', %s)
                """
                
                for item in items_validados:
                    # Crear detalle
                    cursor.execute(query_detalle, (
                        venta_id,
                        item['producto_id'],
                        item['cantidad'],
                        item['precio_unitario'],
                        item['descuento_unitario']
                    ))
                    
                    # Actualizar stock
                    cursor.execute(query_update_stock, (
                        item['cantidad'],
                        item['producto_id']
                    ))
                    
                    # Registrar movimiento
                    stock_anterior = item['producto']['stock']
                    stock_nuevo = stock_anterior - item['cantidad']
                    
                    cursor.execute(query_movimiento, (
                        item['producto_id'],
                        -item['cantidad'],
                        stock_anterior,
                        stock_nuevo,
                        venta_id,
                        cajero_id
                    ))
            
            # Limpiar cache de productos afectados
            for item in items_validados:
                if item['producto_id'] in ProductoModel._productos_por_id:
                    del ProductoModel._productos_por_id[item['producto_id']]
            
            return {
                'venta_id': venta_id,
                'numero_boleta': numero_boleta,
                'total': total,
                'items': len(items_validados)
            }
            
        except Exception as e:

            raise
    
    @staticmethod
    def obtener_venta(venta_id):
        """Obtiene una venta completa"""
        return VentaModel.obtener_por_id(venta_id)
    
    @staticmethod
    def listar_ventas(limite=100, offset=0):
        """Lista ventas con paginación"""
        return VentaModel.obtener_todas(limite, offset)
    
    @staticmethod
    def obtener_ventas_por_fecha(fecha_inicio, fecha_fin):
        """Obtiene ventas por rango de fechas"""
        return VentaModel.obtener_por_fecha(fecha_inicio, fecha_fin)
    
    @staticmethod
    def obtener_ventas_cajero(cajero_id, fecha_inicio=None, fecha_fin=None):
        """Obtiene ventas de un cajero"""
        return VentaModel.obtener_por_cajero(cajero_id, fecha_inicio, fecha_fin)
    
    @staticmethod
    def obtener_resumen_dia(fecha=None):
        """Obtiene resumen de ventas del día"""
        return VentaModel.obtener_resumen_dia(fecha)
    
    @staticmethod
    def obtener_productos_mas_vendidos(limite=10, fecha_inicio=None, fecha_fin=None):
        """Obtiene estadísticas de productos más vendidos"""
        return VentaModel.obtener_productos_mas_vendidos(limite, fecha_inicio, fecha_fin)
    
    @staticmethod
    def calcular_comision_cajero(cajero_id, fecha_inicio, fecha_fin, porcentaje=0.02):
        """Calcula la comisión de un cajero por ventas realizadas"""
        ventas = VentaModel.obtener_por_cajero(cajero_id, fecha_inicio, fecha_fin)
        
        total_ventas = sum(venta['total'] for venta in ventas)
        comision = total_ventas * porcentaje
        
        return {
            'cajero_id': cajero_id,
            'total_ventas': len(ventas),
            'monto_total': total_ventas,
            'porcentaje_comision': porcentaje * 100,
            'comision': comision
        }
