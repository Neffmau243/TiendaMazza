// stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const IVA = 0.18

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref([])
  const metodoPago = ref(null)
  const clienteInfo = ref(null)

  // Getters
  const subtotal = computed(() => {
    return items.value.reduce((sum, item) => {
      return sum + (item.precio_unitario * item.cantidad)
    }, 0)
  })

  const iva = computed(() => subtotal.value * IVA)
  
  const total = computed(() => subtotal.value + iva.value)
  
  const itemCount = computed(() => items.value.length)
  
  const totalItems = computed(() => {
    return items.value.reduce((sum, item) => sum + item.cantidad, 0)
  })

  const isEmpty = computed(() => items.value.length === 0)

  // Actions
  const addItem = (producto, cantidad = 1) => {
    const existingItem = items.value.find(item => item.producto_id === producto.id)
    
    if (existingItem) {
      // Verificar stock disponible
      if (existingItem.cantidad + cantidad <= existingItem.stock_disponible) {
        existingItem.cantidad += cantidad
        return { success: true }
      } else {
        return { success: false, message: 'Stock insuficiente' }
      }
    } else {
      // Agregar nuevo item
      if (cantidad <= producto.stock) {
        items.value.push({
          producto_id: producto.id,
          nombre: producto.nombre,
          codigo_barras: producto.codigo_barras,
          precio_unitario: producto.precio_venta,
          cantidad: cantidad,
          stock_disponible: producto.stock
        })
        return { success: true }
      } else {
        return { success: false, message: 'Stock insuficiente' }
      }
    }
  }

  const removeItem = (productoId) => {
    const index = items.value.findIndex(item => item.producto_id === productoId)
    if (index !== -1) {
      items.value.splice(index, 1)
      return { success: true }
    }
    return { success: false }
  }

  const updateQuantity = (productoId, cantidad) => {
    const item = items.value.find(item => item.producto_id === productoId)
    if (item) {
      if (cantidad <= 0) {
        return removeItem(productoId)
      } else if (cantidad <= item.stock_disponible) {
        item.cantidad = cantidad
        return { success: true }
      } else {
        return { success: false, message: 'Stock insuficiente' }
      }
    }
    return { success: false }
  }

  const incrementQuantity = (productoId) => {
    const item = items.value.find(item => item.producto_id === productoId)
    if (item && item.cantidad < item.stock_disponible) {
      item.cantidad++
      return { success: true }
    }
    return { success: false, message: 'Stock insuficiente' }
  }

  const decrementQuantity = (productoId) => {
    const item = items.value.find(item => item.producto_id === productoId)
    if (item) {
      if (item.cantidad > 1) {
        item.cantidad--
        return { success: true }
      } else {
        return removeItem(productoId)
      }
    }
    return { success: false }
  }

  const clearCart = () => {
    items.value = []
    metodoPago.value = null
    clienteInfo.value = null
  }

  const setMetodoPago = (metodo) => {
    metodoPago.value = metodo
  }

  const setClienteInfo = (info) => {
    clienteInfo.value = info
  }

  const getCartData = () => {
    return {
      items: items.value.map(item => ({
        producto_id: item.producto_id,
        cantidad: item.cantidad,
        precio_unitario: item.precio_unitario
      })),
      metodo_pago_id: metodoPago.value,
      subtotal: subtotal.value,
      iva: iva.value,
      total: total.value
    }
  }

  return {
    // State
    items,
    metodoPago,
    clienteInfo,
    // Getters
    subtotal,
    iva,
    total,
    itemCount,
    totalItems,
    isEmpty,
    // Actions
    addItem,
    removeItem,
    updateQuantity,
    incrementQuantity,
    decrementQuantity,
    clearCart,
    setMetodoPago,
    setClienteInfo,
    getCartData
  }
})
