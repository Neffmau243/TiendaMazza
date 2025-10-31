<!-- views/ComprasView.vue -->
<template>
  <div class="compras">
    <div class="page-header">
      <h1>Gestión de Compras</h1>
      <BaseButton
        @click="openModal('create')"
        variant="primary"
        icon="fa-plus"
      >
        Nueva Compra
      </BaseButton>
    </div>

    <BaseCard>
      <div class="search-bar">
        <BaseInput
          v-model="searchTerm"
          placeholder="Buscar por factura o proveedor..."
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

      <BaseTable
        :columns="columns"
        :data="filteredCompras"
        :loading="loading"
        empty-text="No hay compras registradas"
      >
        <template #cell-fecha="{ value }">
          {{ formatDate(value) }}
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

    <!-- Modal de Detalle -->
    <BaseModal
      :show="modalDetalle"
      title="Detalle de Compra"
      @close="cerrarDetalle"
      size="large"
    >
      <div v-if="detalleCompra" class="detalle-compra">
        <div class="info-grid">
          <div class="info-card">
            <label>Número de Factura</label>
            <span>{{ detalleCompra.numero_factura }}</span>
          </div>
          <div class="info-card">
            <label>Fecha</label>
            <span>{{ formatDate(detalleCompra.fecha) }}</span>
          </div>
          <div class="info-card">
            <label>Proveedor</label>
            <span>{{ detalleCompra.proveedor_nombre }}</span>
          </div>
        </div>

        <div class="productos-detalle">
          <h3>Productos Comprados</h3>
          <div class="productos-list-detalle">
            <div 
              v-for="item in detalleCompra.items" 
              :key="item.id"
              class="producto-detalle-item"
            >
              {{ item.producto_nombre }}
            </div>
          </div>
        </div>

        <div class="resumen-financiero">
          <h3>Resumen</h3>
          <div class="resumen-grid">
            <div class="resumen-item">
              <span class="resumen-label">Subtotal</span>
              <span class="resumen-valor">{{ formatCurrency(detalleCompra.subtotal) }}</span>
            </div>
            <div class="resumen-item">
              <span class="resumen-label">Impuestos (IGV 18%)</span>
              <span class="resumen-valor">{{ formatCurrency(detalleCompra.impuestos) }}</span>
            </div>
            <div class="resumen-item resumen-total">
              <span class="resumen-label">Total</span>
              <span class="resumen-valor">{{ formatCurrency(detalleCompra.total) }}</span>
            </div>
          </div>
        </div>

        <div v-if="detalleCompra.observaciones" class="observaciones">
          <label>Observaciones</label>
          <p>{{ detalleCompra.observaciones }}</p>
        </div>
      </div>
      
      <template #footer>
        <BaseButton @click="cerrarDetalle" variant="secondary">
          Cerrar
        </BaseButton>
      </template>
    </BaseModal>

    <!-- Modal de Nueva Compra -->
    <BaseModal
      :show="modal.isOpen.value"
      title="Nueva Compra"
      @close="closeModal"
      size="large"
    >
      <div class="compra-form">
        <div class="form-row">
          <div class="form-group">
            <label>Proveedor</label>
            <select v-model="form.values.proveedor_id" class="form-select">
              <option value="">Seleccionar...</option>
              <option 
                v-for="proveedor in proveedores" 
                :key="proveedor.id" 
                :value="proveedor.id"
              >
                {{ proveedor.nombre }}
              </option>
            </select>
          </div>
          <BaseInput
            v-model="form.values.numero_factura"
            label="Número de Factura"
            required
          />
        </div>

        <h3>Productos</h3>
        <div class="productos-section">
          <div class="producto-search">
            <BaseInput
              v-model="productoSearch"
              placeholder="Buscar producto..."
              icon="fa-search"
            />
          </div>
          
          <div class="productos-list">
            <div 
              v-for="item in form.values.items" 
              :key="item.producto_id"
              class="producto-item"
            >
              <span>{{ item.nombre }}</span>
              <BaseInput
                v-model="item.cantidad"
                type="number"
                placeholder="Cantidad"
                min="1"
              />
              <BaseInput
                v-model="item.precio_compra"
                type="number"
                step="0.01"
                placeholder="Precio"
                min="0"
              />
              <button @click="removeProducto(item.producto_id)" class="btn-remove">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>

          <div class="total-compra">
            <strong>Total: {{ formatCurrency(totalCompra) }}</strong>
          </div>
        </div>
      </div>
      
      <template #footer>
        <BaseButton @click="closeModal" variant="secondary">
          Cancelar
        </BaseButton>
        <BaseButton
          @click="saveCompra"
          variant="primary"
          :loading="saving"
        >
          Registrar Compra
        </BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProveedoresStore } from '@/stores/proveedores'
import { useAuthStore } from '@/stores/auth'
import { comprasService } from '@/services/comprasService'
import { useModal } from '@/composables/useModal'
import { useForm } from '@/composables/useForm'
import { useToast } from '@/composables/useToast'
import { formatCurrency, formatDate } from '@/utils/formatters'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseTable from '@/components/common/BaseTable.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseModal from '@/components/common/BaseModal.vue'

const proveedoresStore = useProveedoresStore()
const authStore = useAuthStore()
const modal = useModal()
const toast = useToast()

const compras = ref([])
const proveedores = ref([])
const loading = ref(false)
const saving = ref(false)
const productoSearch = ref('')
const searchTerm = ref('')

const filters = ref({
  fecha_inicio: '',
  fecha_fin: ''
})

const columns = [
  { key: 'numero_factura', label: 'Factura' },
  { key: 'fecha', label: 'Fecha' },
  { key: 'proveedor_nombre', label: 'Proveedor' },
  { key: 'total', label: 'Total', align: 'text-right' }
]

const form = useForm({
  proveedor_id: '',
  numero_factura: '',
  items: []
})

const filteredCompras = computed(() => {
  if (!searchTerm.value) return compras.value
  
  const term = searchTerm.value.toLowerCase()
  return compras.value.filter(c => 
    c.numero_factura?.toLowerCase().includes(term) ||
    c.proveedor_nombre?.toLowerCase().includes(term)
  )
})

const totalCompra = computed(() => {
  return form.values.items.reduce((sum, item) => {
    return sum + (parseFloat(item.cantidad) * parseFloat(item.precio_compra || 0))
  }, 0)
})

const openModal = () => {
  form.reset()
  form.values.items = []
  modal.open()
}

const closeModal = () => {
  modal.close()
  form.reset()
}

const loadCompras = async () => {
  loading.value = true
  try {
    const filtros = {
      fechaInicio: filters.value.fecha_inicio || null,
      fechaFin: filters.value.fecha_fin || null
    }
    const response = await comprasService.getAll(filtros)
    if (response.success) {
      compras.value = response.data
    } else {
      toast.error(response.message || 'Error al cargar compras')
    }
  } catch (error) {
    toast.error('Error al cargar compras')
  } finally {
    loading.value = false
  }
}

const aplicarFiltros = () => {
  loadCompras()
}

const detalleCompra = ref(null)
const modalDetalle = ref(false)

const verDetalle = async (compra) => {
  try {
    const response = await comprasService.getById(compra.id)
    if (response.success) {
      detalleCompra.value = response.data
      modalDetalle.value = true
    } else {
      toast.error(response.message || 'Error al cargar detalle')
    }
  } catch (error) {
    toast.error('Error al cargar detalle de compra')
  }
}

const cerrarDetalle = () => {
  modalDetalle.value = false
  detalleCompra.value = null
}

const removeProducto = (productoId) => {
  form.values.items = form.values.items.filter(item => item.producto_id !== productoId)
}

const saveCompra = async () => {
  if (!form.values.proveedor_id) {
    toast.error('Seleccione un proveedor')
    return
  }

  if (form.values.items.length === 0) {
    toast.error('Agregue al menos un producto')
    return
  }

  saving.value = true
  
  const compraData = {
    ...form.values,
    usuario_id: authStore.user?.id  // Agregar el ID del usuario actual
  }
  
  const result = await comprasService.create(compraData)
  
  if (result.success) {
    toast.success('Compra registrada exitosamente')
    await loadCompras()
    closeModal()
  } else {
    toast.error(result.message || 'Error al registrar la compra')
  }
  
  saving.value = false
}

onMounted(async () => {
  await proveedoresStore.fetchProveedores()
  proveedores.value = proveedoresStore.proveedores
  await loadCompras()
})
</script>

<style scoped>
.compras {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.compra-form {
  padding: 1rem 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: var(--border-radius);
  font-size: 1rem;
}

.productos-section {
  border: 1px solid #eee;
  border-radius: var(--border-radius);
  padding: 1rem;
  margin-top: 1rem;
}

.productos-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 1rem 0;
}

.producto-item {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: 0.75rem;
  align-items: center;
  padding: 0.75rem;
  background: #f9f9f9;
  border-radius: var(--border-radius);
}

.btn-remove {
  padding: 0.5rem;
  background: var(--color-danger);
  color: white;
  border: none;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
}

.total-compra {
  text-align: right;
  padding-top: 1rem;
  border-top: 2px solid #eee;
  font-size: 1.25rem;
}

.detalle-compra {
  padding: 0.5rem 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.info-card {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: var(--border-radius);
  border-left: 3px solid var(--color-primary);
}

.info-card label {
  display: block;
  font-size: 0.85rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.info-card span {
  display: block;
  font-size: 1rem;
  color: var(--color-texto);
  font-weight: 600;
}

.productos-detalle {
  margin-bottom: 2rem;
}

.productos-detalle h3 {
  margin: 0 0 1rem 0;
  color: var(--color-texto);
  font-size: 1.1rem;
}

.productos-list-detalle {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.producto-detalle-item {
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-radius: var(--border-radius);
  border-left: 3px solid #28a745;
}

.resumen-financiero {
  margin-bottom: 2rem;
}

.resumen-financiero h3 {
  margin: 0 0 1rem 0;
  color: var(--color-texto);
  font-size: 1.1rem;
}

.resumen-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: var(--border-radius);
}

.resumen-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.resumen-label {
  color: #6c757d;
  font-weight: 500;
}

.resumen-valor {
  color: var(--color-texto);
  font-weight: 600;
  font-size: 1.1rem;
}

.resumen-total {
  border-top: 2px solid #dee2e6;
  padding-top: 1rem;
  margin-top: 0.5rem;
}

.resumen-total .resumen-label {
  color: var(--color-texto);
  font-size: 1.1rem;
  font-weight: 600;
}

.resumen-total .resumen-valor {
  color: var(--color-primary);
  font-size: 1.3rem;
}

.observaciones {
  padding: 1rem;
  background: #fff3cd;
  border-radius: var(--border-radius);
  border-left: 4px solid #ffc107;
}

.observaciones label {
  display: block;
  font-weight: 600;
  color: #856404;
  margin-bottom: 0.5rem;
}

.observaciones p {
  margin: 0;
  color: #856404;
  line-height: 1.5;
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
