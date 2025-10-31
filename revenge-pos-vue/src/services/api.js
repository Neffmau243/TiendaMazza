// services/api.js
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
})

// Interceptor de request - agregar token JWT
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor de response - manejar errores globales
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Token expirado o inválido
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      router.push('/login')
    }
    
    // Error de servidor
    if (error.response?.status === 500) {
      console.error('Error del servidor:', error.response.data)
    }
    
    return Promise.reject(error)
  }
)

export default api
