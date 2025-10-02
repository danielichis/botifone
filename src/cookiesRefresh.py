import undetected_playwright
from playwright.sync_api import sync_playwright
import json
import os
import random
import time

class botIphone:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]
    
    def setup_page(self, persistent_data=True, browser_engine="chromium", channel="chrome"):
        """
        Setup the browser page
        
        Args:
            persistent_data (bool): Whether to use persistent user data
            browser_engine (str): Browser engine to use ('chromium', 'firefox', 'webkit')
            channel (str): Browser channel to use ('chrome', 'edge'). Only used with chromium engine
        """
        self.playwright = sync_playwright().start()        
        try:
            # Get the browser engine
            if browser_engine == "chromium":
                engine = self.playwright.chromium
            elif browser_engine == "firefox":
                engine = self.playwright.firefox
            elif browser_engine == "webkit":
                engine = self.playwright.webkit
            else:
                raise ValueError(f"Unsupported browser engine: {browser_engine}")
            
            # Validate channel parameter
            if browser_engine == "chromium" and channel not in ["chrome", "edge"]:
                raise ValueError(f"Unsupported channel for chromium: {channel}. Use 'chrome' or 'edge'")
            
            if persistent_data:
                # Determine user data directory based on channel
                if browser_engine == "chromium":
                    if channel == "chrome":
                        user_data_dir = os.path.expanduser("~") + "/AppData/Local/Google/Chrome/User Data"
                        # Use existing browser installation with persistent data
                        context = engine.launch_persistent_context(
                            user_data_dir=user_data_dir,
                            channel=channel,
                            headless=False,
                            args=['--profile-directory=Default',
                                  '--disable-blink-features=AutomationControlled',  # Deshabilita flags de automatización
                                  '--no-sandbox',  # Opcional, para entornos restrictivos
                                  '--disable-infobars'  # Oculta barras de "controlado por software"
                                  ]  # Use default profile
                        )
                        # Apply stealth techniques using undetected_playwright
                        self.browser = undetected_playwright.stealth_sync(context)
                    elif channel == "edge":
                        # For Edge with persistent data, use a separate temporary directory
                        # to avoid conflicts with actual Edge user data
                        import tempfile
                        temp_dir = tempfile.mkdtemp(prefix="playwright_edge_")
                        user_data_dir = temp_dir
                        
                        # Try common Edge installation paths
                        edge_paths = [
                            "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
                            "C:/Program Files/Microsoft/Edge/Application/msedge.exe"
                        ]
                        edge_exe = None
                        for path in edge_paths:
                            if os.path.exists(path):
                                edge_exe = path
                                break
                        
                        if edge_exe:
                            context = engine.launch_persistent_context(
                                user_data_dir=user_data_dir,
                                executable_path=edge_exe,
                                headless=False,
                                args=['--profile-directory=Default']  # Use default profile
                            )
                            # Apply stealth techniques using undetected_playwright
                            self.browser = undetected_playwright.stealth_sync(context)
                        else:
                            # Fallback: launch without persistent data if Edge not found
                            print("Edge executable not found, launching without persistent data...")
                            browser_instance = engine.launch(headless=False)
                            context = browser_instance.new_context()
                            self.browser = undetected_playwright.stealth_sync(context)
                else:
                    # For firefox and webkit, don't use channel parameter
                    context = engine.launch_persistent_context(
                        headless=False
                    )
                    # Apply stealth techniques using undetected_playwright
                    self.browser = undetected_playwright.stealth_sync(context)
            else:
                # Launch browser without persistent data
                if browser_engine == "chromium":
                    browser_instance = engine.launch(headless=False, channel=channel)
                else:
                    browser_instance = engine.launch(headless=False)
                context = browser_instance.new_context()
                # Apply stealth techniques using undetected_playwright
                self.browser = undetected_playwright.stealth_sync(context)
            
            # Get the first page or create one
            if len(self.browser.pages) > 0:
                self.page = self.browser.pages[0]
            else:
                self.page = self.browser.new_page()
                
            print(f"Browser setup completed with {browser_engine} engine, channel={channel if browser_engine == 'chromium' else 'N/A'}, persistent_data={persistent_data}")
            
            
        except Exception as e:
            print(f"Failed to setup browser: {str(e)}")
            if self.playwright:
                self.playwright.stop()
            raise

    def apply_anti_detection_techniques(self):
        """
        Aplica técnicas para evitar la detección como bot
        """
        if not self.page:
            return
            
        # 1. Sobrescribir propiedades que detectan automatización
        self.page.add_init_script("""
            // Eliminar webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Sobrescribir plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Sobrescribir languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Sobrescribir chrome object
            window.chrome = {
                runtime: {},
            };
            
            // Sobrescribir permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Cypress.getTestRunner().config('platform') === 'chrome' ? 'granted' : 'prompt' }) :
                    originalQuery(parameters)
            );
            
            // Modificar mouse events para parecer más humano
            const originalAddEventListener = EventTarget.prototype.addEventListener;
            EventTarget.prototype.addEventListener = function(type, listener, options) {
                if (type === 'mousedown' || type === 'mouseup' || type === 'click') {
                    const wrappedListener = function(event) {
                        // Añadir pequeños delays aleatorios
                        setTimeout(() => listener.call(this, event), Math.random() * 50);
                    };
                    return originalAddEventListener.call(this, type, wrappedListener, options);
                }
                return originalAddEventListener.call(this, type, listener, options);
            };
        """)
        
        # 2. Establecer viewport más realista
        self.page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 3. Establecer user agent aleatorio
        user_agent = random.choice(self.user_agents)
        self.page.set_extra_http_headers({
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })

    def check_bot_detection(self):
        """
        Verifica si la página está detectando que somos un bot
        """
        if not self.page:
            return False
            
        detection_indicators = []
        
        try:
            # 1. Verificar si hay mensajes de error relacionados con bots
            bot_messages = [
                "bot", "robot", "automated", "captcha", "verification",
                "unusual traffic", "suspicious activity", "blocked"
            ]
            
            page_content = self.page.content().lower()
            for message in bot_messages:
                if message in page_content:
                    detection_indicators.append(f"Detectado mensaje sospechoso: {message}")
            
            # 2. Verificar si hay CAPTCHAs
            captcha_selectors = [
                "[data-sitekey]",  # reCAPTCHA
                ".g-recaptcha",    # reCAPTCHA
                "#captcha",        # CAPTCHA genérico
                ".captcha",        # CAPTCHA genérico
                "iframe[src*='recaptcha']",  # reCAPTCHA iframe
                "iframe[src*='hcaptcha']",   # hCaptcha
            ]
            
            for selector in captcha_selectors:
                if self.page.locator(selector).count() > 0:
                    detection_indicators.append(f"CAPTCHA detectado: {selector}")
            
            # 3. Verificar códigos de estado HTTP
            response = self.page.goto(self.page.url, wait_until="networkidle")
            if response and response.status in [403, 429, 503]:
                detection_indicators.append(f"Código de estado sospechoso: {response.status}")
            
            # 4. Verificar propiedades del navegador que indican automatización
            try:
                webdriver_detected = self.page.evaluate("() => window.navigator.webdriver")
                if webdriver_detected:
                    detection_indicators.append("Propiedad webdriver detectada")
            except Exception as e:
                detection_indicators.append(f"Error al verificar webdriver: {e}")
            
            # 5. Verificar si hay redirects sospechosos
            current_url = self.page.url
            if "challenge" in current_url or "verify" in current_url or "blocked" in current_url:
                detection_indicators.append(f"URL sospechosa: {current_url}")
            
            # 6. Verificar timing de carga anormal
            try:
                timing = self.page.evaluate("""() => {
                    try {
                        const perf = performance.getEntriesByType('navigation')[0];
                        return perf ? perf.loadEventEnd - perf.fetchStart : 0;
                    } catch (e) {
                        return -1; // Error indicator
                    }
                }""")
                
                if timing == -1:
                    detection_indicators.append("Error al obtener timing de performance")
                elif timing > 10000:  # Más de 10 segundos
                    detection_indicators.append(f"Tiempo de carga anormal: {timing}ms")
            except Exception as e:
                detection_indicators.append(f"Error al verificar timing: {e}")
            
            # Reportar resultados
            if detection_indicators:
                print("\n🚨 POSIBLE DETECCIÓN DE BOT:")
                for indicator in detection_indicators:
                    print(f"   - {indicator}")
                return True
            else:
                print("\n✅ No se detectaron señales de detección de bot")
                return False
                
        except Exception as e:
            print(f"Error al verificar detección de bot: {e}")
            return False

    def human_like_interaction(self, element_selector, action_type="click"):
        """
        Interactúa con elementos de manera más humana
        """
        try:
            element = self.page.locator(element_selector)
            
            # Scroll hasta el elemento de manera gradual
            self.page.evaluate(f"""(selector) => {{
                const element = document.querySelector(selector);
                if (element) {{
                    const rect = element.getBoundingClientRect();
                    const scrollTop = window.pageYOffset + rect.top;
                    const targetScroll = scrollTop - window.innerHeight / 2;
                    
                    // Scroll gradual
                    const start = window.pageYOffset;
                    const distance = targetScroll - start;
                    const duration = 1000 + Math.random() * 500; // 1-1.5 segundos
                    let startTime = null;
                    
                    function animation(currentTime) {{
                        if (startTime === null) startTime = currentTime;
                        const timeElapsed = currentTime - startTime;
                        const progress = Math.min(timeElapsed / duration, 1);
                        
                        // Easing function para movimiento más natural
                        const easeInOutQuad = progress < 0.5 ? 
                            2 * progress * progress : 
                            1 - Math.pow(-2 * progress + 2, 2) / 2;
                        
                        window.scrollTo(0, start + distance * easeInOutQuad);
                        
                        if (progress < 1) {{
                            requestAnimationFrame(animation);
                        }}
                    }}
                    
                    requestAnimationFrame(animation);
                }}
            }}""", element_selector)
            
            # Esperar un tiempo aleatorio (simular lectura/pensamiento)
            wait_time = random.uniform(1000, 3000)
            self.page.wait_for_timeout(wait_time)
            
            # Mover el mouse al elemento de manera gradual
            box = element.bounding_box()
            if box:
                # Calcular posición aleatoria dentro del elemento
                x = box['x'] + random.uniform(box['width'] * 0.2, box['width'] * 0.8)
                y = box['y'] + random.uniform(box['height'] * 0.2, box['height'] * 0.8)
                
                # Movimiento gradual del mouse
                self.page.mouse.move(x, y, steps=random.randint(5, 15))
                
                # Pausa antes de la acción
                self.page.wait_for_timeout(random.uniform(100, 500))
                
                if action_type == "click":
                    # Click con timing humano
                    self.page.mouse.down()
                    self.page.wait_for_timeout(random.uniform(50, 150))
                    self.page.mouse.up()
                elif action_type == "type":
                    element.click()
                    
            return True
            
        except Exception as e:
            print(f"Error en interacción humana: {e}")
            return False

    def type_like_human(self, text, delay_range=(100, 300)):
        """
        Escribe texto de manera más humana con delays variables
        """
        for char in text:
            self.page.keyboard.type(char)
            # Delay aleatorio entre caracteres
            delay = random.uniform(delay_range[0], delay_range[1])
            self.page.wait_for_timeout(delay)
            
            # Ocasionalmente hacer pausas más largas (como si fuera pensando)
            if random.random() < 0.1:  # 10% de probabilidad
                self.page.wait_for_timeout(random.uniform(500, 1500))

    def get_cookies_availability(self):
        """
        Navigate to Apple Store and get cookies for availability check
        """
        if not self.page:
            raise ValueError("Browser page not initialized. Call setup_page() first.")
        
        try:
            # Navigate to Apple Store page directly with retry mechanism
            print("Accessing Apple Store website...")
            
            target_url = 'https://www.apple.com/shop/buy-iphone/iphone-17-pro'
            self.page.on("request", lambda request: self.parse_request(request) if "fulfillment-messages" in request.url else None)
            self.page.goto(target_url)
            self.page.wait_for_load_state('networkidle')
            
            # Esperar a que la página se estabilice
            self.page.wait_for_timeout(2000)
            # Obtener información básica de la página cargada
            page_title = self.page.title()
            current_url = self.page.url
            print(f"📄 Página cargada: '{page_title}'")
            print(f"🔗 URL final: {current_url}")
            

             # Esperar al elemento y asegurarse de que está en la vista
            size_selector = self.page.locator("input[data-autom='dimensionScreensize6_9inch']")
            size_selector.wait_for(state='attached')
            
            # Desactivar el scroll suave de la página
            self.page.evaluate("""() => {
                document.querySelector('.rf-bfe-stickybar').style.position = 'static';
                window.scrollTo = (x, y) => { window.scroll(x, y) };
            }""")
            
            # Hacer scroll y esperar
            self.page.evaluate("""() => {
                const element = document.querySelector("input[data-autom='dimensionScreensize6_9inch']");
                if (element) {
                    element.scrollIntoView();
                    window.scrollBy(0, -100); // Ajuste para evitar headers flotantes
                }
            }""")
            
            # Esperar a que el scroll se complete
            self.page.wait_for_timeout(1000)
            
            # Hacer click via JavaScript
            self.page.evaluate("""() => {
                const element = document.querySelector("input[data-autom='dimensionScreensize6_9inch']");
                if (element) {
                    element.click();
                    element.checked = true;
                }
            }""")
            
            # Esperar a que el click tome efecto
            self.page.wait_for_timeout(1000)
            
            # Continuar con las selecciones usando interacción humana
            for selector in [
                "input[data-autom='dimensionColordeepblue']",
                "input[value='2tb'][name='dimensionCapacity']",
                "#noTradeIn",
                "input[value='fullprice']",
                "input[name='carrierModel'][value='UNLOCKED/US']",
                "input[name='applecare-options'][data-autom='noapplecare']"
            ]:
                self.page.evaluate(f"""() => {{
                    const element = document.querySelector("{selector}");
                    if (element) {{
                        element.click();
                    }}
                }}""")
                self.page.wait_for_timeout(1000)
            # Click en Check availability con interacción humana
            # print("Haciendo click en 'Check availability'...")
            # availability_clicked = self.page.evaluate("""() => {
            #     const element = document.evaluate("//span[text()='Check availability']", 
            #         document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            #     if (element) {
            #         element.click();
            #         return true;
            #     }
            #     return false;
            # }""")
            
            # if not availability_clicked:
            #     print("❌ No se pudo hacer click en 'Check availability'")
            #     return None
            
            # Interceptar el request al hacer enter el zip code
            
            
            # # Escribir ZIP code de manera humana
            # print("Escribiendo código postal...")
            # search_input = self.page.locator("input[name='search']")
            # search_input.click()
            # self.type_like_human("33139")
            
            # # Esperar un momento antes de presionar Enter
            # self.page.wait_for_timeout(random.uniform(500, 1500))
            # self.page.keyboard.press("Enter")
            
            # # Esperar a que se complete la búsqueda
            # self.page.wait_for_timeout(3000)
            #request = request_info.value
            # print(f"Intercepted request to: {request.url}")
            # print(f"Request method: {request.method}")
            # print(f"Request headers: {request.headers}")
            # cookies = request.cookies()
            # print(f"Request cookies: {cookies}")
            # Get all cookies from the browser context
            
            cookies = self.browser.cookies()
            formatted_cookies = {}
            for cookie in cookies:
                formatted_cookies[cookie['name']] = cookie['value']
            # Save all formatted cookies
            with open('src/appleEndpoints/cookiesHome.json', 'w') as f:
                json.dump(formatted_cookies, f, indent=4)
                
            print(f"\nSaved {len(formatted_cookies)} cookies to cookiesHome.json")
            
            return formatted_cookies

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
    
    def close(self):
        """Close the browser and playwright instance"""
        try:
            if self.browser:
                self.browser.close()
        except Exception as e:
            print(f"Error closing browser: {str(e)}")
        
        try:
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            print(f"Error stopping playwright: {str(e)}")

    def diagnose_blank_page(self):
        """
        Diagnostica por qué una página está apareciendo en blanco
        """
        print("\n🔧 DIAGNÓSTICO DE PÁGINA EN BLANCO")
        print("="*50)
        
        try:
            # 1. Verificar si hay JavaScript errors
            print("1. Verificando errores de JavaScript...")
            js_errors = self.page.evaluate("""() => {
                const errors = [];
                
                // Verificar si hay errores en la consola
                if (window.console && window.console.error) {
                    errors.push('Console methods available');
                }
                
                // Verificar estado del documento
                errors.push('Document ready state: ' + document.readyState);
                errors.push('Document URL: ' + document.location.href);
                errors.push('Document title: ' + document.title);
                
                // Verificar si hay elementos básicos
                const bodyExists = !!document.body;
                const headExists = !!document.head;
                errors.push('Body exists: ' + bodyExists);
                errors.push('Head exists: ' + headExists);
                
                if (document.body) {
                    errors.push('Body children count: ' + document.body.children.length);
                    errors.push('Body innerHTML length: ' + document.body.innerHTML.length);
                }
                
                return errors;
            }""")
            
            for error in js_errors:
                print(f"   - {error}")
            
            # 2. Verificar si hay frames/iframes
            print("\n3. Verificando frames...")
            frames_count = len(self.page.frames)
            print(f"   - Total de frames: {frames_count}")
            
            for i, frame in enumerate(self.page.frames):
                try:
                    frame_url = frame.url
                    print(f"   - Frame {i}: {frame_url}")
                except:
                    print(f"   - Frame {i}: Error al obtener URL")
            
            # 3. Verificar si hay elementos visibles
            print("\n4. Verificando elementos visibles...")
            visible_elements = self.page.evaluate("""() => {
                const elements = document.querySelectorAll('*');
                let visible = 0;
                let hidden = 0;
                
                for (let el of elements) {
                    const style = window.getComputedStyle(el);
                    if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
                        visible++;
                    } else {
                        hidden++;
                    }
                }
                
                return {
                    total: elements.length,
                    visible: visible,
                    hidden: hidden,
                    viewportWidth: window.innerWidth,
                    viewportHeight: window.innerHeight
                };
            }""")
            
            print(f"   - Elementos totales: {visible_elements.get('total', 0)}")
            print(f"   - Elementos visibles: {visible_elements.get('visible', 0)}")
            print(f"   - Elementos ocultos: {visible_elements.get('hidden', 0)}")
            print(f"   - Viewport: {visible_elements.get('viewportWidth', 0)}x{visible_elements.get('viewportHeight', 0)}")
            
            # 4. Verificar CSS
            print("\n5. Verificando CSS...")
            css_info = self.page.evaluate("""() => {
                const stylesheets = document.styleSheets;
                const info = {
                    stylesheetCount: stylesheets.length,
                    loadedSheets: 0,
                    blockedSheets: 0
                };
                
                for (let sheet of stylesheets) {
                    try {
                        if (sheet.cssRules) {
                            info.loadedSheets++;
                        }
                    } catch (e) {
                        info.blockedSheets++;
                    }
                }
                
                return info;
            }""")
            
            print(f"   - Hojas de estilo: {css_info.get('stylesheetCount', 0)}")
            print(f"   - Cargadas: {css_info.get('loadedSheets', 0)}")
            print(f"   - Bloqueadas: {css_info.get('blockedSheets', 0)}")
            
            # 5. Tomar captura para análisis visual
            print("\n6. Tomando captura de pantalla...")
            self.take_screenshot_for_analysis("blank_page_diagnosis.png")
            
            # 6. Recomendaciones
            print("\n💡 RECOMENDACIONES:")
            if visible_elements.get('total', 0) < 10:
                print("   - La página tiene muy pocos elementos, posible bloqueo total")
            if css_info.get('blockedSheets', 0) > 0:
                print("   - Hay hojas de estilo bloqueadas, posible problema de CORS")
            if visible_elements.get('visible', 0) == 0:
                print("   - No hay elementos visibles, posible CSS que oculta todo")
            
            print("   - Considerar usar proxy/VPN diferente")
            print("   - Verificar si el sitio funciona en navegador normal")
            print("   - Intentar con User-Agent diferente")
            
        except Exception as e:
            print(f"❌ Error durante el diagnóstico: {e}")

    def try_alternative_urls(self):
        """
        Intenta URLs alternativas si la principal no funciona
        """
        alternative_urls = [
            'https://www.apple.com/shop/buy-iphone/iphone-17-pro',
            'https://www.apple.com/shop/buy-iphone',
            'https://www.apple.com/iphone/',
            'https://www.apple.com/shop/',
            'https://www.apple.com/'
        ]
        
        print("\n🔄 Intentando URLs alternativas...")
        
        for i, url in enumerate(alternative_urls):
            try:
                print(f"Intentando URL {i+1}: {url}")
                response = self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
                
                if response and response.status == 200:
                    content = self.page.inner_text('body', timeout=5000)
                    if len(content.strip()) > 100:
                        print(f"✅ URL funcional encontrada: {url}")
                        return url
                    else:
                        print(f"⚠️  URL carga pero con poco contenido")
                else:
                    print(f"❌ URL no respondió correctamente")
                    
            except Exception as e:
                print(f"❌ Error con URL {url}: {e}")
                continue
        
        print("❌ Ninguna URL alternativa funcionó")
        return None

    def wait_for_page_load_with_retry(self, url, max_retries=3):
        """
        Carga una página con reintentos automáticos en caso de fallo
        """
        for attempt in range(max_retries):
            try:
                print(f"🔄 Intento {attempt + 1} de {max_retries} para cargar: {url}")
                
                # Intentar cargar la página
                response = self.page.goto(url, wait_until='networkidle', timeout=45000)
                
                if not response:
                    print(f"❌ Intento {attempt + 1}: No se recibió respuesta")
                    continue
                
                if response.status != 200:
                    print(f"❌ Intento {attempt + 1}: Código HTTP {response.status}")
                    if attempt < max_retries - 1:
                        print("⏳ Esperando antes del siguiente intento...")
                        self.page.wait_for_timeout(random.uniform(3000, 7000))
                    continue
                
                # Verificar que haya contenido
                try:
                    content = self.page.inner_text('body', timeout=10000)
                    if len(content.strip()) < 50:
                        print(f"❌ Intento {attempt + 1}: Página con poco contenido")
                        if attempt < max_retries - 1:
                            print("🔄 Recargando página...")
                            self.page.reload(wait_until='networkidle', timeout=30000)
                        continue
                    else:
                        print(f"✅ Página cargada exitosamente en intento {attempt + 1}")
                        return True
                        
                except Exception as e:
                    print(f"❌ Intento {attempt + 1}: Error al verificar contenido: {e}")
                    continue
                    
            except Exception as e:
                print(f"❌ Intento {attempt + 1}: Error de navegación: {e}")
                if attempt < max_retries - 1:
                    print("⏳ Esperando antes del siguiente intento...")
                    self.page.wait_for_timeout(random.uniform(5000, 10000))
                continue
        
        print(f"❌ Falló la carga después de {max_retries} intentos")
        return False

    def monitor_network_requests(self):
        """
        Monitorea requests para detectar bloqueos o comportamientos anómalos
        """
        blocked_requests = []
        suspicious_responses = []
        
        def handle_request(request):
            # Detectar requests bloqueados o sospechosos
            if request.failure:
                blocked_requests.append({
                    'url': request.url,
                    'failure': request.failure,
                    'method': request.method
                })
        
        def handle_response(response):
            # Detectar respuestas sospechosas
            if response.status in [403, 429, 503, 406]:
                suspicious_responses.append({
                    'url': response.url,
                    'status': response.status,
                    'headers': dict(response.headers)
                })
        
        # Configurar listeners
        self.page.on("request", handle_request)
        self.page.on("response", handle_response)
        
        return blocked_requests, suspicious_responses

    def get_fingerprint_info(self):
        """
        Obtiene información del fingerprint del navegador para análisis
        """
        fingerprint = self.page.evaluate("""() => {
            const info = {};
            
            try {
                info.userAgent = navigator.userAgent;
                info.language = navigator.language;
                info.languages = navigator.languages;
                info.platform = navigator.platform;
                info.hardwareConcurrency = navigator.hardwareConcurrency;
                info.deviceMemory = navigator.deviceMemory || 'undefined';
                info.webdriver = navigator.webdriver;
                
                // Plugins con manejo de errores
                try {
                    info.plugins = Array.from(navigator.plugins).map(p => p.name);
                } catch (e) {
                    info.plugins = [];
                    info.pluginsError = e.message;
                }
                
                // MimeTypes con manejo de errores
                try {
                    info.mimeTypes = Array.from(navigator.mimeTypes).map(m => m.type);
                } catch (e) {
                    info.mimeTypes = [];
                    info.mimeTypesError = e.message;
                }
                
                // Screen info con manejo de errores
                try {
                    info.screen = {
                        width: screen.width,
                        height: screen.height,
                        colorDepth: screen.colorDepth,
                        pixelDepth: screen.pixelDepth
                    };
                } catch (e) {
                    info.screen = {};
                    info.screenError = e.message;
                }
                
                // Timezone con manejo de errores
                try {
                    info.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
                } catch (e) {
                    info.timezone = 'undefined';
                    info.timezoneError = e.message;
                }
                
                // Canvas fingerprint con manejo de errores
                try {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    ctx.textBaseline = 'top';
                    ctx.font = '14px Arial';
                    ctx.fillText('Bot detection test 🤖', 2, 2);
                    info.canvas = canvas.toDataURL();
                } catch (e) {
                    info.canvas = 'error';
                    info.canvasError = e.message;
                }
                
                // WebGL info con manejo de errores
                try {
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                    if (!gl) {
                        info.webgl = 'not supported';
                    } else {
                        info.webgl = {
                            vendor: gl.getParameter(gl.VENDOR),
                            renderer: gl.getParameter(gl.RENDERER)
                        };
                    }
                } catch (e) {
                    info.webgl = 'error';
                    info.webglError = e.message;
                }
                
            } catch (e) {
                info.generalError = e.message;
            }
            
            return info;
        }""")
        
        print("\n🔍 INFORMACIÓN DEL FINGERPRINT:")
        print(f"User Agent: {fingerprint.get('userAgent', 'N/A')}")
        print(f"Webdriver detectado: {fingerprint.get('webdriver', 'N/A')}")
        print(f"Plugins: {len(fingerprint.get('plugins', []))}")
        
        screen_info = fingerprint.get('screen', {})
        if screen_info:
            print(f"Resolución: {screen_info.get('width', 'N/A')}x{screen_info.get('height', 'N/A')}")
        else:
            print(f"Resolución: Error - {fingerprint.get('screenError', 'Unknown')}")
            
        print(f"Zona horaria: {fingerprint.get('timezone', 'N/A')}")
        
        # Mostrar errores si los hay
        error_keys = [key for key in fingerprint.keys() if key.endswith('Error')]
        if error_keys:
            print("\n⚠️  Errores detectados:")
            for error_key in error_keys:
                print(f"   - {error_key}: {fingerprint[error_key]}")
        
        return fingerprint

    def take_screenshot_for_analysis(self, filename="bot_detection_analysis.png"):
        """
        Toma una captura de pantalla para análisis visual
        """
        try:
            screenshot_path = f"screenshots/{filename}"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            self.page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Captura guardada en: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"Error al tomar captura: {e}")
            return None

    def quick_bot_check(self):
        """
        Verificación rápida de detección de bot sin acceder a propiedades restringidas
        """
        print("\n🔍 Verificación rápida de detección de bot...")
        
        detection_signs = []
        
        try:
            # 1. Verificar URL actual
            current_url = self.page.url
            if any(keyword in current_url.lower() for keyword in ['challenge', 'verify', 'blocked', 'captcha']):
                detection_signs.append(f"URL sospechosa: {current_url}")
            
            # 2. Verificar título de la página
            title = self.page.title()
            if any(keyword in title.lower() for keyword in ['blocked', 'access denied', 'verification', 'captcha']):
                detection_signs.append(f"Título sospechoso: {title}")
            
            # 3. Verificar presencia de CAPTCHAs (más selectivo)
            captcha_present = self.page.locator("iframe[src*='recaptcha'], iframe[src*='hcaptcha'], .g-recaptcha").count() > 0
            if captcha_present:
                detection_signs.append("CAPTCHA detectado en la página")
            
            # 4. Verificar mensajes de error visibles
            error_messages = [
                "unusual traffic", "suspicious activity", "access denied",
                "blocked", "try again later", "verification required"
            ]
            
            page_text = self.page.inner_text('body').lower() if self.page.locator('body').count() > 0 else ""
            for message in error_messages:
                if message in page_text:
                    detection_signs.append(f"Mensaje de error detectado: '{message}'")
                    break
            
            # 5. Verificar códigos de respuesta HTTP si es posible
            try:
                response = self.page.goto(self.page.url, wait_until="domcontentloaded")
                if response and response.status in [403, 429, 503]:
                    detection_signs.append(f"Código HTTP sospechoso: {response.status}")
            except:
                pass  # Ignorar errores de navegación
            
            if detection_signs:
                print("❌ Señales de detección encontradas:")
                for sign in detection_signs:
                    print(f"   - {sign}")
                return True
            else:
                print("✅ No se detectaron señales obvias de bloqueo")
                return False
                
        except Exception as e:
            print(f"⚠️  Error durante la verificación: {e}")
            return False
        """
        Análisis completo para detectar si somos identificados como bot
        """
        print("\n" + "="*60)
        print("🔍 ANÁLISIS COMPLETO DE DETECCIÓN DE BOT")
        print("="*60)
        
        # 1. Verificar detección básica
        print("\n1. Verificando detección básica...")
        is_detected = self.check_bot_detection()
        
        # 2. Obtener fingerprint
        print("\n2. Analizando fingerprint del navegador...")
        fingerprint = self.get_fingerprint_info()
        
        # 3. Tomar captura para análisis visual
        print("\n3. Tomando captura de pantalla...")
        self.take_screenshot_for_analysis()
        
        # 4. Verificar timing de carga
        print("\n4. Verificando timing de carga...")
        try:
            timing_info = self.page.evaluate("""() => {
                try {
                    const perf = performance.getEntriesByType('navigation')[0];
                    if (!perf) return null;
                    
                    const paintEntries = performance.getEntriesByType('paint');
                    
                    return {
                        loadTime: perf.loadEventEnd - perf.fetchStart,
                        domContentLoaded: perf.domContentLoadedEventEnd - perf.fetchStart,
                        firstPaint: paintEntries.find(p => p.name === 'first-paint')?.startTime || null,
                        firstContentfulPaint: paintEntries.find(p => p.name === 'first-contentful-paint')?.startTime || null
                    };
                } catch (e) {
                    return { error: e.message };
                }
            }""")
            
            if timing_info and not timing_info.get('error'):
                print(f"Tiempo de carga total: {timing_info.get('loadTime', 'N/A')}ms")
                print(f"DOM Content Loaded: {timing_info.get('domContentLoaded', 'N/A')}ms")
                print(f"First Paint: {timing_info.get('firstPaint', 'N/A')}ms")
            elif timing_info and timing_info.get('error'):
                print(f"Error al obtener timing: {timing_info['error']}")
                timing_info = None
            else:
                print("No se pudo obtener información de timing")
                timing_info = None
        except Exception as e:
            print(f"Error al verificar timing: {e}")
            timing_info = None
        
        # 5. Verificar JavaScript capabilities
        print("\n5. Verificando capacidades de JavaScript...")
        js_capabilities = self.page.evaluate("""() => {
            const capabilities = {};
            
            // Verificar localStorage con manejo de errores
            try {
                capabilities.localStorage = typeof localStorage !== 'undefined' && localStorage !== null;
                // Intentar acceder realmente
                localStorage.getItem('test');
            } catch (e) {
                capabilities.localStorage = false;
                capabilities.localStorageError = e.message;
            }
            
            // Verificar sessionStorage con manejo de errores
            try {
                capabilities.sessionStorage = typeof sessionStorage !== 'undefined' && sessionStorage !== null;
                sessionStorage.getItem('test');
            } catch (e) {
                capabilities.sessionStorage = false;
                capabilities.sessionStorageError = e.message;
            }
            
            // Verificar WebGL con manejo de errores
            try {
                const canvas = document.createElement('canvas');
                capabilities.webGL = canvas.getContext('webgl') !== null || canvas.getContext('experimental-webgl') !== null;
            } catch (e) {
                capabilities.webGL = false;
                capabilities.webGLError = e.message;
            }
            
            // Verificar Web Workers con manejo de errores
            try {
                capabilities.webWorkers = typeof Worker !== 'undefined';
            } catch (e) {
                capabilities.webWorkers = false;
                capabilities.webWorkersError = e.message;
            }
            
            // Verificar Geolocation con manejo de errores
            try {
                capabilities.geolocation = 'geolocation' in navigator;
            } catch (e) {
                capabilities.geolocation = false;
                capabilities.geolocationError = e.message;
            }
            
            // Verificar Notifications con manejo de errores
            try {
                capabilities.notifications = 'Notification' in window;
            } catch (e) {
                capabilities.notifications = false;
                capabilities.notificationsError = e.message;
            }
            
            // Verificar IndexedDB con manejo de errores
            try {
                capabilities.indexedDB = 'indexedDB' in window;
            } catch (e) {
                capabilities.indexedDB = false;
                capabilities.indexedDBError = e.message;
            }
            
            // Verificar ServiceWorker con manejo de errores
            try {
                capabilities.serviceWorker = 'serviceWorker' in navigator;
            } catch (e) {
                capabilities.serviceWorker = false;
                capabilities.serviceWorkerError = e.message;
            }
            
            return capabilities;
        }""")
        
        for capability, supported in js_capabilities.items():
            if capability.endswith('Error'):
                continue  # Skip error messages for now
            status = "✅" if supported else "❌"
            error_key = f"{capability}Error"
            error_msg = js_capabilities.get(error_key, "")
            if error_msg:
                print(f"{status} {capability}: {supported} (Error: {error_msg})")
            else:
                print(f"{status} {capability}: {supported}")
        
        # 6. Resumen final
        print("\n" + "="*60)
        print("📊 RESUMEN DEL ANÁLISIS")
        print("="*60)
        
        if is_detected:
            print("❌ RESULTADO: Posible detección como bot")
            print("\n💡 RECOMENDACIONES:")
            print("   - Cambiar User Agent")
            print("   - Usar proxy/VPN")
            print("   - Aumentar delays entre acciones")
            print("   - Verificar fingerprint del navegador")
        else:
            print("✅ RESULTADO: No se detectó como bot")
            print("\n👍 El bot parece estar funcionando correctamente")
        
        return {
            'detected': is_detected,
            'fingerprint': fingerprint,
            'timing': timing_info,
            'js_capabilities': js_capabilities
        }

    def parse_request(self, request):
        """Parse a Playwright request object to extract method, url, headers, and cookies"""
        method = request.method
        url = request.url
        headers = request.headers
        #save headers to a json file
        with open('src/appleEndpoints/headers.json', 'w') as f:
            json.dump(headers, f, indent=4)
        print(f"Request Method: {method},\n--------------------------------")
        print(f"Request URL: {url},\n--------------------------------")
        print(f"Request Headers: {headers},\n--------------------------------")

def format_cookies_for_requests(cookies):
    """Format cookies for use with the requests library"""
    return {cookie['name']: cookie['value'] for cookie in cookies}

def get_apple_auth_cookies():
    """Legacy function for backward compatibility"""
    bot = botIphone()
    try:
        bot.setup_page()
        return bot.get_cookies_availability()
    finally:
        bot.close()

if __name__ == "__main__":
    bot = botIphone()
    bot.setup_page(persistent_data=False,browser_engine="webkit",channel="edge")
    bot.get_cookies_availability()
