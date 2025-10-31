<!-- views/ReportesView.vue -->
<template>
  <div class="reportes">
    <div class="page-header">
      <h1>Reportes y Estadísticas</h1>
      <p class="subtitle">Genera y exporta reportes detallados de tu negocio</p>
    </div>

    <!-- Navegación por Tabs -->
    <div class="tabs-navigation">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="['tab-button', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        <i :class="tab.icon"></i>
        <span>{{ tab.label }}</span>
      </button>
    </div>

    <!-- Contenido de los Tabs -->
    <div class="tab-content">
      <!-- Tab: Reporte de Ventas -->
      <div v-show="activeTab === 'ventas'" class="tab-panel">
        <BaseCard>
          <div class="reporte-header">
            <h2><i class="fas fa-chart-line"></i> Reporte de Ventas</h2>
            <p class="description">Analiza las ventas realizadas en un período específico</p>
          </div>
          
          <div class="reporte-filters">
            <BaseInput
              v-model="ventasFilters.fecha_inicio"
              type="date"
              label="Fecha Inicio"
            />
            <BaseInput
              v-model="ventasFilters.fecha_fin"
              type="date"
              label="Fecha Fin"
            />
            <div class="filter-actions">
              <BaseButton
                @click="exportarVentasPDF"
                variant="danger"
                icon="fa-file-pdf"
              >
                Exportar PDF
              </BaseButton>
              <BaseButton
                @click="exportarVentasExcel"
                variant="success"
                icon="fa-file-excel"
              >
                Exportar Excel
              </BaseButton>
            </div>
          </div>

          <div v-if="reporteVentas" class="reporte-content">
            <div class="stats-grid">
              <div class="stat-card stat-primary">
                <i class="fas fa-shopping-cart"></i>
                <div class="stat-info">
                  <span class="stat-label">Total Ventas</span>
                  <span class="stat-value">{{ reporteVentas.total_ventas || 0 }}</span>
                </div>
              </div>
              <div class="stat-card stat-success">
                <i class="fas fa-dollar-sign"></i>
                <div class="stat-info">
                  <span class="stat-label">Ingresos</span>
                  <span class="stat-value">{{ formatCurrency(reporteVentas.total_ingresos || 0) }}</span>
                </div>
              </div>
              <div class="stat-card stat-info">
                <i class="fas fa-chart-bar"></i>
                <div class="stat-info">
                  <span class="stat-label">Promedio</span>
                  <span class="stat-value">{{ formatCurrency(reporteVentas.promedio || 0) }}</span>
                </div>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- Tab: Reporte de Compras -->
      <div v-show="activeTab === 'compras'" class="tab-panel">
        <BaseCard>
          <div class="reporte-header">
            <h2><i class="fas fa-shopping-bag"></i> Reporte de Compras</h2>
            <p class="description">Revisa las compras realizadas a proveedores</p>
          </div>
          
          <div class="reporte-filters">
            <BaseInput
              v-model="comprasFilters.fecha_inicio"
              type="date"
              label="Fecha Inicio"
            />
            <BaseInput
              v-model="comprasFilters.fecha_fin"
              type="date"
              label="Fecha Fin"
            />
            <div class="filter-actions">
              <BaseButton
                @click="exportarComprasPDF"
                variant="danger"
                icon="fa-file-pdf"
              >
                Exportar PDF
              </BaseButton>
              <BaseButton
                @click="exportarComprasExcel"
                variant="success"
                icon="fa-file-excel"
              >
                Exportar Excel
              </BaseButton>
            </div>
          </div>

          <div v-if="reporteCompras" class="reporte-content">
            <div class="stats-grid">
              <div class="stat-card stat-warning">
                <i class="fas fa-truck"></i>
                <div class="stat-info">
                  <span class="stat-label">Total Compras</span>
                  <span class="stat-value">{{ reporteCompras.total_compras || 0 }}</span>
                </div>
              </div>
              <div class="stat-card stat-danger">
                <i class="fas fa-money-bill-wave"></i>
                <div class="stat-info">
                  <span class="stat-label">Gastos</span>
                  <span class="stat-value">{{ formatCurrency(reporteCompras.total_gastos || 0) }}</span>
                </div>
              </div>
              <div class="stat-card stat-secondary">
                <i class="fas fa-building"></i>
                <div class="stat-info">
                  <span class="stat-label">Proveedores</span>
                  <span class="stat-value">{{ reporteCompras.total_proveedores || 0 }}</span>
                </div>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- Tab: Reporte de Inventario -->
      <div v-show="activeTab === 'inventario'" class="tab-panel">
        <BaseCard>
          <div class="reporte-header">
            <h2><i class="fas fa-warehouse"></i> Reporte de Inventario</h2>
            <p class="description">Estado actual del inventario y productos con stock bajo</p>
          </div>
          
          <div class="inventory-actions">
            <BaseButton
              @click="exportarInventarioPDF"
              variant="danger"
              icon="fa-file-pdf"
            >
              Exportar PDF
            </BaseButton>
            <BaseButton
              @click="exportarInventarioExcel"
              variant="success"
              icon="fa-file-excel"
            >
              Exportar Excel
            </BaseButton>
          </div>

          <div v-if="reporteInventario" class="reporte-content">
            <div class="stats-grid">
              <div class="stat-card stat-primary">
                <i class="fas fa-box"></i>
                <div class="stat-info">
                  <span class="stat-label">Total Productos</span>
                  <span class="stat-value">{{ reporteInventario.total_productos || 0 }}</span>
                </div>
              </div>
              <div class="stat-card stat-success">
                <i class="fas fa-dollar-sign"></i>
                <div class="stat-info">
                  <span class="stat-label">Valor Inventario</span>
                  <span class="stat-value">{{ formatCurrency(reporteInventario.valor_total || 0) }}</span>
                </div>
              </div>
              <div class="stat-card stat-warning">
                <i class="fas fa-exclamation-triangle"></i>
                <div class="stat-info">
                  <span class="stat-label">Stock Bajo</span>
                  <span class="stat-value">{{ reporteInventario.stock_bajo || 0 }}</span>
                </div>
              </div>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- Tab: Productos Más Vendidos -->
      <div v-show="activeTab === 'productos'" class="tab-panel">
        <BaseCard>
          <div class="reporte-header">
            <h2><i class="fas fa-trophy"></i> Productos Más Vendidos</h2>
            <p class="description">Ranking de productos con mayor rotación</p>
          </div>
          
          <div class="reporte-filters">
            <BaseInput
              v-model="productosFilters.fecha_inicio"
              type="date"
              label="Fecha Inicio"
            />
            <BaseInput
              v-model="productosFilters.fecha_fin"
              type="date"
              label="Fecha Fin"
            />
            <div class="filter-actions">
              <BaseButton
                @click="exportarProductosPDF"
                variant="danger"
                icon="fa-file-pdf"
              >
                Exportar PDF
              </BaseButton>
              <BaseButton
                @click="exportarProductosExcel"
                variant="success"
                icon="fa-file-excel"
              >
                Exportar Excel
              </BaseButton>
            </div>
          </div>

          <div v-if="reporteProductos" class="reporte-content">
            <p class="info-text">Top 10 productos más vendidos en el período seleccionado</p>
          </div>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import { formatCurrency } from '@/utils/formatters'
import { reportesService } from '@/services/reportesService'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInput from '@/components/common/BaseInput.vue'

const toast = useToast()

// Tabs
const activeTab = ref('ventas')
const tabs = [
  { id: 'ventas', label: 'Ventas', icon: 'fas fa-chart-line' },
  { id: 'compras', label: 'Compras', icon: 'fas fa-shopping-bag' },
  { id: 'inventario', label: 'Inventario', icon: 'fas fa-warehouse' },
  { id: 'productos', label: 'Top Productos', icon: 'fas fa-trophy' }
]

// Filtros
const ventasFilters = ref({
  fecha_inicio: '',
  fecha_fin: ''
})

const comprasFilters = ref({
  fecha_inicio: '',
  fecha_fin: ''
})

const productosFilters = ref({
  fecha_inicio: '',
  fecha_fin: ''
})

// Reportes
const reporteVentas = ref(null)
const reporteCompras = ref(null)
const reporteInventario = ref(null)
const reporteProductos = ref(null)
const loading = ref(false)

// Generar Reportes
const generarReporteVentas = () => {
  if (!ventasFilters.value.fecha_inicio || !ventasFilters.value.fecha_fin) {
    toast.error('Seleccione el rango de fechas')
    return
  }
  
  // Datos de ejemplo
  reporteVentas.value = {
    total_ventas: 45,
    total_ingresos: 12500.50,
    promedio: 277.79
  }
  
  toast.success('Reporte de ventas generado')
}

const generarReporteCompras = () => {
  if (!comprasFilters.value.fecha_inicio || !comprasFilters.value.fecha_fin) {
    toast.error('Seleccione el rango de fechas')
    return
  }
  
  // Datos de ejemplo
  reporteCompras.value = {
    total_compras: 12,
    total_gastos: 8500.00,
    total_proveedores: 5
  }
  
  toast.success('Reporte de compras generado')
}

const generarReporteInventario = () => {
  // Datos de ejemplo
  reporteInventario.value = {
    total_productos: 150,
    valor_total: 45000.00,
    stock_bajo: 8
  }
  
  toast.success('Reporte de inventario actualizado')
}

const generarReporteProductos = () => {
  if (!productosFilters.value.fecha_inicio || !productosFilters.value.fecha_fin) {
    toast.error('Seleccione el rango de fechas')
    return
  }
  
  reporteProductos.value = {
    productos: []
  }
  
  toast.success('Reporte de productos generado')
}

// Exportar PDF
const exportarVentasPDF = async () => {
  if (!ventasFilters.value.fecha_inicio || !ventasFilters.value.fecha_fin) {
    toast.error('Seleccione el rango de fechas')
    return
  }
  
  loading.value = true
  toast.info('Generando PDF de ventas...')
  
  try {
    const resultado = await reportesService.descargarVentasPDF(
      ventasFilters.value.fecha_inicio,
      ventasFilters.value.fecha_fin
    )
    
    if (resultado.success) {
      toast.success('PDF de ventas descargado correctamente')
    } else {
      toast.error(resultado.message || 'Error al descargar PDF')
    }
  } catch (error) {
    toast.error('Error al generar PDF de ventas')
  } finally {
    loading.value = false
  }
}

const exportarComprasPDF = async () => {
  if (!comprasFilters.value.fecha_inicio || !comprasFilters.value.fecha_fin) {
    toast.error('Seleccione el rango de fechas')
    return
  }
  
  loading.value = true
  toast.info('Generando PDF de compras...')
  
  try {
    const resultado = await reportesService.descargarComprasPDF(
      comprasFilters.value.fecha_inicio,
      comprasFilters.value.fecha_fin
    )
    
    if (resultado.success) {
      toast.success('PDF de compras descargado correctamente')
    } else {
      toast.error(resultado.message || 'Error al descargar PDF')
    }
  } catch (error) {
    toast.error('Error al generar PDF de compras')
  } finally {
    loading.value = false
  }
}

const exportarInventarioPDF = async () => {
  loading.value = true
  toast.info('Generando PDF de inventario...')
  
  try {
    const resultado = await reportesService.descargarInventarioPDF()
    
    if (resultado.success) {
      toast.success('PDF de inventario descargado correctamente')
    } else {
      toast.error(resultado.message || 'Error al descargar PDF')
    }
  } catch (error) {
    toast.error('Error al generar PDF de inventario')
  } finally {
    loading.value = false
  }
}

const exportarProductosPDF = () => {
  toast.info('Función de productos más vendidos en desarrollo...')
}

// Exportar Excel
const exportarVentasExcel = () => {
  toast.info('Exportando reporte de ventas a Excel...')
}

const exportarComprasExcel = () => {
  toast.info('Exportando reporte de compras a Excel...')
}

const exportarInventarioExcel = () => {
  toast.info('Exportando reporte de inventario a Excel...')
}

const exportarProductosExcel = () => {
  toast.info('Exportando reporte de productos a Excel...')
}

onMounted(() => {
  // Establecer fechas por defecto (último mes)
  const hoy = new Date()
  const hace30Dias = new Date()
  hace30Dias.setDate(hoy.getDate() - 30)
  
  const fechaInicio = hace30Dias.toISOString().split('T')[0]
  const fechaFin = hoy.toISOString().split('T')[0]
  
  ventasFilters.value.fecha_inicio = fechaInicio
  ventasFilters.value.fecha_fin = fechaFin
  
  comprasFilters.value.fecha_inicio = fechaInicio
  comprasFilters.value.fecha_fin = fechaFin
  
  productosFilters.value.fecha_inicio = fechaInicio
  productosFilters.value.fecha_fin = fechaFin
})
</script>

<style scoped>
.reportes {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0 0 0.5rem 0;
  color: var(--color-texto);
  font-size: 2rem;
}

.subtitle {
  margin: 0;
  color: #6c757d;
  font-size: 1rem;
}

/* Tabs Navigation */
.tabs-navigation {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #e0e0e0;
  overflow-x: auto;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: #6c757d;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.tab-button:hover {
  color: var(--color-azul);
  background: #f8f9fa;
}

.tab-button.active {
  color: var(--color-azul);
  border-bottom-color: var(--color-azul);
  background: #f0f7ff;
}

.tab-button i {
  font-size: 1.1rem;
}

/* Tab Content */
.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tab-panel {
  animation: fadeIn 0.3s ease;
}

/* Reporte Header */
.reporte-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.reporte-header h2 {
  margin: 0 0 0.5rem 0;
  color: var(--color-texto);
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.reporte-header h2 i {
  color: var(--color-azul);
}

.description {
  margin: 0;
  color: #6c757d;
  font-size: 0.95rem;
}

/* Filtros */
.reporte-filters {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 0.5rem;
}

.inventory-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
  border-radius: 12px;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.stat-card i {
  font-size: 2.5rem;
  opacity: 0.9;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: bold;
}

/* Colores de Stats */
.stat-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-success {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.stat-info {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-danger {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-secondary {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

/* Info Text */
.info-text {
  text-align: center;
  padding: 3rem 1rem;
  color: #6c757d;
  font-size: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .reporte-header {
    flex-direction: column;
    gap: 1rem;
  }

  .export-buttons {
    width: 100%;
  }

  .export-buttons button {
    flex: 1;
  }

  .reporte-filters {
    grid-template-columns: 1fr;
  }

  .filter-actions {
    flex-direction: column;
  }

  .filter-actions button,
  .inventory-actions button {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .tabs-navigation {
    gap: 0.25rem;
  }

  .tab-button {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
  }

  .tab-button span {
    display: none;
  }

  .tab-button i {
    font-size: 1.25rem;
  }
}
</style>
