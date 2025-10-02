import json
import random
import time
import requests


def get_cookies():
    with open('src/appleEndpoints/cookiesHome.json', 'r') as f:
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
    with open('src/appleEndpoints/cookiesHomeSend.json', 'w') as f:
        json.dump(cookies, f, indent=4)
    return cookies
    

def get_headers():
    with open('src/appleEndpoints/headers_simple.json', 'r') as f:
        headers = json.load(f)
    with open('src/appleEndpoints/headersSend.json', 'w') as f:
        json.dump(headers, f, indent=4)
    return headers

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