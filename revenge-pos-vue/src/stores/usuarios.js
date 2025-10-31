// stores/usuarios.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { usuariosService } from '@/services/usuariosService'

export const useUsuariosStore = defineStore('usuarios', () => {
  // State
  const usuarios = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const usuariosActivos = computed(() => {
    return usuarios.value.filter(u => u.activo)
  })

  const usuariosPorRol = computed(() => (rolId) => {
    return usuarios.value.filter(u => u.rol_id === rolId)
  })

  const totalUsuarios = computed(() => usuarios.value.length)

  // Actions
  const fetchUsuarios = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await usuariosService.getAll()
      if (response.success) {
        usuarios.value = response.data
      } else {
        error.value = response.message
      }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const createUsuario = async (data) => {
    try {
      const response = await usuariosService.create(data)
      if (response.success) {
        usuarios.value.push(response.data)
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  const updateUsuario = async (id, data) => {
    try {
      const response = await usuariosService.update(id, data)
      if (response.success) {
        const index = usuarios.value.findIndex(u => u.id === id)
        if (index !== -1) {
          usuarios.value[index] = response.data
        }
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  const deleteUsuario = async (id) => {
    try {
      const response = await usuariosService.delete(id)
      if (response.success) {
        const index = usuarios.value.findIndex(u => u.id === id)
        if (index !== -1) {
          usuarios.value.splice(index, 1)
        }
        return { success: true }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  return {
    usuarios,
    loading,
    error,
    usuariosActivos,
    usuariosPorRol,
    totalUsuarios,
    fetchUsuarios,
    createUsuario,
    updateUsuario,
    deleteUsuario
  }
})
