<!-- views/VentasView.vue -->
<template>
  <div class="ventas">
    <div class="page-header">
      <h1>Historial de Ventas</h1>
    </div>

    <BaseCard>
      <div class="search-bar">
        <BaseInput
          v-model="searchTerm"
          placeholder="Buscar por boleta o cajero..."
          icon="fa-search"
        />
      </div>

      <div class="filters">
        <BaseInput
          v-model="filters.fecha_inicio"
          type="date"
          label="Fecha Inicio"
        />
        <BaseInput
          v-model="filters.fecha_fin"
          type="date"
          label="Fecha Fin"
        />
        <BaseButton
          @click="aplicarFiltros"
          variant="primary"
          icon="fa-search"
        >
          Buscar
        </BaseButton>
      </div>

      <div class="stats">
        <div class="stat-card">
          <span class="stat-label">Total Ventas</span>
          <span class="stat-value">{{ ventasStore.ventas.length }}</span>
        </div>
        <div class="stat-card">
          <span class="stat-label">Monto Total</span>
          <span class="stat-value">{{ formatCurrency(totalVentas) }}</span>
        </div>
      </div>

      <BaseTable
        :columns="columns"
        :data="filteredVentas"
        :loading="ventasStore.loading"
        empty-text="No hay ventas registradas"
      >
        <template #cell-fecha="{ value }">
          {{ formatDate(value, true) }}
        </template>
        <template #cell-total="{ value }">
          {{ formatCurrency(value) }}
        </template>
        <template #actions="{ row }">
          <div class="action-buttons">
            <button 
              @click="verDetalle(row)"
              class="btn-icon btn-view"
              title="Ver Detalle"
            >
              <i class="fas fa-eye"></i>
            </button>
          </div>
        </template>
      </BaseTable>
    </BaseCard>

    <!-- Modal de detalle -->
    <BaseModal
      :show="modal.isOpen.value"
      title="Detalle de Venta"
      @close="modal.close()"
      size="large"
    >
      <div v-if="modal.data.value" class="venta-detalle">
        <div class="detalle-header">
          <div class="detalle-info">
            <p><strong>Boleta:</strong> {{ modal.data.value.numero_boleta }}</p>
            <p><strong>Fecha:</strong> {{ formatDate(modal.data.value.fecha, true) }}</p>
            <p><strong>Cajero:</strong> {{ modal.data.value.cajero_nombre }}</p>
            <p><strong>Método de Pago:</strong> {{ modal.data.value.metodo_pago_nombre }}</p>
          </div>
        </div>

        <h3>Productos</h3>
        <BaseTable
          :columns="detalleColumns"
          :data="modal.data.value.detalles || []"
        >
          <template #cell-precio_unitario="{ value }">
            {{ formatCurrency(value) }}
          </template>
          <template #cell-subtotal="{ row }">
            {{ formatCurrency((row.cantidad * row.precio_unitario) - (row.descuento_unitario || 0)) }}
          </template>
        </BaseTable>

        <div class="detalle-totales">
          <div class="total-row">
            <span>Subtotal:</span>
            <span>{{ formatCurrency(modal.data.value.subtotal) }}</span>
          </div>
          <div class="total-row">
            <span>IVA (18%):</span>
            <span>{{ formatCurrency(modal.data.value.impuestos || (modal.data.value.subtotal - (modal.data.value.descuento || 0)) * 0.18) }}</span>
          </div>
          <div class="total-row total">
            <span>Total:</span>
            <span>{{ formatCurrency(modal.data.value.total) }}</span>
          </div>
        </div>
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useVentasStore } from '@/stores/ventas'
import { useModal } from '@/composables/useModal'
import { formatCurrency, formatDate } from '@/utils/formatters'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseTable from '@/components/common/BaseTable.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseModal from '@/components/common/BaseModal.vue'

const ventasStore = useVentasStore()
const modal = useModal()

const searchTerm = ref('')
const filters = ref({
  fecha_inicio: '',
  fecha_fin: ''
})

const columns = [
  { key: 'numero_boleta', label: 'Boleta' },
  { key: 'fecha', label: 'Fecha' },
  { key: 'cajero_nombre', label: 'Cajero' },
  { key: 'metodo_pago_nombre', label: 'Método Pago' },
  { key: 'total', label: 'Total', align: 'text-right' }
]

const detalleColumns = [
  { key: 'producto_nombre', label: 'Producto' },
  { key: 'cantidad', label: 'Cantidad' },
  { key: 'precio_unitario', label: 'Precio Unit.' },
  { key: 'subtotal', label: 'Subtotal' }
]

const filteredVentas = computed(() => {
  if (!searchTerm.value) return ventasStore.ventas
  
  const term = searchTerm.value.toLowerCase()
  return ventasStore.ventas.filter(v => 
    v.numero_boleta?.toLowerCase().includes(term) ||
    v.cajero_nombre?.toLowerCase().includes(term) ||
    v.metodo_pago_nombre?.toLowerCase().includes(term)
  )
})

const totalVentas = computed(() => {
  return filteredVentas.value.reduce((sum, v) => sum + parseFloat(v.total), 0)
})

const aplicarFiltros = () => {
  ventasStore.fetchVentas(filters.value)
}

const verDetalle = async (venta) => {
  const result = await ventasStore.fetchVentaDetalle(venta.id)
  if (result.success) {
    modal.open(result.data)
  }
}

onMounted(() => {
  ventasStore.fetchVentasHoy()
})
</script>

<style scoped>
.ventas {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0;
  color: var(--color-texto);
}

.search-bar {
  margin-bottom: 1rem;
}

.filters {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  padding: 1.5rem;
  background: linear-gradient(135deg, var(--color-rojo) 0%, #D11820 100%);
  color: white;
  border-radius: var(--border-radius);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: bold;
}

.venta-detalle {
  padding: 0;
}

.venta-detalle h3 {
  font-size: 1.1rem;
  color: var(--color-texto);
  margin: 1.5rem 0 1rem 0;
  font-weight: 600;
}

.detalle-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.detalle-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.detalle-info p {
  margin: 0;
  font-size: 0.95rem;
}

.detalle-info strong {
  color: var(--color-texto);
  font-weight: 600;
}

.detalle-totales {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: var(--border-radius);
}

.total-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  font-size: 1rem;
  color: var(--color-texto);
}

.total-row span:first-child {
  font-weight: 500;
}

.total-row span:last-child {
  font-weight: 600;
}

.total-row.total {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-rojo);
  border-top: 2px solid var(--color-rojo);
  padding-top: 1rem;
  margin-top: 0.5rem;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-view {
  background: #e8f5e9;
  color: #2e7d32;
}

.btn-view:hover {
  background: #2e7d32;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(46, 125, 50, 0.3);
}
</style>
