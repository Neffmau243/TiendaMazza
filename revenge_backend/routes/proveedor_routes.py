"""
Rutas de Proveedores
"""

from flask import Blueprint
from flask import request
from models.proveedor_model import ProveedorModel
from utils.error_handler import success_response, error_response
from utils.decorators import validar_json, validar_campos_requeridos

proveedor_bp = Blueprint('proveedores', __name__)


@proveedor_bp.route('/', methods=['GET'])
def listar():
    """GET /api/proveedores"""
    try:
        incluir_inactivos = request.args.get('incluir_inactivos', 'false').lower() == 'true'
        proveedores = ProveedorModel.obtener_todos(incluir_inactivos)
        return success_response(data=proveedores)
    except Exception as e:
        return error_response(str(e), 500)


@proveedor_bp.route('/<int:proveedor_id>', methods=['GET'])
def obtener(proveedor_id):
    """GET /api/proveedores/<id>"""
    try:
        proveedor = ProveedorModel.obtener_por_id(proveedor_id)
        if not proveedor:
            return error_response("Proveedor no encontrado", 404)
        return success_response(data=proveedor)
    except Exception as e:
        return error_response(str(e), 500)


@proveedor_bp.route('/', methods=['POST'])
@validar_json
@validar_campos_requeridos('nombre')
def crear():
    """POST /api/proveedores"""
    try:
        data = request.get_json()
        
        proveedor_id = ProveedorModel.crear(
            nombre=data['nombre'],
            ruc=data.get('ruc'),
            telefono=data.get('telefono'),
            direccion=data.get('direccion'),
            email=data.get('email'),
            contacto=data.get('contacto'),
            created_by=data.get('created_by')
        )
        
        return success_response(
            data={'proveedor_id': proveedor_id},
            message="Proveedor creado exitosamente",
            status_code=201
        )
    except Exception as e:
        return error_response(str(e), 500)


@proveedor_bp.route('/<int:proveedor_id>', methods=['PUT'])
@validar_json
def actualizar(proveedor_id):
    """PUT /api/proveedores/<id>"""
    try:
        data = request.get_json()
        ProveedorModel.actualizar(proveedor_id, **data)
        return success_response(message="Proveedor actualizado exitosamente")
    except Exception as e:
        return error_response(str(e), 500)


@proveedor_bp.route('/<int:proveedor_id>', methods=['DELETE'])
def eliminar(proveedor_id):
    """DELETE /api/proveedores/<id>"""
    try:
        ProveedorModel.eliminar_logico(proveedor_id)
        return success_response(message="Proveedor eliminado exitosamente")
    except Exception as e:
        return error_response(str(e), 400)
