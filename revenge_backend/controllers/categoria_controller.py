"""
Controlador de Categorías
"""

from flask import request
from models.categoria_model import CategoriaModel
from utils.error_handler import success_response, error_response
from utils.decorators import validar_json, validar_campos_requeridos


class CategoriaController:
    """Controlador para endpoints de categorías"""
    
    @staticmethod
    def listar():
        """GET /api/categorias"""
        try:
            categorias = CategoriaModel.obtener_todas()
            return success_response(data=categorias)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def obtener(categoria_id):
        """GET /api/categorias/<id>"""
        try:
            categoria = CategoriaModel.obtener_por_id(categoria_id)
            if not categoria:
                return error_response("Categoría no encontrada", 404)
            return success_response(data=categoria)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    @validar_json
    @validar_campos_requeridos('nombre')
    def crear():
        """POST /api/categorias"""
        try:
            data = request.get_json()
            
            if CategoriaModel.verificar_nombre_existe(data['nombre']):
                return error_response("La categoría ya existe", 409)
            
            categoria_id = CategoriaModel.crear(
                nombre=data['nombre'],
                descripcion=data.get('descripcion'),
                created_by=data.get('created_by')
            )
            
            return success_response(
                data={'categoria_id': categoria_id},
                message="Categoría creada exitosamente",
                status_code=201
            )
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    @validar_json
    def actualizar(categoria_id):
        """PUT /api/categorias/<id>"""
        try:
            data = request.get_json()
            CategoriaModel.actualizar(categoria_id, **data)
            return success_response(message="Categoría actualizada exitosamente")
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def eliminar(categoria_id):
        """DELETE /api/categorias/<id>"""
        try:
            CategoriaModel.eliminar_logico(categoria_id)
            return success_response(message="Categoría eliminada exitosamente")
        except Exception as e:
            return error_response(str(e), 400)
