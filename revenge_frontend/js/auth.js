// Autenticación y Gestión de Sesión

// Guardar usuario en sessionStorage
function guardarUsuario(usuario) {
  sessionStorage.setItem('usuario', JSON.stringify(usuario));
  if (usuario.token) {
    sessionStorage.setItem('token', usuario.token);
  }
}

// Obtener usuario de sessionStorage
function obtenerUsuario() {
  const usuarioStr = sessionStorage.getItem('usuario');
  return usuarioStr ? JSON.parse(usuarioStr) : null;
}

// Obtener token
function obtenerToken() {
  return sessionStorage.getItem('token');
}

// Verificar si hay sesión activa
function verificarSesion() {
  const usuario = obtenerUsuario();
  if (!usuario || !obtenerToken()) {
    window.location.href = 'index.html';
    return null;
  }
  return usuario;
}

// Cerrar sesión
function cerrarSesion() {
  sessionStorage.clear();
  window.location.href = 'index.html';
}

// Login
async function login(email, password) {
  try {
    const response = await fetch(ENDPOINTS.auth.login, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok && data.success) {
      guardarUsuario(data.data);
      return { success: true, data: data.data };
    } else {
      return { success: false, message: data.message || 'Error al iniciar sesión' };
    }
  } catch (error) {
    console.error('Error en login:', error);
    return { success: false, message: 'Error de conexión con el servidor' };
  }
}

// Verificar si el usuario tiene un rol específico
function tieneRol(rolId) {
  const usuario = obtenerUsuario();
  return usuario && usuario.rol_id === rolId;
}

// Verificar si es administrador
function esAdministrador() {
  return tieneRol(ROLES.ADMINISTRADOR);
}

// Verificar si puede vender (Admin o Cajero)
function puedeVender() {
  const usuario = obtenerUsuario();
  return usuario && (usuario.rol_id === ROLES.ADMINISTRADOR || usuario.rol_id === ROLES.CAJERO);
}

// Verificar si puede gestionar inventario (Admin o Almacenista)
function puedeGestionarInventario() {
  const usuario = obtenerUsuario();
  return usuario && (usuario.rol_id === ROLES.ADMINISTRADOR || usuario.rol_id === ROLES.ALMACENISTA);
}
