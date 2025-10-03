"""
Navegador web simple usando undetected-chromedriver
Versión final que suprime el error conocido del destructor de Chrome en Windows
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import logging
import os
import tempfile
import gc
import warnings
import sys
import json

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Suprimir warnings específicos de undetected_chromedriver
warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_chrome_user_data_dir():
    """
    Obtener el directorio de datos del usuario de Chrome
    """
    import os
    
    # Rutas comunes de Chrome en Windows
    possible_paths = [
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data"),
        os.path.expanduser(r"~\AppData\Local\Google\Chrome Beta\User Data"),
        os.path.expanduser(r"~\AppData\Local\Google\Chrome Dev\User Data"),
        os.path.expanduser(r"~\AppData\Local\Chromium\User Data"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Encontrado directorio de Chrome: {path}")
            return path
    
    logger.warning("No se encontró ningún directorio de datos de Chrome")
    return None

def list_chrome_profiles(user_data_dir):
    """
    Listar los perfiles disponibles en Chrome
    """
    import os
    import json
    
    if not user_data_dir or not os.path.exists(user_data_dir):
        return []
    
    profiles = []
    
    # Buscar carpetas de perfil
    for item in os.listdir(user_data_dir):
        profile_path = os.path.join(user_data_dir, item)
        if os.path.isdir(profile_path) and (item == "Default" or item.startswith("Profile ")):
            profiles.append(item)
    
    logger.info(f"Perfiles encontrados: {profiles}")
    return profiles

def suppress_chrome_destructor_error():
    """
    Función para suprimir el error conocido del destructor de Chrome en Windows
    """
    import builtins
    original_print = builtins.print
    
    def patched_print(*args, **kwargs):
        # Filtrar mensajes de error específicos del destructor de Chrome
        text = ' '.join(str(arg) for arg in args)
        if (
            "Exception ignored in:" in text and 
            "Chrome.__del__" in text and 
            "Controlador no válido" in text
        ):
            return  # No imprimir este error específico
        return original_print(*args, **kwargs)
    
    builtins.print = patched_print

class SafeChromeDriver:
    """Wrapper para undetected_chromedriver con manejo seguro del cierre"""
    
    def __init__(self, version_main=119):
        self.driver = None
        self.version_main = version_main
        self._closed = False
        # Registro de procesos para limpieza manual si es necesario
        self._processes = []
        
    def __enter__(self):
        self.driver = self._create_driver()
        return self.driver
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def _create_driver(self):
        """Crear driver de Chrome con configuración optimizada usando datos persistentes del usuario"""
        try:
            options = uc.ChromeOptions()
            
            # Obtener el directorio de datos del usuario real de Chrome
            chrome_user_data = get_chrome_user_data_dir()
            
            # Configurar el directorio de datos del usuario si se encuentra
            if chrome_user_data:
                profiles = list_chrome_profiles(chrome_user_data)

                # Usar el perfil 3 si existe, sino el primero disponible
                profile_to_use = "Default"
                if "Default" not in profiles and profiles:
                    profile_to_use = profiles[0]
                    logger.info(f"Perfil Default no encontrado, usando: {profile_to_use}")
                
                logger.info(f"Usando datos de usuario de Chrome: {chrome_user_data}")
                logger.info(f"Usando perfil: {profile_to_use}")
                
                options.add_argument(f'--user-data-dir={chrome_user_data}')
                options.add_argument(f'--profile-directory={profile_to_use}')
                
                # IMPORTANTE: Evitar conflictos si Chrome está abierto
                #options.add_argument('--remote-debugging-port=9222')
                
            else:
                logger.warning("No se encontró el directorio de datos de Chrome, usando perfil temporal")
            
            # Configuraciones básicas de seguridad (reducidas para permitir más funcionalidades)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-first-run')
            
            # IMPORTANTE: NO deshabilitar extensiones para mantener la experiencia real del usuario
            # options.add_argument('--disable-extensions')  # Comentado para permitir extensiones
            
            # Configuraciones adicionales para estabilidad con datos reales
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-features=VizDisplayCompositor')
            
            # Configurar el User-Agent para que coincida con el navegador real
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--window-size=1920,1080')
            
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--enable-javascript')
        

            ##testing
            options.add_argument('--window-size=1920,1080')

            logger.info(f"Configurando ChromeDriver para versión {self.version_main} con datos persistentes...")
            
            driver = uc.Chrome(
                options=options,
                version_main=119,
                headless=False,
                use_subprocess=True,  # Importante para evitar conflictos con Chrome abierto
                driver_executable_path=None
            )
            
            logger.info(f"✓ Driver creado exitosamente con versión {self.version_main}")
            return driver
            
        except Exception as e:
            logger.error(f"Error creando driver: {e}")
            raise
    
    def close(self):
        """Cerrar el driver de forma segura"""
        if self.driver is not None and not self._closed:
            try:
                logger.info("Cerrando navegador de forma segura...")
                
                # Intentar ejecutar JavaScript para limpiar la página
                try:
                    self.driver.execute_script("window.stop();")
                except:
                    pass
                
                # Cerrar todas las pestañas de una en una
                try:
                    handles = list(self.driver.window_handles)
                    while len(handles) > 1:
                        self.driver.switch_to.window(handles[-1])
                        self.driver.close()
                        handles = self.driver.window_handles
                        
                    # Volver a la ventana principal y cerrarla
                    if handles:
                        self.driver.switch_to.window(handles[0])
                        
                except Exception as e:
                    logger.debug(f"Error cerrando ventanas: {e}")
                
                # Llamar quit() con manejo de excepciones
                try:
                    self.driver.quit()
                except Exception as e:
                    logger.debug(f"Error en quit(): {e}")
                
                # Marcar como cerrado antes de limpiar
                self._closed = True
                
                # Limpiar referencia
                old_driver = self.driver
                self.driver = None
                del old_driver
                
                # Esperar un momento para que los procesos terminen
                time.sleep(0.3)
                
                logger.info("✓ Navegador cerrado correctamente")
                
            except Exception as e:
                logger.warning(f"Error al cerrar navegador: {e}")
                self._closed = True
                self.driver = None

def configure_apple_product(driver):
    """
    Configura las opciones del producto Apple utilizando los selectores específicos
    """
    logger.info("Configurando opciones del producto...")
    
    # Lista de selectores a procesar
    selectors = [
        ("input[data-autom='dimensionColordeepblue']", "Color Deep Blue"),
        ("input[value='2tb'][name='dimensionCapacity']", "Capacidad 2TB"),
        ("#noTradeIn", "Sin intercambio"),
        ("input[value='fullprice']", "Precio completo"),
        ("input[name='carrierModel'][value='UNLOCKED/US']", "Desbloqueado US"),
        ("input[name='applecare-options'][data-autom='noapplecare']", "Sin AppleCare")
    ]
    
    for selector, description in selectors:
        try:
            logger.info(f"Seleccionando: {description}")
            
            # Ejecutar click usando JavaScript como en el código original
            result = driver.execute_script(f"""
                const element = document.querySelector("{selector}");
                if (element) {{
                    element.click();
                    return 'success';
                }} else {{
                    return 'not_found';
                }}
            """)
            
            if result == 'success':
                logger.info(f"✓ {description} seleccionado exitosamente")
            else:
                logger.warning(f"⚠ Elemento no encontrado para: {description}")
            
            # Pausa entre selecciones para comportamiento más natural
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error seleccionando {description}: {e}")
    
    logger.info("Configuración del producto completada")

def configure_apple_product_selenium(driver):
    """
    Versión alternativa usando Selenium WebDriverWait para configurar las opciones del producto
    """
    logger.info("Configurando opciones del producto usando Selenium WebDriverWait...")
    
    wait = WebDriverWait(driver, 10)
    
    # Lista de selectores con sus respectivos localizadores de Selenium
    selectors = [
        (By.CSS_SELECTOR, "input[data-autom='dimensionColordeepblue']", "Color Deep Blue"),
        (By.CSS_SELECTOR, "input[value='2tb'][name='dimensionCapacity']", "Capacidad 2TB"),
        (By.CSS_SELECTOR, "#noTradeIn", "Sin intercambio"),
        (By.CSS_SELECTOR, "input[value='fullprice']", "Precio completo"),
        (By.CSS_SELECTOR, "input[name='carrierModel'][value='UNLOCKED/US']", "Desbloqueado US"),
        (By.CSS_SELECTOR, "input[name='applecare-options'][data-autom='noapplecare']", "Sin AppleCare")
    ]
    
    for by_method, selector, description in selectors:
        try:
            logger.info(f"Esperando y seleccionando: {description}")
            
            # Esperar a que el elemento esté presente y sea clickeable
            element = wait.until(EC.element_to_be_clickable((by_method, selector)))
            
            # Hacer scroll al elemento si es necesario
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
            
            # Intentar click normal primero, luego JavaScript si falla
            try:
                element.click()
                logger.info(f"✓ {description} seleccionado exitosamente (click normal)")
            except Exception:
                driver.execute_script("arguments[0].click();", element)
                logger.info(f"✓ {description} seleccionado exitosamente (JavaScript click)")
            
            # Pausa entre selecciones
            time.sleep(1)
            
        except TimeoutException:
            logger.warning(f"⚠ Timeout esperando elemento: {description}")
        except Exception as e:
            logger.error(f"Error seleccionando {description}: {e}")
    
    logger.info("Configuración del producto completada con Selenium")

def save_cookies_to_file(driver, filename='cookiesHome.json'):
    """
    Guarda las cookies del navegador en un archivo JSON
    """
    try:
        cookies = driver.get_cookies()
        formatted_cookies = {}
        
        for cookie in cookies:
            formatted_cookies[cookie['name']] = cookie['value']
        
        # Crear directorio si no existe
        os.makedirs('src/appleEndpoints', exist_ok=True)
        filepath = f'src/appleEndpoints/{filename}'
        
        with open(filepath, 'w') as f:
            json.dump(formatted_cookies, f, indent=4)
        
        logger.info(f"✓ Guardadas {len(formatted_cookies)} cookies en {filepath}")
        return formatted_cookies
        
    except Exception as e:
        logger.error(f"Error guardando cookies: {e}")
        return None

def capture_network_headers_advanced(driver):
    """
    Intenta capturar headers de red usando Performance API y otras técnicas avanzadas
    Esta función demuestra las limitaciones adicionales de captura de headers
    """
    try:
        logger.info("Intentando capturar headers de red usando Performance API...")
        
        # Intentar capturar información de rendimiento de red
        performance_data = driver.execute_script("""
            const perfEntries = performance.getEntriesByType('navigation');
            const resourceEntries = performance.getEntriesByType('resource');
            
            return {
                navigationEntries: perfEntries.map(entry => ({
                    name: entry.name,
                    type: entry.type,
                    startTime: entry.startTime,
                    duration: entry.duration,
                    transferSize: entry.transferSize,
                    encodedBodySize: entry.encodedBodySize,
                    decodedBodySize: entry.decodedBodySize,
                    protocol: entry.nextHopProtocol,
                    redirectCount: entry.redirectCount
                })),
                resourceEntries: resourceEntries.slice(0, 5).map(entry => ({
                    name: entry.name,
                    type: entry.initiatorType,
                    transferSize: entry.transferSize,
                    protocol: entry.nextHopProtocol
                })),
                timing: performance.timing ? {
                    navigationStart: performance.timing.navigationStart,
                    fetchStart: performance.timing.fetchStart,
                    connectStart: performance.timing.connectStart,
                    secureConnectionStart: performance.timing.secureConnectionStart,
                    requestStart: performance.timing.requestStart,
                    responseStart: performance.timing.responseStart,
                    responseEnd: performance.timing.responseEnd
                } : null
            };
        """)
        
        logger.info(f"Performance API capturó {len(performance_data['navigationEntries'])} navigation entries")
        logger.info(f"Performance API capturó {len(performance_data['resourceEntries'])} resource entries")
        
        return performance_data
        
    except Exception as e:
        logger.warning(f"No se pudo capturar datos de Performance API: {e}")
        return None

def save_headers_to_file(driver, filename='headers.json'):
    """
    Guarda los headers del navegador en un archivo JSON
    Extrae toda la información posible del navegador (limitado por las APIs de Selenium/JavaScript)
    """
    try:
        logger.info("Capturando información del navegador para generar headers...")
        
        # Capturar información avanzada de red si es posible
        performance_data = capture_network_headers_advanced(driver)
        
        # Obtener toda la información posible del navegador
        browser_info = driver.execute_script("""
            return {
                userAgent: navigator.userAgent,
                language: navigator.language,
                languages: navigator.languages,
                platform: navigator.platform,
                cookieEnabled: navigator.cookieEnabled,
                onLine: navigator.onLine,
                doNotTrack: navigator.doNotTrack,
                maxTouchPoints: navigator.maxTouchPoints,
                hardwareConcurrency: navigator.hardwareConcurrency,
                deviceMemory: navigator.deviceMemory || 'unknown',
                connection: navigator.connection ? {
                    effectiveType: navigator.connection.effectiveType,
                    type: navigator.connection.type,
                    downlink: navigator.connection.downlink,
                    rtt: navigator.connection.rtt
                } : null,
                webdriver: navigator.webdriver,
                vendor: navigator.vendor,
                vendorSub: navigator.vendorSub,
                product: navigator.product,
                productSub: navigator.productSub,
                appName: navigator.appName,
                appVersion: navigator.appVersion,
                appCodeName: navigator.appCodeName,
                // Screen info
                screenWidth: screen.width,
                screenHeight: screen.height,
                screenColorDepth: screen.colorDepth,
                screenPixelDepth: screen.pixelDepth,
                // Window info
                windowInnerWidth: window.innerWidth,
                windowInnerHeight: window.innerHeight,
                windowOuterWidth: window.outerWidth,
                windowOuterHeight: window.outerHeight,
                // Timezone
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                // Chrome specific
                chrome: !!window.chrome,
                chromeVersion: window.chrome ? window.chrome.runtime ? 'available' : 'limited' : 'not_chrome'
            };
        """)
        
        logger.info(f"Información del navegador capturada: {len(browser_info)} propiedades")
        
        # Extraer versión de Chrome del User-Agent
        import re
        chrome_version_match = re.search(r'Chrome/(\d+)\.(\d+)\.(\d+)\.(\d+)', browser_info['userAgent'])
        chrome_version = chrome_version_match.group(1) if chrome_version_match else '141'
        
        # Generar headers basados en información real del navegador
        headers = {
            'User-Agent': browser_info['userAgent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': f"{browser_info['language']},{browser_info['language'].split('-')[0]};q=0.9" if browser_info['language'] else 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': f'"Google Chrome";v="{chrome_version}", "Chromium";v="{chrome_version}", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': f'"{browser_info["platform"]}"' if browser_info['platform'] else '"Windows"',
            'Cache-Control': 'max-age=0'
        }
        
        # Guardar tanto los headers como la información completa del navegador
        output_data = {
            'headers': headers,
            'browser_info': browser_info,
            'performance_data': performance_data,
            'generation_timestamp': time.time(),
            'note': 'Headers generados desde información real del navegador. Limitado por APIs de Selenium/JavaScript.',
            'limitations': [
                'No se pueden capturar headers HTTP reales (limitación de Selenium/WebDriver)',
                'Los headers se generan basándose en información del navegador disponible via JavaScript',
                'Algunos headers como Referer, Host, etc. se generan automáticamente en peticiones reales',
                'Performance API proporciona información limitada sobre transferencias de red',
                'Para capturar headers HTTP completos necesitarías usar herramientas como mitmproxy o Chrome DevTools Protocol'
            ]
        }
        
        # Crear directorio si no existe
        os.makedirs('src/appleEndpoints', exist_ok=True)
        filepath = f'src/appleEndpoints/{filename}'
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=4)
        
        # También crear un archivo simplificado solo con headers para compatibilidad
        headers_only_file = filename.replace('.json', '_simple.json')
        headers_only_path = f'src/appleEndpoints/{headers_only_file}'
        with open(headers_only_path, 'w') as f:
            json.dump(headers, f, indent=4)
        
        logger.info(f"✓ Guardados headers y información del navegador en {filepath}")
        logger.info(f"✓ Guardados headers simplificados en {headers_only_path}")
        logger.info(f"User-Agent detectado: {browser_info['userAgent'][:100]}...")
        logger.info(f"Plataforma: {browser_info['platform']}")
        logger.info(f"Idioma: {browser_info['language']}")
        
        # Información sobre limitaciones y alternativas
        logger.info("=== LIMITACIONES Y ALTERNATIVAS ===")
        logger.info("❌ Selenium NO puede capturar headers HTTP reales de las peticiones")
        logger.info("❌ JavaScript en el navegador NO tiene acceso a headers HTTP completos")
        logger.info("✅ Alternativas para capturar headers completos:")
        logger.info("  1. Chrome DevTools Protocol (CDP)")
        logger.info("  2. Proxy interceptor como mitmproxy")
        logger.info("  3. Network monitoring tools")
        logger.info("  4. Browser extensions con permisos especiales")
        
        return headers
        
    except Exception as e:
        logger.error(f"Error guardando headers: {e}")
        return None

def capture_real_headers_with_cdp(driver):
    """
    Función experimental para capturar headers reales usando Chrome DevTools Protocol
    NOTA: Esto requiere configuración especial del driver y no está implementado completamente
    """
    logger.info("=== FUNCIÓN EXPERIMENTAL: Chrome DevTools Protocol ===")
    logger.info("Para capturar headers HTTP reales necesitarías:")
    logger.info("1. Habilitar CDP en el driver")
    logger.info("2. Usar driver.execute_cdp_cmd() si está disponible")
    logger.info("3. Configurar Network domain para capturar eventos de red")
    
    try:
        # Verificar si CDP está disponible
        if hasattr(driver, 'execute_cdp_cmd'):
            logger.info("✅ CDP disponible en este driver")
            
            # Intentar habilitar network domain
            try:
                driver.execute_cdp_cmd('Network.enable', {})
                logger.info("✅ Network domain habilitado")
                
                # Esta sería la forma de capturar eventos de red, pero requiere
                # configuración adicional y manejo de eventos asíncronos
                logger.info("⚠ Captura completa de headers requiere implementación adicional de eventos CDP")
                
            except Exception as e:
                logger.warning(f"⚠ No se pudo habilitar Network domain: {e}")
                
        else:
            logger.warning("❌ CDP no disponible en este driver")
            
    except Exception as e:
        logger.error(f"Error explorando CDP: {e}")
    
    return None

def main():
    """Función principal del script"""
    # Activar supresión de errores del destructor
    suppress_chrome_destructor_error()
    
    logger.info("=== Iniciando navegador para Chrome versión 134 ===")
    
    try:
        # Usar el context manager para manejo seguro
        with SafeChromeDriver(version_main=119) as driver:
            
            # Navegar a la página
            logger.info("Navegando a Apple iPhone...")
            driver.get('https://www.apple.com/shop/buy-iphone/iphone-17-pro')
            
            # Esperar a que la página cargue completamente
            wait = WebDriverWait(driver,20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Esperar un momento adicional para que todos los elementos se carguen
            time.sleep(5)
            
            # Configurar las opciones del producto
            # Puedes cambiar entre configure_apple_product (JavaScript) o 
            # configure_apple_product_selenium (Selenium WebDriverWait)
            try:
                configure_apple_product(driver)  # Método JavaScript
            except Exception as e:
                logger.warning(f"Error con método JavaScript, intentando con Selenium: {e}")
                configure_apple_product_selenium(driver)  # Método Selenium alternativo
            
            # Tomar captura de pantalla después de las configuraciones
            screenshot_name = 'apple_iphone_chrome134_configured.png'
            driver.save_screenshot(screenshot_name)
            logger.info(f"Captura guardada como: {screenshot_name}")
            
            # Mostrar información del navegador y perfil
            try:
                user_agent = driver.execute_script("return navigator.userAgent")
                logger.info(f"User Agent: {user_agent}")
                
                chrome_version = driver.execute_script("return navigator.appVersion")
                logger.info(f"Chrome Version Info: {chrome_version}")
                
                # Verificar si las cookies del usuario están disponibles
                cookies = driver.get_cookies()
                logger.info(f"Cookies cargadas: {len(cookies)} cookies encontradas")
                
                # Guardar cookies en archivo
                save_cookies_to_file(driver)
                
                # Guardar headers en archivo
                save_headers_to_file(driver)
                
                # Explorar captura avanzada de headers (experimental)
                capture_real_headers_with_cdp(driver)
                
                # Verificar si hay extensiones cargadas (esto indica que el perfil del usuario está activo)
                try:
                    extension_info = driver.execute_script("return window.chrome && window.chrome.runtime ? 'Extensions available' : 'No extensions'")
                    logger.info(f"Estado de extensiones: {extension_info}")
                except:
                    logger.info("No se pudo verificar el estado de las extensiones")
                
            except Exception as e:
                logger.warning(f"No se pudo obtener información del navegador: {e}")
            
            # Mantener abierto por más tiempo para ver los resultados
            logger.info("Manteniendo navegador abierto por 10 segundos para revisar configuración...")
            time.sleep(10)
    
    except Exception as e:
        logger.error(f"Error durante la ejecución: {e}")
        raise
    
    finally:
        # Limpieza final agresiva
        gc.collect()
        logger.info("=== Script finalizado exitosamente ===")

if __name__ == "__main__":
    main()