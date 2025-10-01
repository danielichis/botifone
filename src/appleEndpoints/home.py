import json
import requests

cookies = {
    'geo': 'PE',
    'at_check': 'true',
    'dssid2': '3179e515-f447-46c1-a71c-ad5105cad26f',
    'dssf': '1',
    'as_pcts': 'HCcSgPsGpSow_2oqIOJrhnGG_+bMWi6ottIxOozIJeoc88uhsBbIDMGayKneU:Y9KG-PWbFA:gTG1Q5JrLh1Q8yyQYD2kEgI976H4I:kipvJsA4b71O4Qm3FH8guY0kaF+iOFkSGsmJxuPRpirQIP9',
    's_cc': 'true',
    'as_sfa': 'Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE',
    'as_rumid': 'c164e884-caf6-48d4-be10-bcded1c01272',
    'as_uct': '0',
    's_sq': '%5B%5BB%5D%5D',
    's_fid': '4E33E044639A9697-021F86F26C05F38B',
    'as_dc': 'ucp5',
    'shld_bt_m': 'UbzcGZm98fmredXMtZ5I6A|1759012002|fN1vG1P5lpodLTzwPtCSXw|xAbloQrfPMuFWsx9I_WDe113CPE',
    'as_atb': '1.0|MjAyNS0wOS0yNyAwMToyNjo0Mg|c92501489cf79df833f1041217171d897f27047c',
}

headers = {
    'accept': '*/*',
    'accept-language': 'es-419,es;q=0.9',
    'cache-control': 'max-age=0',
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
    'x-aos-ui-fetch-call-1': 'waj36a30dt-mg2q1gbd',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'geo=PE; at_check=true; dssid2=3179e515-f447-46c1-a71c-ad5105cad26f; dssf=1; as_pcts=HCcSgPsGpSow_2oqIOJrhnGG_+bMWi6ottIxOozIJeoc88uhsBbIDMGayKneU:Y9KG-PWbFA:gTG1Q5JrLh1Q8yyQYD2kEgI976H4I:kipvJsA4b71O4Qm3FH8guY0kaF+iOFkSGsmJxuPRpirQIP9; s_cc=true; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; as_rumid=c164e884-caf6-48d4-be10-bcded1c01272; as_uct=0; s_sq=%5B%5BB%5D%5D; s_fid=4E33E044639A9697-021F86F26C05F38B; as_dc=ucp5; shld_bt_m=UbzcGZm98fmredXMtZ5I6A|1759012002|fN1vG1P5lpodLTzwPtCSXw|xAbloQrfPMuFWsx9I_WDe113CPE; as_atb=1.0|MjAyNS0wOS0yNyAwMToyNjo0Mg|c92501489cf79df833f1041217171d897f27047c',
}

response = requests.get('https://www.apple.com/shop/favoritesx/fetch', cookies=cookies, headers=headers)