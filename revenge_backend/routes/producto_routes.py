"""
Rutas de Productos
"""

from flask import Blueprint
from controllers.producto_controller import ProductoController

producto_bp = Blueprint('productos', __name__)

# GET /api/productos
producto_bp.route('/', methods=['GET'])(ProductoController.listar)

# GET /api/productos/buscar
producto_bp.route('/buscar', methods=['GET'])(ProductoController.buscar)

# GET /api/productos/stock-bajo
producto_bp.route('/stock-bajo', methods=['GET'])(ProductoController.stock_bajo)

# GET /api/productos/<id>
producto_bp.route('/<int:producto_id>', methods=['GET'])(ProductoController.obtener)

# POST /api/productos
producto_bp.route('/', methods=['POST'])(ProductoController.crear)

# PUT /api/productos/<id>
producto_bp.route('/<int:producto_id>', methods=['PUT'])(ProductoController.actualizar)

# DELETE /api/productos/<id>
producto_bp.route('/<int:producto_id>', methods=['DELETE'])(ProductoController.eliminar)

# POST /api/productos/<id>/ajustar-stock
producto_bp.route('/<int:producto_id>/ajustar-stock', methods=['POST'])(ProductoController.ajustar_stock)
