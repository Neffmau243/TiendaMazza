<!-- layouts/AuthLayout.vue -->
<template>
  <div class="auth-layout">
    <slot />
  </div>
</template>

<script setup>
// Layout simple para páginas de autenticación (login)
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-azul) 0%, var(--color-amarillo) 100%);
}
</style>
