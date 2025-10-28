"""
Revenge Backend - Sistema de Gestión de Tienda
Aplicación principal Flask con arquitectura modular
"""

import sys
import os

# Agregar revenge_backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'revenge_backend'))

from flask import Flask, jsonify, send_from_directory, redirect
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno desde revenge_backend
load_dotenv(os.path.join(os.path.dirname(__file__), 'revenge_backend', '.env'))

# Importar rutas desde revenge_backend
from revenge_backend.routes.auth_routes import auth_bp
from revenge_backend.routes.producto_routes import producto_bp
from revenge_backend.routes.categoria_routes import categoria_bp
from revenge_backend.routes.venta_routes import venta_bp
from revenge_backend.routes.compra_routes import compra_bp
from revenge_backend.routes.usuario_routes import usuario_bp
from revenge_backend.routes.proveedor_routes import proveedor_bp
from revenge_backend.routes.reporte_routes import reporte_bp

# Importar manejador de errores desde revenge_backend
from revenge_backend.utils.error_handler import register_error_handlers

def create_app():
    """Factory pattern para crear la aplicación Flask"""
    # Configurar Flask para servir el frontend
    frontend_folder = os.path.join(os.path.dirname(__file__), 'revenge_frontend')
    app = Flask(__name__, 
                static_folder=frontend_folder,
                static_url_path='')
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_AS_ASCII'] = False  # Para caracteres especiales
    app.config['JSON_SORT_KEYS'] = False
    
    # Habilitar CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Registrar blueprints (rutas)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(producto_bp, url_prefix='/api/productos')
    app.register_blueprint(categoria_bp, url_prefix='/api/categorias')
    app.register_blueprint(venta_bp, url_prefix='/api/ventas')
    app.register_blueprint(compra_bp, url_prefix='/api/compras')
    app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')
    app.register_blueprint(proveedor_bp, url_prefix='/api/proveedores')
    app.register_blueprint(reporte_bp, url_prefix='/api/reportes')
    
    # Registrar manejadores de errores
    register_error_handlers(app)
    
    # ==================== RUTAS DEL FRONTEND ====================
    
    # Ruta principal - Servir index.html (página de login)
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    # Servir todas las páginas HTML
    @app.route('/<path:filename>')
    def serve_frontend(filename):
        # Si es una página HTML, servirla
        if filename.endswith('.html'):
            return send_from_directory(app.static_folder, filename)
        
        # Si es un archivo estático (css, js, etc.)
        if '.' in filename:
            # Determinar la subcarpeta (css, js, assets)
            if filename.startswith('css/') or filename.startswith('js/') or filename.startswith('assets/'):
                return send_from_directory(app.static_folder, filename)
            # Si no tiene subcarpeta, buscar en la raíz
            return send_from_directory(app.static_folder, filename)
        
        # Si no tiene extensión, redirigir al login
        return redirect('/')
    
    # API Health check
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    # API Info (solo para verificar que la API está funcionando)
    @app.route('/api')
    def api_info():
        return jsonify({
            'message': '🚀 Revenge Backend API',
            'version': '1.0.0',
            'status': 'active',
            'endpoints': {
                'auth': '/api/auth',
                'productos': '/api/productos',
                'categorias': '/api/categorias',
                'ventas': '/api/ventas',
                'compras': '/api/compras',
                'usuarios': '/api/usuarios',
                'proveedores': '/api/proveedores',
                'reportes': '/api/reportes'
            }
        })
    
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"\n{'='*60}")
    print(f"⚡ Revenge POS - Sistema Completo")
    print(f"{'='*60}")
    print(f"🌐 Frontend:  http://127.0.0.1:{port}")
    print(f"🔧 API:       http://127.0.0.1:{port}/api")
    print(f"� Health:    http://127.0.0.1:{port}/health")
    print(f"{'='*60}")
    print(f"📂 Sirviendo: revenge_frontend/")
    print(f"🔑 Login:     admin@revenge.com / 123456")
    print(f"� Debug:     {debug}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
