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
    
    def __init__(self, version_main=134):
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
                
                # Usar el perfil Default si existe, sino el primero disponible
                profile_to_use = "Default"
                if "Default" not in profiles and profiles:
                    profile_to_use = profiles[0]
                    logger.info(f"Perfil Default no encontrado, usando: {profile_to_use}")
                
                logger.info(f"Usando datos de usuario de Chrome: {chrome_user_data}")
                logger.info(f"Usando perfil: {profile_to_use}")
                
                options.add_argument(f'--user-data-dir={chrome_user_data}')
                options.add_argument(f'--profile-directory={profile_to_use}')
                
                # IMPORTANTE: Evitar conflictos si Chrome está abierto
                options.add_argument('--remote-debugging-port=9222')
                
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
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36')
            
            logger.info(f"Configurando ChromeDriver para versión {self.version_main} con datos persistentes...")
            
            driver = uc.Chrome(
                options=options,
                version_main=self.version_main,
                headless=False,
                use_subprocess=False  # Importante para evitar conflictos con Chrome abierto
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

def main():
    """Función principal del script"""
    # Activar supresión de errores del destructor
    suppress_chrome_destructor_error()
    
    logger.info("=== Iniciando navegador para Chrome versión 134 ===")
    
    try:
        # Usar el context manager para manejo seguro
        with SafeChromeDriver(version_main=134) as driver:
            
            # Navegar a la página
            logger.info("Navegando a Apple iPhone...")
            driver.get('https://www.apple.com/shop/buy-iphone/iphone-17-pro')
            
            # Esperar un momento para que cargue
            time.sleep(3)
            
            # Tomar captura de pantalla
            screenshot_name = 'apple_iphone_chrome134_user_profile.png'
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
                
                # Verificar si hay extensiones cargadas (esto indica que el perfil del usuario está activo)
                try:
                    extension_info = driver.execute_script("return window.chrome && window.chrome.runtime ? 'Extensions available' : 'No extensions'")
                    logger.info(f"Estado de extensiones: {extension_info}")
                except:
                    logger.info("No se pudo verificar el estado de las extensiones")
                
            except Exception as e:
                logger.warning(f"No se pudo obtener información del navegador: {e}")
            
            # Mantener abierto por unos segundos
            logger.info("Manteniendo navegador abierto por 3 segundos...")
            time.sleep(3)
    
    except Exception as e:
        logger.error(f"Error durante la ejecución: {e}")
        raise
    
    finally:
        # Limpieza final agresiva
        gc.collect()
        logger.info("=== Script finalizado exitosamente ===")

if __name__ == "__main__":
    main()