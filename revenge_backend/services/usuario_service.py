"""
Servicio de Usuarios
"""

from models.usuario_model import UsuarioModel


class UsuarioService:
    """Servicio para lógica de negocio de usuarios"""
    
    @staticmethod
    def crear_usuario(nombre, email, password, rol_id, created_by=None):
        """Crea un nuevo usuario"""
        # Importar aquí para evitar circular import
        from services.auth_service import AuthService
        
        return AuthService.registrar_usuario(nombre, email, password, rol_id, created_by)
    
    @staticmethod
    def obtener_usuario(usuario_id):
        """Obtiene un usuario por ID"""
        usuario = UsuarioModel.obtener_por_id(usuario_id)
        if usuario:
            # Ocultar password
            usuario_seguro = usuario.copy()
            usuario_seguro.pop('password_hash', None)
            return usuario_seguro
        return None
    
    @staticmethod
    def listar_usuarios(incluir_inactivos=False):
        """Lista todos los usuarios"""
        usuarios = UsuarioModel.obtener_todos(incluir_inactivos)
        # Ocultar passwords
        usuarios_seguros = []
        for usuario in usuarios:
            usuario_seguro = usuario.copy()
            usuario_seguro.pop('password_hash', None)
            usuarios_seguros.append(usuario_seguro)
        return usuarios_seguros
    
    @staticmethod
    def actualizar_usuario(usuario_id, **datos):
        """Actualiza un usuario"""
        usuario = UsuarioModel.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        # No permitir actualizar password por este método
        if 'password' in datos or 'password_hash' in datos:
            raise ValueError("Use el método de cambio de contraseña")
        
        # Validar email si se actualiza
        if 'email' in datos:
            if UsuarioModel.verificar_email_existe(datos['email'], usuario_id):
                raise ValueError("El email ya está en uso")
        
        return UsuarioModel.actualizar(usuario_id, **datos)
    
    @staticmethod
    def cambiar_estado(usuario_id, estado_id):
        """Cambia el estado de un usuario"""
        return UsuarioModel.actualizar(usuario_id, estado_id=estado_id)
    
    @staticmethod
    def eliminar_usuario(usuario_id):
        """Elimina lógicamente un usuario"""
        usuario = UsuarioModel.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        return UsuarioModel.eliminar_logico(usuario_id)
    
    @staticmethod
    def obtener_usuarios_por_rol(rol_id):
        """Obtiene usuarios de un rol específico"""
        return UsuarioModel.obtener_por_rol(rol_id)
    
    @staticmethod
    def obtener_cajeros():
        """Obtiene todos los cajeros activos"""
        return UsuarioModel.obtener_por_rol(2)
    
    @staticmethod
    def obtener_trabajadores():
        """Obtiene todos los trabajadores activos"""
        return UsuarioModel.obtener_por_rol(3)
