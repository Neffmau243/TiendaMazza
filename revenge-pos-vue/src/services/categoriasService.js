// services/categoriasService.js
import api from './api'

export const categoriasService = {
  /**
   * Obtener todas las categorías
   * GET /api/categorias
   */
  async getAll() {
    try {
      const response = await api.get('/categorias')
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener categorías' 
      }
    }
  },

  /**
   * Obtener una categoría por ID
   * GET /api/categorias/:id
   */
  async getById(id) {
    try {
      const response = await api.get(`/categorias/${id}`)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener categoría' 
      }
    }
  },

  /**
   * Crear una nueva categoría
   * POST /api/categorias
   */
  async create(data) {
    try {
      const response = await api.post('/categorias', data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al crear categoría' 
      }
    }
  },

  /**
   * Actualizar una categoría
   * PUT /api/categorias/:id
   */
  async update(id, data) {
    try {
      const response = await api.put(`/categorias/${id}`, data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al actualizar categoría' 
      }
    }
  },

  /**
   * Eliminar una categoría
   * DELETE /api/categorias/:id
   */
  async delete(id) {
    try {
      await api.delete(`/categorias/${id}`)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al eliminar categoría' 
      }
    }
  }
}
