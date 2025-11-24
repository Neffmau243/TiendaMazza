<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <!-- Logo -->
        <div class="logo-section">
          <img src="@/assets/images/opg-tw-plazavea.webp" alt="Plaza Vea" class="logo" />
        </div>

        <!-- Title -->
        <div class="title-section">
          <h1>Revenge POS</h1>
          <p>Sistema de Punto de Venta</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="login-form">
          <!-- Email -->
          <div class="input-group">
            <label for="email">Correo Electrónico</label>
            <div class="input-wrapper">
              <i class="fas fa-envelope"></i>
              <input
                id="email"
                v-model="form.values.email"
                type="email"
                placeholder="usuario@revenge.com"
                :disabled="loading"
                @blur="form.touch('email')"
                required
              />
            </div>
            <span v-if="form.touched.email && form.errors.email" class="error-message">
              {{ form.errors.email }}
            </span>
          </div>

          <!-- Password -->
          <div class="input-group">
            <label for="password">Contraseña</label>
            <div class="input-wrapper">
              <i class="fas fa-lock"></i>
              <input
                id="password"
                v-model="form.values.password"
                type="password"
                placeholder="••••••••"
                :disabled="loading"
                @blur="form.touch('password')"
                required
              />
            </div>
            <span v-if="form.touched.password && form.errors.password" class="error-message">
              {{ form.errors.password }}
            </span>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn-submit"
            :disabled="!form.isValid || loading"
          >
            <i v-if="loading" class="fas fa-spinner fa-spin"></i>
            <i v-else class="fas fa-sign-in-alt"></i>
            {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
          </button>
        </form>

        <!-- Footer Info -->
        <div class="footer-info">
          <i class="fas fa-info-circle"></i>
          Usuarios de prueba disponibles en la documentación
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useForm } from '@/composables/useForm'
import { validateEmail, validateRequired } from '@/utils/validators'

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
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  padding: var(--spacing-md);
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: var(--color-white);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-xl);
  padding: var(--spacing-2xl);
}

/* Logo Section */
.logo-section {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.logo {
  width: 100%;
  max-width: 200px;
  height: auto;
}

/* Title Section */
.title-section {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.title-section h1 {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.title-section p {
  font-size: var(--font-size-base);
  color: var(--color-text-light);
  margin: 0;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.input-group label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper i {
  position: absolute;
  left: var(--spacing-md);
  color: var(--color-text-light);
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) 2.75rem;
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius);
  font-size: 16px; /* Prevent zoom on iOS */
  min-height: 48px; /* Touch-friendly */
  font-family: var(--font-family);
  color: var(--color-text);
  background: var(--color-white);
  transition: all var(--transition);
}

.input-wrapper input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.1);
}

.input-wrapper input:disabled {
  background: var(--color-background);
  cursor: not-allowed;
}

.input-wrapper input::placeholder {
  color: var(--color-text-muted);
}

.error-message {
  font-size: var(--font-size-xs);
  color: var(--color-danger);
}

/* Submit Button */
.btn-submit {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-family);
  cursor: pointer;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
}

.btn-submit:hover:not(:disabled) {
  background: #CC0000;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Footer Info */
.footer-info {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-divider);
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
}

.footer-info i {
  color: var(--color-info);
}

/* Responsive */
@media (max-width: 767px) {
  .login-page {
    padding: var(--spacing-sm);
  }

  .login-card {
    padding: var(--spacing-xl);
  }

  .logo {
    max-width: 180px;
  }

  .title-section h1 {
    font-size: var(--font-size-2xl);
  }
}

@media (max-width: 374px) {
  .login-card {
    padding: var(--spacing-lg);
  }

  .logo {
    max-width: 150px;
  }
}
</style>
