"""
Password Helper
Helper para hasheo y verificación de contraseñas
(Preparado para implementación futura con bcrypt)
"""

# TODO: Instalar bcrypt cuando esté listo
# import bcrypt


class PasswordHelper:
    """Helper para manejo de contraseñas"""
    
    @staticmethod
    def hash_password(password):
        """
        Hashea una contraseña
        
        TODO: Implementar con bcrypt
        
        Args:
            password: Contraseña en texto plano
        
        Returns:
            str: Hash de la contraseña
        """
        # TEMPORAL - NO SEGURO
        # Retorna la contraseña tal cual (solo para desarrollo)
        return password
        
        # CUANDO ESTÉ LISTO:
        # salt = bcrypt.gensalt()
        # hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        # return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed_password):
        """
        Verifica una contraseña contra su hash
        
        TODO: Implementar con bcrypt
        
        Args:
            password: Contraseña en texto plano
            hashed_password: Hash almacenado
        
        Returns:
            bool: True si coincide
        """
        # TEMPORAL - NO SEGURO
        # Comparación directa (solo para desarrollo)
        return password == hashed_password
        
        # CUANDO ESTÉ LISTO:
        # return bcrypt.checkpw(
        #     password.encode('utf-8'),
        #     hashed_password.encode('utf-8')
        # )
    
    @staticmethod
    def validar_fortaleza_password(password):
        """
        Valida la fortaleza de una contraseña
        
        Args:
            password: Contraseña a validar
        
        Returns:
            tuple: (bool es_valida, str mensaje)
        """
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        # Aquí puedes agregar más validaciones
        # - Al menos una mayúscula
        # - Al menos un número
        # - Al menos un carácter especial
        # etc.
        
        return True, "Contraseña válida"


# Para cuando implementes bcrypt, agrega a requirements.txt:
# bcrypt==4.1.2
