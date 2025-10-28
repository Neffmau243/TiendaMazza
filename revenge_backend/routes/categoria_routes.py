"""
Rutas de Categorías
"""

from flask import Blueprint
from controllers.categoria_controller import CategoriaController

categoria_bp = Blueprint('categorias', __name__)

# GET /api/categorias
categoria_bp.route('/', methods=['GET'])(CategoriaController.listar)

# GET /api/categorias/<id>
categoria_bp.route('/<int:categoria_id>', methods=['GET'])(CategoriaController.obtener)

# POST /api/categorias
categoria_bp.route('/', methods=['POST'])(CategoriaController.crear)

# PUT /api/categorias/<id>
categoria_bp.route('/<int:categoria_id>', methods=['PUT'])(CategoriaController.actualizar)

# DELETE /api/categorias/<id>
categoria_bp.route('/<int:categoria_id>', methods=['DELETE'])(CategoriaController.eliminar)
