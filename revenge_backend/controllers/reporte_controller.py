"""
Controlador de Reportes
Maneja las peticiones HTTP para reportes
"""

from flask import request, jsonify, send_file
from services.reporte_service import ReporteService
from utils.error_handler import BadRequestError
from utils.pdf_generator import PDFGenerator
from datetime import datetime


class ReporteController:
    """Controlador para endpoints de reportes"""
    
    @staticmethod
    def reporte_ventas():
        """GET - Obtiene reporte de ventas"""
        try:
            # Obtener parámetros de query (aceptar ambos formatos)
            fecha_inicio = request.args.get('fecha_inicio') or request.args.get('fecha_desde')
            fecha_fin = request.args.get('fecha_fin') or request.args.get('fecha_hasta')
            
            resultado = ReporteService.generar_reporte_ventas(fecha_inicio, fecha_fin)
            
            if resultado['success']:
                return jsonify(resultado), 200
            else:
                error_msg = resultado.get('error', 'Error al generar reporte')
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
    
    # ==================== ENDPOINTS PDF ====================
    
    @staticmethod
    def reporte_ventas_pdf():
        """GET - Genera PDF de reporte de ventas"""
        try:
            fecha_inicio = request.args.get('fecha_inicio') or request.args.get('fecha_desde')
            fecha_fin = request.args.get('fecha_fin') or request.args.get('fecha_hasta')
            
            # Obtener datos del reporte
            resultado = ReporteService.generar_reporte_ventas(fecha_inicio, fecha_fin)
            
            if not resultado['success']:
                raise BadRequestError(resultado.get('error', 'Error al generar reporte'))
            
            # Generar PDF
            pdf_buffer = PDFGenerator.generar_reporte_ventas(
                resultado['data'], 
                fecha_inicio, 
                fecha_fin
            )
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_ventas_{timestamp}.pdf"
            
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
            
        except ImportError as e:
            raise BadRequestError("reportlab no está instalado. Ejecuta: pip install reportlab")
        except Exception as e:
            print(f"❌ Error generando PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            raise BadRequestError(f"Error al generar PDF: {str(e)}")
    
    @staticmethod
    def reporte_compras_pdf():
        """GET - Genera PDF de reporte de compras"""
        try:
            fecha_inicio = request.args.get('fecha_inicio') or request.args.get('fecha_desde')
            fecha_fin = request.args.get('fecha_fin') or request.args.get('fecha_hasta')
            
            # Obtener datos del reporte
            resultado = ReporteService.generar_reporte_compras(fecha_inicio, fecha_fin)
            
            if not resultado['success']:
                raise BadRequestError(resultado.get('error', 'Error al generar reporte'))
            
            # Generar PDF
            pdf_buffer = PDFGenerator.generar_reporte_compras(
                resultado['data'], 
                fecha_inicio, 
                fecha_fin
            )
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_compras_{timestamp}.pdf"
            
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
            
        except ImportError as e:
            raise BadRequestError("reportlab no está instalado. Ejecuta: pip install reportlab")
        except Exception as e:
            print(f"❌ Error generando PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            raise BadRequestError(f"Error al generar PDF: {str(e)}")
    
    @staticmethod
    def reporte_inventario_pdf():
        """GET - Genera PDF de reporte de inventario"""
        try:
            # Obtener datos del reporte
            resultado = ReporteService.generar_reporte_inventario()
            
            if not resultado['success']:
                raise BadRequestError(resultado.get('error', 'Error al generar reporte'))
            
            # Generar PDF
            pdf_buffer = PDFGenerator.generar_reporte_inventario(resultado['data'])
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_inventario_{timestamp}.pdf"
            
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
            
        except ImportError as e:
            raise BadRequestError("reportlab no está instalado. Ejecuta: pip install reportlab")
        except Exception as e:
            print(f"❌ Error generando PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            raise BadRequestError(f"Error al generar PDF: {str(e)}")

    # ==================== ENDPOINTS EXCEL ====================
    
    @staticmethod
    def reporte_ventas_excel():
        """GET - Genera Excel de reporte de ventas"""
        try:
            from utils.excel_generator import ExcelGenerator
            
            fecha_inicio = request.args.get('fecha_inicio') or request.args.get('fecha_desde')
            fecha_fin = request.args.get('fecha_fin') or request.args.get('fecha_hasta')
            
            # Obtener datos del reporte
            resultado = ReporteService.generar_reporte_ventas(fecha_inicio, fecha_fin)
            
            if not resultado['success']:
                raise BadRequestError(resultado.get('error', 'Error al generar reporte'))
            
            # Generar Excel
            excel_buffer = ExcelGenerator.generar_reporte_ventas(
                resultado['data'], 
                fecha_inicio, 
                fecha_fin
            )
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_ventas_{timestamp}.xlsx"
            
            return send_file(
                excel_buffer,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
            
        except ImportError as e:
            raise BadRequestError("openpyxl no está instalado. Ejecuta: pip install openpyxl")
        except Exception as e:
            print(f"❌ Error generando Excel: {str(e)}")
            import traceback
            traceback.print_exc()
            raise BadRequestError(f"Error al generar Excel: {str(e)}")
    
    @staticmethod
    def reporte_compras_excel():
        """GET - Genera Excel de reporte de compras"""
        try:
            from utils.excel_generator import ExcelGenerator
            
            fecha_inicio = request.args.get('fecha_inicio') or request.args.get('fecha_desde')
            fecha_fin = request.args.get('fecha_fin') or request.args.get('fecha_hasta')
            
            # Obtener datos del reporte
            resultado = ReporteService.generar_reporte_compras(fecha_inicio, fecha_fin)
            
            if not resultado['success']:
                raise BadRequestError(resultado.get('error', 'Error al generar reporte'))
            
            # Generar Excel
            excel_buffer = ExcelGenerator.generar_reporte_compras(
                resultado['data'], 
                fecha_inicio, 
                fecha_fin
            )
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_compras_{timestamp}.xlsx"
            
            return send_file(
                excel_buffer,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
            
        except ImportError as e:
            raise BadRequestError("openpyxl no está instalado. Ejecuta: pip install openpyxl")
        except Exception as e:
            print(f"❌ Error generando Excel: {str(e)}")
            import traceback
            traceback.print_exc()
            raise BadRequestError(f"Error al generar Excel: {str(e)}")
    
    @staticmethod
    def reporte_inventario_excel():
        """GET - Genera Excel de reporte de inventario"""
        try:
            from utils.excel_generator import ExcelGenerator
            
            # Obtener datos del reporte
            resultado = ReporteService.generar_reporte_inventario()
            
            if not resultado['success']:
                raise BadRequestError(resultado.get('error', 'Error al generar reporte'))
            
            # Generar Excel
            excel_buffer = ExcelGenerator.generar_reporte_inventario(resultado['data'])
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_inventario_{timestamp}.xlsx"
            
            return send_file(
                excel_buffer,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
            
        except ImportError as e:
            raise BadRequestError("openpyxl no está instalado. Ejecuta: pip install openpyxl")
        except Exception as e:
            print(f"❌ Error generando Excel: {str(e)}")
            import traceback
            traceback.print_exc()
            raise BadRequestError(f"Error al generar Excel: {str(e)}")
