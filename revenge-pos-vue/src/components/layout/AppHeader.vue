<template>
  <header class="app-header">
    <div class="header-content">
      <!-- Menú Móvil (solo visible en móvil) -->
      <MobileMenu class="mobile-only" />
      
      <h1 class="page-title">{{ pageTitle }}</h1>
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
import MobileMenu from './MobileMenu.vue'

const route = useRoute()
const auth = useAuth()

const pageTitle = computed(() => route.meta.title || 'Revenge POS')
</script>

<style scoped>
.app-header {
  height: var(--header-height);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-divider);
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  box-shadow: var(--shadow-sm);
}

.header-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-xl);
  max-width: var(--container-max-width);
  margin: 0 auto;
}

.page-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.125rem;
}

.user-name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
}

.user-role {
  font-size: var(--font-size-xs);
  color: var(--color-text-light);
  text-transform: capitalize;
}

.user-avatar {
  font-size: 2.5rem;
  color: var(--color-primary);
  line-height: 1;
}

/* Utility: Mobile only */
.mobile-only {
  display: none;
}

/* Mobile */
@media (max-width: 767px) {
  .mobile-only {
    display: flex;
  }

  .header-content {
    padding: 0 var(--spacing-md);
  }

  .page-title {
    font-size: var(--font-size-lg);
    flex: 1;
    text-align: center;
  }

  .user-info {
    display: none;
  }

  .user-avatar {
    font-size: 1.75rem;
  }
}
</style>
