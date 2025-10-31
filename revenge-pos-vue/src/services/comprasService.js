// services/comprasService.js
import api from './api'

export const comprasService = {
  /**
   * Obtener todas las compras
   * GET /api/compras
   */
  async getAll(filtros = null) {
    try {
      let url = '/compras'
      if (filtros) {
        const params = new URLSearchParams()
        if (filtros.fechaInicio) params.append('fecha_desde', filtros.fechaInicio)
        if (filtros.fechaFin) params.append('fecha_hasta', filtros.fechaFin)
        if (filtros.proveedor) params.append('proveedor', filtros.proveedor)
        
        const queryString = params.toString()
        if (queryString) url += `?${queryString}`
      }
      
      const response = await api.get(url)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener compras' 
      }
    }
  },

  /**
   * Obtener detalle de una compra
   * GET /api/compras/:id
   */
  async getById(id) {
    try {
      const response = await api.get(`/compras/${id}`)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener compra' 
      }
    }
  },

  /**
   * Crear una nueva compra
   * POST /api/compras
   * Body: { proveedor_id, usuario_id, numero_factura, items: [{ producto_id, cantidad, precio_unitario }] }
   */
  async create(data) {
    try {
      const response = await api.post('/compras', data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al crear compra' 
      }
    }
  }
}
