"""
Rutas de Ventas
"""

from flask import Blueprint
from controllers.venta_controller import VentaController

venta_bp = Blueprint('ventas', __name__)

# GET /api/ventas
venta_bp.route('/', methods=['GET'])(VentaController.listar)

# GET /api/ventas/resumen-dia
venta_bp.route('/resumen-dia', methods=['GET'])(VentaController.resumen_dia)

# GET /api/ventas/productos-mas-vendidos
venta_bp.route('/productos-mas-vendidos', methods=['GET'])(VentaController.productos_mas_vendidos)

# GET /api/ventas/por-fecha
venta_bp.route('/por-fecha', methods=['GET'])(VentaController.por_fecha)

# GET /api/ventas/<id>
venta_bp.route('/<int:venta_id>', methods=['GET'])(VentaController.obtener)

# POST /api/ventas
venta_bp.route('/', methods=['POST'])(VentaController.crear)
