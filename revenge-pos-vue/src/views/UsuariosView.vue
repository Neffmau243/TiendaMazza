<!-- views/UsuariosView.vue -->
<template>
  <div class="usuarios">
    <div class="page-header">
      <h1>Gestión de Usuarios</h1>
      <BaseButton
        @click="openModal('create')"
        variant="primary"
        icon="fa-plus"
      >
        Nuevo Usuario
      </BaseButton>
    </div>

    <BaseCard>
      <BaseTable
        :columns="columns"
        :data="usuariosStore.usuarios"
        :loading="usuariosStore.loading"
        empty-text="No hay usuarios registrados"
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
              @click="deleteUsuario(row.id)"
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
      :title="modal.data.value ? 'Editar Usuario' : 'Nuevo Usuario'"
      @close="closeModal"
    >
      <form @submit.prevent="saveUsuario">
        <BaseInput
          v-model="form.values.nombre"
          label="Nombre Completo"
          :error="form.errors.nombre"
          required
        />
        <BaseInput
          v-model="form.values.email"
          type="email"
          label="Email"
          :error="form.errors.email"
          required
        />
        <BaseInput
          v-model="form.values.usuario"
          label="Usuario"
          :error="form.errors.usuario"
          required
        />
        <BaseInput
          v-if="!modal.data.value"
          v-model="form.values.password"
          type="password"
          label="Contraseña"
          :error="form.errors.password"
          required
        />
        <div v-if="modal.data.value" class="form-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="cambiarPassword" />
            Cambiar contraseña
          </label>
        </div>
        <BaseInput
          v-if="modal.data.value && cambiarPassword"
          v-model="form.values.password"
          type="password"
          label="Nueva Contraseña"
          :error="form.errors.password"
          placeholder="Ingresa la nueva contraseña"
        />
        <div class="form-group">
          <label>Rol</label>
          <select v-model="form.values.rol_id" class="form-select">
            <option value="1">Administrador</option>
            <option value="2">Cajero</option>
          </select>
        </div>
      </form>
      
      <template #footer>
        <BaseButton @click="closeModal" variant="secondary">
          Cancelar
        </BaseButton>
        <BaseButton
          @click="saveUsuario"
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
import { useUsuariosStore } from '@/stores/usuarios'
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

const usuariosStore = useUsuariosStore()
const authStore = useAuthStore()
const modal = useModal()
const toast = useToast()

const saving = ref(false)
const cambiarPassword = ref(false)

const columns = [
  { key: 'nombre', label: 'Nombre' },
  { key: 'email', label: 'Email' },
  { key: 'rol_nombre', label: 'Rol' },
  { key: 'estado_nombre', label: 'Estado' }
]

const form = useForm(
  {
    nombre: '',
    email: '',
    usuario: '',
    password: '',
    rol_id: '2'
  },
  {
    nombre: [(v) => validateRequired(v, 'El nombre')],
    email: [(v) => validateEmail(v)],
    usuario: [(v) => validateRequired(v, 'El usuario')],
    password: [(v) => !modal.data.value ? validateRequired(v, 'La contraseña') : null]
  }
)

const openModal = (mode, data = null) => {
  cambiarPassword.value = false
  if (data) {
    form.setValues({
      nombre: data.nombre,
      email: data.email,
      usuario: data.usuario,
      rol_id: data.rol_id.toString(),
      password: ''
    })
  } else {
    form.reset()
  }
  modal.open(data)
}

const closeModal = () => {
  modal.close()
  form.reset()
}

const saveUsuario = async () => {
  if (!form.validate()) return

  saving.value = true
  
  // Si es edición, incluir password solo si se marcó cambiar contraseña
  const usuarioData = modal.data.value 
    ? {
        nombre: form.values.nombre,
        email: form.values.email,
        usuario: form.values.usuario,
        rol_id: parseInt(form.values.rol_id),
        ...(cambiarPassword.value && form.values.password ? { password: form.values.password } : {})
      }
    : {
        ...form.values,
        rol_id: parseInt(form.values.rol_id),
        created_by: authStore.user?.id
      }
  
  const result = modal.data.value
    ? await usuariosStore.updateUsuario(modal.data.value.id, usuarioData)
    : await usuariosStore.createUsuario(usuarioData)

  if (result.success) {
    toast.success(modal.data.value ? 'Usuario actualizado' : 'Usuario creado')
    
    // Si se editó el usuario logueado, actualizar el authStore
    if (modal.data.value && modal.data.value.id === authStore.user?.id) {
      authStore.updateUserData(usuarioData)
    }
    
    await usuariosStore.fetchUsuarios()
    closeModal()
  } else {
    toast.error(result.message || 'Error al guardar el usuario')
  }

  saving.value = false
}

const deleteUsuario = async (id) => {
  if (!confirm('¿Está seguro de eliminar este usuario?')) return

  const result = await usuariosStore.deleteUsuario(id)
  
  if (result.success) {
    toast.success('Usuario eliminado')
    await usuariosStore.fetchUsuarios()
  } else {
    toast.error(result.message || 'Error al eliminar el usuario')
  }
}

onMounted(() => {
  usuariosStore.fetchUsuarios()
})
</script>

<style scoped>
.usuarios {
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

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--color-texto);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 400 !important;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
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
