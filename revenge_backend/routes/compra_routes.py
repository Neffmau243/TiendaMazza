"""
Rutas de Compras
"""

from flask import Blueprint
from controllers.compra_controller import CompraController

compra_bp = Blueprint('compras', __name__)

# GET /api/compras
compra_bp.route('/', methods=['GET'])(CompraController.listar)

# GET /api/compras/<id>
compra_bp.route('/<int:compra_id>', methods=['GET'])(CompraController.obtener)

# POST /api/compras
compra_bp.route('/', methods=['POST'])(CompraController.crear)
