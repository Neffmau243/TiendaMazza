<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <img src="@/assets/images/opg-tw-plazavea.webp" alt="Plaza Vea Logo" class="sidebar-logo" />
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
      <button @click="handleLogout" class="btn-logout">
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

const handleLogout = () => {
  auth.logout()
}
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  background: var(--color-primary);
  color: var(--color-white);
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  z-index: var(--z-fixed);
  box-shadow: var(--shadow-lg);
}

.sidebar-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
}

.sidebar-logo {
  width: 100%;
  max-width: 180px;
  height: auto;
  object-fit: contain;
}

.sidebar-nav {
  flex: 1;
  padding: var(--spacing-md) 0;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: 0.875rem var(--spacing-lg);
  color: var(--color-white);
  text-decoration: none;
  transition: all var(--transition);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  border-left: 4px solid var(--color-secondary);
  font-weight: var(--font-weight-semibold);
}

.nav-item i {
  width: 20px;
  text-align: center;
  font-size: 1.125rem;
}

.sidebar-footer {
  padding: var(--spacing-md);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-logout {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-white);
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition);
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Mobile */
@media (max-width: 767px) {
  .sidebar {
    display: none; /* Simplificado para mobile - mostraremos un header con menú */
  }
}
</style>
