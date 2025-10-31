<!-- components/layout/AppHeader.vue -->
<template>
  <header class="app-header">
    <div class="header-left">
      <button class="menu-toggle" @click="toggleSidebar">
        <i class="fas fa-bars"></i>
      </button>
      <h2 class="page-title">{{ pageTitle }}</h2>
    </div>
    <div class="header-right">
      <div class="user-menu">
        <div class="user-info">
          <span class="user-name">{{ auth.userName }}</span>
          <span class="user-role">{{ auth.roleName }}</span>
        </div>
        <div class="user-avatar">
          <i class="fas fa-user-circle"></i>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const route = useRoute()
const auth = useAuth()

const pageTitle = computed(() => route.meta.title || 'Revenge POS')

const toggleSidebar = () => {
  // Implementar toggle del sidebar si es necesario
}
</script>

<style scoped>
.app-header {
  height: 70px;
  background: white;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--color-texto);
  cursor: pointer;
  padding: 0.5rem;
}

.page-title {
  margin: 0;
  font-size: 1.5rem;
  color: var(--color-texto);
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  font-weight: 600;
  color: var(--color-texto);
  font-size: 0.875rem;
}

.user-role {
  font-size: 0.75rem;
  color: #666;
}

.user-avatar {
  font-size: 2rem;
  color: var(--color-azul);
}

@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }
  
  .user-info {
    display: none;
  }
}
</style>
