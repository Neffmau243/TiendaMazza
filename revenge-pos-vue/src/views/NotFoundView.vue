<!-- views/NotFoundView.vue -->
<template>
  <div class="not-found">
    <div class="not-found-content">
      <i class="fas fa-exclamation-triangle"></i>
      <h1>404</h1>
      <h2>Página no encontrada</h2>
      <p>La página que buscas no existe o ha sido movida.</p>
      <BaseButton @click="goHome" variant="primary" icon="fa-home">
        Volver al Inicio
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'

const router = useRouter()

const goHome = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.not-found-content {
  text-align: center;
  color: white;
  padding: 2rem;
}

.not-found-content i {
  font-size: 5rem;
  margin-bottom: 1rem;
  opacity: 0.9;
}

.not-found-content h1 {
  font-size: 6rem;
  margin: 0;
  font-weight: bold;
}

.not-found-content h2 {
  font-size: 2rem;
  margin: 1rem 0;
}

.not-found-content p {
  font-size: 1.125rem;
  margin: 1rem 0 2rem 0;
  opacity: 0.9;
}
</style>
