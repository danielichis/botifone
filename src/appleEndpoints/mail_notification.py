import requests
from typing import Dict, Any, Optional
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_availability_notification(is_available: bool, 
                                product_info: Dict[str, str], 
                                store_info: Optional[Dict[str, Any]] = None,
                                zip_code: str = "") -> bool:
    """
    Send iPhone availability notification through HTTP POST request
    
    Args:
        is_available (bool): Whether the iPhone is available
        product_info (Dict[str, str]): Product information (name, code, price, etc.)
        store_info (Optional[Dict[str, Any]]): Store information if iPhone is available
        zip_code (str): ZIP code where availability was checked
        
    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    # n8n test webhook
    #NOTIFICATION_ENDPOINT = "https://integrations.unalukaglobal.com/webhook-test/d459b874-b2fc-4218-a0b2-564dd76abf7a"
    #n8n production webhook
    NOTIFICATION_ENDPOINT = "https://integrations.unalukaglobal.com/webhook/d459b874-b2fc-4218-a0b2-564dd76abf7a"
    # Current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the notification payload
    payload = {
        "timestamp": current_time,
        "isAvailable": is_available,
        "product": {
            "name": product_info.get("name", ""),
            "code": product_info.get("code", ""),
            "price": product_info.get("price", ""),
            "color": product_info.get("color", ""),
            "capacity": product_info.get("capacity", "")
        },
        "zipCode": zip_code
    }
    
    # Add store information if available
    if is_available and store_info:
        payload["store"] = {
            "name": store_info.get("storeName", ""),
            "city": store_info.get("city", ""),
            "state": store_info.get("state", ""),
            "email": store_info.get("storeEmail", "")
        }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Send the notification with retry mechanism
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                NOTIFICATION_ENDPOINT,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info(
                f"✓ Notification sent successfully for {product_info.get('name', 'Unknown Product')}"
                f"{' at ' + store_info.get('storeName', '') if store_info else ''}"
            )
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                logger.error("Failed to send notification after all retries")
                return False
    
    return False

def test_notification():
    """
    Test the notification functionality with mock data
    """
    # Mock product data
    mock_product = {
        "name": "iPhone 17 Pro Max 256GB Silver",
        "code": "MFXG4LL",
        "price": "1299",
        "color": "Silver",
        "capacity": "256GB"
    }
    
    # Mock store data
    mock_store = {
        "storeName": "Lincoln Road",
        "city": "Miami Beach",
        "state": "FL",
        "storeEmail": "lincolnroad@apple.com"
    }
    
    # Test Case 1: Available iPhone
    print("\nTest Case 1: Available iPhone")
    success = send_availability_notification(
        is_available=True,
        product_info=mock_product,
        store_info=mock_store,
        zip_code="33139"
    )
    print("✓ Test passed" if success else "✗ Test failed")
    
    # Test Case 2: Unavailable iPhone
    print("\nTest Case 2: Unavailable iPhone")
    success = send_availability_notification(
        is_available=False,
        product_info=mock_product,
        zip_code="33139"
    )
    print("✓ Test passed" if success else "✗ Test failed")

if __name__ == "__main__":
    test_notification()
