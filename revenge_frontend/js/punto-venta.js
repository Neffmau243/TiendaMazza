// Punto de Venta Script

let usuario = null;

// Carrito de compras
let carrito = [];
let ventaActual = null;

// Inicializar
window.addEventListener('DOMContentLoaded', () => {
  // Verificar sesión y permisos
  usuario = verificarSesion();
  if (!puedeVender()) {
    alert('No tienes permisos para acceder al punto de venta');
    window.location.href = 'dashboard.html';
    return;
  }

  // El menú y usuario ya se cargan en menu.js
  // Solo enfocamos el campo de búsqueda
  document.getElementById('inputCodigo').focus();
});

// Buscar producto
document.getElementById('formBuscar').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const codigo = document.getElementById('inputCodigo').value.trim();
  if (!codigo) {
    mostrarToast('Por favor ingresa un código', 'warning');
    return;
  }

  await buscarProducto(codigo);
});

// Buscar producto por código
async function buscarProducto(codigo) {
  const resultadoDiv = document.getElementById('resultadoBusqueda');
  resultadoDiv.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Buscando...</div>';
  resultadoDiv.classList.remove('hidden');

  const response = await apiGet(`${ENDPOINTS.productos.search}?codigo=${codigo}`);

  if (response.success && response.data.data) {
    const producto = response.data.data;
    
    // Normalizar: si viene 'id' en lugar de 'producto_id'
    if (!producto.producto_id && producto.id) {
      producto.producto_id = producto.id;
    }
    
    console.log('🔍 Producto encontrado:', producto);
    mostrarProductoEncontrado(producto);
  } else {
    resultadoDiv.innerHTML = `
      <div class="alert alert-warning">
        <i class="fas fa-exclamation-triangle"></i>
        Producto no encontrado con código: <strong>${codigo}</strong>
      </div>
    `;
    setTimeout(() => {
      resultadoDiv.classList.add('hidden');
    }, 3000);
  }

  // Limpiar y enfocar input
  document.getElementById('inputCodigo').value = '';
  document.getElementById('inputCodigo').focus();
}

// Mostrar producto encontrado
function mostrarProductoEncontrado(producto) {
  const resultadoDiv = document.getElementById('resultadoBusqueda');
  
  resultadoDiv.innerHTML = `
    <div class="product-card">
      <div class="product-info">
        <h4>${producto.nombre}</h4>
        <p><i class="fas fa-barcode"></i> ${producto.codigo_barras}</p>
        <p><i class="fas fa-box"></i> Stock: <strong>${producto.stock_actual}</strong></p>
        ${producto.descripcion ? `<p><i class="fas fa-info-circle"></i> ${producto.descripcion}</p>` : ''}
      </div>
      <div>
        <div class="product-price">${formatearMoneda(producto.precio_venta)}</div>
      </div>
    </div>
    
    <div class="quantity-selector">
      <label>Cantidad:</label>
      <button onclick="cambiarCantidadTemporal(-1)" type="button">-</button>
      <input type="number" id="cantidadTemporal" value="1" min="1" max="${producto.stock_actual}">
      <button onclick="cambiarCantidadTemporal(1)" type="button">+</button>
    </div>

    <button onclick='agregarAlCarrito(${JSON.stringify(producto).replace(/'/g, "&apos;")})' class="btn btn-success btn-block">
      <i class="fas fa-cart-plus"></i> Agregar al Carrito
    </button>
  `;
}

// Cambiar cantidad temporal
function cambiarCantidadTemporal(delta) {
  const input = document.getElementById('cantidadTemporal');
  const nuevoValor = parseInt(input.value) + delta;
  if (nuevoValor >= 1 && nuevoValor <= parseInt(input.max)) {
    input.value = nuevoValor;
  }
}

// Agregar producto al carrito
function agregarAlCarrito(producto) {
  const cantidadInput = document.getElementById('cantidadTemporal');
  const cantidad = parseInt(cantidadInput.value) || 1;

  // Verificar stock
  if (cantidad > producto.stock_actual) {
    mostrarToast(`Stock insuficiente. Disponible: ${producto.stock_actual}`, 'danger');
    return;
  }

  // Verificar si ya existe en el carrito
  const existente = carrito.find(item => item.producto_id === producto.producto_id);
  
  if (existente) {
    const nuevaCantidad = existente.cantidad + cantidad;
    if (nuevaCantidad > producto.stock_actual) {
      mostrarToast(`Stock insuficiente. Disponible: ${producto.stock_actual}`, 'danger');
      return;
    }
    existente.cantidad = nuevaCantidad;
  } else {
    carrito.push({
      producto_id: producto.producto_id,
      nombre: producto.nombre,
      precio_unitario: parseFloat(producto.precio_venta),
      cantidad: cantidad,
      stock_disponible: producto.stock_actual
    });
  }

  mostrarToast(`${producto.nombre} agregado al carrito`, 'success');
  actualizarCarrito();
  
  // Ocultar resultado
  document.getElementById('resultadoBusqueda').classList.add('hidden');
  document.getElementById('inputCodigo').focus();
}

// Actualizar visualización del carrito
function actualizarCarrito() {
  const cartItems = document.getElementById('cartItems');
  
  if (carrito.length === 0) {
    cartItems.innerHTML = `
      <div class="empty-cart">
        <i class="fas fa-shopping-cart"></i>
        <p>El carrito está vacío</p>
        <small>Busca y agrega productos</small>
      </div>
    `;
  } else {
    cartItems.innerHTML = carrito.map((item, index) => `
      <div class="cart-item">
        <div class="cart-item-info">
          <h5>${item.nombre}</h5>
          <p>${formatearMoneda(item.precio_unitario)} c/u</p>
        </div>
        <div class="cart-item-actions">
          <div class="cart-item-quantity">
            <button onclick="cambiarCantidad(${index}, -1)">-</button>
            <span>${item.cantidad}</span>
            <button onclick="cambiarCantidad(${index}, 1)">+</button>
          </div>
          <div class="cart-item-price">
            ${formatearMoneda(item.precio_unitario * item.cantidad)}
          </div>
          <button onclick="eliminarDelCarrito(${index})" class="btn-remove">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    `).join('');
  }

  actualizarTotales();
}

// Cambiar cantidad de un item
function cambiarCantidad(index, delta) {
  const item = carrito[index];
  const nuevaCantidad = item.cantidad + delta;
  
  if (nuevaCantidad < 1) {
    eliminarDelCarrito(index);
    return;
  }
  
  if (nuevaCantidad > item.stock_disponible) {
    mostrarToast(`Stock máximo: ${item.stock_disponible}`, 'warning');
    return;
  }
  
  item.cantidad = nuevaCantidad;
  actualizarCarrito();
}

// Eliminar item del carrito
function eliminarDelCarrito(index) {
  carrito.splice(index, 1);
  actualizarCarrito();
  mostrarToast('Producto eliminado del carrito', 'info');
}

// Actualizar totales
function actualizarTotales() {
  const subtotal = carrito.reduce((sum, item) => sum + (item.precio_unitario * item.cantidad), 0);
  const iva = subtotal * IVA;
  const total = subtotal + iva;

  document.getElementById('subtotal').textContent = formatearMoneda(subtotal);
  document.getElementById('iva').textContent = formatearMoneda(iva);
  document.getElementById('total').textContent = formatearMoneda(total);
}

// Limpiar carrito
function limpiarCarrito() {
  if (carrito.length === 0) return;
  
  if (confirm('¿Estás seguro de limpiar el carrito?')) {
    carrito = [];
    actualizarCarrito();
    mostrarToast('Carrito limpiado', 'info');
  }
}

// Finalizar venta
async function finalizarVenta() {
  // Validaciones
  if (carrito.length === 0) {
    mostrarToast('El carrito está vacío', 'warning');
    return;
  }

  const metodoPagoId = parseInt(document.getElementById('metodoPago').value);
  const clienteNombre = document.getElementById('clienteNombre').value.trim() || 'Cliente general';

  // Confirmar venta
  if (!confirm('¿Confirmar venta?')) return;

  // Preparar datos
  const ventaData = {
    cajero_id: usuario.id, // Backend espera cajero_id
    cliente_nombre: clienteNombre,
    metodo_pago_id: metodoPagoId,
    items: carrito.map(item => ({ // Backend espera items, no productos
      producto_id: item.producto_id,
      cantidad: item.cantidad,
      precio_unitario: item.precio_unitario
    }))
  };

  // Mostrar loading
  const btnFinalizar = event.target;
  btnFinalizar.disabled = true;
  btnFinalizar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';

  // Enviar al backend
  const response = await apiPost(ENDPOINTS.ventas.create, ventaData);

  if (response.success && response.data.data) {
    ventaActual = response.data.data;
    // Normalizar folio
    ventaActual.folio = ventaActual.folio || ventaActual.numero_boleta || 'N/A';
    mostrarModalExito();
    carrito = [];
    actualizarCarrito();
    document.getElementById('clienteNombre').value = '';
  } else {
    mostrarToast(response.data.message || 'Error al procesar la venta', 'danger');
  }

  // Rehabilitar botón
  btnFinalizar.disabled = false;
  btnFinalizar.innerHTML = '<i class="fas fa-check"></i> FINALIZAR VENTA';
}

// Mostrar modal de éxito
function mostrarModalExito() {
  document.getElementById('totalVenta').textContent = formatearMoneda(ventaActual.total);
  document.getElementById('folioVenta').textContent = ventaActual.folio || 'N/A';
  document.getElementById('modalExito').classList.remove('hidden');
}

// Cerrar modal
function cerrarModal() {
  document.getElementById('modalExito').classList.add('hidden');
  document.getElementById('inputCodigo').focus();
}

// Imprimir ticket (placeholder)
function imprimirTicket() {
  alert('Función de impresión de ticket en desarrollo');
  cerrarModal();
}

// Atajo de teclado F2 para enfocar búsqueda
document.addEventListener('keydown', (e) => {
  if (e.key === 'F2') {
    e.preventDefault();
    document.getElementById('inputCodigo').focus();
  }
});
