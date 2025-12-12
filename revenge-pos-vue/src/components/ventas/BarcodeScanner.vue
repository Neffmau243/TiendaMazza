<template>
  <div class="barcode-scanner-wrapper">
    <!-- Botón compacto para abrir el escáner -->
    <button 
      @click="toggleScanner" 
      class="scanner-toggle-btn"
      :class="{ active: isActive }"
      title="Escanear con cámara"
    >
      <i class="fas fa-camera"></i>
      <span>{{ isActive ? 'Cerrar Cámara' : 'Escanear' }}</span>
    </button>

    <!-- Modal del escáner -->
    <Transition name="scanner-modal">
      <div v-if="showScanner" class="scanner-modal-overlay" @click.self="closeScanner">
        <div class="scanner-modal-content">
          <div class="scanner-modal-header">
            <h3>
              <i class="fas fa-camera"></i>
              Escanear Código de Barras
            </h3>
            <button @click="closeScanner" class="close-btn">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="scanner-modal-body">
            <!-- Área de la cámara -->
            <div class="scanner-container" :class="{ 'scanner-active': isActive }">
              <div id="barcode-scanner" ref="scannerElement"></div>
              
              <!-- Overlay con guía visual -->
              <div v-if="isActive" class="scanner-overlay">
                <div class="scanner-guide">
                  <div class="scanner-corners corner-tl"></div>
                  <div class="scanner-corners corner-tr"></div>
                  <div class="scanner-corners corner-bl"></div>
                  <div class="scanner-corners corner-br"></div>
                  <div class="scanner-line"></div>
                </div>
                <div class="scanner-instruction">
                  <i class="fas fa-barcode"></i>
                  Coloca el código de barras dentro del marco
                </div>
                <div class="scanner-status">
                  <div class="pulse-dot"></div>
                  Buscando código...
                </div>
              </div>

              <!-- Estado de carga -->
              <div v-if="loading" class="scanner-loading">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Iniciando cámara...</p>
              </div>

              <!-- Mensaje de error -->
              <div v-if="error" class="scanner-error">
                <i class="fas fa-exclamation-circle"></i>
                <p>{{ error }}</p>
              </div>
            </div>

            <!-- Último código escaneado -->
            <div v-if="lastScannedCode" class="last-scanned">
              <div class="last-scanned-label">
                <i class="fas fa-check-circle"></i>
                Último código escaneado:
              </div>
              <div class="last-scanned-code">{{ lastScannedCode }}</div>
            </div>

            <!-- Instrucciones -->
            <div class="scanner-tips">
              <div class="tip">
                <i class="fas fa-lightbulb"></i>
                <span>Asegúrate de tener buena iluminación</span>
              </div>
              <div class="tip">
                <i class="fas fa-barcode"></i>
                <span>Solo se aceptan códigos EAN-13 (13 dígitos)</span>
              </div>
            </div>
          </div>

          <div class="scanner-modal-footer">
            <button 
              @click="startScanner" 
              :disabled="isActive || loading"
              class="btn btn-primary"
            >
              <i class="fas fa-play"></i>
              {{ isActive ? 'Escaneando...' : 'Iniciar Escáner' }}
            </button>
            <button 
              @click="stopScanner" 
              :disabled="!isActive"
              class="btn btn-secondary"
            >
              <i class="fas fa-stop"></i>
              Detener
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import Quagga from 'quagga'

const emit = defineEmits(['code-scanned'])

const showScanner = ref(false)
const isActive = ref(false)
const loading = ref(false)
const error = ref('')
const lastScannedCode = ref('')
const scannerElement = ref(null)
const lastDetectionTime = ref(0)
const detectionCooldown = 2000 // 2 segundos entre detecciones

const toggleScanner = () => {
  showScanner.value = !showScanner.value
  if (!showScanner.value) {
    stopScanner()
  }
}

const closeScanner = () => {
  stopScanner()
  showScanner.value = false
}

const startScanner = async () => {
  if (isActive.value) return

  loading.value = true
  error.value = ''

  // Verificar si estamos en contexto seguro
  const isSecureContext = window.isSecureContext || 
                         window.location.hostname === 'localhost' || 
                         window.location.hostname === '127.0.0.1'

  if (!isSecureContext) {
    error.value = 'La cámara solo funciona en HTTPS o localhost. Accede desde: http://localhost:5000 o http://127.0.0.1:5000'
    loading.value = false
    return
  }

  // Verificar soporte del navegador
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    error.value = 'Tu navegador no soporta acceso a la cámara'
    loading.value = false
    return
  }

  // Intentar obtener permiso de cámara primero
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    // Detener el stream de prueba
    stream.getTracks().forEach(track => track.stop())
  } catch (err) {
    console.error('Error al obtener permiso de cámara:', err)
    if (err.name === 'NotAllowedError') {
      error.value = 'Permiso de cámara denegado. Por favor, permite el acceso a la cámara en la configuración de tu navegador.'
    } else if (err.name === 'NotFoundError') {
      error.value = 'No se encontró ninguna cámara en tu dispositivo.'
    } else if (err.name === 'NotReadableError') {
      error.value = 'La cámara está siendo usada por otra aplicación. Cierra otras aplicaciones que usen la cámara.'
    } else {
      error.value = 'Error al acceder a la cámara. Asegúrate de usar http://localhost:5000'
    }
    loading.value = false
    return
  }

  const config = {
    inputStream: {
      name: "Live",
      type: "LiveStream",
      target: scannerElement.value,
      constraints: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: "environment"
      }
    },
    locator: {
      patchSize: "medium",
      halfSample: true
    },
    numOfWorkers: navigator.hardwareConcurrency || 2,
    frequency: 10,
    decoder: {
      readers: [
        "ean_reader",
        "ean_8_reader",
        "code_128_reader",
        "upc_reader"
      ]
    },
    locate: true
  }

  Quagga.init(config, (err) => {
    loading.value = false

    if (err) {
      console.error('Error al inicializar escáner:', err)
      
      // Mensajes de error más amigables
      if (err.name === 'NotAllowedError') {
        error.value = 'Permiso de cámara denegado. Por favor, permite el acceso a la cámara.'
      } else if (err.name === 'NotFoundError') {
        error.value = 'No se encontró ninguna cámara en tu dispositivo.'
      } else if (err.name === 'NotReadableError') {
        error.value = 'La cámara está siendo usada por otra aplicación.'
      } else {
        error.value = 'Error al acceder a la cámara. Intenta recargar la página.'
      }
      return
    }

    Quagga.start()
    isActive.value = true
    lastDetectionTime.value = 0

    // Configurar callback de detección
    Quagga.onDetected(onBarcodeDetected)
    
    // Optimizar canvas para múltiples lecturas
    setTimeout(() => {
      const canvas = document.querySelector('#barcode-scanner canvas')
      if (canvas) {
        const ctx = canvas.getContext('2d', { willReadFrequently: true })
      }
    }, 100)
  })
}

const stopScanner = () => {
  if (!isActive.value) return

  try {
    Quagga.stop()
    Quagga.offDetected(onBarcodeDetected)
  } catch (e) {
    console.error('Error al detener escáner:', e)
  }

  isActive.value = false
}

const onBarcodeDetected = (result) => {
  const code = result.codeResult.code
  const currentTime = Date.now()

  // Verificar cooldown
  if (currentTime - lastDetectionTime.value < detectionCooldown) {
    return
  }

  // Solo aceptar códigos EAN-13 de 13 dígitos
  if (code && code.length === 13 && /^\d{13}$/.test(code)) {
    lastScannedCode.value = code
    lastDetectionTime.value = currentTime

    // Reproducir beep
    playBeep()

    // Emitir evento al componente padre
    emit('code-scanned', code)

    // Auto-cerrar después de escanear
    setTimeout(() => {
      closeScanner()
    }, 1000)
  }
}

const playBeep = () => {
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()

    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)

    oscillator.frequency.value = 800
    oscillator.type = 'sine'

    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime)
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1)

    oscillator.start(audioContext.currentTime)
    oscillator.stop(audioContext.currentTime + 0.1)
  } catch (error) {
    console.log('No se pudo reproducir el sonido:', error)
  }
}

// Limpiar al desmontar
onBeforeUnmount(() => {
  stopScanner()
})
</script>

<style scoped>
/* Botón toggle compacto */
.scanner-toggle-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3);
}

.scanner-toggle-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
}

.scanner-toggle-btn.active {
  background: linear-gradient(135deg, #ff6b6b 0%, #e74c3c 100%);
}

.scanner-toggle-btn i {
  font-size: 1.1rem;
}

/* Modal */
.scanner-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.scanner-modal-content {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.scanner-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
}

.scanner-modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.scanner-modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.scanner-container {
  position: relative;
  width: 100%;
  height: 400px;
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.scanner-container.scanner-active {
  border: 3px solid #e74c3c;
}

#barcode-scanner {
  width: 100%;
  height: 100%;
}

#barcode-scanner video,
#barcode-scanner canvas {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover;
}

/* Overlay con guía */
.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.scanner-guide {
  position: relative;
  width: 80%;
  max-width: 400px;
  height: 200px;
  border: 2px solid transparent;
}

.scanner-corners {
  position: absolute;
  width: 40px;
  height: 40px;
  border-color: #00ff00;
  border-style: solid;
}

.corner-tl {
  top: -2px;
  left: -2px;
  border-width: 4px 0 0 4px;
}

.corner-tr {
  top: -2px;
  right: -2px;
  border-width: 4px 4px 0 0;
}

.corner-bl {
  bottom: -2px;
  left: -2px;
  border-width: 0 0 4px 4px;
}

.corner-br {
  bottom: -2px;
  right: -2px;
  border-width: 0 4px 4px 0;
}

.scanner-line {
  position: absolute;
  width: 100%;
  height: 3px;
  background: linear-gradient(to right, transparent, #00ff00, transparent);
  top: 50%;
  animation: scan-line 2s linear infinite;
  box-shadow: 0 0 10px #00ff00;
}

@keyframes scan-line {
  0%, 100% {
    top: 10%;
  }
  50% {
    top: 90%;
  }
}

.scanner-instruction {
  margin-top: 1rem;
  color: white;
  background: rgba(0, 0, 0, 0.7);
  padding: 0.75rem 1.5rem;
  border-radius: 20px;
  font-size: 0.9rem;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.scanner-instruction i {
  font-size: 1.2rem;
}

.scanner-status {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  background: rgba(231, 76, 60, 0.9);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  backdrop-filter: blur(10px);
  font-weight: 600;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.3);
  }
}

/* Estados */
.scanner-loading,
.scanner-error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: white;
  background: rgba(0, 0, 0, 0.8);
  padding: 2rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.scanner-loading i,
.scanner-error i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.scanner-error {
  color: #ff6b6b;
}

/* Último código escaneado */
.last-scanned {
  background: linear-gradient(135deg, #e74c3c15 0%, #c0392b15 100%);
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  border: 2px solid #e74c3c;
}

.last-scanned-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e74c3c;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.last-scanned-code {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  font-family: 'Courier New', monospace;
  letter-spacing: 2px;
}

/* Tips */
.scanner-tips {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.tip {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
  font-size: 0.85rem;
  color: #666;
}

.tip i {
  color: #e74c3c;
  font-size: 1.1rem;
}

/* Footer */
.scanner-modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 2px solid #f0f0f0;
  background: #f8f9fa;
}

.btn {
  flex: 1;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #5a6268;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Transiciones */
.scanner-modal-enter-active,
.scanner-modal-leave-active {
  transition: all 0.3s ease;
}

.scanner-modal-enter-from,
.scanner-modal-leave-to {
  opacity: 0;
}

.scanner-modal-enter-from .scanner-modal-content,
.scanner-modal-leave-to .scanner-modal-content {
  transform: scale(0.9);
}

/* Responsive */
@media (max-width: 768px) {
  .scanner-modal-content {
    max-width: 100%;
    border-radius: 0;
  }

  .scanner-container {
    height: 300px;
  }

  .scanner-modal-footer {
    flex-direction: column;
  }

  .scanner-toggle-btn {
    font-size: 0.85rem;
    padding: 0.625rem 0.875rem;
  }
}
</style>
