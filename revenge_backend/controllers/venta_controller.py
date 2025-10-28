"""
Controlador de Ventas
"""

from flask import request
from services.venta_service import VentaService
from utils.error_handler import success_response, error_response
from utils.decorators import validar_json, validar_campos_requeridos


class VentaController:
    """Controlador para endpoints de ventas"""
    
    @staticmethod
    @validar_json
    @validar_campos_requeridos('cajero_id', 'items', 'metodo_pago_id')
    def crear():
        """POST /api/ventas"""
        try:
            data = request.get_json()
            
            resultado = VentaService.crear_venta(
                cajero_id=data['cajero_id'],
                items=data['items'],
                metodo_pago_id=data['metodo_pago_id'],
                descuento_general=data.get('descuento', 0),
                impuestos=data.get('impuestos'),  # None para cálculo automático
                observaciones=data.get('observaciones')
            )
            
            return success_response(
                data=resultado,
                message="Venta registrada exitosamente",
                status_code=201
            )
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def listar():
        """GET /api/ventas"""
        try:
            limite = int(request.args.get('limite', 100))
            offset = int(request.args.get('offset', 0))
            
            ventas = VentaService.listar_ventas(limite, offset)
            return success_response(data=ventas)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def obtener(venta_id):
        """GET /api/ventas/<id>"""
        try:
            venta = VentaService.obtener_venta(venta_id)
            if not venta:
                return error_response("Venta no encontrada", 404)
            return success_response(data=venta)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def por_fecha():
        """GET /api/ventas/por-fecha"""
        try:
            fecha_inicio = request.args.get('fecha_inicio')
            fecha_fin = request.args.get('fecha_fin')
            
            if not fecha_inicio or not fecha_fin:
                return error_response("Proporcione fecha_inicio y fecha_fin", 400)
            
            ventas = VentaService.obtener_ventas_por_fecha(fecha_inicio, fecha_fin)
            return success_response(data=ventas)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def resumen_dia():
        """GET /api/ventas/resumen-dia"""
        try:
            fecha = request.args.get('fecha')
            resumen = VentaService.obtener_resumen_dia(fecha)
            return success_response(data=resumen)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def productos_mas_vendidos():
        """GET /api/ventas/productos-mas-vendidos"""
        try:
            limite = int(request.args.get('limite', 10))
            fecha_inicio = request.args.get('fecha_inicio')
            fecha_fin = request.args.get('fecha_fin')
            
            productos = VentaService.obtener_productos_mas_vendidos(
                limite, fecha_inicio, fecha_fin
            )
            return success_response(data=productos)
        except Exception as e:
            return error_response(str(e), 500)
