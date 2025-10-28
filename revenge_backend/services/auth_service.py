"""
Servicio de Autenticación
Principios SOLID aplicados:
- Single Responsibility: Solo maneja autenticación
- Open/Closed: Extendible para nuevos métodos de auth
- Dependency Inversion: Depende de abstracciones (models)
"""

from models.usuario_model import UsuarioModel
from datetime import datetime, timedelta
import os


class AuthService:
    """Servicio para manejar autenticación y autorización"""
    
    @staticmethod
    def login(email, password):
        """
        Autentica un usuario
        Por ahora sin hash (según solicitud del usuario)
        
        Returns:
            dict: Información del usuario o None
        """
        usuario = UsuarioModel.obtener_por_email(email)
        
        if not usuario:
            return None
        
        # Verificar estado activo
        if usuario['estado_id'] != 1:
            raise Exception("Usuario inactivo")
        
        # TODO: Implementar verificación de hash cuando esté listo
        # Por ahora comparación simple (TEMPORAL - NO SEGURO)
        if usuario['password_hash'] != password:
            return None
        
        # Agregar al cache de usuarios activos
        UsuarioModel.agregar_a_cache(usuario['id'], usuario)
        
        # Retornar información del usuario (sin password)
        return {
            'id': usuario['id'],
            'nombre': usuario['nombre'],
            'email': usuario['email'],
            'rol_id': usuario['rol_id'],
            'rol_nombre': usuario['rol_nombre'],
            'estado': usuario['estado_nombre']
        }
    
    @staticmethod
    def registrar_usuario(nombre, email, password, rol_id, created_by=None):
        """
        Registra un nuevo usuario
        
        Args:
            rol_id: 1=admin, 2=cajero, 3=trabajador
        """
        # Verificar que el email no exista
        if UsuarioModel.verificar_email_existe(email):
            raise Exception("El email ya está registrado")
        
        # TODO: Implementar hash de contraseña
        # Por ahora guarda directamente (TEMPORAL - NO SEGURO)
        password_hash = password
        
        # Crear usuario
        usuario_id = UsuarioModel.crear(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            rol_id=rol_id,
            created_by=created_by
        )
        
        return usuario_id
    
    @staticmethod
    def verificar_permisos(usuario_id, accion):
        """
        Verifica si un usuario tiene permisos para una acción
        
        Args:
            accion: 'venta', 'compra', 'gestion_usuarios', etc.
        
        Returns:
            bool: True si tiene permiso
        """
        usuario = UsuarioModel.obtener_por_id(usuario_id)
        
        if not usuario:
            return False
        
        rol_id = usuario['rol_id']
        
        # Definir permisos por rol
        permisos = {
            1: ['*'],  # Administrador: todos los permisos
            2: ['venta', 'ver_productos', 'ver_categorias'],  # Cajero
            3: ['compra', 'gestion_productos', 'gestion_inventario', 
                'gestion_proveedores', 'ver_productos', 'ver_categorias']  # Trabajador
        }
        
        permisos_rol = permisos.get(rol_id, [])
        
        # Admin tiene todos los permisos
        if '*' in permisos_rol:
            return True
        
        return accion in permisos_rol
    
    @staticmethod
    def puede_realizar_venta(usuario_id):
        """Verifica si un usuario puede realizar ventas"""
        usuario = UsuarioModel.obtener_por_id(usuario_id)
        
        if not usuario:
            return False
        
        # Solo admin (1) y cajero (2) pueden realizar ventas
        return usuario['rol_id'] in [1, 2]
    
    @staticmethod
    def es_administrador(usuario_id):
        """Verifica si un usuario es administrador"""
        usuario = UsuarioModel.obtener_por_id(usuario_id)
        
        if not usuario:
            return False
        
        return usuario['rol_id'] == 1
    
    @staticmethod
    def cambiar_password(usuario_id, password_actual, password_nueva):
        """
        Cambia la contraseña de un usuario
        TODO: Implementar con hash
        """
        usuario = UsuarioModel.obtener_por_id(usuario_id)
        
        if not usuario:
            raise Exception("Usuario no encontrado")
        
        # TODO: Verificar password actual con hash
        if usuario['password_hash'] != password_actual:
            raise Exception("Contraseña actual incorrecta")
        
        # TODO: Hashear nueva contraseña
        password_hash = password_nueva
        
        # Actualizar
        return UsuarioModel.actualizar(usuario_id, password_hash=password_hash)
    
    @staticmethod
    def logout(usuario_id):
        """Cierra sesión de un usuario"""
        # Remover del cache de usuarios activos
        if usuario_id in UsuarioModel.obtener_cache():
            cache = UsuarioModel.obtener_cache()
            del cache[usuario_id]
        
        return True
