<template>
  <div class="app-layout">
    <AppSidebar class="desktop-only" />
    <div class="app-main">
      <AppHeader />
      <main class="app-content">
        <slot />
      </main>
      <AppFooter />
    </div>
  </div>
</template>

<script setup>
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background: var(--color-background);
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0; /* Prevent flex overflow */
  margin-left: var(--sidebar-width);
  transition: margin-left var(--transition-slow);
}

.app-content {
  flex: 1;
  padding: var(--spacing-xl);
  width: 100%;
  max-width: var(--container-max-width);
  margin: 0 auto;
  min-height: calc(100vh - var(--header-height) - 200px); /* Asegurar espacio mínimo */
}

/* Utility: Desktop only */
.desktop-only {
  display: flex;
}

/* Mobile */
@media (max-width: 767px) {
  .desktop-only {
    display: none;
  }

  .app-main {
    margin-left: 0;
  }

  .app-content {
    padding: var(--spacing-md);
  }
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) {
  .app-content {
    padding: var(--spacing-lg);
  }
}
</style>
