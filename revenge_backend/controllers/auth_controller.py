"""
Controlador de Autenticación
Maneja las solicitudes HTTP relacionadas con auth
"""

from flask import request
from services.auth_service import AuthService
from utils.error_handler import success_response, error_response, UnauthorizedError
from utils.decorators import validar_json, validar_campos_requeridos


class AuthController:
    """Controlador para endpoints de autenticación"""
    
    @staticmethod
    @validar_json
    @validar_campos_requeridos('email', 'password')
    def login():
        """POST /api/auth/login"""
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']
            
            usuario = AuthService.login(email, password)
            
            if not usuario:
                raise UnauthorizedError("Credenciales inválidas")
            
            # Generar token temporal (básico para desarrollo)
            import hashlib
            import time
            token_data = f"{usuario['id']}:{usuario['email']}:{time.time()}"
            usuario['token'] = hashlib.sha256(token_data.encode()).hexdigest()
            
            # TODO: Implementar JWT real para producción
            # from utils.jwt_helper import JWTHelper
            # token = JWTHelper.generar_token(
            #     usuario['id'], usuario['email'], usuario['rol_id']
            # )
            # usuario['token'] = token
            
            return success_response(
                data=usuario,
                message="Login exitoso"
            )
            
        except UnauthorizedError as e:
            return error_response(str(e), 401)
        except Exception as e:
            return error_response(f"Error en login: {str(e)}", 500)
    
    @staticmethod
    @validar_json
    @validar_campos_requeridos('nombre', 'email', 'password', 'rol_id')
    def registrar():
        """POST /api/auth/registrar"""
        try:
            data = request.get_json()
            
            usuario_id = AuthService.registrar_usuario(
                nombre=data['nombre'],
                email=data['email'],
                password=data['password'],
                rol_id=data['rol_id'],
                created_by=data.get('created_by')
            )
            
            return success_response(
                data={'usuario_id': usuario_id},
                message="Usuario registrado exitosamente",
                status_code=201
            )
            
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(f"Error registrando usuario: {str(e)}", 500)
    
    @staticmethod
    def logout():
        """POST /api/auth/logout"""
        try:
            # TODO: Implementar con JWT
            return success_response(message="Logout exitoso")
        except Exception as e:
            return error_response(f"Error en logout: {str(e)}", 500)
