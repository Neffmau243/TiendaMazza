/**
 * Formatear número como moneda
 */
export function formatCurrency(value, currency = 'S/.') {
  if (value === null || value === undefined) return `${currency} 0.00`
  
  const number = parseFloat(value)
  if (isNaN(number)) return `${currency} 0.00`
  
  return `${currency} ${number.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}`
}

/**
 * Formatear fecha
 */
export function formatDate(date, includeTime = false) {
  if (!date) return ''
  
  const d = new Date(date)
  if (isNaN(d.getTime())) return ''
  
  const day = String(d.getDate()).padStart(2, '0')
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const year = d.getFullYear()
  
  let formatted = `${day}/${month}/${year}`
  
  if (includeTime) {
    const hours = String(d.getHours()).padStart(2, '0')
    const minutes = String(d.getMinutes()).padStart(2, '0')
    formatted += ` ${hours}:${minutes}`
  }
  
  return formatted
}

/**
 * Formatear número con separadores de miles
 */
export function formatNumber(value) {
  if (value === null || value === undefined) return '0'
  
  const number = parseFloat(value)
  if (isNaN(number)) return '0'
  
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * Formatear porcentaje
 */
export function formatPercentage(value, decimals = 2) {
  if (value === null || value === undefined) return '0%'
  
  const number = parseFloat(value)
  if (isNaN(number)) return '0%'
  
  return `${(number * 100).toFixed(decimals)}%`
}

/**
 * Truncar texto
 */
export function truncate(text, length = 50) {
  if (!text) return ''
  if (text.length <= length) return text
  return `${text.substring(0, length)}...`
}
