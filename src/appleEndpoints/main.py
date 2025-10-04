#llamar a obtener cookies y headers con selenium
#guardar cookies y headers en json
#obtener configuraciones de productos y zip codes desde un archivo json
#de dicho json obtener las combinaciones de codigos de productos y zip codes
# Por cada combinación realizar peticiones con requests usando cookies y headers guardados mientras la respuesta sea 200
#si la respuesta es 200,buscar la disponibilidad de los iphones segun data_processing.py
#si hay disponibilidad,cargar a google sheets mediante una petición post a su endpoint
#si no hay disponibilidad,solo imprimir en consola
#si la peticion falla y es 541, volver a obtener cookies y headers con selenium y repetir el proceso

import json
import requests
from botifone.src.appleEndpoints.data_processing import check_availability
from botifone.src.appleEndpoints.avaitability import request_available_iphones,are_new_cookies_expired
from botifone.src.appleEndpoints.simple_navigator_final import refreshCookies
from botifone.src.appleEndpoints.mail_notification import send_availability_notification
from botifone.src.appleEndpoints.data_processing import register_available_stores, record_iphone_availability
    
def read_config_data():
    with open(r'botifone\src\input\config_data.json', 'r') as f:
        config_data = json.load(f)
    return config_data


def get_product_codes(config_data):
    return [product['code'] for product in config_data.get("configData").get("products", [])]


def get_available_iphones_and_update_sheets():
    """
    Main function to check iPhone availability and update Google Sheets.
    - Checks availability for all product and zip code combinations
    - Records availability status for each iPhone
    - Records store information when iPhones are available
    """

    config_data = read_config_data()
    all_products = config_data.get("configData", {}).get("products", [])
    zip_codes = config_data.get("configData", {}).get("zipcodes", [])
    
    # Create combinations of products and zip codes
    combinations = [(product, str(zip_code)) for product in all_products for zip_code in zip_codes]
    
    # Get initial cookies and headers
    refreshCookies()
    while True:
        for product, zip_code in combinations:
            product_code = product['code']
            print(f"\nChecking availability for {product['name']} in {zip_code}...")
            
            # Try to get availability data
            response_data = request_available_iphones(product_code, zip_code)
            
            if response_data:
                # Check store availability
                available_stores = check_availability(
                    content=response_data,
                    config_data=config_data.get("configData", {}),
                    product_info={"code": product_code},
                    zip_code=zip_code
                )
                
                is_available = len(available_stores) > 0
                
                # Record iPhone availability status
                availability_recorded = record_iphone_availability(
                    product_info=product,  # Contains name, price, etc.
                    zip_code=zip_code,
                    is_available=is_available
                )
                if is_available:
                    #function to send notificaiton mail
                    print("Sending availability notification email...")
                    send_availability_notification(
                        is_available=True,
                        product_info=product,
                        store_info=available_stores[0] if available_stores else None,
                        zip_code=zip_code
                    )
                
                if availability_recorded:
                    print(f"✓ Recorded availability status for {product['name']}")
                else:
                    print(f"✗ Failed to record availability status for {product['name']}")
                
                # If available in any store, register the stores
                if available_stores:
                    print(f"Product {product['name']} available in {len(available_stores)} stores for ZIP code {zip_code}:")
                    for store in available_stores:
                        print(f"- {store.get('storeName', 'Unknown Store')}")
                    
                    # Register available stores in Google Sheets
                    stores_recorded = register_available_stores(available_stores, zip_code)
                    if stores_recorded:
                        print("✓ Successfully registered available stores")
                    else:
                        print("✗ Failed to register available stores")
                else:
                    print(f"Product {product['name']} not available in preferred stores for ZIP code {zip_code}")
            else:
                print(f"Request failed for {product['name']} in {zip_code}. Getting new cookies and headers...")
                # Record the unavailability even when request fails
                print("Refreshing cookies and headers...")
                refreshCookies()  # Refresh cookies and headers
                print("Verifying if new cookies are valid...")
                if are_new_cookies_expired():
                    print("New cookies are expired, refreshing again...")
                    return 0
                else:
                    print("Retrying the request...")



if __name__ == "__main__":
    get_available_iphones_and_update_sheets()








