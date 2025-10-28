"""
Rutas de Usuarios
"""

from flask import Blueprint
from controllers.usuario_controller import UsuarioController

usuario_bp = Blueprint('usuarios', __name__)

# GET /api/usuarios
usuario_bp.route('/', methods=['GET'])(UsuarioController.listar)

# GET /api/usuarios/<id>
usuario_bp.route('/<int:usuario_id>', methods=['GET'])(UsuarioController.obtener)

# PUT /api/usuarios/<id>
usuario_bp.route('/<int:usuario_id>', methods=['PUT'])(UsuarioController.actualizar)

# DELETE /api/usuarios/<id>
usuario_bp.route('/<int:usuario_id>', methods=['DELETE'])(UsuarioController.eliminar)
