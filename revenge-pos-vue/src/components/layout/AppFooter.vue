<!-- components/layout/AppFooter.vue -->
<template>
  <footer class="app-footer">
    <div class="footer-content">
      <p class="footer-text">
        © {{ currentYear }} Revenge POS - Todos los derechos reservados
      </p>
      <p class="footer-version">
        Versión 2.0.0
      </p>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.app-footer {
  background: white;
  border-top: 1px solid #eee;
  padding: 1rem 2rem;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text,
.footer-version {
  margin: 0;
  font-size: 0.875rem;
  color: #666;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
}
</style>
