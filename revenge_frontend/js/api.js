// API Helper Functions

// Hacer llamada a la API
async function apiCall(url, options = {}) {
  try {
    const token = obtenerToken();
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers
    });

    const data = await response.json();

    // Si hay error 401, redirigir al login
    if (response.status === 401) {
      mostrarToast('Sesión expirada. Por favor inicia sesión nuevamente.', 'warning');
      setTimeout(() => {
        cerrarSesion();
      }, 2000);
      return { success: false, data: null };
    }

    return { success: response.ok, data };
  } catch (error) {
    console.error('Error en API call:', error);
    mostrarToast('Error de conexión con el servidor', 'danger');
    return { success: false, data: null };
  }
}

// GET request
async function apiGet(url) {
  return await apiCall(url, { method: 'GET' });
}

// POST request
async function apiPost(url, body) {
  return await apiCall(url, {
    method: 'POST',
    body: JSON.stringify(body)
  });
}

// PUT request
async function apiPut(url, body) {
  return await apiCall(url, {
    method: 'PUT',
    body: JSON.stringify(body)
  });
}

// DELETE request
async function apiDelete(url) {
  return await apiCall(url, { method: 'DELETE' });
}

// Mostrar mensaje toast
function mostrarToast(mensaje, tipo = 'info') {
  // Crear elemento toast
  const toast = document.createElement('div');
  toast.className = `toast ${tipo}`;
  toast.textContent = mensaje;
  
  // Agregar al body
  document.body.appendChild(toast);
  
  // Remover después de 3 segundos
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, 3000);
}

// Mostrar spinner de carga
function mostrarLoading(elemento) {
  if (elemento) {
    elemento.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
  }
}

// Formatear moneda
function formatearMoneda(valor) {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN'
  }).format(valor);
}

// Formatear fecha
function formatearFecha(fecha) {
  return new Date(fecha).toLocaleString('es-MX', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Confirmar acción
function confirmar(mensaje) {
  return confirm(mensaje);
}

// Agregar estilo para toast si no existe
if (!document.querySelector('style[data-toast]')) {
  const style = document.createElement('style');
  style.setAttribute('data-toast', 'true');
  style.textContent = `
    .toast {
      position: fixed;
      bottom: 20px;
      right: 20px;
      padding: 1rem 1.5rem;
      border-radius: 8px;
      color: white;
      font-weight: 500;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      animation: slideIn 0.3s ease-out;
      z-index: 10000;
      max-width: 400px;
    }
    .toast.success { background-color: #10b981; }
    .toast.danger { background-color: #ef4444; }
    .toast.warning { background-color: #f59e0b; }
    .toast.info { background-color: #3b82f6; }
    
    @keyframes slideIn {
      from { transform: translateX(400px); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
      from { transform: translateX(0); opacity: 1; }
      to { transform: translateX(400px); opacity: 0; }
    }
  `;
  document.head.appendChild(style);
}
