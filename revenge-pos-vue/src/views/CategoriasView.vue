<!-- views/CategoriasView.vue -->
<template>
  <div class="categorias">
    <div class="page-header">
      <h1>Gestión de Categorías</h1>
      <BaseButton
        @click="openModal('create')"
        variant="primary"
        icon="fa-plus"
      >
        Nueva Categoría
      </BaseButton>
    </div>

    <BaseCard>
      <BaseTable
        :columns="columns"
        :data="categoriasStore.categorias"
        :loading="categoriasStore.loading"
        empty-text="No hay categorías registradas"
      >
        <template #cell-estado_nombre="{ value }">
          <span :class="['badge', value?.toLowerCase().trim() === 'activo' ? 'badge-success' : 'badge-danger']">
            {{ value }}
          </span>
        </template>
        <template #actions="{ row }">
          <div class="action-buttons">
            <button 
              @click="openModal('edit', row)"
              class="btn-icon btn-edit"
              title="Editar"
            >
              <i class="fas fa-edit"></i>
            </button>
            <button 
              @click="deleteCategoria(row.id)"
              class="btn-icon btn-delete"
              title="Eliminar"
            >
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </template>
      </BaseTable>
    </BaseCard>

    <!-- Modal -->
    <BaseModal
      :show="modal.isOpen.value"
      :title="modal.data.value ? 'Editar Categoría' : 'Nueva Categoría'"
      @close="closeModal"
    >
      <form @submit.prevent="saveCategoria">
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
      </form>
      
      <template #footer>
        <BaseButton @click="closeModal" variant="secondary">
          Cancelar
        </BaseButton>
        <BaseButton
          @click="saveCategoria"
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
import { ref, onMounted } from 'vue'
import { useCategoriasStore } from '@/stores/categorias'
import { useAuthStore } from '@/stores/auth'
import { useModal } from '@/composables/useModal'
import { useForm } from '@/composables/useForm'
import { useToast } from '@/composables/useToast'
import { validateRequired } from '@/utils/validators'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseTable from '@/components/common/BaseTable.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseModal from '@/components/common/BaseModal.vue'

const categoriasStore = useCategoriasStore()
const authStore = useAuthStore()
const modal = useModal()
const toast = useToast()

const saving = ref(false)

const columns = [
  { key: 'nombre', label: 'Nombre' },
  { key: 'descripcion', label: 'Descripción' },
  { key: 'estado_nombre', label: 'Estado' }
]

const form = useForm(
  {
    nombre: '',
    descripcion: ''
  },
  {
    nombre: [(v) => validateRequired(v, 'El nombre')]
  }
)

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

const saveCategoria = async () => {
  if (!form.validate()) return

  saving.value = true
  
  const categoriaData = {
    ...form.values,
    created_by: authStore.user?.id
  }
  
  const result = modal.data.value
    ? await categoriasStore.updateCategoria(modal.data.value.id, categoriaData)
    : await categoriasStore.createCategoria(categoriaData)

  if (result.success) {
    toast.success(modal.data.value ? 'Categoría actualizada' : 'Categoría creada')
    await categoriasStore.fetchCategorias()
    closeModal()
  } else {
    toast.error(result.message || 'Error al guardar la categoría')
  }

  saving.value = false
}

const deleteCategoria = async (id) => {
  if (!confirm('¿Está seguro de eliminar esta categoría?')) return

  const result = await categoriasStore.deleteCategoria(id)
  
  if (result.success) {
    toast.success('Categoría eliminada')
    await categoriasStore.fetchCategorias()
  } else {
    toast.error(result.message || 'Error al eliminar la categoría')
  }
}

onMounted(() => {
  categoriasStore.fetchCategorias()
})
</script>

<style scoped>
.categorias {
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
