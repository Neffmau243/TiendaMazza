<template>
  <div class="dashboard">
    <!-- Metrics Grid -->
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

    <!-- Content Grid -->
    <div class="content-grid">
      <!-- Últimas Ventas -->
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Últimas Ventas</h2>
        </div>
        <div class="card-body">
          <LoadingSpinner v-if="loading" />
          <div v-else-if="ultimasVentas.length === 0" class="empty-state">
            <i class="fas fa-receipt"></i>
            <p>No hay ventas registradas hoy</p>
          </div>
          <div v-else class="table-wrapper">
            <table class="table">
              <thead>
                <tr>
                  <th>Boleta</th>
                  <th>Cajero</th>
                  <th>Total</th>
                  <th>Fecha</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="venta in ultimasVentas" :key="venta.id">
                  <td>{{ venta.numero_boleta }}</td>
                  <td>{{ venta.cajero_nombre }}</td>
                  <td class="text-semibold">{{ formatCurrency(venta.total) }}</td>
                  <td>{{ formatDate(venta.fecha, true) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Productos con Stock Bajo -->
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">Stock Bajo</h2>
        </div>
        <div class="card-body">
          <div v-if="productosStore.productosStockBajo.length === 0" class="empty-state">
            <i class="fas fa-check-circle"></i>
            <p>No hay productos con stock bajo</p>
          </div>
          <div v-else class="stock-list">
            <div 
              v-for="producto in productosStore.productosStockBajo" 
              :key="producto.id"
              class="stock-item"
            >
              <span class="stock-name">{{ producto.nombre }}</span>
              <span class="stock-value">
                <span class="stock-current">{{ producto.stock }}</span> 
                / 
                <span class="stock-min">{{ producto.stock_minimo }}</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProductosStore } from '@/stores/productos'
import { useVentasStore } from '@/stores/ventas'
import MetricCard from '@/components/dashboard/MetricCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import { formatCurrency, formatDate } from '@/utils/formatters'

const productosStore = useProductosStore()
const ventasStore = useVentasStore()
const loading = ref(false)

const ultimasVentas = computed(() => ventasStore.ventasDelDia.ventas.slice(0, 5))

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
  width: 100%;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-lg);
}

.stock-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.stock-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: var(--color-background);
  border-radius: var(--border-radius);
  transition: background var(--transition-fast);
}

.stock-item:hover {
  background: var(--color-border);
}

.stock-name {
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
}

.stock-value {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
}

.stock-current {
  color: var(--color-danger);
}

.stock-min {
  color: var(--color-text-muted);
}

/* Responsive */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 767px) {
  .metrics-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
  }

  .content-grid {
    gap: var(--spacing-md);
  }
}
</style>
