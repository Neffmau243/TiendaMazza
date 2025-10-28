// Ventas Script

let usuario = null;

// Variables globales
let ventasData = [];
let ventaActual = null;

// Métodos de pago
const METODOS_PAGO_NOMBRES = {
  1: 'Efectivo',
  2: 'Tarjeta de Crédito',
  3: 'Tarjeta de Débito',
  4: 'Transferencia'
};

// Inicializar
window.addEventListener('DOMContentLoaded', async () => {
  // Verificar sesión y permisos
  usuario = verificarSesion();
  if (!puedeVender()) {
    alert('No tienes permisos para ver las ventas');
    window.location.href = 'dashboard.html';
    return;
  }

  // El menú y usuario ya se cargan en menu.js
  establecerFechasDefault();
  await cargarVentas();
});

// Establecer fechas por defecto (hoy)
function establecerFechasDefault() {
  const hoy = new Date().toISOString().split('T')[0];
  document.getElementById('fechaDesde').value = hoy;
  document.getElementById('fechaHasta').value = hoy;
}

// Cargar ventas
async function cargarVentas() {
  document.getElementById('loadingVentas').style.display = 'block';
  document.getElementById('tablaVentas').style.display = 'none';

  const fechaDesde = document.getElementById('fechaDesde').value;
  const fechaHasta = document.getElementById('fechaHasta').value;

  let url = ENDPOINTS.ventas.list;
  if (fechaDesde && fechaHasta) {
    url += `?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}`;
  }

  const response = await apiGet(url);

  document.getElementById('loadingVentas').style.display = 'none';
  document.getElementById('tablaVentas').style.display = 'block';

  if (response.success && response.data.data) {
    ventasData = response.data.data;
    
    // Normalizar campos para coincidir con frontend
    ventasData.forEach(venta => {
      venta.venta_id = venta.venta_id || venta.id;
      venta.folio = venta.folio || venta.numero_boleta;
      venta.fecha_venta = venta.fecha_venta || venta.fecha;
      venta.usuario_nombre = venta.usuario_nombre || venta.cajero_nombre;
      venta.iva = venta.iva || venta.impuestos;
      venta.metodo_pago = venta.metodo_pago || venta.metodo_pago_nombre;
    });
    
    console.log('✅ Ventas normalizadas:', ventasData[0]);
    mostrarVentas(ventasData);
    actualizarResumen(ventasData);
  } else {
    mostrarToast('Error al cargar ventas', 'danger');
  }
}

// Mostrar ventas en tabla
function mostrarVentas(ventas) {
  const tbody = document.getElementById('ventasTableBody');
  
  if (ventas.length === 0) {
    tbody.innerHTML = '<tr><td colspan="9" class="text-center">No hay ventas en este período</td></tr>';
    return;
  }

  tbody.innerHTML = ventas.map(venta => {
    return `
      <tr>
        <td><strong>${venta.folio || 'N/A'}</strong></td>
        <td>${formatearFecha(venta.fecha_venta)}</td>
        <td>${venta.cliente_nombre || 'Cliente general'}</td>
        <td>
          <span class="badge badge-info">
            ${venta.metodo_pago || 'N/A'}
          </span>
        </td>
        <td>${formatearMoneda(venta.subtotal)}</td>
        <td>${formatearMoneda(venta.iva)}</td>
        <td><strong>${formatearMoneda(venta.total)}</strong></td>
        <td>${venta.usuario_nombre || 'N/A'}</td>
        <td>
          <button onclick="verDetalle(${venta.venta_id})" class="btn btn-sm btn-primary" title="Ver detalle">
            <i class="fas fa-eye"></i>
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

// Actualizar resumen
function actualizarResumen(ventas) {
  const totalVentas = ventas.length;
  const montoTotal = ventas.reduce((sum, v) => sum + parseFloat(v.total), 0);
  const productosVendidos = ventas.reduce((sum, v) => sum + (v.total_productos || 0), 0);
  const ticketPromedio = totalVentas > 0 ? montoTotal / totalVentas : 0;

  document.getElementById('totalVentas').textContent = totalVentas;
  document.getElementById('montoTotal').textContent = formatearMoneda(montoTotal);
  document.getElementById('productosVendidos').textContent = productosVendidos;
  document.getElementById('ticketPromedio').textContent = formatearMoneda(ticketPromedio);
}

// Filtrar ventas
async function filtrarVentas() {
  const fechaDesde = document.getElementById('fechaDesde').value;
  const fechaHasta = document.getElementById('fechaHasta').value;
  const metodoPagoId = document.getElementById('filterMetodoPago').value;

  if (!fechaDesde || !fechaHasta) {
    mostrarToast('Por favor selecciona un rango de fechas', 'warning');
    return;
  }

  await cargarVentas();

  // Filtro adicional por método de pago
  if (metodoPagoId) {
    const filtradas = ventasData.filter(v => v.metodo_pago_id == metodoPagoId);
    mostrarVentas(filtradas);
    actualizarResumen(filtradas);
  }
}

// Limpiar filtros
function limpiarFiltros() {
  establecerFechasDefault();
  document.getElementById('filterMetodoPago').value = '';
  cargarVentas();
}

// Ver detalle de venta
async function verDetalle(ventaId) {
  const response = await apiGet(`${ENDPOINTS.ventas.get}/${ventaId}`);
  
  if (response.success && response.data.data) {
    ventaActual = response.data.data;
    mostrarDetalleVenta(ventaActual);
  }
}

// Mostrar detalle en modal
function mostrarDetalleVenta(venta) {
  // Información general
  document.getElementById('detalleFolio').textContent = venta.folio || 'N/A';
  document.getElementById('detalleFecha').textContent = formatearFecha(venta.fecha_venta);
  document.getElementById('detalleCliente').textContent = venta.cliente_nombre || 'Cliente general';
  document.getElementById('detalleMetodoPago').textContent = METODOS_PAGO_NOMBRES[venta.metodo_pago_id] || 'N/A';
  document.getElementById('detalleCajero').textContent = venta.usuario_nombre || 'N/A';
  document.getElementById('detalleEstado').innerHTML = '<span class="badge badge-success">Completada</span>';

  // Productos
  const productosHtml = venta.productos.map(prod => `
    <tr>
      <td>${prod.producto_nombre}</td>
      <td>${formatearMoneda(prod.precio_unitario)}</td>
      <td class="text-center">${prod.cantidad}</td>
      <td class="text-right"><strong>${formatearMoneda(prod.subtotal)}</strong></td>
    </tr>
  `).join('');
  document.getElementById('detalleProductos').innerHTML = productosHtml;

  // Totales
  document.getElementById('detalleSubtotal').textContent = formatearMoneda(venta.subtotal);
  document.getElementById('detalleIVA').textContent = formatearMoneda(venta.iva);
  document.getElementById('detalleTotal').textContent = formatearMoneda(venta.total);

  // Mostrar modal
  document.getElementById('modalDetalle').classList.remove('hidden');
}

// Cerrar modal
function cerrarModalDetalle() {
  document.getElementById('modalDetalle').classList.add('hidden');
  ventaActual = null;
}

// Imprimir venta
function imprimirVenta() {
  if (!ventaActual) return;

  // Crear ventana de impresión
  const ventanaImpresion = window.open('', '_blank', 'width=300,height=600');
  
  const contenido = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Ticket - ${ventaActual.folio}</title>
      <style>
        body {
          font-family: 'Courier New', monospace;
          font-size: 12px;
          margin: 10px;
        }
        .center { text-align: center; }
        .right { text-align: right; }
        .bold { font-weight: bold; }
        hr { border: none; border-top: 1px dashed #000; }
        table { width: 100%; border-collapse: collapse; }
        td { padding: 2px 0; }
      </style>
    </head>
    <body>
      <div class="center bold">
        <h2>REVENGE POS</h2>
        <p>TICKET DE VENTA</p>
      </div>
      <hr>
      <p><strong>Folio:</strong> ${ventaActual.folio || 'N/A'}</p>
      <p><strong>Fecha:</strong> ${formatearFecha(ventaActual.fecha_venta)}</p>
      <p><strong>Cliente:</strong> ${ventaActual.cliente_nombre || 'Cliente general'}</p>
      <p><strong>Cajero:</strong> ${ventaActual.usuario_nombre || 'N/A'}</p>
      <hr>
      <table>
        <thead>
          <tr>
            <th style="text-align: left;">Producto</th>
            <th>Cant</th>
            <th style="text-align: right;">Precio</th>
            <th style="text-align: right;">Total</th>
          </tr>
        </thead>
        <tbody>
          ${ventaActual.productos.map(p => `
            <tr>
              <td>${p.producto_nombre}</td>
              <td class="center">${p.cantidad}</td>
              <td class="right">${formatearMoneda(p.precio_unitario)}</td>
              <td class="right">${formatearMoneda(p.subtotal)}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      <hr>
      <table>
        <tr>
          <td><strong>Subtotal:</strong></td>
          <td class="right">${formatearMoneda(ventaActual.subtotal)}</td>
        </tr>
        <tr>
          <td><strong>IVA (16%):</strong></td>
          <td class="right">${formatearMoneda(ventaActual.iva)}</td>
        </tr>
        <tr>
          <td><strong>TOTAL:</strong></td>
          <td class="right bold" style="font-size: 14px;">${formatearMoneda(ventaActual.total)}</td>
        </tr>
        <tr>
          <td><strong>Método de Pago:</strong></td>
          <td class="right">${METODOS_PAGO_NOMBRES[ventaActual.metodo_pago_id]}</td>
        </tr>
      </table>
      <hr>
      <div class="center">
        <p>¡Gracias por su compra!</p>
        <p>${new Date().toLocaleString()}</p>
      </div>
    </body>
    </html>
  `;

  ventanaImpresion.document.write(contenido);
  ventanaImpresion.document.close();
  
  setTimeout(() => {
    ventanaImpresion.print();
  }, 500);
}

// Cerrar modal con ESC
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    cerrarModalDetalle();
  }
});
