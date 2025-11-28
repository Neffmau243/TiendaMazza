"""
Revenge Backend - Sistema de Gestión de Tienda
Aplicación principal Flask con arquitectura modular

CONFIGURACIÓN DE FRONTEND:
- Por defecto: Flask sirve el build de Vue (Producción)
- Modo desarrollo: python app.py --dev (Frontend separado en puerto 5173)
  
Ejecuta 'npm run build' en revenge-pos-vue/ antes del primer uso.
"""

import sys
import os

# Agregar revenge_backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'revenge_backend'))

from flask import Flask, jsonify, send_from_directory
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

def create_app(serve_frontend=False):
    """
    Factory pattern para crear la aplicación Flask
    
    Args:
        serve_frontend (bool): Si True, sirve el frontend Vue desde Flask (producción)
                              Si False, solo API (desarrollo con Vue en puerto 5173)
    """
    
    # Determinar carpeta del frontend
    if serve_frontend:
        # Producción: Servir build de Vue
        frontend_folder = os.path.join(os.path.dirname(__file__), 'revenge-pos-vue', 'dist')
        if not os.path.exists(frontend_folder):
            print("⚠️  WARNING: Frontend build no encontrado en revenge-pos-vue/dist")
            print("   Ejecuta 'npm run build' en revenge-pos-vue/")
            frontend_folder = None
    else:
        frontend_folder = None
    
    # Crear app Flask
    if frontend_folder:
        app = Flask(__name__, 
                    static_folder=frontend_folder,
                    static_url_path='')
    else:
        app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_AS_ASCII'] = False  # Para caracteres especiales
    app.config['JSON_SORT_KEYS'] = False
    
    # Deshabilitar redirección automática de trailing slashes
    app.url_map.strict_slashes = False
    
    # Habilitar CORS
    # En desarrollo, permitir requests desde Vue (puerto 5173 o 3000)
    # En producción, más restrictivo
    cors_origins = [
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ] if not serve_frontend else "*"
    
    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Registrar blueprints (rutas API)
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
    
    # ==================== RUTAS DEL FRONTEND (Solo en producción) ====================
    
    if serve_frontend and frontend_folder:
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve_spa(path):
            """
            Servir SPA de Vue - Maneja todas las rutas que no sean /api
            """
            # Si es una ruta API, dejar que los blueprints la manejen
            if path.startswith('api'):
                return jsonify({'error': 'API endpoint not found'}), 404
            
            # Si el archivo existe en assets, servirlo
            if path.startswith('assets/'):
                file_path = os.path.join(app.static_folder, path)
                if os.path.exists(file_path):
                    return send_from_directory(app.static_folder, path)
            
            # Para cualquier archivo que exista (CSS, JS, imágenes)
            file_path = os.path.join(app.static_folder, path)
            if path and os.path.exists(file_path) and os.path.isfile(file_path):
                return send_from_directory(app.static_folder, path)
            
            # Para todas las rutas de Vue Router, servir index.html
            return send_from_directory(app.static_folder, 'index.html')
        
        @app.errorhandler(404)
        def not_found(e):
            """
            Manejar 404 - Servir index.html para rutas de Vue Router
            """
            from flask import request
            # Si es una petición a /api, devolver JSON
            if request.path.startswith('/api'):
                return jsonify({'error': 'Not found', 'path': request.path}), 404
            # Si no, servir index.html para Vue Router
            return send_from_directory(app.static_folder, 'index.html')
    
    # ==================== RUTAS DE INFORMACIÓN ====================
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'mode': 'production' if serve_frontend else 'development'
        }), 200
    
    @app.route('/api')
    def api_info():
        """Información de la API"""
        return jsonify({
            'message': '🚀 Revenge POS - Backend API',
            'version': '2.0.0',
            'status': 'active',
            'mode': 'production' if serve_frontend else 'development',
            'frontend': 'Vue.js 3 + Vite',
            'endpoints': {
                'auth': '/api/auth',
                'productos': '/api/productos',
                'categorias': '/api/categorias',
                'ventas': '/api/ventas',
                'compras': '/api/compras',
                'usuarios': '/api/usuarios',
                'proveedores': '/api/proveedores',
                'reportes': '/api/reportes'
            },
            'docs': {
                'development': 'Frontend en http://localhost:5173',
                'production': 'Frontend servido desde Flask'
            }
        })
    
    return app


if __name__ == '__main__':
    # Determinar modo de ejecución
    # Por defecto: PRODUCCIÓN (API + Frontend Vue)
    # Para desarrollo: python app.py --dev (solo API, Frontend separado en puerto 5173)
    
    import sys
    # INVERTIDO: Por defecto sirve frontend, usa --dev para modo desarrollo
    serve_frontend = not ('--dev' in sys.argv or '--development' in sys.argv)
    
    app = create_app(serve_frontend=serve_frontend)
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True' and not serve_frontend
    
    print("\n" + "="*60)
    print("🚀 REVENGE POS - Backend Server")
    print("="*60)
    
    if serve_frontend:
        print("📦 Modo: PRODUCCIÓN (API + Frontend Vue)")
        print(f"🌐 Aplicación completa: http://localhost:{port}")
        print("✅ Frontend servido desde Flask")
        print("\n💡 Para modo desarrollo: python app.py --dev")
    else:
        print("🔧 Modo: DESARROLLO (Solo API)")
        print(f"🔌 API Backend: http://localhost:{port}")
        print(f"🎨 Frontend Vue: http://localhost:5173")
        print("\n📝 Para iniciar el frontend:")
        print("   cd revenge-pos-vue")
        print("   npm run dev")
    
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
