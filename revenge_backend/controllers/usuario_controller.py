"""
Controlador de Usuarios
"""

from flask import request
from services.usuario_service import UsuarioService
from utils.error_handler import success_response, error_response
from utils.decorators import validar_json


class UsuarioController:
    """Controlador para endpoints de usuarios"""
    
    @staticmethod
    def listar():
        """GET /api/usuarios"""
        try:
            incluir_inactivos = request.args.get('incluir_inactivos', 'false').lower() == 'true'
            usuarios = UsuarioService.listar_usuarios(incluir_inactivos)
            return success_response(data=usuarios)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def obtener(usuario_id):
        """GET /api/usuarios/<id>"""
        try:
            usuario = UsuarioService.obtener_usuario(usuario_id)
            if not usuario:
                return error_response("Usuario no encontrado", 404)
            return success_response(data=usuario)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    @validar_json
    def actualizar(usuario_id):
        """PUT /api/usuarios/<id>"""
        try:
            data = request.get_json()
            UsuarioService.actualizar_usuario(usuario_id, **data)
            return success_response(message="Usuario actualizado exitosamente")
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def eliminar(usuario_id):
        """DELETE /api/usuarios/<id>"""
        try:
            UsuarioService.eliminar_usuario(usuario_id)
            return success_response(message="Usuario eliminado exitosamente")
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
