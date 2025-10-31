// services/usuariosService.js
import api from './api'

export const usuariosService = {
  async getAll() {
    try {
      const response = await api.get('/usuarios')
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener usuarios' 
      }
    }
  },

  async getById(id) {
    try {
      const response = await api.get(`/usuarios/${id}`)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener usuario' 
      }
    }
  },

  async create(data) {
    try {
      const response = await api.post('/usuarios', data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al crear usuario' 
      }
    }
  },

  async update(id, data) {
    try {
      const response = await api.put(`/usuarios/${id}`, data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al actualizar usuario' 
      }
    }
  },

  async delete(id) {
    try {
      await api.delete(`/usuarios/${id}`)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al eliminar usuario' 
      }
    }
  }
}
