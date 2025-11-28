// Variables globales
let scannerActive = false;
let scannedCodes = [];
let lastDetectionTime = 0;
let detectionCooldown = 2000; // 2 segundos entre detecciones

// Elementos del DOM
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const clearBtn = document.getElementById('clearBtn');
const scannerDiv = document.getElementById('scanner');
const scannerOverlay = document.querySelector('.scanner-overlay');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const resultDiv = document.getElementById('result');
const resultCode = document.getElementById('result-code');
const resultFormat = document.getElementById('result-format');
const historyList = document.getElementById('history-list');

// Configuración de QuaggaJS
const quaggaConfig = {
    inputStream: {
        name: "Live",
        type: "LiveStream",
        target: document.querySelector('#scanner'),
        constraints: {
            width: 640,
            height: 480,
            facingMode: "environment" // Cámara trasera en móviles
        }
    },
    locator: {
        patchSize: "medium",
        halfSample: true
    },
    numOfWorkers: 2,
    decoder: {
        readers: [
            "ean_reader",
            "ean_8_reader",
            "code_128_reader",
            "upc_reader"
        ]
    },
    locate: true
};

// Función para iniciar el escáner
function startScanner() {
    if (scannerActive) return;
    
    // Mostrar loading
    showLoading(true);
    hideError();
    
    // Verificar si el navegador soporta getUserMedia
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showError('Tu navegador no soporta acceso a la cámara. Usa un navegador más moderno.');
        showLoading(false);
        return;
    }
    
    // Inicializar QuaggaJS
    Quagga.init(quaggaConfig, function(err) {
        showLoading(false);
        
        if (err) {
            console.error('Error al inicializar QuaggaJS:', err);
            showError('Error al acceder a la cámara: ' + err.message);
            return;
        }
        
        console.log('QuaggaJS inicializado correctamente');
        Quagga.start();
        scannerActive = true;
        lastDetectionTime = 0; // Reset del tiempo
        updateButtons();
        showScannerGuide(true);
        
        // Configurar evento de detección
        Quagga.onDetected(onBarcodeDetected);
    });
}

// Función para detener el escáner
function stopScanner() {
    if (!scannerActive) return;
    
    Quagga.stop();
    scannerActive = false;
    updateButtons();
    showScannerGuide(false);
    hideResult();
    console.log('Escáner detenido');
}

// Función que se ejecuta cuando se detecta un código
function onBarcodeDetected(result) {
    const code = result.codeResult.code;
    const format = result.codeResult.format;
    const currentTime = Date.now();
    
    console.log('Código detectado:', code, 'Formato:', format, 'Longitud:', code ? code.length : 0);
    
    // Verificar tiempo entre detecciones para evitar spam
    if (currentTime - lastDetectionTime < detectionCooldown) {
        console.log('Detección ignorada - Muy pronto después de la anterior');
        return;
    }
    
    // SOLO aceptar códigos de exactamente 13 dígitos (sin importar el formato detectado)
    if (code && code.length === 13 && /^\d{13}$/.test(code)) {
        // Evitar duplicados consecutivos
        if (scannedCodes.length === 0 || scannedCodes[scannedCodes.length - 1].code !== code) {
            const scannedItem = {
                code: code,
                format: 'EAN-13',
                timestamp: new Date()
            };
            
            scannedCodes.push(scannedItem);
            showResult(code, 'EAN-13');
            updateHistory();
            lastDetectionTime = currentTime;
            
            // Reproducir sonido de éxito
            playBeep();
            
            // Mensaje de confirmación sin detener
            showTemporaryMessage('✅ Código guardado: ' + code);
        }
    } else {
        console.log('Código rechazado - No tiene 13 dígitos:', code, 'Longitud:', code ? code.length : 0, 'Formato:', format);
    }
}

// Función para mostrar el resultado
function showResult(code, format) {
    resultCode.textContent = code;
    resultFormat.textContent = `Formato: ${format.toUpperCase()}`;
    resultDiv.style.display = 'block';
    
    // Scroll hacia el resultado
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Función para ocultar el resultado
function hideResult() {
    resultDiv.style.display = 'none';
}

// Función para actualizar el historial
function updateHistory() {
    if (scannedCodes.length === 0) {
        historyList.innerHTML = '<div style="text-align: center; color: #666; padding: 20px;">No hay códigos escaneados aún</div>';
        return;
    }
    
    historyList.innerHTML = '';
    
    // Mostrar los últimos 10 códigos
    const recentCodes = scannedCodes.slice(-10).reverse();
    
    recentCodes.forEach((item, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        const timeString = item.timestamp.toLocaleString('es-ES');
        
        historyItem.innerHTML = `
            <div class="history-time">${timeString}</div>
            <div class="history-code">${item.code}</div>
            <div style="color: #666; font-size: 12px;">Formato: ${item.format}</div>
        `;
        
        // Agregar evento de clic para copiar al portapapeles
        historyItem.addEventListener('click', () => {
            copyToClipboard(item.code);
            showTemporaryMessage('Código copiado al portapapeles');
        });
        
        historyItem.style.cursor = 'pointer';
        historyItem.title = 'Click para copiar al portapapeles';
        
        historyList.appendChild(historyItem);
    });
}

// Función para limpiar el historial
function clearHistory() {
    if (confirm('¿Estás seguro de que quieres limpiar el historial?')) {
        scannedCodes = [];
        updateHistory();
        hideResult();
    }
}

// Función para mostrar/ocultar la guía del escáner
function showScannerGuide(show) {
    if (scannerOverlay) {
        scannerOverlay.style.display = show ? 'block' : 'none';
    }
}

// Función para actualizar el estado de los botones
function updateButtons() {
    startBtn.disabled = scannerActive;
    stopBtn.disabled = !scannerActive;
}

// Función para mostrar/ocultar loading
function showLoading(show) {
    loadingDiv.style.display = show ? 'block' : 'none';
}

// Función para mostrar errores
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Función para ocultar errores
function hideError() {
    errorDiv.style.display = 'none';
}

// Función para reproducir un beep
function playBeep() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (error) {
        console.log('No se pudo reproducir el sonido:', error);
    }
}

// Función para copiar al portapapeles
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        // Usar la API moderna del portapapeles
        navigator.clipboard.writeText(text).catch(err => {
            console.error('Error al copiar:', err);
            fallbackCopyTextToClipboard(text);
        });
    } else {
        // Fallback para navegadores más antiguos
        fallbackCopyTextToClipboard(text);
    }
}

// Función fallback para copiar texto
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (!successful) {
            console.error('Error al copiar texto');
        }
    } catch (err) {
        console.error('Error al copiar:', err);
    }
    
    document.body.removeChild(textArea);
}

// Función para mostrar mensajes temporales
function showTemporaryMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #007bff;
        color: white;
        padding: 12px 20px;
        border-radius: 5px;
        z-index: 1000;
        font-weight: bold;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        font-size: 14px;
    `;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        if (document.body.contains(messageDiv)) {
            document.body.removeChild(messageDiv);
        }
    }, 3000);
}

// Manejar errores de QuaggaJS
Quagga.onProcessed(function(result) {
    const drawingCtx = Quagga.canvas.ctx.overlay;
    const drawingCanvas = Quagga.canvas.dom.overlay;

    if (result) {
        if (result.boxes) {
            drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
            result.boxes.filter(function (box) {
                return box !== result.box;
            }).forEach(function (box) {
                Quagga.ImageDebug.drawPath(box, {x: 0, y: 1}, drawingCtx, {color: "green", lineWidth: 2});
            });
        }

        if (result.box) {
            Quagga.ImageDebug.drawPath(result.box, {x: 0, y: 1}, drawingCtx, {color: "#00F", lineWidth: 2});
        }

        if (result.codeResult && result.codeResult.code) {
            Quagga.ImageDebug.drawPath(result.line, {x: 'x', y: 'y'}, drawingCtx, {color: 'red', lineWidth: 3});
        }
    }
});

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Lector de códigos de barras iniciado');
    updateButtons();
    updateHistory();
    
    // Manejar visibilidad de la página para pausar/reanudar
    document.addEventListener('visibilitychange', function() {
        if (document.hidden && scannerActive) {
            console.log('Página oculta, pausando escáner');
            stopScanner();
        }
    });
});

// Manejar eventos de teclado
document.addEventListener('keydown', function(event) {
    switch(event.key) {
        case 'Enter':
        case ' ':
            if (!scannerActive) {
                startScanner();
            } else {
                stopScanner();
            }
            event.preventDefault();
            break;
        case 'Escape':
            if (scannerActive) {
                stopScanner();
            }
            event.preventDefault();
            break;
    }
});

// Exportar funciones para uso en el HTML
window.startScanner = startScanner;
window.stopScanner = stopScanner;
window.clearHistory = clearHistory;