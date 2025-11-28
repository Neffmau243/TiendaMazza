<!-- views/ProductosView.vue -->
<template>
  <div class="productos">
    <div class="page-header">
      <h1>{{ canEdit ? 'Gestión de Productos' : 'Consulta de Productos' }}</h1>
      <BaseButton
        v-if="canEdit"
        @click="openModal('create')"
        variant="primary"
        icon="fa-plus"
      >
        Nuevo Producto
      </BaseButton>
    </div>

    <BaseCard>
      <div class="filters">
        <BaseInput
          v-model="searchTerm"
          placeholder="Buscar productos..."
          icon="fa-search"
        />
      </div>

      <BaseTable
        :columns="columns"
        :data="filteredProductos"
        :loading="productosStore.loading"
        empty-text="No hay productos registrados"
      >
        <template #cell-precio_venta="{ value }">
          {{ formatCurrency(value) }}
        </template>
        <template #cell-stock="{ value, row }">
          <span :class="{ 'stock-bajo': value < row.stock_minimo }">
            {{ value }}
          </span>
        </template>
        <template #cell-estado_nombre="{ value }">
          <span :class="['badge', value?.toLowerCase().trim() === 'activo' ? 'badge-success' : 'badge-danger']">
            {{ value }}
          </span>
        </template>
        <template #actions="{ row }">
          <div class="action-buttons" v-if="canEdit">
            <button 
              @click="openModal('edit', row)"
              class="btn-icon btn-edit"
              title="Editar"
            >
              <i class="fas fa-edit"></i>
            </button>
            <button 
              @click="deleteProducto(row.id)"
              class="btn-icon btn-delete"
              title="Eliminar"
            >
              <i class="fas fa-trash"></i>
            </button>
          </div>
          <span v-else class="text-muted">Solo lectura</span>
        </template>
      </BaseTable>
    </BaseCard>

    <!-- Modal para crear/editar producto -->
    <BaseModal
      :show="modal.isOpen.value"
      :title="modal.data.value ? 'Editar Producto' : 'Nuevo Producto'"
      @close="closeModal"
    >
      <form @submit.prevent="saveProducto">
        <div class="form-row">
          <BaseInput
            v-model="form.values.codigo_barras"
            label="Código de Barras"
            :error="form.errors.codigo_barras"
            required
          />
          <BarcodeScanner @code-scanned="onCodeScanned" />
        </div>
        <BaseInput
          v-model="form.values.nombre"
          label="Nombre"
          :error="form.errors.nombre"
          required
        />
        <BaseInput
          v-model="form.values.descripcion"
          label="Descripción"
        />
        <div class="form-group">
          <label>Categoría</label>
          <select v-model="form.values.categoria_id" class="form-select">
            <option value="">Seleccionar...</option>
            <option 
              v-for="categoria in categorias" 
              :key="categoria.id" 
              :value="categoria.id"
            >
              {{ categoria.nombre }}
            </option>
          </select>
        </div>
        <BaseInput
          v-model="form.values.precio_compra"
          type="number"
          step="0.01"
          label="Precio de Compra"
          :error="form.errors.precio_compra"
          required
        />
        <BaseInput
          v-model="form.values.precio_venta"
          type="number"
          step="0.01"
          label="Precio de Venta"
          :error="form.errors.precio_venta"
          required
        />
        <BaseInput
          v-model="form.values.stock"
          type="number"
          label="Stock Actual"
          :error="form.errors.stock"
          required
        />
        <BaseInput
          v-model="form.values.stock_minimo"
          type="number"
          label="Stock Mínimo"
          :error="form.errors.stock_minimo"
          required
        />
      </form>
      
      <template #footer>
        <BaseButton @click="closeModal" variant="secondary">
          Cancelar
        </BaseButton>
        <BaseButton
          @click="saveProducto"
          variant="primary"
          :loading="saving"
        >
          {{ modal.data.value ? 'Actualizar' : 'Crear' }}
        </BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProductosStore } from '@/stores/productos'
import { useCategoriasStore } from '@/stores/categorias'
import { useAuthStore } from '@/stores/auth'
import { useModal } from '@/composables/useModal'
import { useForm } from '@/composables/useForm'
import { useToast } from '@/composables/useToast'
import { validateRequired, validatePositiveNumber } from '@/utils/validators'
import { formatCurrency } from '@/utils/formatters'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseTable from '@/components/common/BaseTable.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import BarcodeScanner from '@/components/ventas/BarcodeScanner.vue'

const productosStore = useProductosStore()
const categoriasStore = useCategoriasStore()
const authStore = useAuthStore()
const modal = useModal()
const toast = useToast()

const searchTerm = ref('')
const saving = ref(false)
const categorias = ref([])

// Función para manejar código escaneado
const onCodeScanned = (code) => {
  form.values.codigo_barras = code
  toast.success(`Código escaneado: ${code}`)
}

// Verificar si el usuario puede editar (Admin o Almacenero)
const canEdit = computed(() => {
  const rolId = authStore.user?.rol_id
  return rolId === 1 || rolId === 3 // 1: Admin, 3: Almacenero
})

const columns = [
  { key: 'codigo_barras', label: 'Código' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'categoria_nombre', label: 'Categoría' },
  { key: 'precio_venta', label: 'Precio' },
  { key: 'stock', label: 'Stock' },
  { key: 'estado_nombre', label: 'Estado' }
]

const form = useForm(
  {
    codigo_barras: '',
    nombre: '',
    descripcion: '',
    categoria_id: 1,
    precio_compra: '',
    precio_venta: '',
    stock: '',
    stock_minimo: ''
  },
  {
    codigo_barras: [(v) => validateRequired(v, 'El código de barras')],
    nombre: [(v) => validateRequired(v, 'El nombre')],
    precio_compra: [(v) => validatePositiveNumber(v, 'El precio de compra')],
    precio_venta: [(v) => validatePositiveNumber(v, 'El precio de venta')],
    stock: [(v) => validatePositiveNumber(v, 'El stock actual')],
    stock_minimo: [(v) => validatePositiveNumber(v, 'El stock mínimo')]
  }
)

const filteredProductos = computed(() => {
  if (!searchTerm.value) return productosStore.productos
  
  const term = searchTerm.value.toLowerCase()
  return productosStore.productos.filter(p => 
    p.nombre.toLowerCase().includes(term) ||
    p.codigo_barras.toLowerCase().includes(term)
  )
})

const openModal = (mode, data = null) => {
  if (data) {
    form.setValues(data)
  } else {
    form.reset()
  }
  modal.open(data)
}

const closeModal = () => {
  modal.close()
  form.reset()
}

const saveProducto = async () => {
  if (!form.validate()) return

  saving.value = true
  
  // Convertir valores numéricos de string a número
  const productData = {
    ...form.values,
    categoria_id: parseInt(form.values.categoria_id),
    precio_compra: parseFloat(form.values.precio_compra),
    precio_venta: parseFloat(form.values.precio_venta),
    stock: parseInt(form.values.stock),
    stock_minimo: parseInt(form.values.stock_minimo),
    created_by: authStore.user?.id  // Agregar el ID del usuario actual
  }
  
  const result = modal.data.value
    ? await productosStore.updateProducto(modal.data.value.id, productData)
    : await productosStore.createProducto(productData)

  if (result.success) {
    toast.success(modal.data.value ? 'Producto actualizado' : 'Producto creado')
    await productosStore.fetchProductos()
    closeModal()
  } else {
    toast.error(result.message || 'Error al guardar el producto')
  }

  saving.value = false
}

const deleteProducto = async (id) => {
  if (!confirm('¿Está seguro de eliminar este producto?')) return

  const result = await productosStore.deleteProducto(id)
  
  if (result.success) {
    toast.success('Producto eliminado')
    await productosStore.fetchProductos()
  } else {
    toast.error(result.message || 'Error al eliminar el producto')
  }
}

onMounted(async () => {
  await productosStore.fetchProductos()
  await categoriasStore.fetchCategorias()
  categorias.value = categoriasStore.categorias
})
</script>

<style scoped>
.productos {
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

.filters {
  margin-bottom: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  margin-bottom: 1rem;
}

.form-row > :first-child {
  flex: 1;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--color-texto);
}

.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: var(--border-radius);
  font-size: 1rem;
  transition: border-color var(--transition-base);
}

.form-select:focus {
  outline: none;
  border-color: var(--color-azul);
}

.stock-bajo {
  color: var(--color-danger);
  font-weight: 600;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-success {
  background: #d4edda;
  color: #155724;
}

.badge-danger {
  background: #f8d7da;
  color: #721c24;
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

.btn-edit {
  background: #e3f2fd;
  color: #1976d2;
}

.btn-edit:hover {
  background: #1976d2;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);
}

.btn-delete {
  background: #ffebee;
  color: #d32f2f;
}

.btn-delete:hover {
  background: #d32f2f;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(211, 47, 47, 0.3);
}
</style>
