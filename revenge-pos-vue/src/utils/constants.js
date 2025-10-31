// Configuración de API
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
export const APP_NAME = import.meta.env.VITE_APP_NAME

// Impuestos
export const IVA = parseFloat(import.meta.env.VITE_IVA) || 0.18

// Roles de usuario
export const ROLES = {
  ADMINISTRADOR: 1,
  CAJERO: 2,
  ALMACENISTA: 3
}

export const ROLES_NOMBRES = {
  1: 'Administrador',
  2: 'Cajero',
  3: 'Almacenista'
}

// Métodos de pago
export const METODOS_PAGO = {
  EFECTIVO: 1,
  TARJETA_CREDITO: 2,
  TARJETA_DEBITO: 3,
  TRANSFERENCIA: 4,
  YAPE: 5,
  PLIN: 6
}

export const METODOS_PAGO_NOMBRES = {
  1: 'Efectivo',
  2: 'Tarjeta de Crédito',
  3: 'Tarjeta de Débito',
  4: 'Transferencia',
  5: 'Yape',
  6: 'Plin'
}

// Estados
export const ESTADOS = {
  ACTIVO: true,
  INACTIVO: false
}

// Colores corporativos
export const COLORS = {
  PRIMARY: '#0048A0',
  SECONDARY: '#FFD200',
  SUCCESS: '#28a745',
  DANGER: '#dc3545',
  WARNING: '#ffc107',
  INFO: '#17a2b8',
  LIGHT: '#f8f9fa',
  DARK: '#343a40'
}

// Configuración de paginación
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 25, 50, 100]
}

// Formatos
export const FORMATS = {
  DATE: 'DD/MM/YYYY',
  DATETIME: 'DD/MM/YYYY HH:mm',
  TIME: 'HH:mm',
  CURRENCY: 'S/.'
}
