<template>
  <div class="metric-card" :class="`metric-${color}`">
    <div class="metric-icon">
      <i :class="['fas', icon]"></i>
    </div>
    <div class="metric-content">
      <p class="metric-title">{{ title }}</p>
      <p class="metric-value">
        <LoadingSpinner v-if="loading" size="small" />
        <span v-else>{{ value }}</span>
      </p>
    </div>
  </div>
</template>

<script setup>
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  icon: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: 'blue',
    validator: (value) => ['blue', 'green', 'orange', 'purple', 'red'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.metric-card {
  background: var(--color-surface);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  transition: all var(--transition);
  min-width: 0;
}

.metric-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.metric-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--border-radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  flex-shrink: 0;
}

.metric-blue .metric-icon {
  background: rgba(237, 28, 36, 0.1);
  color: var(--color-primary);
}

.metric-green .metric-icon {
  background: rgba(40, 167, 69, 0.1);
  color: var(--color-success);
}

.metric-orange .metric-icon {
  background: rgba(255, 193, 7, 0.1);
  color: var(--color-warning);
}

.metric-purple .metric-icon {
  background: rgba(111, 66, 193, 0.1);
  color: #6f42c1;
}

.metric-red .metric-icon {
  background: rgba(255, 0, 0, 0.1);
  color: var(--color-danger);
}

.metric-content {
  flex: 1;
  min-width: 0;
}

.metric-title {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-light);
  text-transform: uppercase;
  font-weight: var(--font-weight-semibold);
  letter-spacing: 0.5px;
  line-height: var(--line-height-tight);
}

.metric-value {
  margin: 0;
  font-size: 1.875rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  line-height: var(--line-height-tight);
}

/* Responsive */
@media (max-width: 1200px) {
  .metric-card {
    padding: var(--spacing-md);
    gap: var(--spacing-md);
  }

  .metric-icon {
    width: 56px;
    height: 56px;
    font-size: 1.5rem;
  }

  .metric-value {
    font-size: 1.5rem;
  }
}

@media (max-width: 767px) {
  .metric-card {
    padding: var(--spacing-md);
  }

  .metric-title {
    font-size: var(--font-size-xs);
  }

  .metric-value {
    font-size: 1.375rem;
  }
}
</style>
