<!-- components/dashboard/MetricCard.vue -->
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
  background: white;
  padding: 1.5rem;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: all var(--transition-base);
}

.metric-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
}

.metric-blue .metric-icon {
  background: rgba(0, 72, 160, 0.1);
  color: var(--color-azul);
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
  background: rgba(220, 53, 69, 0.1);
  color: var(--color-danger);
}

.metric-content {
  flex: 1;
}

.metric-title {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  color: #666;
  text-transform: uppercase;
  font-weight: 600;
}

.metric-value {
  margin: 0;
  font-size: 1.75rem;
  font-weight: bold;
  color: var(--color-texto);
}
</style>
