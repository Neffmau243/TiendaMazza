<!-- components/ventas/CarritoItem.vue -->
<template>
  <div class="carrito-item">
    <div class="item-info">
      <h4 class="item-nombre">{{ item.nombre }}</h4>
      <p class="item-codigo">{{ item.codigo_barras }}</p>
      <p class="item-precio">{{ formatCurrency(item.precio_unitario) }}</p>
    </div>
    <div class="item-controls">
      <div class="quantity-controls">
        <button 
          class="qty-btn" 
          @click="decrementQuantity"
          :disabled="item.cantidad <= 1"
        >
          <i class="fas fa-minus"></i>
        </button>
        <span class="quantity">{{ item.cantidad }}</span>
        <button 
          class="qty-btn" 
          @click="incrementQuantity"
          :disabled="item.cantidad >= item.stock_disponible"
        >
          <i class="fas fa-plus"></i>
        </button>
      </div>
      <div class="item-total">
        {{ formatCurrency(item.precio_unitario * item.cantidad) }}
      </div>
      <button class="remove-btn" @click="removeItem">
        <i class="fas fa-trash"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { formatCurrency } from '@/utils/formatters'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update-quantity', 'remove'])

const incrementQuantity = () => {
  emit('update-quantity', props.item.producto_id, props.item.cantidad + 1)
}

const decrementQuantity = () => {
  if (props.item.cantidad > 1) {
    emit('update-quantity', props.item.producto_id, props.item.cantidad - 1)
  }
}

const removeItem = () => {
  emit('remove', props.item.producto_id)
}
</script>

<style scoped>
.carrito-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: var(--border-radius);
  margin-bottom: 0.75rem;
  background: white;
}

.item-info {
  flex: 1;
}

.item-nombre {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  color: var(--color-texto);
}

.item-codigo {
  margin: 0 0 0.25rem 0;
  font-size: 0.75rem;
  color: #666;
}

.item-precio {
  margin: 0;
  font-size: 0.875rem;
  color: var(--color-azul);
  font-weight: 600;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #ddd;
  background: white;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
}

.qty-btn:hover:not(:disabled) {
  background: #f5f5f5;
  border-color: var(--color-azul);
}

.qty-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity {
  min-width: 40px;
  text-align: center;
  font-weight: 600;
  font-size: 1rem;
}

.item-total {
  font-weight: 600;
  color: var(--color-azul);
  min-width: 80px;
  text-align: right;
}

.remove-btn {
  width: 32px;
  height: 32px;
  background: var(--color-danger);
  color: white;
  border: none;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
}

.remove-btn:hover {
  background: #c82333;
}
</style>
