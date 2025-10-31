// stores/productos.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { productosService } from '@/services/productosService'

export const useProductosStore = defineStore('productos', () => {
  // State
  const productos = ref([])
  const loading = ref(false)
  const error = ref(null)
  const currentProducto = ref(null)

  // Getters
  const productosPorCategoria = computed(() => (categoriaId) => {
    return productos.value.filter(p => p.categoria_id === categoriaId)
  })

  const productosActivos = computed(() => {
    return productos.value.filter(p => p.activo)
  })

  const productosStockBajo = computed(() => {
    const stockBajo = productos.value.filter(p => {
      // Convertir a números para asegurar comparación correcta
      const stock = parseInt(p.stock)
      const stockMinimo = parseInt(p.stock_minimo)
      return stock <= stockMinimo
    })
    
    // Debug temporal
    console.log('🔍 Productos con stock bajo:', stockBajo.length)
    if (stockBajo.length > 0) {
      console.log('📦 Productos:', stockBajo.map(p => ({
        nombre: p.nombre,
        stock: p.stock,
        stock_minimo: p.stock_minimo
      })))
    }
    
    return stockBajo
  })

  const productosSinStock = computed(() => {
    return productos.value.filter(p => p.stock === 0)
  })

  const totalProductos = computed(() => productos.value.length)

  const valorInventario = computed(() => {
    return productos.value.reduce((total, p) => {
      return total + (p.precio_compra * p.stock)
    }, 0)
  })

  // Actions
  const fetchProductos = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await productosService.getAll()
      if (response.success) {
        productos.value = response.data
      } else {
        error.value = response.message
      }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const fetchProducto = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await productosService.getById(id)
      if (response.success) {
        currentProducto.value = response.data
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  const createProducto = async (data) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await productosService.create(data)
      if (response.success) {
        productos.value.push(response.data)
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  const updateProducto = async (id, data) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await productosService.update(id, data)
      if (response.success) {
        const index = productos.value.findIndex(p => p.id === id)
        if (index !== -1) {
          productos.value[index] = response.data
        }
        return { success: true, data: response.data }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  const deleteProducto = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await productosService.delete(id)
      if (response.success) {
        const index = productos.value.findIndex(p => p.id === id)
        if (index !== -1) {
          productos.value.splice(index, 1)
        }
        return { success: true }
      }
      return { success: false, message: response.message }
    } catch (err) {
      return { success: false, message: err.message }
    } finally {
      loading.value = false
    }
  }

  const buscarProducto = async (codigo) => {
    try {
      const response = await productosService.buscar(codigo)
      return response
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  const fetchProductosStockBajo = async () => {
    try {
      const response = await productosService.getStockBajo()
      return response
    } catch (err) {
      return { success: false, message: err.message }
    }
  }

  return {
    // State
    productos,
    loading,
    error,
    currentProducto,
    // Getters
    productosPorCategoria,
    productosActivos,
    productosStockBajo,
    productosSinStock,
    totalProductos,
    valorInventario,
    // Actions
    fetchProductos,
    fetchProducto,
    createProducto,
    updateProducto,
    deleteProducto,
    buscarProducto,
    fetchProductosStockBajo
  }
})
