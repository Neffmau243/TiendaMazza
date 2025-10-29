// Reportes Script

// Variables globales para reportes
const ReportesApp = {
  usuario: null,
  datosReporte: null
};

// jsPDF
const { jsPDF } = window.jspdf;

// Métodos de pago (usar el global si existe, sino crear)
const METODOS_PAGO_REPORTES = window.METODOS_PAGO || {
  1: 'Efectivo',
  2: 'Tarjeta de Crédito',
  3: 'Tarjeta de Débito',
  4: 'Transferencia'
};

// Inicializar
window.addEventListener('DOMContentLoaded', async () => {
  // Verificar sesión y permisos
  ReportesApp.usuario = verificarSesion();
  if (!esAdministrador()) {
    alert('Solo administradores pueden generar reportes');
    window.location.href = 'dashboard.html';
    return;
  }

  // El menú y usuario ya se cargan en menu.js
  establecerFechasDefault();
  await cargarCatalogos();
});

// Establecer fechas por defecto
function establecerFechasDefault() {
  // Obtener fecha local en formato YYYY-MM-DD
  const hoy = new Date();
  const year = hoy.getFullYear();
  const month = String(hoy.getMonth() + 1).padStart(2, '0');
  const day = String(hoy.getDate()).padStart(2, '0');
  const fechaLocal = `${year}-${month}-${day}`;
  
  document.getElementById('ventasFechaDesde').value = fechaLocal;
  document.getElementById('ventasFechaHasta').value = fechaLocal;
  document.getElementById('comprasFechaDesde').value = fechaLocal;
  document.getElementById('comprasFechaHasta').value = fechaLocal;
}

// Cargar catálogos
async function cargarCatalogos() {
  // Categorías
  const catResponse = await apiGet(ENDPOINTS.categorias.list);
  if (catResponse.success && catResponse.data.data) {
    const select = document.getElementById('inventarioCategoria');
    catResponse.data.data.forEach(cat => {
      if (cat.estado_id === 1) { // 1 = activo
        select.innerHTML += `<option value="${cat.id}">${cat.nombre}</option>`;
      }
    });
  }

  // Proveedores
  const provResponse = await apiGet(ENDPOINTS.proveedores.list);
  if (provResponse.success && provResponse.data.data) {
    const select = document.getElementById('comprasProveedor');
    provResponse.data.data.forEach(prov => {
      if (prov.estado_id === 1) { // 1 = activo
        select.innerHTML += `<option value="${prov.id}">${prov.nombre}</option>`;
      }
    });
  }
}

// Mostrar filtros según tipo de reporte
function mostrarFiltros() {
  const tipo = document.getElementById('tipoReporte').value;
  
  document.getElementById('filtrosVentas').classList.add('hidden');
  document.getElementById('filtrosInventario').classList.add('hidden');
  document.getElementById('filtrosCompras').classList.add('hidden');
  document.getElementById('vistaPrevia').classList.add('hidden');

  if (tipo === 'ventas') {
    document.getElementById('filtrosVentas').classList.remove('hidden');
  } else if (tipo === 'inventario') {
    document.getElementById('filtrosInventario').classList.remove('hidden');
  } else if (tipo === 'compras') {
    document.getElementById('filtrosCompras').classList.remove('hidden');
  }
}

// ==================== REPORTE DE VENTAS ====================

async function generarReporteVentas() {
  const fechaDesde = document.getElementById('ventasFechaDesde').value;
  const fechaHasta = document.getElementById('ventasFechaHasta').value;
  const metodoPago = document.getElementById('ventasMetodoPago').value;

  if (!fechaDesde || !fechaHasta) {
    mostrarToast('Selecciona las fechas', 'warning');
    return;
  }

  // Obtener datos del backend
  let url = `${ENDPOINTS.reportes.ventas}?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}`;
  if (metodoPago) url += `&metodo_pago_id=${metodoPago}`;

  const response = await apiGet(url);
  if (!response.success || !response.data.data) {
    mostrarToast('Error al obtener datos del reporte', 'danger');
    return;
  }

  datosReporte = response.data.data;
  crearPDFVentas(datosReporte, fechaDesde, fechaHasta);
}

function crearPDFVentas(datos, fechaDesde, fechaHasta) {
  const doc = new jsPDF();

  // Encabezado
  doc.setFontSize(20);
  doc.setTextColor(0, 72, 160); // Azul Revenge
  doc.text('REVENGE POS', 105, 20, { align: 'center' });
  
  doc.setFontSize(16);
  doc.setTextColor(0, 0, 0);
  doc.text('Reporte de Ventas', 105, 30, { align: 'center' });
  
  doc.setFontSize(10);
  doc.text(`Período: ${fechaDesde} al ${fechaHasta}`, 105, 38, { align: 'center' });
  doc.text(`Generado: ${new Date().toLocaleString()}`, 105, 44, { align: 'center' });

  // Resumen
  doc.setFontSize(12);
  doc.setFont(undefined, 'bold');
  doc.text('Resumen', 14, 55);
  doc.setFont(undefined, 'normal');
  doc.setFontSize(10);
  
  const resumen = [
    ['Total de Ventas:', datos.resumen.total_ventas.toString()],
    ['Monto Total:', formatearMoneda(datos.resumen.monto_total)],
    ['Venta Mínima:', formatearMoneda(datos.resumen.venta_minima)],
    ['Venta Máxima:', formatearMoneda(datos.resumen.venta_maxima)],
    ['Ticket Promedio:', formatearMoneda(datos.resumen.promedio_venta)]
  ];

  doc.autoTable({
    startY: 60,
    head: [],
    body: resumen,
    theme: 'plain',
    styles: { fontSize: 10 },
    columnStyles: {
      0: { fontStyle: 'bold', cellWidth: 60 },
      1: { cellWidth: 50 }
    },
    margin: { left: 14, right: 14 }
  });

  // Ventas por método de pago
  if (datos.ventas_por_metodo_pago && datos.ventas_por_metodo_pago.length > 0) {
    doc.setFontSize(12);
    doc.setFont(undefined, 'bold');
    doc.text('Ventas por Método de Pago', 14, doc.lastAutoTable.finalY + 15);
    
    const metodoRows = datos.ventas_por_metodo_pago.map(m => [
      m.metodo || 'Desconocido',
      m.cantidad.toString(),
      formatearMoneda(m.total)
    ]);

    doc.autoTable({
      startY: doc.lastAutoTable.finalY + 20,
      head: [['Método de Pago', 'Cantidad', 'Monto']],
      body: metodoRows,
      theme: 'grid',
      headStyles: { fillColor: [0, 72, 160] },
      styles: { fontSize: 9 },
      columnStyles: {
        0: { cellWidth: 76 },
        1: { cellWidth: 38, halign: 'center' },
        2: { cellWidth: 56, halign: 'right' }
      },
      margin: { left: 14, right: 14 }
    });
  }

  // Productos más vendidos
  if (datos.productos_mas_vendidos && datos.productos_mas_vendidos.length > 0) {
    doc.addPage();
    doc.setFontSize(12);
    doc.setFont(undefined, 'bold');
    doc.text('Top 10 Productos Más Vendidos', 14, 20);
    
    const productosRows = datos.productos_mas_vendidos.slice(0, 10).map((p, i) => [
      (i + 1).toString(),
      p.producto,
      p.cantidad.toString(),
      formatearMoneda(p.total)
    ]);

    doc.autoTable({
      startY: 25,
      head: [['#', 'Producto', 'Cantidad', 'Monto']],
      body: productosRows,
      theme: 'striped',
      headStyles: { fillColor: [255, 210, 0] }, // Amarillo Revenge
      styles: { fontSize: 9 },
      columnStyles: {
        0: { cellWidth: 12, halign: 'center' },
        1: { cellWidth: 88 },
        2: { cellWidth: 28, halign: 'center' },
        3: { cellWidth: 42, halign: 'right' }
      },
      margin: { left: 14, right: 14 }
    });
  }

  // Guardar PDF
  const nombreArchivo = `Reporte_Ventas_${fechaDesde}_${fechaHasta}.pdf`;
  doc.save(nombreArchivo);
  mostrarToast('PDF generado correctamente', 'success');
}

// ==================== REPORTE DE INVENTARIO ====================

async function generarReporteInventario() {
  const categoriaId = document.getElementById('inventarioCategoria').value;
  const filtroStock = document.getElementById('inventarioStock').value;

  let url = ENDPOINTS.reportes.inventario;
  const params = [];
  if (categoriaId) params.push(`categoria_id=${categoriaId}`);
  if (filtroStock) params.push(`stock=${filtroStock}`);
  if (params.length > 0) url += '?' + params.join('&');

  const response = await apiGet(url);
  if (!response.success || !response.data.data) {
    mostrarToast('Error al obtener datos del reporte', 'danger');
    return;
  }

  datosReporte = response.data.data;
  crearPDFInventario(datosReporte);
}

function crearPDFInventario(datos) {
  const doc = new jsPDF();

  // Encabezado
  doc.setFontSize(20);
  doc.setTextColor(0, 72, 160);
  doc.text('REVENGE POS', 105, 20, { align: 'center' });
  
  doc.setFontSize(16);
  doc.setTextColor(0, 0, 0);
  doc.text('Reporte de Inventario', 105, 30, { align: 'center' });
  
  doc.setFontSize(10);
  doc.text(`Generado: ${new Date().toLocaleString()}`, 105, 38, { align: 'center' });

  // Resumen
  doc.setFontSize(12);
  doc.setFont(undefined, 'bold');
  doc.text('Resumen', 14, 50);
  doc.setFont(undefined, 'normal');
  doc.setFontSize(10);
  
  const resumen = [
    ['Total de Productos:', datos.resumen.total_productos.toString()],
    ['Valor Total Inventario:', formatearMoneda(datos.resumen.valor_inventario)],
    ['Valor Venta Potencial:', formatearMoneda(datos.resumen.valor_venta_potencial)],
    ['Productos Stock Bajo:', datos.resumen.productos_stock_bajo.toString()],
    ['Productos Sin Stock:', datos.resumen.productos_sin_stock.toString()]
  ];

  doc.autoTable({
    startY: 55,
    head: [],
    body: resumen,
    theme: 'plain',
    styles: { fontSize: 10 },
    columnStyles: {
      0: { fontStyle: 'bold', cellWidth: 70 },
      1: { cellWidth: 50 }
    },
    margin: { left: 14, right: 14 }
  });

  // Productos con stock bajo
  if (datos.productos_stock_bajo && datos.productos_stock_bajo.length > 0) {
    doc.addPage();
    doc.setFontSize(12);
    doc.setFont(undefined, 'bold');
    doc.text('Productos con Stock Bajo', 14, 20);
    
    const productosRows = datos.productos_stock_bajo.map(p => [
      p.codigo_barras,
      p.nombre,
      p.categoria || 'S/C',
      p.stock_actual.toString(),
      p.stock_minimo.toString(),
      '⚠️'
    ]);

    doc.autoTable({
      startY: 25,
      head: [['Código', 'Producto', 'Categoría', 'Stock', 'Mínimo', 'Estado']],
      body: productosRows,
      theme: 'striped',
      headStyles: { fillColor: [255, 193, 7] }, // Amarillo de advertencia
      styles: { fontSize: 8 },
      columnStyles: {
        0: { cellWidth: 26 },
        1: { cellWidth: 68 },
        2: { cellWidth: 28 },
        3: { cellWidth: 18, halign: 'center' },
        4: { cellWidth: 18, halign: 'center' },
        5: { cellWidth: 12, halign: 'center' }
      },
      margin: { left: 14, right: 14 }
    });
  }

  // Productos sin stock
  if (datos.productos_sin_stock && datos.productos_sin_stock.length > 0) {
    const yPos = doc.lastAutoTable ? doc.lastAutoTable.finalY + 15 : 25;
    if (yPos > 250) doc.addPage();
    
    doc.setFontSize(12);
    doc.setFont(undefined, 'bold');
    doc.text('Productos Sin Stock', 14, yPos > 250 ? 20 : yPos);
    
    const productosRows = datos.productos_sin_stock.map(p => [
      p.codigo_barras,
      p.nombre,
      p.categoria || 'S/C',
      '🚨'
    ]);

    doc.autoTable({
      startY: yPos > 250 ? 25 : yPos + 5,
      head: [['Código', 'Producto', 'Categoría', 'Estado']],
      body: productosRows,
      theme: 'striped',
      headStyles: { fillColor: [220, 53, 69] }, // Rojo de alerta
      styles: { fontSize: 8 },
      columnStyles: {
        0: { cellWidth: 30 },
        1: { cellWidth: 80 },
        2: { cellWidth: 40 },
        3: { cellWidth: 15, halign: 'center' }
      },
      margin: { left: 14, right: 14 }
    });
  }

  // Productos por categoría
  if (datos.productos_por_categoria && datos.productos_por_categoria.length > 0) {
    doc.addPage();
    doc.setFontSize(12);
    doc.setFont(undefined, 'bold');
    doc.text('Productos por Categoría', 14, 20);
    
    const categoriaRows = datos.productos_por_categoria.map(c => [
      c.categoria,
      c.cantidad.toString(),
      c.stock_total.toString(),
      formatearMoneda(c.valor)
    ]);

    doc.autoTable({
      startY: 25,
      head: [['Categoría', 'Productos', 'Stock Total', 'Valor']],
      body: categoriaRows,
      theme: 'grid',
      headStyles: { fillColor: [0, 72, 160] },
      styles: { fontSize: 9 },
      columnStyles: {
        0: { cellWidth: 58 },
        1: { cellWidth: 34, halign: 'center' },
        2: { cellWidth: 38, halign: 'center' },
        3: { cellWidth: 40, halign: 'right' }
      },
      margin: { left: 14, right: 14 }
    });
  }

  // Guardar PDF
  const nombreArchivo = `Reporte_Inventario_${new Date().toISOString().split('T')[0]}.pdf`;
  doc.save(nombreArchivo);
  mostrarToast('PDF generado correctamente', 'success');
}

// ==================== REPORTE DE COMPRAS ====================

async function generarReporteCompras() {
  const fechaDesde = document.getElementById('comprasFechaDesde').value;
  const fechaHasta = document.getElementById('comprasFechaHasta').value;
  const proveedorId = document.getElementById('comprasProveedor').value;

  if (!fechaDesde || !fechaHasta) {
    mostrarToast('Selecciona las fechas', 'warning');
    return;
  }

  let url = `${ENDPOINTS.reportes.compras}?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}`;
  if (proveedorId) url += `&proveedor_id=${proveedorId}`;

  const response = await apiGet(url);
  if (!response.success || !response.data.data) {
    mostrarToast('Error al obtener datos del reporte', 'danger');
    return;
  }

  datosReporte = response.data.data;
  crearPDFCompras(datosReporte, fechaDesde, fechaHasta);
}

function crearPDFCompras(datos, fechaDesde, fechaHasta) {
  const doc = new jsPDF();

  // Encabezado
  doc.setFontSize(20);
  doc.setTextColor(0, 72, 160);
  doc.text('REVENGE POS', 105, 20, { align: 'center' });
  
  doc.setFontSize(16);
  doc.setTextColor(0, 0, 0);
  doc.text('Reporte de Compras', 105, 30, { align: 'center' });
  
  doc.setFontSize(10);
  doc.text(`Período: ${fechaDesde} al ${fechaHasta}`, 105, 38, { align: 'center' });
  doc.text(`Generado: ${new Date().toLocaleString()}`, 105, 44, { align: 'center' });

  // Resumen
  doc.setFontSize(12);
  doc.setFont(undefined, 'bold');
  doc.text('Resumen', 14, 55);
  doc.setFont(undefined, 'normal');
  doc.setFontSize(10);
  
  const resumen = [
    ['Total de Compras:', datos.resumen.total_compras.toString()],
    ['Monto Total:', formatearMoneda(datos.resumen.monto_total)],
    ['Compra Promedio:', formatearMoneda(datos.resumen.promedio_compra)]
  ];

  doc.autoTable({
    startY: 60,
    head: [],
    body: resumen,
    theme: 'plain',
    styles: { fontSize: 10 },
    columnStyles: {
      0: { fontStyle: 'bold', cellWidth: 60 },
      1: { cellWidth: 50 }
    },
    margin: { left: 14, right: 14 }
  });

  // Compras por proveedor
  if (datos.compras_por_proveedor && datos.compras_por_proveedor.length > 0) {
    doc.setFontSize(12);
    doc.setFont(undefined, 'bold');
    doc.text('Compras por Proveedor', 14, doc.lastAutoTable.finalY + 15);
    
    const proveedorRows = datos.compras_por_proveedor.map(p => [
      p.proveedor,
      p.cantidad.toString(),
      formatearMoneda(p.total)
    ]);

    doc.autoTable({
      startY: doc.lastAutoTable.finalY + 20,
      head: [['Proveedor', 'Cantidad', 'Monto']],
      body: proveedorRows,
      theme: 'grid',
      headStyles: { fillColor: [0, 72, 160] },
      styles: { fontSize: 9 },
      columnStyles: {
        0: { cellWidth: 76 },
        1: { cellWidth: 38, halign: 'center' },
        2: { cellWidth: 56, halign: 'right' }
      },
      margin: { left: 14, right: 14 }
    });
  }

  // Productos más comprados
  if (datos.productos_mas_comprados && datos.productos_mas_comprados.length > 0) {
    doc.addPage();
    doc.setFontSize(12);
    doc.setFont(undefined, 'bold');
    doc.text('Productos Más Comprados', 14, 20);
    
    const productosRows = datos.productos_mas_comprados.map((p, i) => [
      (i + 1).toString(),
      p.producto,
      p.cantidad.toString(),
      formatearMoneda(p.total)
    ]);

    doc.autoTable({
      startY: 25,
      head: [['#', 'Producto', 'Cantidad', 'Total']],
      body: productosRows,
      theme: 'striped',
      headStyles: { fillColor: [255, 210, 0] },
      styles: { fontSize: 9 },
      columnStyles: {
        0: { cellWidth: 12, halign: 'center' },
        1: { cellWidth: 88 },
        2: { cellWidth: 28, halign: 'center' },
        3: { cellWidth: 42, halign: 'right' }
      },
      margin: { left: 14, right: 14 }
    });
  }

  // Guardar PDF
  const nombreArchivo = `Reporte_Compras_${fechaDesde}_${fechaHasta}.pdf`;
  doc.save(nombreArchivo);
  mostrarToast('PDF generado correctamente', 'success');
}

// ==================== VISTA PREVIA ====================

async function verVistaPrevia(tipo) {
  let datos = null;

  if (tipo === 'ventas') {
    const fechaDesde = document.getElementById('ventasFechaDesde').value;
    const fechaHasta = document.getElementById('ventasFechaHasta').value;
    if (!fechaDesde || !fechaHasta) {
      mostrarToast('Selecciona las fechas', 'warning');
      return;
    }
    let url = `${ENDPOINTS.reportes.ventas}?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}`;
    const metodoPago = document.getElementById('ventasMetodoPago').value;
    if (metodoPago) url += `&metodo_pago_id=${metodoPago}`;
    const response = await apiGet(url);
    if (response.success) datos = response.data.data;

  } else if (tipo === 'inventario') {
    let url = ENDPOINTS.reportes.inventario;
    const params = [];
    const categoriaId = document.getElementById('inventarioCategoria').value;
    const filtroStock = document.getElementById('inventarioStock').value;
    if (categoriaId) params.push(`categoria_id=${categoriaId}`);
    if (filtroStock) params.push(`stock=${filtroStock}`);
    if (params.length > 0) url += '?' + params.join('&');
    const response = await apiGet(url);
    if (response.success) datos = response.data.data;

  } else if (tipo === 'compras') {
    const fechaDesde = document.getElementById('comprasFechaDesde').value;
    const fechaHasta = document.getElementById('comprasFechaHasta').value;
    if (!fechaDesde || !fechaHasta) {
      mostrarToast('Selecciona las fechas', 'warning');
      return;
    }
    let url = `${ENDPOINTS.reportes.compras}?fecha_desde=${fechaDesde}&fecha_hasta=${fechaHasta}`;
    const proveedorId = document.getElementById('comprasProveedor').value;
    if (proveedorId) url += `&proveedor_id=${proveedorId}`;
    const response = await apiGet(url);
    if (response.success) datos = response.data.data;
  }

  if (!datos) {
    mostrarToast('Error al obtener datos', 'danger');
    return;
  }

  mostrarDatosPrevia(datos, tipo);
}

function mostrarDatosPrevia(datos, tipo) {
  const contenido = document.getElementById('contenidoPrevia');
  
  let html = '<h4>Resumen</h4><table class="table"><tbody>';
  for (const [key, value] of Object.entries(datos.resumen)) {
    const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    const valor = typeof value === 'number' && key.includes('monto') 
      ? formatearMoneda(value) 
      : value;
    html += `<tr><td><strong>${label}:</strong></td><td>${valor}</td></tr>`;
  }
  html += '</tbody></table>';

  contenido.innerHTML = html;
  document.getElementById('vistaPrevia').classList.remove('hidden');
}

function cerrarVistaPrevia() {
  document.getElementById('vistaPrevia').classList.add('hidden');
}
