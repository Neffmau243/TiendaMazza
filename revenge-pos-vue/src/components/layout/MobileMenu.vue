<template>
  <div class="mobile-menu">
    <!-- Botón Hamburguesa -->
    <button 
      class="hamburger-btn" 
      @click="toggleMenu"
      :class="{ 'active': isOpen }"
      aria-label="Toggle menu"
    >
      <span></span>
      <span></span>
      <span></span>
    </button>

    <!-- Overlay -->
    <transition name="fade">
      <div 
        v-if="isOpen" 
        class="menu-overlay" 
        @click="closeMenu"
      ></div>
    </transition>

    <!-- Sidebar Móvil -->
    <transition name="slide">
      <aside v-if="isOpen" class="mobile-sidebar">
        <div class="sidebar-header">
          <img src="@/assets/images/opg-tw-plazavea.webp" alt="Plaza Vea Logo" class="sidebar-logo" />
          <button class="close-btn" @click="closeMenu" aria-label="Close menu">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <nav class="sidebar-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            active-class="active"
            @click="closeMenu"
          >
            <i :class="['fas', item.icon]"></i>
            <span>{{ item.title }}</span>
          </router-link>
        </nav>

        <div class="sidebar-footer">
          <div class="user-info">
            <i class="fas fa-user-circle"></i>
            <div>
              <div class="user-name">{{ user?.nombre }}</div>
              <div class="user-role">{{ getRoleName(user?.rol_id) }}</div>
            </div>
          </div>
          <button @click="handleLogout" class="btn-logout">
            <i class="fas fa-sign-out-alt"></i>
            <span>Cerrar Sesión</span>
          </button>
        </div>
      </aside>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const auth = useAuth()
const isOpen = ref(false)

const user = computed(() => auth.user.value)

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

const getRoleName = (rolId) => {
  const roles = {
    1: 'Administrador',
    2: 'Cajero',
    3: 'Almacenista'
  }
  return roles[rolId] || 'Usuario'
}

const toggleMenu = () => {
  isOpen.value = !isOpen.value
  // Prevenir scroll del body cuando el menú está abierto
  if (isOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeMenu = () => {
  isOpen.value = false
  document.body.style.overflow = ''
}

const handleLogout = () => {
  closeMenu()
  auth.logout()
}
</script>

<style scoped>
/* ============================================
   BOTÓN HAMBURGUESA
   ============================================ */
.hamburger-btn {
  display: none; /* Oculto por defecto, visible solo en móvil */
  flex-direction: column;
  justify-content: space-around;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: calc(var(--z-fixed) + 1);
  position: relative;
}

.hamburger-btn span {
  width: 100%;
  height: 3px;
  background: var(--color-primary);
  border-radius: 2px;
  transition: all var(--transition);
  transform-origin: center;
}

.hamburger-btn.active span:nth-child(1) {
  transform: translateY(9px) rotate(45deg);
}

.hamburger-btn.active span:nth-child(2) {
  opacity: 0;
  transform: translateX(-20px);
}

.hamburger-btn.active span:nth-child(3) {
  transform: translateY(-9px) rotate(-45deg);
}

/* ============================================
   OVERLAY
   ============================================ */
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: var(--z-modal-backdrop);
  backdrop-filter: blur(2px);
}

/* ============================================
   SIDEBAR MÓVIL
   ============================================ */
.mobile-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 280px;
  max-width: 85vw;
  background: var(--color-primary);
  color: var(--color-white);
  display: flex;
  flex-direction: column;
  z-index: var(--z-modal);
  box-shadow: var(--shadow-xl);
  overflow-y: auto;
}

.sidebar-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--color-primary);
  position: sticky;
  top: 0;
  z-index: 1;
}

.sidebar-logo {
  width: 140px;
  height: auto;
  object-fit: contain;
}

.close-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: var(--border-radius);
  color: var(--color-white);
  cursor: pointer;
  font-size: 1.25rem;
  transition: all var(--transition);
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
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
  padding: 1rem var(--spacing-lg);
  color: var(--color-white);
  text-decoration: none;
  transition: all var(--transition);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  border-left: 4px solid transparent;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  border-left-color: var(--color-secondary);
  font-weight: var(--font-weight-semibold);
}

.nav-item i {
  width: 24px;
  text-align: center;
  font-size: 1.25rem;
}

.sidebar-footer {
  padding: var(--spacing-md);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: var(--color-primary);
  position: sticky;
  bottom: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius);
  margin-bottom: var(--spacing-md);
}

.user-info i {
  font-size: 2rem;
  color: var(--color-secondary);
}

.user-name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  color: var(--color-white);
}

.user-role {
  font-size: var(--font-size-xs);
  color: rgba(255, 255, 255, 0.7);
}

.btn-logout {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: 0.875rem;
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

/* ============================================
   ANIMACIONES
   ============================================ */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform var(--transition-slow);
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

/* ============================================
   RESPONSIVE
   ============================================ */
@media (max-width: 767px) {
  .hamburger-btn {
    display: flex;
  }
}

@media (min-width: 768px) {
  .mobile-menu {
    display: none;
  }
}
</style>
