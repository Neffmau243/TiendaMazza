"""
Rutas de Reportes
"""

from flask import Blueprint
from controllers.reporte_controller import ReporteController

reporte_bp = Blueprint('reportes', __name__)

# GET /api/reportes/ventas
reporte_bp.route('/ventas', methods=['GET'])(ReporteController.reporte_ventas)

# GET /api/reportes/inventario
reporte_bp.route('/inventario', methods=['GET'])(ReporteController.reporte_inventario)

# GET /api/reportes/compras
reporte_bp.route('/compras', methods=['GET'])(ReporteController.reporte_compras)
