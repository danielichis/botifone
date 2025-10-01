from playwright.sync_api import sync_playwright
import json
import os

def get_apple_auth_cookies():
    with sync_playwright() as p:
        # Use existing Chrome installation
        browser = p.chromium.launch_persistent_context(
            user_data_dir=os.path.expanduser("~") + "/AppData/Local/Google/Chrome/User Data",
            channel="chrome",
            headless=False,
            args=['--profile-directory=Default']  # Use default profile
        )
        # Get the first page or create one
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = browser.new_page()

        try:
            # Navigate to Apple Store page directly
            print("Accessing Apple Store website...")
            page.goto('https://www.apple.com/shop/buy-iphone/iphone-17-pro')

            # Wait for navigation and dynamic content to load
            page.wait_for_load_state('networkidle')
            
            # Esperar a que la página se estabilice
            page.wait_for_timeout(2000)
            
            # Esperar al elemento y asegurarse de que está en la vista
            size_selector = page.locator("input[data-autom='dimensionScreensize6_9inch']")
            size_selector.wait_for(state='attached')
            
            # Desactivar el scroll suave de la página
            page.evaluate("""() => {
                document.querySelector('.rf-bfe-stickybar').style.position = 'static';
                window.scrollTo = (x, y) => { window.scroll(x, y) };
            }""")
            
            # Hacer scroll y esperar
            page.evaluate("""() => {
                const element = document.querySelector("input[data-autom='dimensionScreensize6_9inch']");
                if (element) {
                    element.scrollIntoView();
                    window.scrollBy(0, -100); // Ajuste para evitar headers flotantes
                }
            }""")
            
            # Esperar a que el scroll se complete
            page.wait_for_timeout(1000)
            
            # Hacer click via JavaScript
            page.evaluate("""() => {
                const element = document.querySelector("input[data-autom='dimensionScreensize6_9inch']");
                if (element) {
                    element.click();
                    element.checked = true;
                }
            }""")
            
            # Esperar a que el click tome efecto
            page.wait_for_timeout(1000)
            
            # Continuar con el resto de las selecciones usando JavaScript
            for selector in [
                "input[data-autom='dimensionColordeepblue']",
                "input[value='2tb'][name='dimensionCapacity']",
                "#noTradeIn",
                "input[value='fullprice']",
                "input[name='carrierModel'][value='UNLOCKED/US']",
                "input[name='applecare-options'][data-autom='noapplecare']"
            ]:
                page.evaluate(f"""() => {{
                    const element = document.querySelector("{selector}");
                    if (element) {{
                        element.click();
                        if (element.type === 'radio' || element.type === 'checkbox') {{
                            element.checked = true;
                        }}
                    }}
                }}""")
                page.wait_for_timeout(500)
            
            # Click en Check availability
            page.evaluate("""() => {
                const element = document.evaluate("//span[text()='Check availability']", 
                    document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) {
                    element.click();
                }
            }""")
            
            # Esperar a que se procese el click
            page.wait_for_timeout(2000)
            print("Clicked on Check availability button.")
            #interceptar el request al hacer enter el zip code
            page.on("request", lambda request: parse_request(request) if "fulfillment-messages" in request.url else None)
            #with page.expect_request("**/fulfillment-messages**") as request_info:
            page.locator("input[name='search']").type("33139")
            page.locator("input[name='search']").press("Enter")
            #request = request_info.value
            # print(f"Intercepted request to: {request.url}")
            # print(f"Request method: {request.method}")
            # print(f"Request headers: {request.headers}")
            # cookies = request.cookies()
            # print(f"Request cookies: {cookies}")
            # Get all cookies from the browser context
            
            cookies = browser.cookies()
            print(f"\nTotal cookies retrieved: {len(cookies)}")
            print(f"Cookies: {cookies}")
            
            # Filter required cookies
            required_cookies = {}
            for cookie in cookies:
                if cookie['name'] in ['dssid2', 'shld_bt_ck']:
                    required_cookies[cookie['name']] = cookie['value']
                    print(f"Found {cookie['name']}: {cookie['value']}")
            
            # Create the cookies directory if it doesn't exist
            os.makedirs(os.path.dirname('src/appleEndpoints/cookiesHome.json'), exist_ok=True)
            
            # Format all cookies for requests
            formatted_cookies = {}
            for cookie in cookies:
                formatted_cookies[cookie['name']] = cookie['value']
            
            # Save all formatted cookies
            with open('src/appleEndpoints/cookiesHome.json', 'w') as f:
                json.dump(formatted_cookies, f, indent=4)
                
            print(f"\nSaved {len(formatted_cookies)} cookies to cookiesHome.json")
            
            # print("\nFound cookies:")
            # for name, value in required_cookies.items():
            #     print(f"{name}: {value}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        finally:
            # Close the browser context
            browser.close()
            
def format_cookies_for_requests(cookies):
    """Format cookies for use with the requests library"""
    return {cookie['name']: cookie['value'] for cookie in cookies}

def parse_request(request):
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


if __name__ == "__main__":
    get_apple_auth_cookies()
