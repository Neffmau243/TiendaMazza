# 📊 Ejemplos de Uso - Endpoints de Reportes

## 🎯 Reporte de Ventas Semanal

### Petición
```http
GET http://localhost:5000/api/reportes/ventas?fecha_inicio=2025-10-06&fecha_fin=2025-10-13
```

### Respuesta
```json
{
  "success": true,
  "data": {
    "fecha_inicio": "2025-10-06",
    "fecha_fin": "2025-10-13",
    "resumen": {
      "total_ventas": 50,
      "monto_total": 5500.00,
      "promedio_venta": 110.00,
      "venta_minima": 50.00,
      "venta_maxima": 250.00
    },
    "ventas_por_dia": [
      {"fecha": "2025-10-06", "cantidad": 8, "total": 880.00},
      {"fecha": "2025-10-07", "cantidad": 10, "total": 1100.00},
      {"fecha": "2025-10-08", "cantidad": 7, "total": 770.00},
      {"fecha": "2025-10-09", "cantidad": 6, "total": 660.00},
      {"fecha": "2025-10-10", "cantidad": 5, "total": 550.00},
      {"fecha": "2025-10-11", "cantidad": 7, "total": 770.00},
      {"fecha": "2025-10-12", "cantidad": 4, "total": 440.00},
      {"fecha": "2025-10-13", "cantidad": 3, "total": 330.00}
    ],
    "productos_mas_vendidos": [
      {"producto": "Coca Cola 600ml", "cantidad": 50, "total": 750.00},
      {"producto": "Sabritas Original", "cantidad": 40, "total": 600.00},
      {"producto": "Agua Natural", "cantidad": 35, "total": 350.00}
    ],
    "ventas_por_metodo_pago": [
      {"metodo": "Efectivo", "cantidad": 30, "total": 3300.00},
      {"metodo": "Tarjeta de Crédito", "cantidad": 15, "total": 1650.00},
      {"metodo": "Tarjeta de Débito", "cantidad": 5, "total": 550.00}
    ],
    "ventas_por_cajero": [
      {"cajero": "Juan Pérez", "cantidad": 20, "total": 2200.00},
      {"cajero": "María López", "cantidad": 30, "total": 3300.00}
    ]
  }
}
```

### Uso en Frontend
```javascript
// Obtener reporte de última semana
async function obtenerReporteVentas() {
  const fechaFin = new Date().toISOString().split('T')[0];
  const fechaInicio = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  
  const response = await fetch(
    `http://localhost:5000/api/reportes/ventas?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`
  );
  const data = await response.json();
  
  if (data.success) {
    // Mostrar resumen
    document.getElementById('total-ventas').textContent = data.data.resumen.total_ventas;
    document.getElementById('monto-total').textContent = `$${data.data.resumen.monto_total}`;
    
    // Crear gráfica con Chart.js
    crearGraficaVentas(data.data.ventas_por_dia);
  }
}

function crearGraficaVentas(ventasPorDia) {
  const ctx = document.getElementById('grafica-ventas').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ventasPorDia.map(v => v.fecha),
      datasets: [{
        label: 'Ventas Diarias',
        data: ventasPorDia.map(v => v.total),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    }
  });
}
```

---

## 📦 Reporte de Inventario

### Petición
```http
GET http://localhost:5000/api/reportes/inventario
```

### Respuesta
```json
{
  "success": true,
  "data": {
    "resumen": {
      "total_productos": 150,
      "valor_inventario": 15000.00,
      "valor_venta_potencial": 22500.00,
      "productos_stock_bajo": 5,
      "productos_sin_stock": 2
    },
    "productos_por_categoria": [
      {
        "categoria": "Bebidas",
        "cantidad": 50,
        "stock_total": 500,
        "valor": 7500.00
      },
      {
        "categoria": "Snacks",
        "cantidad": 30,
        "stock_total": 300,
        "valor": 4500.00
      },
      {
        "categoria": "Lácteos",
        "cantidad": 40,
        "stock_total": 200,
        "valor": 2000.00
      }
    ],
    "productos_stock_bajo": [
      {
        "producto_id": 1,
        "codigo_barras": "7501234567890",
        "nombre": "Coca Cola 600ml",
        "stock_actual": 5,
        "stock_minimo": 10,
        "categoria": "Bebidas"
      },
      {
        "producto_id": 3,
        "codigo_barras": "7501234567892",
        "nombre": "Sabritas Original",
        "stock_actual": 8,
        "stock_minimo": 15,
        "categoria": "Snacks"
      }
    ],
    "productos_sin_stock": [
      {
        "producto_id": 5,
        "codigo_barras": "7501234567894",
        "nombre": "Agua Mineral",
        "categoria": "Bebidas"
      }
    ]
  }
}
```

### Uso en Frontend
```javascript
async function obtenerReporteInventario() {
  const response = await fetch('http://localhost:5000/api/reportes/inventario');
  const data = await response.json();
  
  if (data.success) {
    // Mostrar alertas de stock bajo
    const stockBajo = data.data.productos_stock_bajo.length;
    if (stockBajo > 0) {
      mostrarAlerta(`⚠️ ${stockBajo} productos con stock bajo`);
    }
    
    // Renderizar tabla de productos con stock bajo
    renderizarTablaStockBajo(data.data.productos_stock_bajo);
    
    // Crear gráfica de pastel por categoría
    crearGraficaCategorias(data.data.productos_por_categoria);
  }
}

function renderizarTablaStockBajo(productos) {
  const tbody = document.getElementById('tabla-stock-bajo');
  tbody.innerHTML = productos.map(p => `
    <tr class="text-danger">
      <td>${p.codigo_barras}</td>
      <td>${p.nombre}</td>
      <td>${p.stock_actual}</td>
      <td>${p.stock_minimo}</td>
      <td>${p.categoria}</td>
      <td><button class="btn btn-sm btn-primary" onclick="reabastecer(${p.producto_id})">Reabastecer</button></td>
    </tr>
  `).join('');
}
```

---

## 🛒 Reporte de Compras Mensual

### Petición
```http
GET http://localhost:5000/api/reportes/compras?fecha_inicio=2025-09-13&fecha_fin=2025-10-13
```

### Respuesta
```json
{
  "success": true,
  "data": {
    "fecha_inicio": "2025-09-13",
    "fecha_fin": "2025-10-13",
    "resumen": {
      "total_compras": 20,
      "monto_total": 10000.00,
      "promedio_compra": 500.00
    },
    "compras_por_proveedor": [
      {
        "proveedor": "Coca Cola FEMSA",
        "cantidad": 10,
        "total": 5000.00
      },
      {
        "proveedor": "Sabritas",
        "cantidad": 7,
        "total": 3500.00
      },
      {
        "proveedor": "Grupo Bimbo",
        "cantidad": 3,
        "total": 1500.00
      }
    ],
    "productos_mas_comprados": [
      {"producto": "Coca Cola 600ml", "cantidad": 200, "total": 2000.00},
      {"producto": "Sabritas Original", "cantidad": 150, "total": 1500.00},
      {"producto": "Pan Blanco", "cantidad": 100, "total": 800.00}
    ]
  }
}
```

---

## 📄 Generar PDF con jsPDF

### Instalación
```bash
npm install jspdf jspdf-autotable
# o
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js"></script>
```

### Ejemplo Completo - PDF Reporte de Ventas
```javascript
async function generarPDFVentas() {
  // Obtener datos del reporte
  const fechaFin = new Date().toISOString().split('T')[0];
  const fechaInicio = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  
  const response = await fetch(
    `http://localhost:5000/api/reportes/ventas?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`
  );
  const result = await response.json();
  
  if (!result.success) {
    alert('Error al generar reporte');
    return;
  }
  
  const data = result.data;
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  
  // Header
  doc.setFontSize(20);
  doc.setTextColor(40);
  doc.text('REVENGE POS', 14, 20);
  
  doc.setFontSize(16);
  doc.text('Reporte de Ventas', 14, 30);
  
  doc.setFontSize(11);
  doc.setTextColor(100);
  doc.text(`Periodo: ${data.fecha_inicio} al ${data.fecha_fin}`, 14, 38);
  doc.text(`Generado: ${new Date().toLocaleString('es-MX')}`, 14, 44);
  
  // Línea separadora
  doc.setDrawColor(200);
  doc.line(14, 48, 196, 48);
  
  // Resumen
  doc.setFontSize(14);
  doc.setTextColor(40);
  doc.text('Resumen General', 14, 56);
  
  doc.setFontSize(10);
  doc.setTextColor(60);
  const yStart = 64;
  doc.text(`Total de Ventas: ${data.resumen.total_ventas}`, 14, yStart);
  doc.text(`Monto Total: $${data.resumen.monto_total.toFixed(2)}`, 14, yStart + 6);
  doc.text(`Promedio por Venta: $${data.resumen.promedio_venta.toFixed(2)}`, 14, yStart + 12);
  doc.text(`Venta Mínima: $${data.resumen.venta_minima.toFixed(2)}`, 14, yStart + 18);
  doc.text(`Venta Máxima: $${data.resumen.venta_maxima.toFixed(2)}`, 14, yStart + 24);
  
  // Tabla: Productos Más Vendidos
  doc.setFontSize(14);
  doc.setTextColor(40);
  doc.text('Productos Más Vendidos', 14, yStart + 34);
  
  doc.autoTable({
    startY: yStart + 38,
    head: [['Producto', 'Cantidad', 'Total']],
    body: data.productos_mas_vendidos.map(p => [
      p.producto,
      p.cantidad.toString(),
      `$${p.total.toFixed(2)}`
    ]),
    theme: 'grid',
    headStyles: { fillColor: [37, 99, 235] },
  });
  
  // Tabla: Ventas por Método de Pago
  const finalY1 = doc.lastAutoTable.finalY + 10;
  doc.setFontSize(14);
  doc.text('Ventas por Método de Pago', 14, finalY1);
  
  doc.autoTable({
    startY: finalY1 + 4,
    head: [['Método', 'Cantidad', 'Total']],
    body: data.ventas_por_metodo_pago.map(m => [
      m.metodo,
      m.cantidad.toString(),
      `$${m.total.toFixed(2)}`
    ]),
    theme: 'grid',
    headStyles: { fillColor: [16, 185, 129] },
  });
  
  // Tabla: Ventas por Cajero
  const finalY2 = doc.lastAutoTable.finalY + 10;
  doc.setFontSize(14);
  doc.text('Ventas por Cajero', 14, finalY2);
  
  doc.autoTable({
    startY: finalY2 + 4,
    head: [['Cajero', 'Ventas', 'Total']],
    body: data.ventas_por_cajero.map(c => [
      c.cajero,
      c.cantidad.toString(),
      `$${c.total.toFixed(2)}`
    ]),
    theme: 'grid',
    headStyles: { fillColor: [245, 158, 11] },
  });
  
  // Footer
  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setTextColor(150);
    doc.text(
      `Página ${i} de ${pageCount}`,
      doc.internal.pageSize.width / 2,
      doc.internal.pageSize.height - 10,
      { align: 'center' }
    );
  }
  
  // Guardar PDF
  doc.save(`reporte-ventas-${fechaInicio}-${fechaFin}.pdf`);
}
```

### Ejemplo - PDF Reporte de Inventario
```javascript
async function generarPDFInventario() {
  const response = await fetch('http://localhost:5000/api/reportes/inventario');
  const result = await response.json();
  
  if (!result.success) {
    alert('Error al generar reporte');
    return;
  }
  
  const data = result.data;
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  
  // Header
  doc.setFontSize(20);
  doc.text('REVENGE POS', 14, 20);
  doc.setFontSize(16);
  doc.text('Reporte de Inventario', 14, 30);
  doc.setFontSize(10);
  doc.text(`Generado: ${new Date().toLocaleString('es-MX')}`, 14, 38);
  
  // Resumen
  doc.setFontSize(14);
  doc.text('Resumen General', 14, 50);
  doc.setFontSize(10);
  doc.text(`Total Productos: ${data.resumen.total_productos}`, 14, 58);
  doc.text(`Valor Inventario: $${data.resumen.valor_inventario.toFixed(2)}`, 14, 64);
  doc.text(`Productos con Stock Bajo: ${data.resumen.productos_stock_bajo}`, 14, 70);
  doc.text(`Productos Sin Stock: ${data.resumen.productos_sin_stock}`, 14, 76);
  
  // Tabla: Productos con Stock Bajo (si hay)
  if (data.productos_stock_bajo.length > 0) {
    doc.setFontSize(14);
    doc.setTextColor(220, 38, 38); // Rojo
    doc.text('⚠️ Productos con Stock Bajo', 14, 86);
    
    doc.autoTable({
      startY: 90,
      head: [['Código', 'Producto', 'Stock', 'Mínimo', 'Categoría']],
      body: data.productos_stock_bajo.map(p => [
        p.codigo_barras,
        p.nombre,
        p.stock_actual.toString(),
        p.stock_minimo.toString(),
        p.categoria
      ]),
      theme: 'grid',
      headStyles: { fillColor: [220, 38, 38] },
    });
  }
  
  doc.save(`reporte-inventario-${Date.now()}.pdf`);
}
```

---

## 🎨 Integración en HTML

### Botones en la Vista de Reportes
```html
<div class="container mt-4">
  <h2>📊 Reportes</h2>
  
  <!-- Tabs -->
  <ul class="nav nav-tabs" id="reporteTabs" role="tablist">
    <li class="nav-item">
      <a class="nav-link active" data-bs-toggle="tab" href="#ventas">Ventas</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" data-bs-toggle="tab" href="#inventario">Inventario</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" data-bs-toggle="tab" href="#compras">Compras</a>
    </li>
  </ul>
  
  <!-- Tab Content -->
  <div class="tab-content mt-3">
    <!-- Reporte de Ventas -->
    <div class="tab-pane fade show active" id="ventas">
      <div class="row mb-3">
        <div class="col-md-4">
          <label>Fecha Inicio</label>
          <input type="date" id="fecha-inicio-ventas" class="form-control">
        </div>
        <div class="col-md-4">
          <label>Fecha Fin</label>
          <input type="date" id="fecha-fin-ventas" class="form-control">
        </div>
        <div class="col-md-4 d-flex align-items-end">
          <button class="btn btn-primary me-2" onclick="cargarReporteVentas()">
            📊 Generar Reporte
          </button>
          <button class="btn btn-danger" onclick="generarPDFVentas()">
            📄 Descargar PDF
          </button>
        </div>
      </div>
      
      <!-- Contenido del reporte -->
      <div id="contenido-reporte-ventas"></div>
      
      <!-- Canvas para gráfica -->
      <canvas id="grafica-ventas" width="400" height="200"></canvas>
    </div>
    
    <!-- Reporte de Inventario -->
    <div class="tab-pane fade" id="inventario">
      <button class="btn btn-primary me-2" onclick="cargarReporteInventario()">
        📦 Generar Reporte
      </button>
      <button class="btn btn-danger" onclick="generarPDFInventario()">
        📄 Descargar PDF
      </button>
      
      <div id="contenido-reporte-inventario" class="mt-3"></div>
    </div>
    
    <!-- Reporte de Compras -->
    <div class="tab-pane fade" id="compras">
      <div class="row mb-3">
        <div class="col-md-4">
          <label>Fecha Inicio</label>
          <input type="date" id="fecha-inicio-compras" class="form-control">
        </div>
        <div class="col-md-4">
          <label>Fecha Fin</label>
          <input type="date" id="fecha-fin-compras" class="form-control">
        </div>
        <div class="col-md-4 d-flex align-items-end">
          <button class="btn btn-primary me-2" onclick="cargarReporteCompras()">
            📊 Generar Reporte
          </button>
          <button class="btn btn-danger" onclick="generarPDFCompras()">
            📄 Descargar PDF
          </button>
        </div>
      </div>
      
      <div id="contenido-reporte-compras"></div>
    </div>
  </div>
</div>
```

---

## ✅ Resumen

**Endpoints de Reportes Agregados al Backend:**
- ✅ `GET /api/reportes/ventas` - Reporte completo de ventas
- ✅ `GET /api/reportes/inventario` - Estado del inventario
- ✅ `GET /api/reportes/compras` - Reporte de compras

**Listo para usar en el Frontend:**
- Obtener datos procesados desde el backend
- Generar PDFs con jsPDF
- Crear gráficas con Chart.js
- Tablas con alertas visuales

🚀 **El backend ya está preparado para reportes completos!**
