<!-- views/DashboardView.vue -->
<template>
  <div class="dashboard">
    <div class="metrics-grid">
      <MetricCard
        title="Ventas del Día"
        :value="ventasStore.ventasDelDia.cantidad"
        icon="fa-shopping-cart"
        color="blue"
        :loading="loading"
      />
      
      <MetricCard
        title="Total Vendido"
        :value="formatCurrency(ventasStore.ventasDelDia.total)"
        icon="fa-dollar-sign"
        color="green"
        :loading="loading"
      />
      
      <MetricCard
        title="Stock Bajo"
        :value="productosStore.productosStockBajo.length"
        icon="fa-exclamation-triangle"
        color="orange"
        :loading="loading"
      />
      
      <MetricCard
        title="Total Productos"
        :value="productosStore.totalProductos"
        icon="fa-box"
        color="purple"
        :loading="loading"
      />
    </div>

    <div class="dashboard-content">
      <BaseCard title="Últimas Ventas">
        <LoadingSpinner v-if="loading" />
        <div v-else-if="ultimasVentas.length === 0" class="empty-state">
          No hay ventas registradas hoy
        </div>
        <BaseTable
          v-else
          :columns="ventasColumns"
          :data="ultimasVentas"
        >
          <template #cell-total="{ value }">
            {{ formatCurrency(value) }}
          </template>
          <template #cell-fecha="{ value }">
            {{ formatDate(value, true) }}
          </template>
        </BaseTable>
      </BaseCard>

      <BaseCard title="Productos con Stock Bajo">
        <div v-if="productosStore.productosStockBajo.length === 0" class="empty-state">
          ✓ No hay productos con stock bajo
        </div>
        <div v-else class="stock-list">
          <div 
            v-for="producto in productosStore.productosStockBajo" 
            :key="producto.id"
            class="stock-item"
          >
            <span class="producto-nombre">{{ producto.nombre }}</span>
            <span class="producto-stock">
              {{ producto.stock }} / {{ producto.stock_minimo }}
            </span>
          </div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProductosStore } from '@/stores/productos'
import { useVentasStore } from '@/stores/ventas'
import MetricCard from '@/components/dashboard/MetricCard.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseTable from '@/components/common/BaseTable.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import { formatCurrency, formatDate } from '@/utils/formatters'

const productosStore = useProductosStore()
const ventasStore = useVentasStore()
const loading = ref(false)

const ultimasVentas = computed(() => ventasStore.ventasDelDia.ventas.slice(0, 5))

const ventasColumns = [
  { key: 'numero_boleta', label: 'Boleta' },
  { key: 'fecha', label: 'Fecha' },
  { key: 'cajero_nombre', label: 'Cajero' },
  { key: 'total', label: 'Total', align: 'text-right' }
]

onMounted(async () => {
  loading.value = true
  await Promise.all([
    productosStore.fetchProductos(),
    ventasStore.fetchVentasHoy()
  ])
  loading.value = false
})
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #999;
}

.stock-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.stock-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem;
  background: #f9f9f9;
  border-radius: var(--border-radius);
}

.producto-nombre {
  font-weight: 500;
}

.producto-stock {
  color: var(--color-danger);
  font-weight: 600;
  font-size: 0.875rem;
}

@media (max-width: 1024px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
}
</style>
