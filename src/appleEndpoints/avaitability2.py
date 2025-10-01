import json
import time
import random
import requests

def load_cookies():
    try:
        with open('src/appleEndpoints/cookiesHome.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading cookies: {str(e)}")
        return {}

headers = {
    'accept': '*/*',
    'accept-language': 'es-419,es;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.apple.com/shop/buy-iphone/iphone-17-pro/6.9-inch-display-2tb-cosmic-orange-unlocked',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Brave";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'x-aos-ui-fetch-call-1': 'tzns132fsy-mg0loeqk',
    # 'cookie': 'geo=PE; at_check=true; dssid2=3179e515-f447-46c1-a71c-ad5105cad26f; dssf=1; as_pcts=HCcSgPsGpSow_2oqIOJrhnGG_+bMWi6ottIxOozIJeoc88uhsBbIDMGayKneU:Y9KG-PWbFA:gTG1Q5JrLh1Q8yyQYD2kEgI976H4I:kipvJsA4b71O4Qm3FH8guY0kaF+iOFkSGsmJxuPRpirQIP9; as_dc=ucp3; s_fid=0BD76074D7126455-0A9F9011AAAB46B9; s_cc=true; sh_spksy=.; s_vi=[CS]v1|346B299488868441-60000B8DB602642C[CE]; mbox=session#56aab398d96944e883a05d049a7373fa#1758878314|PC#56aab398d96944e883a05d049a7373fa.34_0#1758878262; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; as_atb=1.0|MjAyNS0wOS0yNiAwMTo0Nzo0OQ|61ba0dbe69ddb6c2fc60926c938c61c3ac21a429; as_rumid=c164e884-caf6-48d4-be10-bcded1c01272; shld_bt_ck=59k3Ozsn4wWSXVMWjh7W1Q|1758883674|SrAsrL7n5vIucvs-OksCC73M4Z5Zc8EyySmlmFTqjmroT9EOuZM2YEw7FTbh0xB0wGR-ElwerdUPqP3ahnwvDZaaVeyTagLUb0KDw-Qj00dezvITNx6pL50CIxXyegZlcpG9pj-w2zJ81yTdEIxVF9PPe2f7y4BjFUJqzAZOj04ViEZcAUBdylJwNGATmksdNVxS2TKpCiU6UhDN8ew-2wcgrFdqHNVXQGq27LfqI3R43OBor7CdGRbNi2WaDQCu8LAW2uldhJMXeupBGQXnjDwUjp_F_HIMayNpFqst4RqRXU8WmBfrgp5NddQxq46stQpdy8bfd1fIh0WxngQn5A|c8igHairZUXYSAXengce3csX1WQ; as_uct=0; shld_bt_m=v1bYeaGnZrDYgUDvVNL11w|1758883726|hUcseL41yIupQ6uRwpUDjA|Xzv-UhHSTynnRSDZ4lgXC-4wCbs; s_sq=applestoreww%3D%2526c.%2526a.%2526activitymap.%2526page%253DAOS%25253A%252520home%25252Fshop_iphone%25252Ffamily%25252Fiphone_17_pro%25252Fselect%2526link%253Diphone%252520availabilitycity%252520or%252520zip%252520resetm%252520%252528inner%252520text%252529%252520%25257C%252520no%252520href%252520%25257C%252520body%2526region%253Dbody%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c',
}

def check_availability():
    # Load cookies from file
    cookies = load_cookies()
    
    print(f"Loaded {len(cookies)} cookies from file")
    print(f"Important cookies present:")
    print(f"dssid2: {'dssid2' in cookies}")
    print(f"shld_bt_ck: {'shld_bt_ck' in cookies}")
    
    # Añadir headers adicionales que hacen la petición más realista
    headers.update({
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)
    
    while True:
        try:
            # Primero visitar la página principal para establecer contexto
            session.get('https://www.apple.com/shop/buy-iphone')
            time.sleep(2 + random.random() * 3)  # Espera aleatoria entre 2-5 segundos
            
            # Luego hacer la petición de disponibilidad
            response = session.get(
                'https://www.apple.com/shop/fulfillment-messages',
                params={
                    'fae': 'true',
                    'little': 'false',
                    'sp': 'true',
                    'parts.0': 'MFXT4LL/A',
                    'cppart': 'UNLOCKED/US',
                    'purchaseOption': 'fullPrice',
                    'mts.0': 'regular',
                    'mts.1': 'sticky',
                    'fts': 'true'
                }
            )
            
            print(f"\nStatus Code: {response.status_code}")
            if response.status_code != 200:
                print(f"Response: {response.text}")
            else:
                print("Request successful!")
                print(f"Response: {response.text}")
                data = response.json()
                print(json.dumps(data, indent=2))
                
        except Exception as e:
            print(f"Error occurred: {str(e)}")
        break  
        time.sleep(5)  # Wait 5 seconds between attempts

if __name__ == "__main__":
    check_availability()