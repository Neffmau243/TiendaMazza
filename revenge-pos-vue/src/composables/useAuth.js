// composables/useAuth.js
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from './useToast'

export function useAuth() {
  const authStore = useAuthStore()
  const router = useRouter()
  const toast = useToast()

  const login = async (email, password) => {
    try {
      const result = await authStore.login(email, password)
      
      if (result.success) {
        toast.success('Inicio de sesión exitoso')
        router.push('/dashboard')
        return { success: true }
      } else {
        toast.error(result.message || 'Credenciales inválidas')
        return { success: false, message: result.message }
      }
    } catch (error) {
      toast.error('Error al iniciar sesión')
      return { success: false, message: error.message }
    }
  }

  const logout = () => {
    authStore.logout()
    toast.info('Sesión cerrada')
    router.push('/login')
  }

  return {
    user: computed(() => authStore.user),
    isAuthenticated: computed(() => authStore.isAuthenticated),
    isAdmin: computed(() => authStore.isAdmin),
    isCajero: computed(() => authStore.isCajero),
    isAlmacenista: computed(() => authStore.isAlmacenista),
    canSell: computed(() => authStore.canSell),
    canManageInventory: computed(() => authStore.canManageInventory),
    userName: computed(() => authStore.userName),
    userEmail: computed(() => authStore.userEmail),
    roleName: computed(() => authStore.roleName),
    login,
    logout
  }
}
