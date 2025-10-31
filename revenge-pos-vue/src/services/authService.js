// services/authService.js
import api from './api'

export const authService = {
  /**
   * Login de usuario
   * POST /api/auth/login
   */
  async login(email, password) {
    try {
      const response = await api.post('/auth/login', { email, password })
      
      // El backend devuelve { success: true, data: {...}, message: "..." }
      if (response.data.success) {
        return { 
          success: true, 
          data: {
            usuario: {
              id: response.data.data.id,
              nombre: response.data.data.nombre,
              email: response.data.data.email,
              rol_id: response.data.data.rol_id,
              rol_nombre: response.data.data.rol_nombre
            },
            token: response.data.data.token
          }
        }
      }
      
      return {
        success: false,
        message: response.data.message || 'Error al iniciar sesión'
      }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al iniciar sesión' 
      }
    }
  }
}
