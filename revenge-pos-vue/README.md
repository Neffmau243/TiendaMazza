# Revenge POS - Vue.js Frontend

Sistema de Punto de Venta desarrollado con Vue.js 3, Pinia y Vue Router.

## 🚀 Tecnologías

- **Vue.js 3** - Framework progresivo de JavaScript
- **Pinia** - Gestión de estado
- **Vue Router** - Enrutamiento
- **Axios** - Cliente HTTP
- **Vite** - Build tool
- **jsPDF** - Generación de PDFs

## 📋 Requisitos

- Node.js 18+
- npm o yarn
- Backend Flask corriendo en http://127.0.0.1:5000

## 🔧 Instalación

```bash
# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env

# Iniciar servidor de desarrollo
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview
```

## 📁 Estructura del Proyecto

```
src/
├── assets/          # Recursos estáticos
├── components/      # Componentes reutilizables
├── views/           # Vistas/Páginas
├── layouts/         # Layouts
├── router/          # Configuración de rutas
├── stores/          # Pinia stores
├── composables/     # Composables
├── services/        # Servicios API
└── utils/           # Utilidades
```

## 🔐 Usuarios de Prueba

- **Administrador**: admin@revenge.com / 123456
- **Cajero**: cajero@revenge.com / 123456
- **Almacenista**: almacen@revenge.com / 123456

## 📝 Scripts Disponibles

- `npm run dev` - Inicia el servidor de desarrollo
- `npm run build` - Construye para producción
- `npm run preview` - Preview del build de producción

## 🌐 Variables de Entorno

```env
VITE_API_BASE_URL=http://127.0.0.1:5000/api
VITE_APP_NAME=Revenge POS
VITE_IVA=0.18
```

## 📄 Licencia

Privado - Todos los derechos reservados
