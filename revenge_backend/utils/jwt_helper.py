"""
JWT Helper
Manejo de tokens JWT (preparado para implementación futura)
"""

import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request


class JWTHelper:
    """Helper para manejo de JWT"""
    
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    
    @staticmethod
    def generar_token(usuario_id, email, rol_id):
        """
        Genera un token JWT
        
        Args:
            usuario_id: ID del usuario
            email: Email del usuario
            rol_id: ID del rol
        
        Returns:
            str: Token JWT
        """
        try:
            payload = {
                'usuario_id': usuario_id,
                'email': email,
                'rol_id': rol_id,
                'exp': datetime.utcnow() + timedelta(hours=JWTHelper.EXPIRATION_HOURS),
                'iat': datetime.utcnow()
            }
            
            token = jwt.encode(payload, JWTHelper.SECRET_KEY, algorithm='HS256')
            return token
        except Exception as e:
            print(f"Error generando token: {e}")
            return None
    
    @staticmethod
    def verificar_token(token):
        """
        Verifica y decodifica un token JWT
        
        Args:
            token: Token JWT
        
        Returns:
            dict: Payload del token o None si es inválido
        """
        try:
            payload = jwt.decode(token, JWTHelper.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return None
        except jwt.InvalidTokenError:
            print("Token inválido")
            return None
    
    @staticmethod
    def extraer_token_header():
        """
        Extrae el token del header Authorization
        
        Returns:
            str: Token o None
        """
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        try:
            # Formato: "Bearer <token>"
            partes = auth_header.split()
            if len(partes) == 2 and partes[0].lower() == 'bearer':
                return partes[1]
        except:
            pass
        
        return None
    
    @staticmethod
    def obtener_usuario_actual():
        """
        Obtiene el usuario actual desde el token
        
        Returns:
            dict: Datos del usuario o None
        """
        token = JWTHelper.extraer_token_header()
        
        if not token:
            return None
        
        return JWTHelper.verificar_token(token)


def token_requerido(f):
    """
    Decorador para requerir token JWT en endpoints
    
    Usage:
        @app.route('/api/protected')
        @token_requerido
        def protected_route():
            usuario = request.usuario_actual
            return jsonify(usuario)
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        usuario = JWTHelper.obtener_usuario_actual()
        
        if not usuario:
            return {
                'error': True,
                'message': 'Token inválido o no proporcionado'
            }, 401
        
        # Agregar usuario al request
        request.usuario_actual = usuario
        
        return f(*args, **kwargs)
    
    return decorator


def rol_requerido(*roles_permitidos):
    """
    Decorador para verificar roles
    
    Args:
        *roles_permitidos: IDs de roles permitidos
    
    Usage:
        @app.route('/api/admin')
        @token_requerido
        @rol_requerido(1)  # Solo admin
        def admin_route():
            return jsonify({'message': 'Admin area'})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            usuario = getattr(request, 'usuario_actual', None)
            
            if not usuario:
                return {
                    'error': True,
                    'message': 'No autenticado'
                }, 401
            
            if usuario['rol_id'] not in roles_permitidos:
                return {
                    'error': True,
                    'message': 'No tienes permisos para esta acción'
                }, 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
