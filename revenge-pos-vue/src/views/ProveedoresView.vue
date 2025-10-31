<!-- views/ProveedoresView.vue -->
<template>
  <div class="proveedores">
    <div class="page-header">
      <h1>Gestión de Proveedores</h1>
      <BaseButton
        @click="openModal('create')"
        variant="primary"
        icon="fa-plus"
      >
        Nuevo Proveedor
      </BaseButton>
    </div>

    <BaseCard>
      <BaseTable
        :columns="columns"
        :data="proveedoresStore.proveedores"
        :loading="proveedoresStore.loading"
        empty-text="No hay proveedores registrados"
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
              @click="deleteProveedor(row.id)"
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
      :title="modal.data.value ? 'Editar Proveedor' : 'Nuevo Proveedor'"
      @close="closeModal"
    >
      <form @submit.prevent="saveProveedor">
        <BaseInput
          v-model="form.values.nombre"
          label="Nombre"
          :error="form.errors.nombre"
          required
        />
        <BaseInput
          v-model="form.values.ruc"
          label="RUC"
          :error="form.errors.ruc"
          required
        />
        <BaseInput
          v-model="form.values.telefono"
          label="Teléfono"
          :error="form.errors.telefono"
        />
        <BaseInput
          v-model="form.values.contacto"
          label="Persona de Contacto"
          :error="form.errors.contacto"
        />
        <BaseInput
          v-model="form.values.email"
          type="email"
          label="Email"
          :error="form.errors.email"
        />
        <BaseInput
          v-model="form.values.direccion"
          label="Dirección"
        />
      </form>
      
      <template #footer>
        <BaseButton @click="closeModal" variant="secondary">
          Cancelar
        </BaseButton>
        <BaseButton
          @click="saveProveedor"
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
import { useProveedoresStore } from '@/stores/proveedores'
import { useAuthStore } from '@/stores/auth'
import { useModal } from '@/composables/useModal'
import { useForm } from '@/composables/useForm'
import { useToast } from '@/composables/useToast'
import { validateRequired, validateEmail } from '@/utils/validators'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseTable from '@/components/common/BaseTable.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseModal from '@/components/common/BaseModal.vue'

const proveedoresStore = useProveedoresStore()
const authStore = useAuthStore()
const modal = useModal()
const toast = useToast()

const saving = ref(false)

const columns = [
  { key: 'nombre', label: 'Nombre' },
  { key: 'ruc', label: 'RUC' },
  { key: 'telefono', label: 'Teléfono' },
  { key: 'email', label: 'Email' },
  { key: 'direccion', label: 'Dirección' },
  { key: 'contacto', label: 'Contacto' },
  { key: 'estado_nombre', label: 'Estado' }
]

const form = useForm(
  {
    nombre: '',
    ruc: '',
    telefono: '',
    contacto: '',
    email: '',
    direccion: ''
  },
  {
    nombre: [(v) => validateRequired(v, 'El nombre')],
    ruc: [(v) => validateRequired(v, 'El RUC')],
    email: [(v) => v ? validateEmail(v) : null]
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

const saveProveedor = async () => {
  if (!form.validate()) return

  saving.value = true
  
  const proveedorData = {
    ...form.values,
    created_by: authStore.user?.id
  }
  
  const result = modal.data.value
    ? await proveedoresStore.updateProveedor(modal.data.value.id, proveedorData)
    : await proveedoresStore.createProveedor(proveedorData)

  if (result.success) {
    toast.success(modal.data.value ? 'Proveedor actualizado' : 'Proveedor creado')
    await proveedoresStore.fetchProveedores() // Recargar la lista
    closeModal()
  } else {
    toast.error(result.message || 'Error al guardar el proveedor')
  }

  saving.value = false
}

const deleteProveedor = async (id) => {
  if (!confirm('¿Está seguro de eliminar este proveedor?')) return

  const result = await proveedoresStore.deleteProveedor(id)
  
  if (result.success) {
    toast.success('Proveedor eliminado')
    await proveedoresStore.fetchProveedores() // Recargar la lista
  } else {
    toast.error(result.message || 'Error al eliminar el proveedor')
  }
}

onMounted(() => {
  proveedoresStore.fetchProveedores()
})
</script>

<style scoped>
.proveedores {
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
