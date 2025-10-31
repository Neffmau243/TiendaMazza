<!-- components/layout/AppSidebar.vue -->
<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1 class="sidebar-title">Mazza</h1>
    </div>

    <nav class="sidebar-nav">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        active-class="active"
      >
        <i :class="['fas', item.icon]"></i>
        <span>{{ item.title }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <button @click="auth.logout" class="btn-logout">
        <i class="fas fa-sign-out-alt"></i>
        <span>Cerrar Sesión</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const auth = useAuth()

const menuItems = computed(() => {
  const allRoutes = router.getRoutes()
  
  return allRoutes
    .filter(route => {
      const meta = route.meta
      if (!meta.requiresAuth) return false
      if (!meta.roles) return false
      if (!meta.roles.includes(auth.user.value?.rol_id)) return false
      return route.path !== '/'
    })
    .map(route => ({
      path: route.path,
      title: route.meta.title,
      icon: route.meta.icon
    }))
    .sort((a, b) => {
      const order = ['dashboard', 'punto-venta', 'productos', 'categorias', 
                     'ventas', 'compras', 'proveedores', 'usuarios', 'reportes']
      return order.indexOf(a.path.slice(1)) - order.indexOf(b.path.slice(1))
    })
})
</script>

<style scoped>
.sidebar {
  width: 250px;
  background: var(--color-azul);
  color: white;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  box-shadow: var(--shadow-lg);
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
  color: white;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem 1.5rem;
  color: white;
  text-decoration: none;
  transition: background var(--transition-base);
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
  border-left: 4px solid var(--color-amarillo);
}

.nav-item i {
  width: 20px;
  text-align: center;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-logout {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: background var(--transition-base);
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform var(--transition-base);
  }
  
  .sidebar.open {
    transform: translateX(0);
  }
}
</style>
