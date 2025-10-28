"""
Controlador de Reportes
Maneja las peticiones HTTP para reportes
"""

from flask import request, jsonify
from services.reporte_service import ReporteService
from utils.error_handler import BadRequestError


class ReporteController:
    """Controlador para endpoints de reportes"""
    
    @staticmethod
    def reporte_ventas():
        """GET - Obtiene reporte de ventas"""
        try:
            # Obtener parámetros de query (aceptar ambos formatos)
            fecha_inicio = request.args.get('fecha_inicio') or request.args.get('fecha_desde')
            fecha_fin = request.args.get('fecha_fin') or request.args.get('fecha_hasta')
            
            print(f"🔍 Generando reporte de ventas: {fecha_inicio} a {fecha_fin}")
            
            resultado = ReporteService.generar_reporte_ventas(fecha_inicio, fecha_fin)
            
            if resultado['success']:
                return jsonify(resultado), 200
            else:
                error_msg = resultado.get('error', 'Error al generar reporte')
                print(f"❌ Error en reporte: {error_msg}")
                raise BadRequestError(error_msg)
                
        except BadRequestError as e:
            raise e
        except Exception as e:
            print(f"❌ Excepción en reporte_ventas: {str(e)}")
            import traceback
            traceback.print_exc()
            raise BadRequestError(f"Error al generar reporte de ventas: {str(e)}")
    
    @staticmethod
    def reporte_inventario():
        """GET - Obtiene reporte de inventario"""
        try:
            resultado = ReporteService.generar_reporte_inventario()
            
            if resultado['success']:
                return jsonify(resultado), 200
            else:
                raise BadRequestError(resultado.get('error', 'Error al generar reporte'))
                
        except BadRequestError as e:
            raise e
        except Exception as e:
            raise BadRequestError(f"Error al generar reporte de inventario: {str(e)}")
    
    @staticmethod
    def reporte_compras():
        """GET - Obtiene reporte de compras"""
        try:
            # Obtener parámetros de query (aceptar ambos formatos)
            fecha_inicio = request.args.get('fecha_inicio') or request.args.get('fecha_desde')
            fecha_fin = request.args.get('fecha_fin') or request.args.get('fecha_hasta')
            
            resultado = ReporteService.generar_reporte_compras(fecha_inicio, fecha_fin)
            
            if resultado['success']:
                return jsonify(resultado), 200
            else:
                raise BadRequestError(resultado.get('error', 'Error al generar reporte'))
                
        except BadRequestError as e:
            raise e
        except Exception as e:
            raise BadRequestError(f"Error al generar reporte de compras: {str(e)}")
