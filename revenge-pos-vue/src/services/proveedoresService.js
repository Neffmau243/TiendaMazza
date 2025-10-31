// services/proveedoresService.js
import api from './api'

export const proveedoresService = {
  async getAll() {
    try {
      const response = await api.get('/proveedores')
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener proveedores' 
      }
    }
  },

  async getById(id) {
    try {
      const response = await api.get(`/proveedores/${id}`)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener proveedor' 
      }
    }
  },

  async create(data) {
    try {
      const response = await api.post('/proveedores', data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al crear proveedor' 
      }
    }
  },

  async update(id, data) {
    try {
      const response = await api.put(`/proveedores/${id}`, data)
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al actualizar proveedor' 
      }
    }
  },

  async delete(id) {
    try {
      await api.delete(`/proveedores/${id}`)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al eliminar proveedor' 
      }
    }
  }
}
