/**
 * Validar email
 */
export function validateEmail(email) {
  if (!email) return 'El email es requerido'
  
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!regex.test(email)) return 'Email inválido'
  
  return true
}

/**
 * Validar campo requerido
 */
export function validateRequired(value, fieldName = 'Este campo') {
  if (value === null || value === undefined || value === '') {
    return `${fieldName} es requerido`
  }
  return true
}

/**
 * Validar longitud mínima
 */
export function validateMinLength(value, min, fieldName = 'Este campo') {
  if (!value || value.length < min) {
    return `${fieldName} debe tener al menos ${min} caracteres`
  }
  return true
}

/**
 * Validar longitud máxima
 */
export function validateMaxLength(value, max, fieldName = 'Este campo') {
  if (value && value.length > max) {
    return `${fieldName} no debe exceder ${max} caracteres`
  }
  return true
}

/**
 * Validar número positivo
 */
export function validatePositiveNumber(value, fieldName = 'Este campo') {
  const num = parseFloat(value)
  if (isNaN(num) || num <= 0) {
    return `${fieldName} debe ser un número positivo`
  }
  return true
}

/**
 * Validar rango numérico
 */
export function validateRange(value, min, max, fieldName = 'Este campo') {
  const num = parseFloat(value)
  if (isNaN(num) || num < min || num > max) {
    return `${fieldName} debe estar entre ${min} y ${max}`
  }
  return true
}
