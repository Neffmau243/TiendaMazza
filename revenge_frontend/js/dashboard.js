// Dashboard Script

let usuario = null;

// Cargar estadísticas del dashboard
async function cargarEstadisticas() {
  try {
    // Obtener ventas del día
    const responseVentas = await apiGet(ENDPOINTS.ventas.list);
    if (responseVentas.success && responseVentas.data.data) {
      const todasLasVentas = responseVentas.data.data;
      
      // Normalizar campos de ventas
      todasLasVentas.forEach(v => {
        v.folio = v.folio || v.numero_boleta || 'N/A';
        v.usuario_nombre = v.usuario_nombre || v.cajero_nombre || 'N/A';
        v.metodo_pago_nombre = v.metodo_pago_nombre || v.metodo_pago || 'N/A';
      });
      
      // Filtrar ventas de hoy
      const hoy = new Date();
      const hoyStr = `${hoy.getDate()}/${hoy.getMonth() + 1}/${hoy.getFullYear()}`;
      
      const ventasHoy = todasLasVentas.filter(v => {
        const fechaVenta = new Date(v.fecha);
        return fechaVenta.getDate() === hoy.getDate() &&
               fechaVenta.getMonth() === hoy.getMonth() &&
               fechaVenta.getFullYear() === hoy.getFullYear();
      });
      
      // Actualizar cards
      document.getElementById('ventasHoy').textContent = ventasHoy.length;
      
      const montoHoy = ventasHoy.reduce((sum, v) => sum + parseFloat(v.total || 0), 0);
      document.getElementById('montoHoy').textContent = formatearMoneda(montoHoy);
      
      // Última venta
      if (todasLasVentas.length > 0) {
        const ultimaVenta = todasLasVentas[0];
        document.getElementById('ultimaVenta').textContent = formatearMoneda(ultimaVenta.total || 0);
        
        // Extraer hora de la fecha
        const hora = ultimaVenta.fecha.split(' ')[1] || '--:--';
        document.getElementById('horaUltimaVenta').textContent = hora.substring(0, 5);
      }
      
      // Mostrar últimas ventas en tabla (máximo 5)
      cargarUltimasVentas(todasLasVentas.slice(0, 5));
    }

    // Obtener productos
    const responseProductos = await apiGet(ENDPOINTS.productos.list);
    if (responseProductos.success && responseProductos.data.data) {
      const productos = responseProductos.data.data;
      document.getElementById('totalProductos').textContent = productos.length;
    }

    // Obtener productos con stock bajo
    const responseStockBajo = await apiGet(ENDPOINTS.productos.stockBajo);
    if (responseStockBajo.success && responseStockBajo.data.data) {
      const productosStockBajo = responseStockBajo.data.data;
      document.getElementById('stockBajo').textContent = productosStockBajo.length;
      
      if (productosStockBajo.length > 0) {
        document.getElementById('stockBajoContainer').style.display = 'block';
        cargarTablaStockBajo(productosStockBajo);
      }
    }

  } catch (error) {
    console.error('Error al cargar estadísticas:', error);
    mostrarToast('Error al cargar datos del dashboard', 'danger');
  }
}

// Cargar tabla de stock bajo
function cargarTablaStockBajo(productos) {
  const tbody = document.getElementById('tbodyStockBajo');
  
  if (productos.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay productos con stock bajo</td></tr>';
    return;
  }

  tbody.innerHTML = productos.map(p => `
    <tr>
      <td>${p.codigo_barras}</td>
      <td><strong>${p.nombre}</strong></td>
      <td>${p.categoria_nombre || 'Sin categoría'}</td>
      <td><span class="badge badge-danger">${p.stock_actual}</span></td>
      <td>${p.stock_minimo}</td>
      <td>
        <span class="badge badge-warning">
          <i class="fas fa-exclamation-triangle"></i> Bajo
        </span>
      </td>
    </tr>
  `).join('');
}

// Cargar últimas ventas
function cargarUltimasVentas(ventas) {
  const tbody = document.getElementById('tbodyUltimasVentas');
  
  if (ventas.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay ventas registradas</td></tr>';
    return;
  }

  tbody.innerHTML = ventas.map(v => `
    <tr>
      <td><strong>${v.folio || 'N/A'}</strong></td>
      <td>${v.fecha ? new Date(v.fecha).toLocaleString('es-MX') : 'N/A'}</td>
      <td>${v.cliente_nombre || 'Cliente general'}</td>
      <td><strong style="color: var(--color-success);">${formatearMoneda(v.total || 0)}</strong></td>
      <td>${v.metodo_pago_nombre || 'N/A'}</td>
      <td>${v.usuario_nombre || 'N/A'}</td>
    </tr>
  `).join('');
}

// Inicializar dashboard
window.addEventListener('DOMContentLoaded', () => {
  // La sesión, menú y usuario ya se inicializan en menu.js
  // Solo cargamos las estadísticas específicas del dashboard
  cargarEstadisticas();
  
  // Recargar estadísticas cada 30 segundos
  setInterval(cargarEstadisticas, 30000);
});
