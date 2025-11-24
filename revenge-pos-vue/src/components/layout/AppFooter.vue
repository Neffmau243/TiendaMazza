<!-- components/layout/AppFooter.vue -->
<template>
  <footer class="app-footer">
    <div class="footer-content">
      <!-- Enlaces rápidos -->
      <div class="footer-section">
        <h4 class="footer-title">Enlaces Rápidos</h4>
        <div class="footer-links">
          <router-link to="/dashboard">
            <i class="fas fa-home"></i>
            Dashboard
          </router-link>
          <router-link to="/punto-venta">
            <i class="fas fa-cash-register"></i>
            Punto de Venta
          </router-link>
          <router-link to="/productos">
            <i class="fas fa-box"></i>
            Productos
          </router-link>
          <router-link to="/reportes" v-if="isAdmin">
            <i class="fas fa-chart-bar"></i>
            Reportes
          </router-link>
        </div>
      </div>

      <!-- Soporte -->
      <div class="footer-section">
        <h4 class="footer-title">Soporte</h4>
        <div class="footer-links">
          <a href="#" @click.prevent>
            <i class="fas fa-question-circle"></i>
            Centro de Ayuda
          </a>
          <a href="#" @click.prevent>
            <i class="fas fa-book"></i>
            Documentación
          </a>
          <a href="#" @click.prevent>
            <i class="fas fa-headset"></i>
            Contactar Soporte
          </a>
          <a href="#" @click.prevent>
            <i class="fas fa-bug"></i>
            Reportar Error
          </a>
        </div>
      </div>

      <!-- Contacto -->
      <div class="footer-section">
        <h4 class="footer-title">Contacto</h4>
        <div class="footer-contact">
          <a href="mailto:soporte@plazavea.com">
            <i class="fas fa-envelope"></i>
            soporte@plazavea.com
          </a>
          <a href="tel:+5116115000">
            <i class="fas fa-phone"></i>
            (01) 611-5000
          </a>
          <a href="#" @click.prevent>
            <i class="fas fa-map-marker-alt"></i>
            Lima, Perú
          </a>
        </div>
        <!-- Redes sociales -->
        <div class="footer-social">
          <a href="#" class="social-link" aria-label="Facebook">
            <i class="fab fa-facebook-f"></i>
          </a>
          <a href="#" class="social-link" aria-label="Twitter">
            <i class="fab fa-twitter"></i>
          </a>
          <a href="#" class="social-link" aria-label="Instagram">
            <i class="fab fa-instagram"></i>
          </a>
          <a href="#" class="social-link" aria-label="LinkedIn">
            <i class="fab fa-linkedin-in"></i>
          </a>
        </div>
      </div>
    </div>

    <!-- Barra inferior -->
    <div class="footer-bottom">
      <p class="copyright">
        © {{ currentYear }} Plaza Vea - Revenge POS. Todos los derechos reservados.
      </p>
      <div class="footer-meta">
        <span class="version">
          <i class="fas fa-code-branch"></i>
          v2.0.0
        </span>
        <span class="separator">•</span>
        <span class="status">
          <i class="fas fa-circle status-icon"></i>
          Sistema Operativo
        </span>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useAuth } from '@/composables/useAuth'

const auth = useAuth()
const currentYear = computed(() => new Date().getFullYear())
const isAdmin = computed(() => auth.user.value?.rol_id === 1)
</script>

<style scoped>
/* ============================================
   FOOTER PRINCIPAL
   ============================================ */
.app-footer {
  background: var(--color-white);
  border-top: 2px solid var(--color-primary);
  margin-top: auto;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.footer-content {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-xl) var(--spacing-lg);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-xl);
}

/* ============================================
   SECCIONES
   ============================================ */
.footer-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.footer-title {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  margin: 0 0 var(--spacing-sm) 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ============================================
   ENLACES
   ============================================ */
.footer-links {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.footer-links a {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-light);
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: all var(--transition);
  padding: 0.25rem 0;
  width: fit-content;
}

.footer-links a:hover {
  color: var(--color-primary);
  transform: translateX(3px);
}

.footer-links a i {
  width: 14px;
  text-align: center;
  font-size: 0.875rem;
  color: var(--color-primary);
}

/* ============================================
   CONTACTO
   ============================================ */
.footer-contact {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-contact a {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-light);
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: all var(--transition);
  width: fit-content;
}

.footer-contact a:hover {
  color: var(--color-primary);
}

.footer-contact a i {
  width: 16px;
  text-align: center;
  color: var(--color-primary);
}

/* ============================================
   REDES SOCIALES
   ============================================ */
.footer-social {
  display: flex;
  gap: 0.5rem;
  margin-top: var(--spacing-sm);
}

.social-link {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background);
  border-radius: var(--border-radius);
  color: var(--color-text-light);
  text-decoration: none;
  transition: all var(--transition);
  font-size: 0.875rem;
}

.social-link:hover {
  background: var(--color-primary);
  color: var(--color-white);
  transform: translateY(-2px);
}

/* ============================================
   BARRA INFERIOR
   ============================================ */
.footer-bottom {
  border-top: 1px solid var(--color-divider);
  background: var(--color-background);
  padding: var(--spacing-md) var(--spacing-xl);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.copyright {
  margin: 0;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.footer-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.version {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.separator {
  opacity: 0.5;
}

.status {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.status-icon {
  font-size: 6px;
  color: var(--color-success);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* ============================================
   RESPONSIVE
   ============================================ */

/* Tablet */
@media (max-width: 1023px) {
  .footer-content {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-lg);
  }

  .footer-section:last-child {
    grid-column: 1 / -1;
  }
}

/* Mobile */
@media (max-width: 767px) {
  .footer-content {
    grid-template-columns: 1fr;
    padding: var(--spacing-lg) var(--spacing-md);
    gap: var(--spacing-lg);
  }

  .footer-section {
    text-align: center;
  }

  .footer-links,
  .footer-contact {
    align-items: center;
  }

  .footer-links a,
  .footer-contact a {
    justify-content: center;
  }

  .footer-social {
    justify-content: center;
  }

  .footer-bottom {
    flex-direction: column;
    gap: var(--spacing-sm);
    text-align: center;
    padding: var(--spacing-md);
  }

  .footer-meta {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
