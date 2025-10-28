"""
Rutas de Autenticación
"""

from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

# POST /api/auth/login
auth_bp.route('/login', methods=['POST'])(AuthController.login)

# POST /api/auth/registrar
auth_bp.route('/registrar', methods=['POST'])(AuthController.registrar)

# POST /api/auth/logout
auth_bp.route('/logout', methods=['POST'])(AuthController.logout)
