// stores/ui.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  // State
  const sidebarOpen = ref(true)
  const modals = ref({})
  const toasts = ref([])

  // Actions
  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
  }

  const openModal = (modalName, data = null) => {
    modals.value[modalName] = {
      isOpen: true,
      data
    }
  }

  const closeModal = (modalName) => {
    if (modals.value[modalName]) {
      modals.value[modalName].isOpen = false
      modals.value[modalName].data = null
    }
  }

  const addToast = (message, type = 'info', duration = 3000) => {
    const id = Date.now()
    toasts.value.push({
      id,
      message,
      type,
      duration
    })

    setTimeout(() => {
      removeToast(id)
    }, duration)

    return id
  }

  const removeToast = (id) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  return {
    sidebarOpen,
    modals,
    toasts,
    toggleSidebar,
    openModal,
    closeModal,
    addToast,
    removeToast
  }
})
