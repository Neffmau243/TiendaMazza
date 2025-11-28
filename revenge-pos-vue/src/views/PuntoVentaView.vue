<!-- views/PuntoVentaView.vue -->
<template>
  <div class="punto-venta">
    <div class="pos-grid">
      <!-- Panel Izquierdo: Búsqueda de Productos -->
      <BaseCard title="Buscar Producto">
        <div class="search-section">
          <BaseInput
            v-model="codigoBarras"
            type="text"
            placeholder="Escanear código de barras o buscar..."
            icon="fa-search"
            @keyup.enter="buscarProducto"
            ref="barcodeInput"
          />
          <BaseButton
            @click="buscarProducto"
            variant="primary"
            icon="fa-search"
          >
            Buscar
          </BaseButton>
          <BarcodeScanner @code-scanned="onCodeScanned" />
        </div>

        <div v-if="productoEncontrado" class="producto-info">
          <h3>{{ productoEncontrado.nombre }}</h3>
          <p class="producto-precio">
            Precio: {{ formatCurrency(productoEncontrado.precio_venta) }}
          </p>
          <p class="producto-stock">
            Stock disponible: {{ productoEncontrado.stock }}
          </p>
          <BaseButton
            @click="agregarAlCarrito"
            variant="success"
            icon="fa-plus"
            block
          >
            Agregar al Carrito
          </BaseButton>
        </div>

        <div v-else-if="searchError" class="error-message">
          {{ searchError }}
        </div>
      </BaseCard>

      <!-- Panel Derecho: Carrito -->
      <BaseCard>
        <template #header>
          <div class="cart-header">
            <h3>Carrito</h3>
            <span class="item-count">{{ cartStore.itemCount }} items</span>
          </div>
        </template>

        <div class="cart-items">
          <div v-if="cartStore.isEmpty" class="empty-cart">
            <i class="fas fa-shopping-cart"></i>
            <p>El carrito está vacío</p>
          </div>
          <CarritoItem
            v-for="item in cartStore.items"
            :key="item.producto_id"
            :item="item"
            @update-quantity="updateQuantity"
            @remove="removeItem"
          />
        </div>

        <div v-if="!cartStore.isEmpty" class="cart-summary">
          <div class="cart-totals">
            <div class="total-row">
              <span>Subtotal:</span>
              <span>{{ formatCurrency(cartStore.subtotal) }}</span>
            </div>
            <div class="total-row">
              <span>IVA (18%):</span>
              <span>{{ formatCurrency(cartStore.iva) }}</span>
            </div>
            <div class="total-row total">
              <span>Total:</span>
              <span>{{ formatCurrency(cartStore.total) }}</span>
            </div>
          </div>

          <div class="payment-section">
            <label>Método de Pago:</label>
            <select v-model="metodoPago" class="payment-select">
              <option value="">Seleccionar...</option>
              <option value="1">Efectivo</option>
              <option value="2">Tarjeta</option>
              <option value="3">Yape</option>
              <option value="4">Transferencia</option>
            </select>
          </div>

          <div class="cart-actions">
            <BaseButton
              @click="limpiarCarrito"
              variant="danger"
              icon="fa-trash"
            >
              Limpiar
            </BaseButton>
            <BaseButton
              @click="procesarVenta"
              variant="primary"
              icon="fa-check"
              :loading="processing"
              :disabled="!metodoPago"
            >
              Procesar Venta
            </BaseButton>
          </div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useProductosStore } from '@/stores/productos'
import { useVentasStore } from '@/stores/ventas'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import CarritoItem from '@/components/ventas/CarritoItem.vue'
import BarcodeScanner from '@/components/ventas/BarcodeScanner.vue'
import { formatCurrency } from '@/utils/formatters'

const cartStore = useCartStore()
const productosStore = useProductosStore()
const ventasStore = useVentasStore()
const authStore = useAuthStore()
const toast = useToast()

const codigoBarras = ref('')
const productoEncontrado = ref(null)
const searchError = ref('')
const metodoPago = ref('')
const processing = ref(false)
const barcodeInput = ref(null)

// Función para manejar código escaneado desde la cámara
const onCodeScanned = (code) => {
  codigoBarras.value = code
  toast.info(`Código escaneado: ${code}`)
  buscarProducto()
}

const buscarProducto = async () => {
  if (!codigoBarras.value.trim()) return

  searchError.value = ''
  productoEncontrado.value = null

  const result = await productosStore.buscarProducto(codigoBarras.value)
  
  if (result.success) {
    productoEncontrado.value = result.data
    toast.success('Producto encontrado')
  } else {
    searchError.value = 'Producto no encontrado'
    toast.error('Producto no encontrado')
  }
  
  codigoBarras.value = ''
}

const agregarAlCarrito = () => {
  if (!productoEncontrado.value) return

  const result = cartStore.addItem(productoEncontrado.value, 1)
  
  if (result.success) {
    toast.success('Producto agregado al carrito')
    productoEncontrado.value = null
    searchError.value = ''
    barcodeInput.value?.focus()
  } else {
    toast.error(result.message)
  }
}

const updateQuantity = (productoId, cantidad) => {
  const result = cartStore.updateQuantity(productoId, cantidad)
  if (!result.success) {
    toast.error(result.message)
  }
}

const removeItem = (productoId) => {
  cartStore.removeItem(productoId)
  toast.info('Producto eliminado del carrito')
}

const limpiarCarrito = () => {
  if (confirm('¿Está seguro de limpiar el carrito?')) {
    cartStore.clearCart()
    metodoPago.value = ''
    toast.info('Carrito limpiado')
  }
}

const procesarVenta = async () => {
  if (!metodoPago.value) {
    toast.error('Seleccione un método de pago')
    return
  }

  processing.value = true

  const ventaData = {
    cajero_id: authStore.user.id,
    metodo_pago_id: parseInt(metodoPago.value),
    items: cartStore.getCartData().items
  }

  const result = await ventasStore.createVenta(ventaData)

  if (result.success) {
    toast.success(`Venta procesada: ${result.data.numero_boleta}`)
    cartStore.clearCart()
    metodoPago.value = ''
    barcodeInput.value?.focus()
  } else {
    toast.error(result.message || 'Error al procesar la venta')
  }

  processing.value = false
}

onMounted(() => {
  barcodeInput.value?.focus()
})
</script>

<style scoped>
.punto-venta {
  max-width: 1400px;
  margin: 0 auto;
}

.pos-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.search-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: flex-start;
}

.search-section > :first-child {
  flex: 1;
  min-width: 200px;
}

.producto-info {
  padding: 1.5rem;
  background: #f5f5f5;
  border-radius: var(--border-radius);
}

.producto-info h3 {
  margin: 0 0 1rem 0;
  color: var(--color-texto);
}

.producto-precio {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-azul);
  margin: 0.5rem 0;
}

.producto-stock {
  color: #666;
  margin: 0.5rem 0 1rem 0;
}

.error-message {
  padding: 1rem;
  background: #fee;
  color: #c33;
  border-radius: var(--border-radius);
  text-align: center;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.cart-header h3 {
  margin: 0;
}

.item-count {
  background: var(--color-azul);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.cart-items {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.empty-cart {
  text-align: center;
  padding: 3rem 1rem;
  color: #999;
}

.empty-cart i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.cart-summary {
  border-top: 2px solid #eee;
  padding-top: 1rem;
}

.cart-totals {
  margin-bottom: 1rem;
}

.total-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  font-size: 1rem;
}

.total-row.total {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-azul);
  border-top: 2px solid var(--color-azul);
  padding-top: 1rem;
  margin-top: 0.5rem;
}

.payment-section {
  margin-bottom: 1rem;
}

.payment-section label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--color-texto);
}

.payment-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: var(--border-radius);
  font-size: 1rem;
}

.cart-actions {
  display: flex;
  gap: 1rem;
}

@media (max-width: 1024px) {
  .pos-grid {
    grid-template-columns: 1fr;
  }

  .search-section {
    flex-direction: column;
  }

  .cart-items {
    max-height: 300px;
  }
}

@media (max-width: 767px) {
  .cart-actions {
    flex-direction: column;
  }

  .total-row.total {
    font-size: 1.25rem;
  }
}
</style>
