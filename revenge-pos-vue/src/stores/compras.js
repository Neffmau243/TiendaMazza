// stores/compras.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { comprasService } from '@/services/comprasService'

export const useComprasStore = defineStore('compras', () => {
  // State
  const compras = ref([])
  const loading = ref(false)
  const error = ref(null)
  const currentCompra = ref(null)

  // Getters
  const totalCompras = computed(() => compras.value.length)

  const montoTotalCompras = computed(() => {
    return compras.value.reduce((sum, c) => sum + c.total, 0)
  })

  // Actions
  const fetchCompras = async (filtros = null) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await comprasService.getAll(filtros)
      if (response.success) {
        compras.value = response.data
      } else {
        error.value = response.message
      }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const fetchCompraDetalle = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await comprasService.getById(id)
      if (response.success) {
        currentCompra.value = response.data
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  const createCompra = async (data) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await comprasService.create(data)
      if (response.success) {
        compras.value.unshift(response.data)
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  return {
    compras,
    loading,
    error,
    currentCompra,
    totalCompras,
    montoTotalCompras,
    fetchCompras,
    fetchCompraDetalle,
    createCompra
  }
})
