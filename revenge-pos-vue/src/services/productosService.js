// services/productosService.js
import api from './api'

export const productosService = {
  /**
   * Obtener todos los productos
   * GET /api/productos
   */
  async getAll() {
    try {
      const response = await api.get('/productos')
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener productos' 
      }
    }
  },

  /**
   * Obtener un producto por ID
   * GET /api/productos/:id
   */
  async getById(id) {
    try {
      const response = await api.get(`/productos/${id}`)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener producto' 
      }
    }
  },

  /**
   * Crear un nuevo producto
   * POST /api/productos
   */
  async create(data) {
    try {
      const response = await api.post('/productos', data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al crear producto' 
      }
    }
  },

  /**
   * Actualizar un producto
   * PUT /api/productos/:id
   */
  async update(id, data) {
    try {
      const response = await api.put(`/productos/${id}`, data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al actualizar producto' 
      }
    }
  },

  /**
   * Eliminar un producto
   * DELETE /api/productos/:id
   */
  async delete(id) {
    try {
      await api.delete(`/productos/${id}`)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al eliminar producto' 
      }
    }
  },

  /**
   * Buscar producto por código de barras
   * GET /api/productos/buscar?codigo=:codigo
   */
  async buscar(codigo) {
    try {
      const response = await api.get(`/productos/buscar?codigo=${codigo}`)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Producto no encontrado' 
      }
    }
  },

  /**
   * Obtener productos con stock bajo
   * GET /api/productos/stock-bajo
   */
  async getStockBajo() {
    try {
      const response = await api.get('/productos/stock-bajo')
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener productos' 
      }
    }
  }
}
