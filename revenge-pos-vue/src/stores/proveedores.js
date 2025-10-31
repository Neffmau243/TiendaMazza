// stores/proveedores.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { proveedoresService } from '@/services/proveedoresService'

export const useProveedoresStore = defineStore('proveedores', () => {
  // State
  const proveedores = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const proveedoresActivos = computed(() => {
    return proveedores.value.filter(p => p.activo)
  })

  const totalProveedores = computed(() => proveedores.value.length)

  // Actions
  const fetchProveedores = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await proveedoresService.getAll()
      if (response.success) {
        proveedores.value = response.data
      } else {
        error.value = response.message
      }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const createProveedor = async (data) => {
    try {
      const response = await proveedoresService.create(data)
      if (response.success) {
        proveedores.value.push(response.data)
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  const updateProveedor = async (id, data) => {
    try {
      const response = await proveedoresService.update(id, data)
      if (response.success) {
        const index = proveedores.value.findIndex(p => p.id === id)
        if (index !== -1) {
          proveedores.value[index] = response.data
        }
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  const deleteProveedor = async (id) => {
    try {
      const response = await proveedoresService.delete(id)
      if (response.success) {
        const index = proveedores.value.findIndex(p => p.id === id)
        if (index !== -1) {
          proveedores.value.splice(index, 1)
        }
        return { success: true }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  return {
    proveedores,
    loading,
    error,
    proveedoresActivos,
    totalProveedores,
    fetchProveedores,
    createProveedor,
    updateProveedor,
    deleteProveedor
  }
})
