"""
Controlador de Productos
"""

from flask import request
from services.producto_service import ProductoService
from utils.error_handler import success_response, error_response
from utils.decorators import validar_json, validar_campos_requeridos


class ProductoController:
    """Controlador para endpoints de productos"""
    
    @staticmethod
    def listar():
        """GET /api/productos"""
        try:
            filtro = request.args.get('filtro')
            productos = ProductoService.listar_productos(filtro)
            return success_response(data=productos)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def obtener(producto_id):
        """GET /api/productos/<id>"""
        try:
            producto = ProductoService.buscar_producto('id', producto_id)
            if not producto:
                return error_response("Producto no encontrado", 404)
            return success_response(data=producto)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def buscar():
        """GET /api/productos/buscar"""
        try:
            codigo = request.args.get('codigo')
            nombre = request.args.get('nombre')
            
            if codigo:
                producto = ProductoService.buscar_producto('codigo', codigo)
                return success_response(data=producto)
            elif nombre:
                productos = ProductoService.buscar_producto('nombre', nombre)
                return success_response(data=productos)
            else:
                return error_response("Proporcione código o nombre para buscar", 400)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    @validar_json
    @validar_campos_requeridos('codigo_barras', 'nombre', 'categoria_id', 
                               'precio_compra', 'precio_venta')
    def crear():
        """POST /api/productos"""
        try:
            data = request.get_json()
            
            producto_id = ProductoService.crear_producto(
                codigo_barras=data['codigo_barras'],
                nombre=data['nombre'],
                descripcion=data.get('descripcion'),
                categoria_id=data['categoria_id'],
                precio_compra=data['precio_compra'],
                precio_venta=data['precio_venta'],
                stock=data.get('stock', 0),
                stock_minimo=data.get('stock_minimo', 5),
                imagen_url=data.get('imagen_url'),
                created_by=data.get('created_by')
            )
            
            return success_response(
                data={'producto_id': producto_id},
                message="Producto creado exitosamente",
                status_code=201
            )
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    @validar_json
    def actualizar(producto_id):
        """PUT /api/productos/<id>"""
        try:
            data = request.get_json()
            ProductoService.actualizar_producto(producto_id, **data)
            return success_response(message="Producto actualizado exitosamente")
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def eliminar(producto_id):
        """DELETE /api/productos/<id>"""
        try:
            ProductoService.eliminar_producto(producto_id)
            return success_response(message="Producto eliminado exitosamente")
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def stock_bajo():
        """GET /api/productos/stock-bajo"""
        try:
            productos = ProductoService.obtener_productos_bajo_stock()
            return success_response(data=productos)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    @validar_json
    @validar_campos_requeridos('cantidad', 'tipo_ajuste', 'motivo', 'usuario_id')
    def ajustar_stock(producto_id):
        """POST /api/productos/<id>/ajustar-stock"""
        try:
            data = request.get_json()
            
            ProductoService.ajustar_stock(
                producto_id=producto_id,
                cantidad=data['cantidad'],
                tipo_ajuste=data['tipo_ajuste'],
                motivo=data['motivo'],
                usuario_id=data['usuario_id']
            )
            
            return success_response(message="Stock ajustado exitosamente")
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
