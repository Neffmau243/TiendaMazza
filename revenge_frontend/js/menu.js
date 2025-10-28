// Menú Sidebar Compartido

function cargarMenuSidebar() {
  const usuario = obtenerUsuario();
  if (!usuario) return;

  const menu = document.getElementById('sidebarMenu');
  if (!menu) return;
  
  const menuItems = [
    {
      icon: 'fas fa-home',
      text: 'Dashboard',
      url: 'dashboard.html',
      roles: [ROLES.ADMINISTRADOR, ROLES.CAJERO, ROLES.ALMACENISTA]
    },
    {
      icon: 'fas fa-cash-register',
      text: 'Punto de Venta',
      url: 'punto-venta.html',
      roles: [ROLES.ADMINISTRADOR, ROLES.CAJERO]
    },
    {
      icon: 'fas fa-box',
      text: 'Productos',
      url: 'productos.html',
      roles: [ROLES.ADMINISTRADOR, ROLES.ALMACENISTA]
    },
    {
      icon: 'fas fa-tags',
      text: 'Categorías',
      url: 'categorias.html',
      roles: [ROLES.ADMINISTRADOR]
    },
    {
      icon: 'fas fa-receipt',
      text: 'Ventas',
      url: 'ventas.html',
      roles: [ROLES.ADMINISTRADOR, ROLES.CAJERO]
    },
    {
      icon: 'fas fa-truck',
      text: 'Compras',
      url: 'compras.html',
      roles: [ROLES.ADMINISTRADOR, ROLES.ALMACENISTA]
    },
    {
      icon: 'fas fa-users',
      text: 'Usuarios',
      url: 'usuarios.html',
      roles: [ROLES.ADMINISTRADOR]
    },
    {
      icon: 'fas fa-building',
      text: 'Proveedores',
      url: 'proveedores.html',
      roles: [ROLES.ADMINISTRADOR]
    },
    {
      icon: 'fas fa-chart-bar',
      text: 'Reportes',
      url: 'reportes.html',
      roles: [ROLES.ADMINISTRADOR]
    },
  ];

  menu.innerHTML = '';

  menuItems.forEach(item => {
    if (item.roles.includes(usuario.rol_id)) {
      const li = document.createElement('li');
      li.className = 'sidebar-item';
      
      const isActive = window.location.pathname.includes(item.url) ? 'active' : '';
      
      li.innerHTML = `
        <a href="${item.url}" class="sidebar-link ${isActive}">
          <i class="${item.icon}"></i>
          <span>${item.text}</span>
        </a>
      `;
      
      menu.appendChild(li);
    }
  });
}

// Inicializar información del usuario en el navbar
function cargarInfoUsuario() {
  const usuario = obtenerUsuario();
  if (!usuario) return;

  const userNameElement = document.getElementById('userName');
  const userRoleElement = document.getElementById('userRole');

  if (userNameElement) {
    userNameElement.textContent = usuario.nombre;
  }
  
  if (userRoleElement) {
    userRoleElement.textContent = usuario.rol_nombre;
  }
}

// Función para inicializar CUALQUIER página del sistema
function inicializarPagina() {
  // Verificar sesión
  const usuario = verificarSesion();
  if (!usuario) return;

  // Cargar menú y usuario
  cargarMenuSidebar();
  cargarInfoUsuario();
}

// Auto-ejecutar al cargar el DOM
window.addEventListener('DOMContentLoaded', inicializarPagina);
