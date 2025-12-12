<!-- components/common/BaseModal.vue -->
<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="props.show" class="modal-overlay" @click="handleOverlayClick">
        <div class="modal-container" :class="`modal-${size}`" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">{{ title }}</h3>
            <button class="modal-close" @click="$emit('close')">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <slot />
          </div>
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const handleOverlayClick = () => {
  if (props.closeOnOverlay) {
    emit('close')
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 2rem 1rem;
  overflow-y: auto;
}

.modal-container {
  background: white;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  width: 100%;
  margin: auto;
}

.modal-small {
  max-width: 400px;
}

.modal-medium {
  max-width: 600px;
}

.modal-large {
  max-width: 900px;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  color: var(--color-texto);
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #999;
  cursor: pointer;
  padding: 0.25rem;
  transition: color var(--transition-base);
}

.modal-close:hover {
  color: var(--color-texto);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}

@media (max-width: 767px) {
  .modal-overlay {
    padding: 0;
    align-items: flex-end;
  }

  .modal-container {
    max-height: 95vh;
    border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0;
    max-width: 100% !important;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-title {
    font-size: 1.125rem;
  }

  .modal-body {
    padding: 1rem;
  }

  .modal-footer {
    padding: 1rem;
    flex-direction: column-reverse;
  }

  .modal-footer button {
    width: 100%;
  }

  .modal-enter-from .modal-container,
  .modal-leave-to .modal-container {
    transform: translateY(100%);
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .modal-small {
    max-width: 90%;
  }

  .modal-medium {
    max-width: 90%;
  }

  .modal-large {
    max-width: 90%;
  }
}
</style>
