// Productos Script

let usuario = null;

// Variables globales
let productosData = [];
let categoriasData = [];
let proveedoresData = [];
let productoEditando = null;

// Inicializar
window.addEventListener('DOMContentLoaded', async () => {
  // Verificar sesión y permisos
  usuario = verificarSesion();
  if (!puedeGestionarInventario()) {
    alert('No tienes permisos para gestionar productos');
    window.location.href = 'dashboard.html';
    return;
  }

  // El menú y usuario ya se cargan en menu.js
  await Promise.all([
    cargarCategorias(),
    cargarProveedores(),
    cargarProductos()
  ]);
});

// Cargar categorías
async function cargarCategorias() {
  try {
    const response = await apiGet(ENDPOINTS.categorias.list);
    if (response.success && response.data.data) {
      categoriasData = response.data.data;
      console.log('🔍 Estructura de categoría:', JSON.stringify(categoriasData[0], null, 2));
      
      // Llenar solo el select de filtro (que sí existe en el DOM inicial)
      const selectFilter = document.getElementById('filterCategoria');
      if (selectFilter) {
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Todas';
        selectFilter.innerHTML = '';
        selectFilter.appendChild(defaultOption);
        
        categoriasData.forEach(cat => {
          // No filtrar por activo en el select de filtro, mostrar todas
          const option = document.createElement('option');
          option.value = cat.id;
          option.textContent = cat.nombre;
          selectFilter.appendChild(option);
          console.log(`📂 Categoría agregada: ID=${option.value}, Nombre=${cat.nombre}`);
        });
      }
      
      console.log(`✅ ${categoriasData.length} categorías cargadas`);
    } else {
      console.error('❌ Error al cargar categorías:', response.message);
      mostrarToast('Error al cargar categorías', 'danger');
    }
  } catch (error) {
    console.error('❌ Error en cargarCategorias:', error);
    mostrarToast('Error al cargar categorías', 'danger');
  }
}

// Cargar proveedores
async function cargarProveedores() {
  try {
    const response = await apiGet(ENDPOINTS.proveedores.list);
    if (response.success && response.data.data) {
      proveedoresData = response.data.data;
      console.log('🔍 Estructura de proveedor:', proveedoresData[0]);
      
      console.log(`✅ ${proveedoresData.length} proveedores cargados`);
    } else {
      console.error('❌ Error al cargar proveedores:', response.message);
      mostrarToast('Error al cargar proveedores', 'danger');
    }
  } catch (error) {
    console.error('❌ Error en cargarProveedores:', error);
    mostrarToast('Error al cargar proveedores', 'danger');
  }
}

// Cargar productos
async function cargarProductos() {
  console.log('🔄 Cargando productos...');
  document.getElementById('loadingProductos').style.display = 'block';
  document.getElementById('tablaProductos').style.display = 'none';

  // Agregar timestamp para evitar caché
  const timestamp = new Date().getTime();
  const response = await apiGet(`${ENDPOINTS.productos.list}?_t=${timestamp}`);
  console.log('📡 Respuesta de cargarProductos:', response);

  document.getElementById('loadingProductos').style.display = 'none';
  document.getElementById('tablaProductos').style.display = 'block';

  if (response.success && response.data.data) {
    productosData = response.data.data;
    console.log('✅ Productos cargados:', productosData.length);
    
    // Normalizar campos de stock y estado
    productosData.forEach(p => {
      p.producto_id = p.producto_id || p.id;
      p.categoria_id = p.categoria_id; // Ya viene del backend
      p.stock_actual = p.stock_actual || p.stock || 0;
      p.stock_minimo = p.stock_minimo || p.stock_min || 0;
      // Normalizar activo - si no existe o es null, considerarlo activo por defecto
      p.activo = p.activo !== undefined && p.activo !== null ? p.activo : true;
    });
    
    console.log('🔍 Ejemplo producto normalizado:', JSON.stringify(productosData[0], null, 2));
    console.log('📊 Total productos cargados:', productosData.length);
    
    mostrarProductos(productosData);
  } else {
    console.error('❌ Error en respuesta:', response);
    mostrarToast('Error al cargar productos', 'danger');
  }
}

// Mostrar productos en tabla
function mostrarProductos(productos) {
  const tbody = document.getElementById('productosTableBody');
  
  if (productos.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" class="text-center">No hay productos</td></tr>';
    return;
  }

  tbody.innerHTML = productos.map(prod => {
    const stockBajo = prod.stock_actual <= prod.stock_minimo;
    const stockClass = stockBajo ? 'text-danger' : '';
    const estadoBadge = prod.activo 
      ? '<span class="badge badge-success">Activo</span>'
      : '<span class="badge badge-secondary">Inactivo</span>';

    return `
      <tr>
        <td>${prod.codigo_barras}</td>
        <td><strong>${prod.nombre}</strong></td>
        <td>${prod.categoria_nombre || 'Sin categoría'}</td>
        <td>${formatearMoneda(prod.precio_compra)}</td>
        <td><strong>${formatearMoneda(prod.precio_venta)}</strong></td>
        <td class="${stockClass}">
          <strong>${prod.stock_actual}</strong>
          ${stockBajo ? '<i class="fas fa-exclamation-triangle text-warning"></i>' : ''}
          <small>(Min: ${prod.stock_minimo})</small>
        </td>
        <td>${estadoBadge}</td>
        <td>
          <button onclick="editarProducto(${prod.producto_id})" class="btn btn-sm btn-primary" title="Editar">
            <i class="fas fa-edit"></i>
          </button>
          <button onclick="toggleEstadoProducto(${prod.producto_id}, ${prod.activo})" 
                  class="btn btn-sm ${prod.activo ? 'btn-warning' : 'btn-success'}" 
                  title="${prod.activo ? 'Desactivar' : 'Activar'}">
            <i class="fas fa-${prod.activo ? 'ban' : 'check'}"></i>
          </button>
          ${!prod.activo ? `
            <button onclick="eliminarProducto(${prod.producto_id})" class="btn btn-sm btn-danger" title="Eliminar">
              <i class="fas fa-trash"></i>
            </button>
          ` : ''}
        </td>
      </tr>
    `;
  }).join('');
}

// Buscar productos
function buscarProductos() {
  const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
  
  if (!searchTerm) {
    mostrarProductos(productosData);
    return;
  }

  const resultados = productosData.filter(prod => 
    prod.nombre.toLowerCase().includes(searchTerm) ||
    prod.codigo_barras.toLowerCase().includes(searchTerm) ||
    (prod.descripcion && prod.descripcion.toLowerCase().includes(searchTerm))
  );

  mostrarProductos(resultados);
  mostrarToast(`${resultados.length} productos encontrados`, 'info');
}

// Filtrar productos
function filtrarProductos() {
  const categoriaId = document.getElementById('filterCategoria').value;
  const estado = document.getElementById('filterEstado').value;
  const stock = document.getElementById('filterStock').value;

  console.log('🔍 Aplicando filtros:', { categoriaId, estado, stock });

  let filtrados = [...productosData];

  if (categoriaId) {
    console.log('📂 Filtrando por categoría:', categoriaId);
    filtrados = filtrados.filter(p => {
      const match = p.categoria_id == categoriaId;
      if (!match) console.log('❌ Producto no coincide:', p.nombre, 'categoria_id:', p.categoria_id);
      return match;
    });
    console.log(`✅ ${filtrados.length} productos después de filtrar por categoría`);
  }

  if (estado !== '') {
    console.log('🔘 Filtrando por estado:', estado, 'tipo:', typeof estado);
    // Convertir el valor del filtro a booleano o número según lo que tenga el producto
    filtrados = filtrados.filter(p => {
      console.log(`Comparando producto "${p.nombre}": activo=${p.activo} (${typeof p.activo}) con filtro=${estado}`);
      // Manejar diferentes formatos de activo
      const productoActivo = p.activo === true || p.activo === 1 || p.activo === '1';
      const filtroActivo = estado === '1' || estado === 'true' || estado === true;
      const match = productoActivo === filtroActivo;
      return match;
    });
    console.log(`✅ ${filtrados.length} productos después de filtrar por estado`);
  }

  if (stock === 'bajo') {
    console.log('📉 Filtrando stock bajo');
    filtrados = filtrados.filter(p => p.stock_actual <= p.stock_minimo);
    console.log(`✅ ${filtrados.length} productos con stock bajo`);
  } else if (stock === 'alto') {
    console.log('📈 Filtrando stock alto');
    filtrados = filtrados.filter(p => p.stock_actual > p.stock_minimo);
    console.log(`✅ ${filtrados.length} productos con stock alto`);
  }

  console.log(`📊 Total filtrados: ${filtrados.length} de ${productosData.length}`);
  mostrarProductos(filtrados);
}

// Limpiar filtros
function limpiarFiltros() {
  document.getElementById('filterCategoria').value = '';
  document.getElementById('filterEstado').value = '';
  document.getElementById('filterStock').value = '';
  document.getElementById('searchInput').value = '';
  mostrarProductos(productosData);
}

// Abrir modal para nuevo producto
function abrirModalProducto() {
  console.log('🚀 Abriendo modal producto...');
  console.log('📊 Estado datos:', {
    categorias: categoriasData.length,
    proveedores: proveedoresData.length
  });
  
  productoEditando = null;
  document.getElementById('modalTitle').innerHTML = '<i class="fas fa-box"></i> Nuevo Producto';
  document.getElementById('formProducto').reset();
  document.getElementById('productoId').value = '';
  document.getElementById('activo').checked = true;
  
  // Re-llenar los selects con los datos cargados
  llenarSelectCategorias();
  llenarSelectProveedores();
  
  document.getElementById('modalProducto').classList.remove('hidden');
}

// Función auxiliar para llenar select de categorías
function llenarSelectCategorias() {
  console.log('🔧 llenarSelectCategorias() - Datos disponibles:', categoriasData.length);
  const selectForm = document.getElementById('categoria_id');
  console.log('🔧 Select encontrado:', selectForm ? 'SÍ' : 'NO');
  
  if (selectForm && categoriasData.length > 0) {
    // Preservar la opción por defecto
    const defaultOption = selectForm.querySelector('option[value=""]');
    selectForm.innerHTML = '';
    if (defaultOption) {
      selectForm.appendChild(defaultOption.cloneNode(true));
    } else {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'Seleccionar...';
      selectForm.appendChild(opt);
    }
    
    // Agregar categorías
    let agregadas = 0;
    categoriasData.forEach(cat => {
      console.log('📦 Categoría completa:', cat);
      console.log('  - cat.id:', cat.id);
      console.log('  - Object.keys(cat):', Object.keys(cat));
      
      const option = document.createElement('option');
      option.value = cat.id;
      option.textContent = cat.nombre;
      selectForm.appendChild(option);
      agregadas++;
    });
    console.log(`✅ ${agregadas} categorías agregadas al select`);
  } else {
    console.warn('⚠️ No se pudo llenar categorías:', {
      selectExists: !!selectForm,
      dataLength: categoriasData.length
    });
  }
}

// Función auxiliar para llenar select de proveedores
function llenarSelectProveedores() {
  console.log('🔧 llenarSelectProveedores() - Datos disponibles:', proveedoresData.length);
  const selectForm = document.getElementById('proveedor_id');
  console.log('🔧 Select encontrado:', selectForm ? 'SÍ' : 'NO');
  
  if (selectForm && proveedoresData.length > 0) {
    // Preservar la opción por defecto
    const defaultOption = selectForm.querySelector('option[value=""]');
    selectForm.innerHTML = '';
    if (defaultOption) {
      selectForm.appendChild(defaultOption.cloneNode(true));
    } else {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'Seleccionar...';
      selectForm.appendChild(opt);
    }
    
    // Agregar proveedores
    let agregados = 0;
    proveedoresData.forEach(prov => {
      console.log('🏪 Proveedor completo:', prov);
      console.log('  - prov.proveedor_id:', prov.proveedor_id);
      console.log('  - prov.id:', prov.id);
      console.log('  - Object.keys(prov):', Object.keys(prov));
      
      const option = document.createElement('option');
      option.value = prov.proveedor_id || prov.id; // Intentar ambos nombres
      option.textContent = prov.nombre;
      selectForm.appendChild(option);
      agregados++;
    });
    console.log(`✅ ${agregados} proveedores agregados al select`);
  } else {
    console.warn('⚠️ No se pudo llenar proveedores:', {
      selectExists: !!selectForm,
      dataLength: proveedoresData.length
    });
  }
}

// Editar producto
async function editarProducto(id) {
  console.log('🔧 Botón EDITAR PRODUCTO clickeado - ID:', id);
  const response = await apiGet(`${ENDPOINTS.productos.get}/${id}`);
  console.log('📡 Respuesta de API editar:', response);
  
  if (response.success && response.data.data) {
    productoEditando = response.data.data;
    console.log('✅ Producto cargado para editar:', productoEditando);
    console.log('  - producto.id:', productoEditando.id);
    console.log('  - producto.producto_id:', productoEditando.producto_id);
    
    const prodId = productoEditando.id || productoEditando.producto_id;
    console.log('  - ID a usar:', prodId);
    
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-edit"></i> Editar Producto';
    document.getElementById('productoId').value = prodId;
    document.getElementById('nombre').value = productoEditando.nombre;
    document.getElementById('codigo_barras').value = productoEditando.codigo_barras;
    
    // IMPORTANTE: Llenar los selects ANTES de establecer los valores
    console.log('🔄 Llenando selects de categorías y proveedores...');
    llenarSelectCategorias();
    llenarSelectProveedores();
    
    // Ahora sí establecer los valores seleccionados
    document.getElementById('categoria_id').value = productoEditando.categoria_id || '';
    document.getElementById('proveedor_id').value = productoEditando.proveedor_id || '';
    console.log('✅ Categoría seleccionada:', productoEditando.categoria_id);
    console.log('✅ Proveedor seleccionado:', productoEditando.proveedor_id);
    
    document.getElementById('descripcion').value = productoEditando.descripcion || '';
    document.getElementById('precio_compra').value = productoEditando.precio_compra;
    document.getElementById('precio_venta').value = productoEditando.precio_venta;
    document.getElementById('stock_actual').value = productoEditando.stock_actual;
    document.getElementById('stock_minimo').value = productoEditando.stock_minimo;
    document.getElementById('activo').checked = productoEditando.activo;
    
    console.log('📝 Campo productoId establecido a:', document.getElementById('productoId').value);
    document.getElementById('modalProducto').classList.remove('hidden');
    console.log('🎯 Modal abierto para editar producto');
  } else {
    console.error('❌ Error al cargar producto para editar');
  }
}

// Guardar producto
async function guardarProducto(event) {
  event.preventDefault();
  
  const productoId = document.getElementById('productoId').value;
  const usuario = JSON.parse(sessionStorage.getItem('usuario'));
  
  // DEBUG: Ver valor del select ANTES de parsear
  const selectCategoria = document.getElementById('categoria_id');
  console.log('🔍 Select categoría:', selectCategoria);
  console.log('🔍 Valor del select:', selectCategoria.value);
  console.log('🔍 Todas las opciones:', Array.from(selectCategoria.options).map(o => ({value: o.value, text: o.text})));
  
  // Validar que se haya seleccionado categoría
  const categoriaId = parseInt(selectCategoria.value);
  console.log('🔍 categoriaId parseado:', categoriaId, '- isNaN:', isNaN(categoriaId));
  
  if (!categoriaId || isNaN(categoriaId)) {
    mostrarToast('Debe seleccionar una categoría', 'warning');
    return;
  }
  
  const datos = {
    nombre: document.getElementById('nombre').value.trim(),
    codigo_barras: document.getElementById('codigo_barras').value.trim(),
    categoria_id: categoriaId,
    proveedor_id: parseInt(document.getElementById('proveedor_id').value) || null,
    descripcion: document.getElementById('descripcion').value.trim() || null,
    precio_compra: parseFloat(document.getElementById('precio_compra').value),
    precio_venta: parseFloat(document.getElementById('precio_venta').value),
    stock: parseInt(document.getElementById('stock_actual').value), // Backend espera 'stock'
    stock_minimo: parseInt(document.getElementById('stock_minimo').value),
    estado_id: document.getElementById('activo').checked ? 1 : 2, // 1=activo, 2=inactivo
    created_by: usuario ? usuario.id : null
  };
  
  console.log('📦 Datos a enviar:', datos);
  console.log('🔢 Stock específico:', {
    valorCampo: document.getElementById('stock_actual').value,
    parseado: parseInt(document.getElementById('stock_actual').value),
    enDatos: datos.stock
  });

  // Validaciones
  if (datos.precio_venta <= datos.precio_compra) {
    mostrarToast('El precio de venta debe ser mayor al precio de compra', 'warning');
    return;
  }

  let response;
  if (productoId) {
    // Actualizar
    console.log('➡️ Actualizando producto ID:', productoId);
    response = await apiPut(`${ENDPOINTS.productos.update}/${productoId}`, datos);
  } else {
    // Crear
    console.log('➡️ Creando nuevo producto');
    response = await apiPost(ENDPOINTS.productos.create, datos);
  }

  console.log('📡 Respuesta del servidor:', response);
  if (response.success) {
    console.log('✅ Guardado exitoso, recargando productos...');
    mostrarToast(
      productoId ? 'Producto actualizado correctamente' : 'Producto creado correctamente',
      'success'
    );
    cerrarModalProducto();
    await cargarProductos();
  } else {
    mostrarToast(response.data.message || 'Error al guardar producto', 'danger');
  }
}

// Cerrar modal
function cerrarModalProducto() {
  document.getElementById('modalProducto').classList.add('hidden');
  document.getElementById('formProducto').reset();
  productoEditando = null;
}

// Toggle estado del producto
async function toggleEstadoProducto(id, estadoActual) {
  console.log('🔄 Botón TOGGLE ESTADO clickeado - ID:', id, 'Estado actual:', estadoActual);
  const accion = estadoActual ? 'desactivar' : 'activar';
  console.log('  - Acción:', accion);
  
  if (!confirm(`¿Estás seguro de ${accion} este producto?`)) {
    console.log('❌ Usuario canceló la acción');
    return;
  }

  const response = await apiPut(`${ENDPOINTS.productos.update}/${id}`, {
    activo: !estadoActual
  });
  console.log('📡 Respuesta de API toggleEstado:', response);

  if (response.success) {
    console.log('✅ Estado actualizado correctamente');
    mostrarToast(`Producto ${accion === 'activar' ? 'activado' : 'desactivado'} correctamente`, 'success');
    await cargarProductos();
  } else {
    console.error('❌ Error al actualizar estado');
  }
}

// Eliminar producto
async function eliminarProducto(id) {
  console.log('🗑️ Botón ELIMINAR PRODUCTO clickeado - ID:', id);
  
  if (!confirm('¿Estás seguro de eliminar este producto? Esta acción no se puede deshacer.')) {
    console.log('❌ Usuario canceló la eliminación');
    return;
  }

  console.log('➡️ Procediendo a eliminar producto...');
  const response = await apiDelete(`${ENDPOINTS.productos.delete}/${id}`);
  console.log('📡 Respuesta de API eliminar:', response);

  if (response.success) {
    console.log('✅ Producto eliminado correctamente');
    mostrarToast('Producto eliminado correctamente', 'success');
    await cargarProductos();
  } else {
    console.error('❌ Error al eliminar producto:', response.data.message);
    mostrarToast(response.data.message || 'Error al eliminar producto', 'danger');
  }
}

// Cerrar modal con ESC
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    cerrarModalProducto();
  }
});
