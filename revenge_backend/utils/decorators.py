"""
Decoradores y Middlewares
Aplica principio Dependency Inversion
"""

from functools import wraps
from flask import request
from utils.error_handler import UnauthorizedError, ForbiddenError


def validar_json(f):
    """
    Decorador para validar que el request tenga JSON
    
    Usage:
        @app.route('/api/create', methods=['POST'])
        @validar_json
        def create():
            data = request.get_json()
            return jsonify(data)
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if not request.is_json:
            raise UnauthorizedError("El contenido debe ser JSON")
        return f(*args, **kwargs)
    return decorator


def validar_campos_requeridos(*campos):
    """
    Decorador para validar campos requeridos en el JSON
    
    Args:
        *campos: Nombres de los campos requeridos
    
    Usage:
        @app.route('/api/create', methods=['POST'])
        @validar_json
        @validar_campos_requeridos('nombre', 'email')
        def create():
            data = request.get_json()
            return jsonify(data)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                raise UnauthorizedError("El contenido debe ser JSON")
            
            data = request.get_json()
            print(f"🔍 Validando campos: {campos}")
            print(f"🔍 Datos recibidos: {data}")
            campos_faltantes = []
            
            for campo in campos:
                valor = data.get(campo)
                print(f"  - Campo '{campo}': {valor} (tipo: {type(valor).__name__})")
                if campo not in data or data[campo] is None or data[campo] == '':
                    campos_faltantes.append(campo)
            
            if campos_faltantes:
                print(f"❌ Campos faltantes: {campos_faltantes}")
                raise UnauthorizedError(
                    f"Campos requeridos faltantes: {', '.join(campos_faltantes)}"
                )
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def permiso_requerido(permiso):
    """
    Decorador para verificar permisos específicos
    
    Args:
        permiso: Nombre del permiso requerido
    
    Usage:
        @app.route('/api/ventas', methods=['POST'])
        @token_requerido
        @permiso_requerido('venta')
        def crear_venta():
            return jsonify({'message': 'Venta creada'})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from services.auth_service import AuthService
            
            usuario = getattr(request, 'usuario_actual', None)
            
            if not usuario:
                raise UnauthorizedError("No autenticado")
            
            if not AuthService.verificar_permisos(usuario['usuario_id'], permiso):
                raise ForbiddenError(f"No tienes permisos para: {permiso}")
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def solo_administrador(f):
    """
    Decorador para endpoints solo de administrador
    
    Usage:
        @app.route('/api/admin/config', methods=['POST'])
        @token_requerido
        @solo_administrador
        def config():
            return jsonify({'message': 'Configuración actualizada'})
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        from services.auth_service import AuthService
        
        usuario = getattr(request, 'usuario_actual', None)
        
        if not usuario:
            raise UnauthorizedError("No autenticado")
        
        if not AuthService.es_administrador(usuario['usuario_id']):
            raise ForbiddenError("Solo administradores pueden acceder")
        
        return f(*args, **kwargs)
    
    return decorator


def puede_vender(f):
    """
    Decorador para verificar si puede realizar ventas
    
    Usage:
        @app.route('/api/ventas', methods=['POST'])
        @token_requerido
        @puede_vender
        def crear_venta():
            return jsonify({'message': 'Venta creada'})
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        from services.auth_service import AuthService
        
        usuario = getattr(request, 'usuario_actual', None)
        
        if not usuario:
            raise UnauthorizedError("No autenticado")
        
        if not AuthService.puede_realizar_venta(usuario['usuario_id']):
            raise ForbiddenError("No tienes permisos para realizar ventas")
        
        return f(*args, **kwargs)
    
    return decorator


def validar_paginacion(f):
    """
    Decorador para validar y establecer parámetros de paginación
    
    Usage:
        @app.route('/api/productos', methods=['GET'])
        @validar_paginacion
        def listar_productos():
            limite = request.limite
            offset = request.offset
            return jsonify({'limite': limite, 'offset': offset})
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            limite = int(request.args.get('limite', 100))
            offset = int(request.args.get('offset', 0))
            
            # Validar límites
            if limite < 1 or limite > 1000:
                limite = 100
            
            if offset < 0:
                offset = 0
            
            # Agregar al request
            request.limite = limite
            request.offset = offset
            
        except ValueError:
            request.limite = 100
            request.offset = 0
        
        return f(*args, **kwargs)
    
    return decorator
