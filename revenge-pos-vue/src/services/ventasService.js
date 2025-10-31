// services/ventasService.js
import api from './api'

export const ventasService = {
  /**
   * Obtener todas las ventas con filtros opcionales
   * GET /api/ventas
   */
  async getAll(filtros = null) {
    try {
      let url = '/ventas'
      if (filtros) {
        const params = new URLSearchParams()
        if (filtros.fechaInicio) params.append('fecha_desde', filtros.fechaInicio)
        if (filtros.fechaFin) params.append('fecha_hasta', filtros.fechaFin)
        if (filtros.metodoPago) params.append('metodo_pago', filtros.metodoPago)
        if (filtros.cajero) params.append('cajero', filtros.cajero)
        
        const queryString = params.toString()
        if (queryString) url += `?${queryString}`
      }
      
      const response = await api.get(url)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener ventas' 
      }
    }
  },

  /**
   * Obtener detalle de una venta
   * GET /api/ventas/:id
   */
  async getById(id) {
    try {
      const response = await api.get(`/ventas/${id}`)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener venta' 
      }
    }
  },

  /**
   * Crear una nueva venta
   * POST /api/ventas
   * Body: { cajero_id, metodo_pago_id, items: [{ producto_id, cantidad, precio_unitario }] }
   */
  async create(data) {
    try {
      const response = await api.post('/ventas', data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al crear venta' 
      }
    }
  }
}
