"""
Navegador web con múltiples opciones: undetected-chromedriver y Selenium estándar
Incluye fallback automático cuando undetected-chromedriver tiene problemas
"""

# Intentar importar undetected_chromedriver
try:
    import undetected_chromedriver as uc
    UC_AVAILABLE = True
except ImportError as e:
    print(f"undetected_chromedriver no disponible: {e}")
    UC_AVAILABLE = False

# Importar Selenium estándar como fallback
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError as e:
    print(f"Selenium estándar no disponible: {e}")
    SELENIUM_AVAILABLE = False

try:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
except ImportError as e:
    print(f"Error importando componentes de selenium: {e}")
    raise

import time
import logging
import sys
import os
import tempfile

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebNavigator:
    """
    Navegador web con fallback automático entre undetected-chromedriver y Selenium estándar
    """
    
    def __init__(self, headless=True, prefer_undetected=True, user_data_dir=None):
        """
        Inicializar el navegador
        
        Args:
            headless (bool): Ejecutar en modo headless
            prefer_undetected (bool): Preferir undetected-chromedriver si está disponible
            user_data_dir (str): Directorio de datos de usuario personalizado
        """
        self.driver = None
        self.headless = headless
        self.prefer_undetected = prefer_undetected and UC_AVAILABLE
        self.user_data_dir = user_data_dir or self._create_temp_profile()
        self.driver_type = None
        
    def _create_temp_profile(self):
        """Crear un directorio temporal para el perfil de Chrome"""
        temp_dir = tempfile.mkdtemp(prefix="web_navigator_")
        logger.info(f"Usando directorio temporal para perfil: {temp_dir}")
        return temp_dir
    
    def setup_driver(self):
        """Configurar el driver de Chrome con fallback automático"""
        
        # Intentar undetected-chromedriver primero si se prefiere
        if self.prefer_undetected:
            if self._setup_undetected_driver():
                return True
            logger.warning("undetected-chromedriver falló, intentando Selenium estándar...")
        
        # Intentar Selenium estándar
        if SELENIUM_AVAILABLE:
            if self._setup_standard_driver():
                return True
            logger.error("Selenium estándar también falló")
        
        # Si no se prefiere undetected pero está disponible, intentarlo como último recurso
        if not self.prefer_undetected and UC_AVAILABLE:
            logger.info("Intentando undetected-chromedriver como último recurso...")
            if self._setup_undetected_driver():
                return True
        
        logger.error("No se pudo configurar ningún driver")
        return False
    
    def _setup_undetected_driver(self):
        """Configurar undetected-chromedriver"""
        try:
            logger.info("Configurando undetected-chromedriver...")
            options = uc.ChromeOptions()
            
            # Configuraciones básicas
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-first-run')
            options.add_argument(f'--user-data-dir={self.user_data_dir}')
            
            if self.headless:
                options.add_argument('--headless=new')
            
            # Intentar crear el driver
            self.driver = uc.Chrome(options=options, version_main=None)
            self.driver_type = "undetected"
            
            # Ejecutar script anti-detección
            try:
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            except:
                pass
            
            logger.info("undetected-chromedriver configurado exitosamente")
            return True
            
        except Exception as e:
            logger.warning(f"Error configurando undetected-chromedriver: {str(e)}")
            return False
    
    def _setup_standard_driver(self):
        """Configurar Selenium estándar con webdriver-manager"""
        try:
            logger.info("Configurando Selenium estándar...")
            chrome_options = Options()
            
            # Configuraciones básicas
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-first-run')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument(f'--user-data-dir={self.user_data_dir}')
            
            if self.headless:
                chrome_options.add_argument('--headless=new')
            
            # User-Agent realista
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Usar webdriver-manager para versión correcta
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver_type = "standard"
            
            # Configurar timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(30)
            
            logger.info("Selenium estándar configurado exitosamente")
            return True
            
        except Exception as e:
            logger.warning(f"Error configurando Selenium estándar: {str(e)}")
            return False
    
    def navigate_to(self, url, timeout=15):
        """
        Navegar a una URL específica
        
        Args:
            url (str): URL de destino
            timeout (int): Tiempo de espera en segundos
            
        Returns:
            dict: Información sobre la navegación
        """
        if not self.driver:
            if not self.setup_driver():
                return {"status": "error", "message": "No se pudo crear ningún driver"}
        
        try:
            logger.info(f"Navegando a: {url} (usando {self.driver_type})")
            self.driver.get(url)
            
            # Esperar a que la página cargue
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Obtener información de la página
            info = {
                "status": "success",
                "title": self.driver.title,
                "url": self.driver.current_url,
                "cookies_count": len(self.driver.get_cookies()),
                "driver_type": self.driver_type,
                "page_loaded": True
            }
            
            logger.info(f"Navegación exitosa a: {info['title']}")
            return info
            
        except TimeoutException:
            logger.warning(f"Timeout al cargar: {url}")
            return {"status": "timeout", "message": f"Timeout cargando {url}"}
            
        except Exception as e:
            logger.error(f"Error navegando: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_page_info(self):
        """Obtener información detallada de la página actual"""
        if not self.driver:
            return {"error": "No hay driver activo"}
        
        try:
            return {
                "title": self.driver.title,
                "url": self.driver.current_url,
                "cookies": self.driver.get_cookies(),
                "page_source_length": len(self.driver.page_source),
                "driver_type": self.driver_type
            }
        except Exception as e:
            return {"error": str(e)}
    
    def find_element_text(self, selector, timeout=10):
        """Obtener texto de un elemento por selector CSS"""
        if not self.driver:
            return None
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element.text.strip()
        except Exception as e:
            logger.warning(f"No se pudo encontrar elemento '{selector}': {e}")
            return None
    
    def close(self):
        """Cerrar el navegador"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info(f"Driver {self.driver_type} cerrado exitosamente")
            except Exception as e:
                logger.warning(f"Error cerrando driver: {e}")
            finally:
                self.driver = None
                self.driver_type = None

def navigate_to_page(url, headless=True, prefer_undetected=True, timeout=15):
    """
    Función de conveniencia para navegación rápida
    
    Args:
        url (str): URL de destino
        headless (bool): Usar modo headless
        prefer_undetected (bool): Preferir undetected-chromedriver
        timeout (int): Timeout en segundos
        
    Returns:
        dict: Resultado de la navegación
    """
    navigator = WebNavigator(headless=headless, prefer_undetected=prefer_undetected)
    
    try:
        result = navigator.navigate_to(url, timeout=timeout)
        
        if result["status"] == "success":
            # Añadir información adicional
            page_info = navigator.get_page_info()
            result.update(page_info)
        
        return result
        
    finally:
        navigator.close()

def test_navigation():
    """Probar la navegación con fallback automático"""
    print("=== Prueba de Navegación con Fallback Automático ===")
    print(f"undetected-chromedriver disponible: {UC_AVAILABLE}")
    print(f"Selenium estándar disponible: {SELENIUM_AVAILABLE}")
    
    # Prueba 1: Navegación rápida con preferencia por undetected
    print("\n1. Prueba preferencia undetected-chromedriver...")
    result = navigate_to_page("https://httpbin.org/ip", prefer_undetected=True)
    print(f"Resultado: {result.get('status')} - Driver: {result.get('driver_type', 'unknown')}")
    
    if result.get("status") == "success":
        print("✓ Navegación exitosa")
        print(f"  - Título: {result.get('title', 'N/A')}")
        print(f"  - URL: {result.get('url', 'N/A')}")
        print(f"  - Cookies: {result.get('cookies_count', 0)}")
    else:
        print("✗ Error en navegación")
        return False
    
    # Prueba 2: Navegación con preferencia por Selenium estándar
    print("\n2. Prueba preferencia Selenium estándar...")
    result2 = navigate_to_page("https://httpbin.org/headers", prefer_undetected=False)
    print(f"Resultado: {result2.get('status')} - Driver: {result2.get('driver_type', 'unknown')}")
    
    # Prueba 3: Navegación con driver persistente
    print("\n3. Prueba con driver persistente...")
    navigator = WebNavigator(headless=True, prefer_undetected=True)
    
    try:
        # Múltiples navegaciones
        urls = [
            "https://httpbin.org/user-agent",
            "https://www.google.com",
            "https://httpbin.org/cookies"
        ]
        
        results = []
        for url in urls:
            result = navigator.navigate_to(url)
            results.append(result)
            print(f"  {url}: {result.get('status')} - {result.get('title', 'Sin título')}")
        
        if all(r.get("status") == "success" for r in results):
            print("✓ Navegación con driver persistente exitosa")
            return True
        else:
            print("✗ Error en alguna navegación")
            return False
            
    finally:
        navigator.close()

if __name__ == "__main__":
    # Ejecutar pruebas
    success = test_navigation()
    
    if success:
        print("\n🎉 ¡Todas las pruebas pasaron! El navegador está funcionando correctamente.")
        print(f"\nDriver principal: {'undetected-chromedriver' if UC_AVAILABLE else 'Selenium estándar'}")
        print(f"Driver de respaldo: {'Selenium estándar' if UC_AVAILABLE else 'No disponible'}")
        
        print("\nEjemplos de uso:")
        print("1. Navegación rápida (con auto-fallback):")
        print("   result = navigate_to_page('https://www.google.com')")
        print("\n2. Navegación con control manual:")
        print("   navigator = WebNavigator(headless=False)")
        print("   result = navigator.navigate_to('https://www.google.com')")
        print("   navigator.close()")
        print("\n3. Forzar tipo de driver:")
        print("   result = navigate_to_page('https://www.google.com', prefer_undetected=False)")
    else:
        print("\n❌ Las pruebas fallaron. Verifica la instalación de Chrome y las dependencias.")

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



# Para compatibilidad con código existente, mantener algunas funciones originales
def setup_chrome_driver(headless=True, user_data_dir=None, profile_directory=None):
    """Función de compatibilidad - usa WebNavigator internamente"""
    navigator = WebNavigator(headless=headless, user_data_dir=user_data_dir)
    if navigator.setup_driver():
        return navigator.driver
    return None

def extract_page_data(driver, selectors=None):
    """Función de compatibilidad para extraer datos"""
    try:
        data = {
            'title': driver.title,
            'url': driver.current_url,
            'timestamp': time.time()
        }
        
        if selectors:
            for name, selector in selectors.items():
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    data[name] = element.text.strip()
                except Exception as e:
                    logger.warning(f"No se pudo extraer '{name}' con selector '{selector}': {str(e)}")
                    data[name] = None
        
        return data
        
    except Exception as e:
        logger.error(f"Error al extraer datos de la página: {str(e)}")
        return {'error': str(e)}

def test_basic_navigation(url="https://httpbin.org/headers", headless=True):
    """Función de prueba usando la nueva implementación"""
    return navigate_to_page(url, headless=headless)