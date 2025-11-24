<!-- components/common/BaseTable.vue -->
<template>
  <div class="base-table">
    <table class="table">
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key" :class="column.align">
            {{ column.label }}
          </th>
          <th v-if="$slots.actions">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="columns.length + ($slots.actions ? 1 : 0)" class="text-center">
            <LoadingSpinner size="small" />
          </td>
        </tr>
        <tr v-else-if="data.length === 0">
          <td :colspan="columns.length + ($slots.actions ? 1 : 0)" class="text-center empty">
            {{ emptyText }}
          </td>
        </tr>
        <tr v-else v-for="(row, index) in data" :key="index" @click="$emit('row-click', row)">
          <td v-for="column in columns" :key="column.key" :class="column.align">
            <slot :name="`cell-${column.key}`" :row="row" :value="row[column.key]">
              {{ row[column.key] }}
            </slot>
          </td>
          <td v-if="$slots.actions" class="actions-cell">
            <slot name="actions" :row="row" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import LoadingSpinner from './LoadingSpinner.vue'

defineProps({
  columns: {
    type: Array,
    required: true
  },
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  emptyText: {
    type: String,
    default: 'No hay datos disponibles'
  }
})

defineEmits(['row-click'])
</script>

<style scoped>
.base-table {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  min-width: 600px;
}

.table th,
.table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.table th {
  background: #f5f5f5;
  font-weight: 600;
  color: #666;
  font-size: 0.875rem;
  text-transform: uppercase;
  white-space: nowrap;
}

.table tbody tr {
  transition: background var(--transition-base);
}

.table tbody tr:hover {
  background: #f9f9f9;
  cursor: pointer;
}

.text-center {
  text-align: center !important;
}

.text-right {
  text-align: right !important;
}

.empty {
  padding: 3rem 1rem;
  color: #999;
}

.actions-cell {
  white-space: nowrap;
}

@media (max-width: 767px) {
  .table th,
  .table td {
    padding: 0.5rem;
    font-size: 0.875rem;
  }

  .table th {
    font-size: 0.75rem;
  }

  .actions-cell {
    position: sticky;
    right: 0;
    background: white;
    box-shadow: -2px 0 4px rgba(0, 0, 0, 0.05);
  }

  .table tbody tr:hover .actions-cell {
    background: #f9f9f9;
  }
}
</style>
