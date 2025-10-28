// Configuración Global - Revenge POS

// URL base de la API
const API_BASE_URL = 'http://127.0.0.1:5000/api';

// IGV Perú (18%)
const IVA = 0.18;

// Roles de usuario
const ROLES = {
  ADMINISTRADOR: 1,
  CAJERO: 2,
  ALMACENISTA: 3
};

// Métodos de pago
const METODOS_PAGO = {
  EFECTIVO: 1,
  TARJETA_CREDITO: 2,
  TARJETA_DEBITO: 3,
  TRANSFERENCIA: 4
};

// Endpoints de la API
const ENDPOINTS = {
  auth: {
    login: `${API_BASE_URL}/auth/login`
  },
  productos: {
    list: `${API_BASE_URL}/productos`,
    get: `${API_BASE_URL}/productos`,
    create: `${API_BASE_URL}/productos`,
    update: `${API_BASE_URL}/productos`,
    delete: `${API_BASE_URL}/productos`,
    search: `${API_BASE_URL}/productos/buscar`,
    stockBajo: `${API_BASE_URL}/productos/stock-bajo`
  },
  categorias: {
    list: `${API_BASE_URL}/categorias`,
    get: `${API_BASE_URL}/categorias`,
    create: `${API_BASE_URL}/categorias`,
    update: `${API_BASE_URL}/categorias`,
    delete: `${API_BASE_URL}/categorias`
  },
  ventas: {
    list: `${API_BASE_URL}/ventas`,
    get: `${API_BASE_URL}/ventas`,
    create: `${API_BASE_URL}/ventas`,
    update: `${API_BASE_URL}/ventas`,
    delete: `${API_BASE_URL}/ventas`
  },
  compras: {
    list: `${API_BASE_URL}/compras`,
    get: `${API_BASE_URL}/compras`,
    create: `${API_BASE_URL}/compras`,
    update: `${API_BASE_URL}/compras`,
    delete: `${API_BASE_URL}/compras`
  },
  usuarios: {
    list: `${API_BASE_URL}/usuarios`,
    get: `${API_BASE_URL}/usuarios`,
    create: `${API_BASE_URL}/usuarios`,
    update: `${API_BASE_URL}/usuarios`,
    delete: `${API_BASE_URL}/usuarios`
  },
  proveedores: {
    list: `${API_BASE_URL}/proveedores`,
    get: `${API_BASE_URL}/proveedores`,
    create: `${API_BASE_URL}/proveedores`,
    update: `${API_BASE_URL}/proveedores`,
    delete: `${API_BASE_URL}/proveedores`
  },
  reportes: {
    ventas: `${API_BASE_URL}/reportes/ventas`,
    inventario: `${API_BASE_URL}/reportes/inventario`,
    compras: `${API_BASE_URL}/reportes/compras`
  }
};
