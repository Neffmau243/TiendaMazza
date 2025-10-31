"""
Rutas de Reportes
"""

from flask import Blueprint
from controllers.reporte_controller import ReporteController

reporte_bp = Blueprint('reportes', __name__)

# GET /api/reportes/ventas - Datos JSON
reporte_bp.route('/ventas', methods=['GET'])(ReporteController.reporte_ventas)

# GET /api/reportes/inventario - Datos JSON
reporte_bp.route('/inventario', methods=['GET'])(ReporteController.reporte_inventario)

# GET /api/reportes/compras - Datos JSON
reporte_bp.route('/compras', methods=['GET'])(ReporteController.reporte_compras)

# GET /api/reportes/ventas/pdf - Generar PDF
reporte_bp.route('/ventas/pdf', methods=['GET'])(ReporteController.reporte_ventas_pdf)

# GET /api/reportes/compras/pdf - Generar PDF
reporte_bp.route('/compras/pdf', methods=['GET'])(ReporteController.reporte_compras_pdf)

# GET /api/reportes/inventario/pdf - Generar PDF
reporte_bp.route('/inventario/pdf', methods=['GET'])(ReporteController.reporte_inventario_pdf)
