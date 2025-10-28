"""
Controlador de Compras
"""

from flask import request
from services.compra_service import CompraService
from utils.error_handler import success_response, error_response
from utils.decorators import validar_json, validar_campos_requeridos


class CompraController:
    """Controlador para endpoints de compras"""
    
    @staticmethod
    @validar_json
    @validar_campos_requeridos('proveedor_id', 'usuario_id', 'items')
    def crear():
        """POST /api/compras"""
        try:
            data = request.get_json()
            
            resultado = CompraService.crear_compra(
                numero_factura=data.get('numero_factura'),
                proveedor_id=data['proveedor_id'],
                usuario_id=data['usuario_id'],
                items=data['items'],
                impuestos=data.get('impuestos', 0),
                observaciones=data.get('observaciones')
            )
            
            return success_response(
                data=resultado,
                message="Compra registrada exitosamente",
                status_code=201
            )
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def listar():
        """GET /api/compras"""
        try:
            limite = int(request.args.get('limite', 100))
            offset = int(request.args.get('offset', 0))
            
            compras = CompraService.listar_compras(limite, offset)
            return success_response(data=compras)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def obtener(compra_id):
        """GET /api/compras/<id>"""
        try:
            compra = CompraService.obtener_compra(compra_id)
            if not compra:
                return error_response("Compra no encontrada", 404)
            return success_response(data=compra)
        except Exception as e:
            return error_response(str(e), 500)
