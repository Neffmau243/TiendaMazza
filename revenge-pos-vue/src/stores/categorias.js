// stores/categorias.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { categoriasService } from '@/services/categoriasService'

export const useCategoriasStore = defineStore('categorias', () => {
  // State
  const categorias = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const categoriasActivas = computed(() => {
    return categorias.value.filter(c => c.activo)
  })

  const totalCategorias = computed(() => categorias.value.length)

  // Actions
  const fetchCategorias = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await categoriasService.getAll()
      if (response.success) {
        categorias.value = response.data
      } else {
        error.value = response.message
      }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const createCategoria = async (data) => {
    try {
      const response = await categoriasService.create(data)
      if (response.success) {
        categorias.value.push(response.data)
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  const updateCategoria = async (id, data) => {
    try {
      const response = await categoriasService.update(id, data)
      if (response.success) {
        const index = categorias.value.findIndex(c => c.id === id)
        if (index !== -1) {
          categorias.value[index] = response.data
        }
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  const deleteCategoria = async (id) => {
    try {
      const response = await categoriasService.delete(id)
      if (response.success) {
        const index = categorias.value.findIndex(c => c.id === id)
        if (index !== -1) {
          categorias.value.splice(index, 1)
        }
        return { success: true }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  return {
    categorias,
    loading,
    error,
    categoriasActivas,
    totalCategorias,
    fetchCategorias,
    createCategoria,
    updateCategoria,
    deleteCategoria
  }
})
