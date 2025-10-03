
import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Any

def check_availability(content: Dict[str, Any], config_data: Dict[str, Any], product_info: Dict[str, str], zip_code: str) -> List[Dict[str, Any]]:
    """
    Check product availability in Apple stores based on response data.
    
    Args:
        content (dict): Response data from Apple API containing store information
        config_data (dict): Configuration data containing preferred stores
        product_info (dict): Product information containing code
        zip_code (str): ZIP code for location search
    
    Returns:
        list: List of stores where the product is available
    """
    product_code = f"{product_info['code']}/A"
    available_stores = []
    preferred_stores = config_data.get('bestMarkets', [])
    
    # Get pickup message from response content
    try:
        pickup_message = content['body']['content']['pickupMessage']
    except (KeyError, TypeError):
        return []
    
    # Check if stores data exists
    if 'stores' not in pickup_message:
        return []
    
    # Process each store in the response
    for store in pickup_message['stores']:
        # Check if the product is available in this store
        if product_code in store.get('partsAvailability', {}):
            availability_info = store['partsAvailability'][product_code]
            pickup_quote = availability_info.get('pickupSearchQuote', '')
            print(pickup_quote)
            # Check if product is available today or tomorrow
            if pickup_quote in ["Available Today", "Available Tomorrow"]:
                store_name = store.get('storeName', '')
                
                # Check if store is in preferred stores list
                if store_name in preferred_stores:
                    available_stores.append(store)
    
    return available_stores

def test_check_availability():
    """
    Test the check_availability function using sample JSON data
    """
    # Load test data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    availability_path = os.path.join(current_dir, 'availability.json')
    config_path = os.path.join(current_dir, '..', 'input', 'config_data.json')
    
    # Load availability data
    with open(availability_path, 'r') as f:
        availability_data = json.load(f)
    
    # Load config data
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    # Test cases
    test_cases = [
        {
            "product_info": {"code": "MFXK4LL"},  # iPhone 17 Pro Max 512GB Silver
            "zip_code": "33139",
            "description": "Test unavailable product"
        },
        {
            "product_info": {"code": "MFXG4LL"},  # iPhone 17 Pro Max 256GB Silver
            "zip_code": "33139",
            "description": "Test another product variant"
        }
    ]
    
    print("Running availability tests...")
    for test_case in test_cases:
        print(f"\nTest case: {test_case['description']}")
        result = check_availability(
            availability_data,
            config_data['configData'],
            test_case['product_info'],
            test_case['zip_code']
        )
        if result:
            print(f"Found {len(result)} store(s) with availability:")
            for store in result:
                print(f"- {store.get('storeName', 'Unknown Store')}")
        else:
            print("No availability found")




def register_available_stores(stores: List[Dict[str, Any]], zip_code: str) -> bool:
    """
    Register available stores in Google Sheets through Apps Script Web App
    
    Args:
        stores (List[Dict]): List of store information dictionaries
        zip_code (str): ZIP code used for the search
        
    Returns:
        bool: True if data was successfully sent, False otherwise
    """
    # Current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare data for each store
    stores_data = []
    for store in stores:
        store_data = {
            "storeName": store.get("storeName", ""),
            "city": store.get("city", ""),
            "zipCode": zip_code,
            "timestamp": current_time
        }
        stores_data.append(store_data)
    
    payload = {
        "sheetName": "TIENDAS",  # Sheet for store availability data
        "data": stores_data
    }
    
    return send_to_apps_script(payload)

def record_iphone_availability(product_info: Dict[str, str], zip_code: str, is_available: bool) -> bool:
    """
    Record iPhone availability status in Google Sheets through Apps Script Web App
    
    Args:
        product_info (Dict[str, str]): Product information including name and price
        zip_code (str): ZIP code used for the search
        is_available (bool): Whether the iPhone is available or not
        
    Returns:
        bool: True if data was successfully sent, False otherwise
    """
    # Current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare data for the record
    payload = {
        "sheetName": "DATA",  # Sheet for iPhone availability data
        "data": [{
            "productName": product_info.get("name", ""),
            "productPrice": product_info.get("price", ""),
            "zipCode": zip_code,
            "timestamp": current_time,
            "status": "DISPONIBLE" if is_available else "NO DISPONIBLE"
        }]
    }
    
    return send_to_apps_script(payload)

def send_to_apps_script(payload: Dict[str, Any], retries: int = 3) -> bool:
    """
    Send data to Google Apps Script Web App endpoint
    
    Args:
        payload (Dict[str, Any]): Dictionary containing sheetName and data to send
        retries (int): Number of retries if request fails
        
    Returns:
        bool: True if data was successfully sent, False otherwise
    """
    # Replace this URL with your Google Apps Script Web App URL
    APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwdig4lVyQlk13gefdBf8IFelMDAc8vU6psj9aAieSnn7R7z_VI_8OIlUv_4LMBJ7ZJ/exec"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(
                APPS_SCRIPT_URL,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == retries - 1:
                print("Failed to send data after all retries")
                return False
            
    return False

def test_record_iphone_availability():
    """
    Test the iPhone availability recording functionality with mock data
    """
    # Mock product data
    mock_products = [
        {
            "name": "iPhone 17 Pro Max 256GB Silver",
            "price": "1299",
            "code": "MFXG4LL"
        },
        {
            "name": "iPhone 17 Pro 512GB Deep Blue",
            "price": "1399",
            "code": "MFXJ4LL"
        }
    ]
    
    test_zip = "33139"
    
    print("\nTesting iPhone availability recording...")
    
    # Test with available product
    try:
        print("\nTest Case 1: Available iPhone")
        success = record_iphone_availability(mock_products[0], test_zip, True)
        if success:
            print("✓ Successfully recorded available iPhone:")
            print(f"  - Product: {mock_products[0]['name']}")
            print(f"  - Status: DISPONIBLE")
        else:
            print("✗ Failed to record available iPhone")
    except Exception as e:
        print(f"✗ Error during available test: {str(e)}")
    
    # Test with unavailable product
    try:
        print("\nTest Case 2: Unavailable iPhone")
        success = record_iphone_availability(mock_products[1], test_zip, False)
        if success:
            print("✓ Successfully recorded unavailable iPhone:")
            print(f"  - Product: {mock_products[1]['name']}")
            print(f"  - Status: NO DISPONIBLE")
        else:
            print("✗ Failed to record unavailable iPhone")
    except Exception as e:
        print(f"✗ Error during unavailable test: {str(e)}")

def test_register_available_store():
    """
    Test the store registration functionality with mock data
    """
    # Mock store data
    mock_stores = [
        {
            "storeName": "Test Store 1",
            "city": "Miami",
            "storeNumber": "R123",
            "partsAvailability": {
                "MFXG4LL/A": {
                    "pickupSearchQuote": "Available Today"
                }
            }
        },
        {
            "storeName": "Test Store 2",
            "city": "Orlando",
            "storeNumber": "R456",
            "partsAvailability": {
                "MFXG4LL/A": {
                    "pickupSearchQuote": "Available Tomorrow"
                }
            }
        }
    ]
    
    # Test zip code
    test_zip = "33139"
    
    print("\nTesting store registration to Apps Script...")
    
    try:
        # Test registration
        success = register_available_stores(mock_stores, test_zip)
        
        if success:
            print("✓ Successfully sent mock data to Apps Script")
            print("Mock data sent:")
            for store in mock_stores:
                print(f"- Store: {store['storeName']}")
                print(f"  City: {store['city']}")
                print(f"  ZIP: {test_zip}")
        else:
            print("✗ Failed to send mock data to Apps Script")
            
    except Exception as e:
        print(f"✗ Error during test: {str(e)}")
        
    # Test error handling with empty data
    print("\nTesting error handling with empty data...")
    try:
        success = register_available_stores([], test_zip)
        if not success:
            print("✓ Successfully handled empty store list")
        else:
            print("✗ Failed to properly handle empty store list")
    except Exception as e:
        print(f"✗ Error during empty data test: {str(e)}")

if __name__ == "__main__":
    # Run all tests
    #test_check_availability()
    test_register_available_store()
    test_record_iphone_availability()


