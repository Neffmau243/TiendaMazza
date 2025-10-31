"""
Servicio de Reportes
Lógica de negocio para generación de reportes
"""

from models.reporte_model import ReporteModel


class ReporteService:
    """Servicio para manejar lógica de reportes"""
    
    @staticmethod
    def generar_reporte_ventas(fecha_inicio=None, fecha_fin=None):
        """
        Genera reporte de ventas
        
        Args:
            fecha_inicio (str): Fecha inicio
            fecha_fin (str): Fecha fin
            
        Returns:
            dict: Datos del reporte
        """
        try:
            datos = ReporteModel.reporte_ventas(fecha_inicio, fecha_fin)
            return {
                'success': True,
                'data': datos
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def generar_reporte_inventario():
        """
        Genera reporte de inventario
        
        Returns:
            dict: Datos del reporte
        """
        try:
            datos = ReporteModel.reporte_inventario()
            return {
                'success': True,
                'data': datos
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def generar_reporte_compras(fecha_inicio=None, fecha_fin=None):
        """
        Genera reporte de compras
        
        Args:
            fecha_inicio (str): Fecha inicio
            fecha_fin (str): Fecha fin
            
        Returns:
            dict: Datos del reporte
        """
        try:
            datos = ReporteModel.reporte_compras(fecha_inicio, fecha_fin)
            return {
                'success': True,
                'data': datos
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
