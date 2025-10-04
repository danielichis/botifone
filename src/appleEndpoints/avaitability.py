import json
import random
import time
import requests
import os
from botifone.src.appleEndpoints.simple_navigator_final import refreshCookies
#from botifone.src.appleEndpoints.simple_navigator_final import main

def get_cookies():
    with open(r"botifone\src\appleEndpoints\cookiesHome.json", 'r') as f:
        coookies = json.load(f)
    cookies = {
    'as_sfa': coookies['as_sfa'],
    'dssf': '1',
    'dssid2': coookies['dssid2'],
    'as_dc': coookies['as_dc'],
    's_fid': coookies['s_fid'],
    's_vi': coookies['s_vi'],
    'sh_spksy': '.',
    'shld_bt_ck': coookies['shld_bt_ck'],
    'as_uct': '0',
    'as_pcts': coookies['as_pcts'],
    'geo': 'PE',
    's_cc': 'true',
    'as_rumid': coookies['as_rumid'],
    'as_atb': coookies['as_atb'],
    'shld_bt_m': coookies['shld_bt_m'],
    #'s_sq': coookies['s_sq'],
              }
    with open(r'botifone\src\appleEndpoints\cookiesHomeSend.json', 'w') as f:
        json.dump(cookies, f, indent=4)
    return cookies
    

def get_headers():
    with open(r"botifone\src\appleEndpoints\headers_simple.json", 'r') as f:
        headers = json.load(f)
    with open(r"botifone\src\appleEndpoints\headersSend.json", 'w') as f:
        json.dump(headers, f, indent=4)
    return headers


def test_request():
    cookies = get_cookies()
    headers = get_headers()
    while True:
        response = requests.get(
        'https://www.apple.com/shop/fulfillment-messages?fae=true&pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0=MG7L4LL/A&location=33139',
        cookies=cookies,
        headers=headers,
        )
        random_between_5_and_10 = random.randint(1,2)  # Espera entre 5 y 10 segundos
        print(response.status_code)
        time.sleep(random_between_5_and_10)

        if response.status_code == 541:
            print("Status 541, obteniendo nuevas cookies y headers...")
            refreshCookies()
            cookies = get_cookies()
            headers = get_headers()


def are_new_cookies_expired():
    cookies = get_cookies()
    headers = get_headers()
    while True:
        response = requests.get(
        'https://www.apple.com/shop/fulfillment-messages?fae=true&pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0=MG7L4LL/A&location=33139',
        cookies=cookies,
        headers=headers,
        )
        random_between_5_and_10 = random.randint(1,2)  # Espera entre 5 y 10 segundos
        print(response.status_code)
        time.sleep(random_between_5_and_10)

        if response.status_code != 200:
            print("Nuevas cookies expiradas")
            return True
        else:
            print("Nuevas cookies válidas")
            return False


def request_available_iphones(product_code,zip_code):
    cookies = get_cookies()
    headers = get_headers()
    iphone_url=f'https://www.apple.com/shop/fulfillment-messages?fae=true&pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0={product_code}/A&location={zip_code}'
    response = requests.get(
        url=iphone_url,
        cookies=cookies,
        headers=headers,
        )

    random_between_5_and_10 = random.randint(3,4)  # Espera entre 3 y 6 segundos
    print(response.status_code)
    time.sleep(random_between_5_and_10)
    file_path = os.path.join('botifone', 'src', 'appleEndpoints', 'availability.json')
    if response.status_code == 200:
        print("Información obtenida exitosamente")
      #  with open(file_path, 'w') as f:
     #       json.dump(response.json(), f, indent=4)
        return response.json()
    if response.status_code != 200:
        print("Error en la petición, obteniendo nuevas cookies y headers...")
        return None


def test_request_2():
    cookies = {
    'dssid2': 'c52eb9cd-1045-41a7-a369-de3d8fe2f3a3',
    'dssf': '1',
    'as_sfa': 'Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE',
    'as_uct': '0',
    'geo': 'PE',
    's_cc': 'true',
    'as_pcts': 'lhRSqITSyo:Ndp-8LD5qnHt9k+eBaF3wCX2DIQEkfgkjpYX-QIz-OpnFCuJoTx-XBnOl4y7M:9pIDiD4axQVSN87sVwUwQuukJWH17U+LH5gLcWnZMWBrEXRNlqlr4lV0ifeRrjvkT91AXN7LOo1zx',
    'as_rumid': 'bd612a1b-2173-4e0f-b0c1-01509c1e8c1a',
    's_fid': '14E50298AB70F3BC-03EB555102D7FD19',
    'as_dc': 'ucp5',
    's_vi': '[CS]v1|34700D6ABDA04741-400013E923406C98[CE]',
    'sh_spksy': '.',
    'shld_bt_ck': 'WYqIs55002BSASh0QdqWrg|1759524603|wVAJW7AV5hDrWGsxjWxlVEXLTwEfdd6Phjf4mw4nkv0RViRLe5r-fD1aOFoFj08X8XWgmwGRkHxZcs5gvai7APuBcY2whnZHdRWWp4n4UBnebrjvTkRiwWAeVkKQkneb6T2_0RO4T2I4hAhwgYSv9C0T4dHyrkBzJdMb3YK1OYEuYaCEm15C5eJPpMjXCKKjKFlEKEX3D2lEBZCS5id5_k2Erk-7uogHvw5bmYew0ZrX4inmgk3CHtt2DS4BIj0zbRpAXl0MGIBdmMLCqx08FrN8fQDV3nbZNPHtm7LZo9YaV0GKf5JtXkEt22gOXJUCXzWW5Y94QqDBdVX-BzMU9A|lBk0n7dnEZLeg9m2xDhtiHPzEFs',
    'as_atb': '1.0|MjAyNS0xMC0wMyAxMTo1MDowNg|c935630bf2818fa9c6fd0907ae86204850750800',
    'shld_bt_m': '0IlcD6pHnO-jU-DGNRl9qQ|1759524666|CACesClmiD3ZABXngEaXAA|GvjLcKZz3EhS6rro_Mh0IokJJgo',
    's_sq': 'applestoreww%3D%2526c.%2526a.%2526activitymap.%2526page%253DAOS%25253A%252520home%25252Fshop_iphone%25252Ffamily%25252Fiphone_17_pro%25252Fselect%2526link%253Dmiami%25252C%252520fl%252520%252528inner%252520text%252529%252520%25257C%252520no%252520href%252520%25257C%252520body%2526region%253Dbody%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c',
}

    headers = {
    'accept': '*/*',
    'accept-language': 'es-US,es-419;q=0.9,es;q=0.8',
    'priority': 'u=1, i',
    'referer': 'https://www.apple.com/shop/buy-iphone/iphone-17-pro/6.9-inch-display-256gb-deep-blue-unlocked',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'x-aos-ui-fetch-call-1': 'iq2ikxi0ga-mgb79ucw',
    # 'cookie': 'dssid2=c52eb9cd-1045-41a7-a369-de3d8fe2f3a3; dssf=1; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; as_uct=0; geo=PE; s_cc=true; as_pcts=lhRSqITSyo:Ndp-8LD5qnHt9k+eBaF3wCX2DIQEkfgkjpYX-QIz-OpnFCuJoTx-XBnOl4y7M:9pIDiD4axQVSN87sVwUwQuukJWH17U+LH5gLcWnZMWBrEXRNlqlr4lV0ifeRrjvkT91AXN7LOo1zx; as_rumid=bd612a1b-2173-4e0f-b0c1-01509c1e8c1a; s_fid=14E50298AB70F3BC-03EB555102D7FD19; as_dc=ucp5; s_vi=[CS]v1|34700D6ABDA04741-400013E923406C98[CE]; sh_spksy=.; shld_bt_ck=WYqIs55002BSASh0QdqWrg|1759524603|wVAJW7AV5hDrWGsxjWxlVEXLTwEfdd6Phjf4mw4nkv0RViRLe5r-fD1aOFoFj08X8XWgmwGRkHxZcs5gvai7APuBcY2whnZHdRWWp4n4UBnebrjvTkRiwWAeVkKQkneb6T2_0RO4T2I4hAhwgYSv9C0T4dHyrkBzJdMb3YK1OYEuYaCEm15C5eJPpMjXCKKjKFlEKEX3D2lEBZCS5id5_k2Erk-7uogHvw5bmYew0ZrX4inmgk3CHtt2DS4BIj0zbRpAXl0MGIBdmMLCqx08FrN8fQDV3nbZNPHtm7LZo9YaV0GKf5JtXkEt22gOXJUCXzWW5Y94QqDBdVX-BzMU9A|lBk0n7dnEZLeg9m2xDhtiHPzEFs; as_atb=1.0|MjAyNS0xMC0wMyAxMTo1MDowNg|c935630bf2818fa9c6fd0907ae86204850750800; shld_bt_m=0IlcD6pHnO-jU-DGNRl9qQ|1759524666|CACesClmiD3ZABXngEaXAA|GvjLcKZz3EhS6rro_Mh0IokJJgo; s_sq=applestoreww%3D%2526c.%2526a.%2526activitymap.%2526page%253DAOS%25253A%252520home%25252Fshop_iphone%25252Ffamily%25252Fiphone_17_pro%25252Fselect%2526link%253Dmiami%25252C%252520fl%252520%252528inner%252520text%252529%252520%25257C%252520no%252520href%252520%25257C%252520body%2526region%253Dbody%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c',
}
    response = requests.get(
        'https://www.apple.com/shop/fulfillment-messages?fae=true&pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0=MFXK4LL/A&location=Miami,%20FL',
        cookies=cookies,
        headers=headers,
    )

    #save response to json file
    with open('botifone/src/appleEndpoints/availability.json', 'w') as f:
        json.dump(response.json(), f, indent=4)

if __name__ == "__main__":
    test_request()
    #test_request_2()
    #request_available_iphones("MGP63LL/A","33139")