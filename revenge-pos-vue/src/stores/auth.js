// stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/authService'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.rol_id === 1)
  const isCajero = computed(() => user.value?.rol_id === 2)
  const isAlmacenista = computed(() => user.value?.rol_id === 3)
  const canSell = computed(() => [1, 2].includes(user.value?.rol_id))
  const canManageInventory = computed(() => [1, 3].includes(user.value?.rol_id))
  const userName = computed(() => user.value?.nombre || '')
  const userEmail = computed(() => user.value?.email || '')
  const roleName = computed(() => user.value?.rol_nombre || '')

  // Actions
  const login = async (email, password) => {
    try {
      const response = await authService.login(email, password)
      
      if (response.success) {
        user.value = response.data.usuario
        token.value = response.data.token
        
        sessionStorage.setItem('user', JSON.stringify(user.value))
        sessionStorage.setItem('token', token.value)
        
        return { success: true }
      }
      
      return { success: false, message: response.message }
    } catch (error) {
      return { success: false, message: error.message }
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    sessionStorage.removeItem('user')
    sessionStorage.removeItem('token')
  }

  const checkAuth = () => {
    const savedUser = sessionStorage.getItem('user')
    const savedToken = sessionStorage.getItem('token')
    
    if (savedUser && savedToken) {
      try {
        user.value = JSON.parse(savedUser)
        token.value = savedToken
        return true
      } catch (error) {
        logout()
        return false
      }
    }
    
    return false
  }

  const updateUserData = (userData) => {
    // Actualizar datos del usuario en sesión
    if (user.value && userData.id === user.value.id) {
      user.value = { ...user.value, ...userData }
      sessionStorage.setItem('user', JSON.stringify(user.value))
    }
  }

  // Inicializar desde sessionStorage
  checkAuth()

  return {
    // State
    user,
    token,
    // Getters
    isAuthenticated,
    isAdmin,
    isCajero,
    isAlmacenista,
    canSell,
    canManageInventory,
    userName,
    userEmail,
    roleName,
    // Actions
    login,
    logout,
    checkAuth,
    updateUserData
  }
})
