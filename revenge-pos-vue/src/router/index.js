// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy loading de vistas
const LoginView = () => import('@/views/LoginView.vue')
const DashboardView = () => import('@/views/DashboardView.vue')
const PuntoVentaView = () => import('@/views/PuntoVentaView.vue')
const ProductosView = () => import('@/views/ProductosView.vue')
const CategoriasView = () => import('@/views/CategoriasView.vue')
const VentasView = () => import('@/views/VentasView.vue')
const ComprasView = () => import('@/views/ComprasView.vue')
const ProveedoresView = () => import('@/views/ProveedoresView.vue')
const UsuariosView = () => import('@/views/UsuariosView.vue')
const ReportesView = () => import('@/views/ReportesView.vue')
const NotFoundView = () => import('@/views/NotFoundView.vue')

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { 
      requiresAuth: false, 
      layout: 'auth',
      title: 'Iniciar Sesión'
    }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { 
      requiresAuth: true,
      roles: [1, 2, 3],
      title: 'Dashboard',
      icon: 'fa-home'
    }
  },
  {
    path: '/punto-venta',
    name: 'PuntoVenta',
    component: PuntoVentaView,
    meta: { 
      requiresAuth: true,
      roles: [1, 2],
      title: 'Punto de Venta',
      icon: 'fa-cash-register'
    }
  },
  {
    path: '/productos',
    name: 'Productos',
    component: ProductosView,
    meta: { 
      requiresAuth: true,
      roles: [1, 3],
      title: 'Productos',
      icon: 'fa-box'
    }
  },
  {
    path: '/categorias',
    name: 'Categorias',
    component: CategoriasView,
    meta: { 
      requiresAuth: true,
      roles: [1],
      title: 'Categorías',
      icon: 'fa-tags'
    }
  },
  {
    path: '/ventas',
    name: 'Ventas',
    component: VentasView,
    meta: { 
      requiresAuth: true,
      roles: [1, 2],
      title: 'Ventas',
      icon: 'fa-shopping-cart'
    }
  },
  {
    path: '/compras',
    name: 'Compras',
    component: ComprasView,
    meta: { 
      requiresAuth: true,
      roles: [1, 3],
      title: 'Compras',
      icon: 'fa-truck'
    }
  },
  {
    path: '/proveedores',
    name: 'Proveedores',
    component: ProveedoresView,
    meta: { 
      requiresAuth: true,
      roles: [1],
      title: 'Proveedores',
      icon: 'fa-building'
    }
  },
  {
    path: '/usuarios',
    name: 'Usuarios',
    component: UsuariosView,
    meta: { 
      requiresAuth: true,
      roles: [1],
      title: 'Usuarios',
      icon: 'fa-users'
    }
  },
  {
    path: '/reportes',
    name: 'Reportes',
    component: ReportesView,
    meta: { 
      requiresAuth: true,
      roles: [1],
      title: 'Reportes',
      icon: 'fa-chart-bar'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView,
    meta: {
      title: 'Página no encontrada'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth !== false
  const requiredRoles = to.meta.roles

  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  if (to.path === '/login' && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }

  if (requiredRoles && !requiredRoles.includes(authStore.user?.rol_id)) {
    next('/dashboard')
    return
  }

  document.title = `${to.meta.title || 'Revenge POS'} - Revenge POS`
  next()
})

export default router
