# Guía para Evitar la Detección de Bots

## 🔍 Señales que indican detección como bot

### 1. Respuestas HTTP sospechosas
- **403 Forbidden**: Acceso denegado
- **429 Too Many Requests**: Demasiadas solicitudes
- **503 Service Unavailable**: Servicio no disponible (posible rate limiting)

### 2. Elementos en la página
- Aparición de CAPTCHAs
- Mensajes como "Unusual traffic detected"
- Redirects a páginas de verificación
- Campos de verificación adicionales

### 3. Comportamiento de JavaScript
- Detección de `navigator.webdriver = true`
- Verificación de plugins del navegador
- Análisis de timing de eventos
- Fingerprinting del canvas/WebGL

## 🛡️ Técnicas implementadas para evitar detección

### 1. Configuración del navegador
```python
# User agents rotativos
self.user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    # Múltiples user agents actualizados
]

# Headers HTTP realistas
self.page.set_extra_http_headers({
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
})
```

### 2. Modificación de propiedades del navegador
```javascript
// Eliminar webdriver property
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
});

// Simular plugins
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5],
});
```

### 3. Comportamiento humano simulado
- **Movimiento del mouse**: Trayectorias graduales con pasos aleatorios
- **Timing de clicks**: Delays variables entre acciones
- **Escritura**: Velocidad variable con pausas ocasionales
- **Scroll**: Movimiento gradual y natural

## 📊 Cómo usar las funciones de análisis

### 1. Verificación básica
```python
if bot.check_bot_detection():
    print("⚠️ Posible detección como bot")
```

### 2. Análisis completo
```python
result = bot.comprehensive_bot_analysis()
if result['detected']:
    print("Implementar contramedidas adicionales")
```

### 3. Monitoreo de red
```python
blocked, suspicious = bot.monitor_network_requests()
for req in blocked:
    print(f"Request bloqueado: {req['url']}")
```

## 🔧 Configuraciones adicionales recomendadas

### 1. Proxies y VPN
```python
# Configurar proxy en Playwright
context = browser.new_context(
    proxy={"server": "http://proxy-server:port"}
)
```

### 2. Cookies persistentes
```python
# Usar datos persistentes del navegador real
bot.setup_page(persistent_data=True, channel="edge")
```

### 3. Delays inteligentes
```python
# Delays aleatorios entre acciones
delay = random.uniform(1000, 3000)
page.wait_for_timeout(delay)
```

## 🎯 Señales específicas en Apple.com

### 1. Rate limiting
- Requests a `/fulfillment-messages` bloqueados
- Timeouts en la carga de productos
- Redirecciones inesperadas

### 2. JavaScript challenges
- Verificación de canvas fingerprinting
- Challenges de timing
- Verificación de eventos de mouse

### 3. Comportamiento del sitio
- Elementos que no cargan correctamente
- Formularios que no responden
- Cambios en la estructura del DOM

## 🛠️ Troubleshooting

### Si detectan tu bot:
1. **Cambiar User Agent y headers**
2. **Usar diferentes IPs/proxies**
3. **Aumentar delays entre acciones**
4. **Revisar el fingerprint del navegador**
5. **Limpiar cookies y caché**

### Para verificar efectividad:
1. **Ejecutar análisis completo**
2. **Revisar screenshots generadas**
3. **Monitorear requests de red**
4. **Verificar timing de respuestas**

## 📝 Logs importantes

Mantén un registro de:
- User agents utilizados
- IPs y proxies
- Timing de requests exitosos
- Patrones de detección observados
- Cambios en el sitio web objetivo