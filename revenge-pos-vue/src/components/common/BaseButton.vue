<!-- components/common/BaseButton.vue -->
<template>
  <button
    :type="type"
    :class="['base-button', `btn-${variant}`, `btn-${size}`, { 'btn-loading': loading, 'btn-block': block }]"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <i v-if="icon && !loading" :class="['fas', icon]"></i>
    <i v-if="loading" class="fas fa-spinner fa-spin"></i>
    <span v-if="$slots.default"><slot /></span>
  </button>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'button'
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'danger', 'warning', 'info'].includes(value)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  icon: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  block: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  white-space: nowrap;
}

.base-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.btn-medium {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1.125rem;
}

.btn-block {
  width: 100%;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #CC0000;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 0, 0, 0.3);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #5a6268;
}

.btn-success {
  background: var(--color-success);
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #218838;
}

.btn-danger {
  background: var(--color-danger);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c82333;
}

.btn-warning {
  background: var(--color-warning);
  color: #212529;
}

.btn-warning:hover:not(:disabled) {
  background: #e0a800;
}

.btn-info {
  background: var(--color-info);
  color: white;
}

.btn-info:hover:not(:disabled) {
  background: #138496;
}
</style>
