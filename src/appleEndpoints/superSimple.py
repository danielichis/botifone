import undetected_chromedriver as uc
import time

try:
    driver = uc.Chrome()
    driver.get('https://www.apple.com/shop/buy-iphone/iphone-17-pro')
    print(driver.title)
    time.sleep(1)  # Pequeña pausa antes de cerrar
    driver.close()  # Primero cerramos la ventana
    driver.quit()   # Luego cerramos el driver
except Exception as e:
    print(f"Error durante la ejecución: {e}")
finally:
    try:
        if 'driver' in locals():
            driver.quit()
    except:
        pass  # Ignoramos cualquier error durante la limpieza final