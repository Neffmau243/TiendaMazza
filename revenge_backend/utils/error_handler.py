"""
Manejador de errores HTTP
Aplica principio Open/Closed para extender manejo de errores
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException


class APIError(Exception):
    """Clase base para errores de la API"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = True
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


class ValidationError(APIError):
    """Error de validación"""
    def __init__(self, message, payload=None):
        super().__init__(message, 400, payload)


class BadRequestError(APIError):
    """Petición incorrecta"""
    def __init__(self, message="Petición incorrecta", payload=None):
        super().__init__(message, 400, payload)


class NotFoundError(APIError):
    """Recurso no encontrado"""
    def __init__(self, message="Recurso no encontrado", payload=None):
        super().__init__(message, 404, payload)


class UnauthorizedError(APIError):
    """No autorizado"""
    def __init__(self, message="No autorizado", payload=None):
        super().__init__(message, 401, payload)


class ForbiddenError(APIError):
    """Acceso prohibido"""
    def __init__(self, message="Acceso prohibido", payload=None):
        super().__init__(message, 403, payload)


class ConflictError(APIError):
    """Conflicto - recurso duplicado"""
    def __init__(self, message="El recurso ya existe", payload=None):
        super().__init__(message, 409, payload)


class ServerError(APIError):
    """Error interno del servidor"""
    def __init__(self, message="Error interno del servidor", payload=None):
        super().__init__(message, 500, payload)


def register_error_handlers(app):
    """Registra los manejadores de errores en la aplicación Flask"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Maneja errores personalizados de la API"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Maneja excepciones HTTP estándar"""
        response = jsonify({
            'error': True,
            'message': error.description,
            'status_code': error.code
        })
        response.status_code = error.code
        return response
    
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """Maneja errores de validación (ValueError)"""
        response = jsonify({
            'error': True,
            'message': str(error),
            'status_code': 400
        })
        response.status_code = 400
        return response
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Maneja errores no capturados"""
        response = jsonify({
            'error': True,
            'message': 'Ha ocurrido un error interno',
            'details': str(error),
            'status_code': 500
        })
        response.status_code = 500
        return response
    
    @app.errorhandler(404)
    def handle_404(error):
        """Maneja errores 404"""
        response = jsonify({
            'error': True,
            'message': 'Endpoint no encontrado',
            'status_code': 404
        })
        response.status_code = 404
        return response
    
    @app.errorhandler(405)
    def handle_405(error):
        """Maneja errores 405 - Método no permitido"""
        response = jsonify({
            'error': True,
            'message': 'Método HTTP no permitido',
            'status_code': 405
        })
        response.status_code = 405
        return response


def success_response(data=None, message="Operación exitosa", status_code=200):
    """
    Genera una respuesta exitosa estandarizada
    
    Args:
        data: Datos a retornar
        message: Mensaje de éxito
        status_code: Código HTTP
    
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return response, status_code


def error_response(message="Ha ocurrido un error", status_code=400, details=None):
    """
    Genera una respuesta de error estandarizada
    
    Args:
        message: Mensaje de error
        status_code: Código HTTP
        details: Detalles adicionales del error
    
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {
        'error': True,
        'message': message,
        'status_code': status_code
    }
    
    if details:
        response['details'] = details
    
    return response, status_code
