// composables/useModal.js
import { ref } from 'vue'

export function useModal() {
  const isOpen = ref(false)
  const data = ref(null)

  const open = (modalData = null) => {
    data.value = modalData
    isOpen.value = true
  }

  const close = () => {
    isOpen.value = false
    data.value = null
  }

  const toggle = () => {
    isOpen.value = !isOpen.value
  }

  return {
    isOpen,
    data,
    open,
    close,
    toggle
  }
}
