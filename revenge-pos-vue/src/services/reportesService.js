// services/reportesService.js
import api from './api'

export const reportesService = {
  /**
   * Obtener reporte de ventas
   * GET /api/reportes/ventas?fecha_desde=YYYY-MM-DD&fecha_hasta=YYYY-MM-DD
   */
  async getReporteVentas(fechaDesde, fechaHasta) {
    try {
      const response = await api.get('/reportes/ventas', {
        params: {
          fecha_desde: fechaDesde,
          fecha_hasta: fechaHasta
        }
      })
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener reporte de ventas' 
      }
    }
  },

  /**
   * Obtener reporte de inventario
   * GET /api/reportes/inventario
   */
  async getReporteInventario() {
    try {
      const response = await api.get('/reportes/inventario')
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener reporte de inventario' 
      }
    }
  },

  /**
   * Obtener reporte de compras
   * GET /api/reportes/compras?fecha_desde=YYYY-MM-DD&fecha_hasta=YYYY-MM-DD
   */
  async getReporteCompras(fechaDesde, fechaHasta) {
    try {
      const response = await api.get('/reportes/compras', {
        params: {
          fecha_desde: fechaDesde,
          fecha_hasta: fechaHasta
        }
      })
      return { success: true, data: response.data.data || response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al obtener reporte de compras' 
      }
    }
  },

  /**
   * Descargar PDF de reporte de ventas
   * GET /api/reportes/ventas/pdf?fecha_desde=YYYY-MM-DD&fecha_hasta=YYYY-MM-DD
   */
  async descargarVentasPDF(fechaDesde, fechaHasta) {
    try {
      const response = await api.get('/reportes/ventas/pdf', {
        params: {
          fecha_desde: fechaDesde,
          fecha_hasta: fechaHasta
        },
        responseType: 'blob'
      })
      
      // Crear URL del blob y descargar
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `reporte_ventas_${new Date().getTime()}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al descargar PDF de ventas' 
      }
    }
  },

  /**
   * Descargar PDF de reporte de compras
   * GET /api/reportes/compras/pdf?fecha_desde=YYYY-MM-DD&fecha_hasta=YYYY-MM-DD
   */
  async descargarComprasPDF(fechaDesde, fechaHasta) {
    try {
      const response = await api.get('/reportes/compras/pdf', {
        params: {
          fecha_desde: fechaDesde,
          fecha_hasta: fechaHasta
        },
        responseType: 'blob'
      })
      
      // Crear URL del blob y descargar
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `reporte_compras_${new Date().getTime()}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al descargar PDF de compras' 
      }
    }
  },

  /**
   * Descargar PDF de reporte de inventario
   * GET /api/reportes/inventario/pdf
   */
  async descargarInventarioPDF() {
    try {
      const response = await api.get('/reportes/inventario/pdf', {
        responseType: 'blob'
      })
      
      // Crear URL del blob y descargar
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `reporte_inventario_${new Date().getTime()}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error al descargar PDF de inventario' 
      }
    }
  }
}
