// stores/ventas.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ventasService } from '@/services/ventasService'

export const useVentasStore = defineStore('ventas', () => {
  // State
  const ventas = ref([])
  const loading = ref(false)
  const error = ref(null)
  const currentVenta = ref(null)
  const filters = ref({
    fechaInicio: null,
    fechaFin: null,
    metodoPago: null,
    cajero: null
  })

  // Getters
  const ventasDelDia = computed(() => {
    const hoy = new Date().toISOString().split('T')[0]
    const ventasHoy = ventas.value.filter(v => {
      if (!v.fecha) return false
      try {
        const fechaVenta = new Date(v.fecha).toISOString().split('T')[0]
        return fechaVenta === hoy
      } catch {
        return false
      }
    })
    
    return {
      cantidad: ventasHoy.length,
      total: ventasHoy.reduce((sum, v) => sum + v.total, 0),
      ventas: ventasHoy
    }
  })

  const ventasPorMetodoPago = computed(() => {
    const agrupadas = {}
    ventas.value.forEach(venta => {
      const metodo = venta.metodo_pago_nombre || 'Sin especificar'
      if (!agrupadas[metodo]) {
        agrupadas[metodo] = {
          cantidad: 0,
          total: 0
        }
      }
      agrupadas[metodo].cantidad++
      agrupadas[metodo].total += venta.total
    })
    return agrupadas
  })

  const totalVentas = computed(() => ventas.value.length)

  const montoTotalVentas = computed(() => {
    return ventas.value.reduce((sum, v) => sum + v.total, 0)
  })

  // Actions
  const fetchVentas = async (filtros = null) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await ventasService.getAll(filtros || filters.value)
      if (response.success) {
        ventas.value = response.data
      } else {
        error.value = response.message
      }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const fetchVentaDetalle = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await ventasService.getById(id)
      if (response.success) {
        currentVenta.value = response.data
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  const createVenta = async (data) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await ventasService.create(data)
      if (response.success) {
        ventas.value.unshift(response.data)
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  const fetchVentasHoy = async () => {
    const hoy = new Date().toISOString().split('T')[0]
    return await fetchVentas({
      fechaInicio: hoy,
      fechaFin: hoy
    })
  }

  const setFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
  }

  const clearFilters = () => {
    filters.value = {
      fechaInicio: null,
      fechaFin: null,
      metodoPago: null,
      cajero: null
    }
  }

  return {
    // State
    ventas,
    loading,
    error,
    currentVenta,
    filters,
    // Getters
    ventasDelDia,
    ventasPorMetodoPago,
    totalVentas,
    montoTotalVentas,
    // Actions
    fetchVentas,
    fetchVentaDetalle,
    createVenta,
    fetchVentasHoy,
    setFilters,
    clearFilters
  }
})
