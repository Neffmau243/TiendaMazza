<!-- views/LoginView.vue -->
<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Revenge POS</h1>
        <p>Sistema de Punto de Venta</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <BaseInput
          v-model="form.values.email"
          type="email"
          label="Email"
          placeholder="usuario@revenge.com"
          icon="fa-envelope"
          :error="form.touched.email && form.errors.email"
          :disabled="loading"
          @blur="form.touch('email')"
          required
        />

        <BaseInput
          v-model="form.values.password"
          type="password"
          label="Contraseña"
          placeholder="••••••••"
          icon="fa-lock"
          :error="form.touched.password && form.errors.password"
          :disabled="loading"
          @blur="form.touch('password')"
          required
        />

        <BaseButton
          type="submit"
          variant="primary"
          size="large"
          :loading="loading"
          :disabled="!form.isValid"
          block
        >
          Iniciar Sesión
        </BaseButton>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useForm } from '@/composables/useForm'
import { validateEmail, validateRequired } from '@/utils/validators'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const auth = useAuth()
const loading = ref(false)

const form = useForm(
  {
    email: '',
    password: ''
  },
  {
    email: [
      (v) => validateRequired(v, 'El email'),
      (v) => validateEmail(v)
    ],
    password: [
      (v) => validateRequired(v, 'La contraseña')
    ]
  }
)

const handleLogin = async () => {
  if (!form.validateAll()) return

  loading.value = true
  await auth.login(form.values.email, form.values.password)
  loading.value = false
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: var(--shadow-xl);
  width: 100%;
  max-width: 420px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  color: var(--color-azul);
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.login-header p {
  color: #666;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
