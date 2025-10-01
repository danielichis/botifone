import requests

cookies = {
    'as_sfa': 'Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE',
    'dssf': '1',
    'dssid2': '44e1fba8-50c3-4f03-b70e-0282f216ba4f',
    'as_dc': 'ucp5',
    's_fid': '0CB86A3084024776-26A658113DDE232E',
    's_vi': '[CS]v1|346D243D4179A454-600017AC22F53B93[CE]',
    'sh_spksy': '.',
    'shld_bt_ck': '9ZyBN7NghZtNMPjMX0PUMA|1759143070|DZKrzvLQtKc8vGCZzj1S_koBqM6q-JtRIHhrkIpm1aoKT9unDiQsrQc1-ZP7PTE9UeCBR275dOzyTUSd4crKBgnGnGwDp7sVjAxBkvpTYu7Yp4lde7rDOgybUM_Tq9xhHPgvfap1zrgZqR-lix0ZeIAs4qIzQk4F-ManledDRyRJFxir-JdNOJt043UJR-0A6fnWI-Zsrl8prTQv5JcTwGJrYv9bUDr9pRDw9CkOTeibcVcyV4QwrdAB7AsfpjcmRYAcqLZFjv9KzW4W0sn5j4cOFPO_gdZdwMdZ_YWCjOvBsKGTHJe5CVwehpffyUj3gcFzaKPnMOSIIINwKnJvew|rkVBpnLxjYRPh4CmJKnAPYEaAFk',
    'as_uct': '0',
    'as_pcts': '0QGZo5K_98R0e5cN-wvTd_o2u:S3O_X:6orywgOwg51r9j+du6yxD7FyQYarGIkJpB2B1VsfRq2d6D+:yd1SmJtnGNl6UbSlOCxlYFbYUyoHA0TUpaEJJGVVLvS7iVksETrrqjpHmgqXp:ZXuNu3uX',
    'geo': 'PE',
    's_cc': 'true',
    'as_rumid': '308c56c1-00cc-43a9-bf5e-5484ecf56585',
    'as_atb': '1.0|MjAyNS0wOS0yOSAwMzowODoyMQ|b879c07aea9328e8660b90b1dd10381c2f61e801',
    'shld_bt_m': 'Vxrbh8XH0tr29RUJDcLnOg|1759147730|JjAV0h-brNnEF7HL5Prmgw|tVjlMLWl5nghiv2IVnTyuHKmJfY',
    's_sq': 'applestoreww%3D%2526c.%2526a.%2526activitymap.%2526page%253DAOS%25253A%252520home%25252Fshop_iphone%25252Ffamily%25252Fiphone_17_pro%25252Fselect%2526link%253Diphone%252520availabilitycity%252520or%252520zip%252520resetm%252520%252528inner%252520text%252529%252520%25257C%252520no%252520href%252520%25257C%252520body%2526region%253Dbody%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c',
}

headers = {
    'accept': '*/*',
    'accept-language': 'es-419,es;q=0.9,en;q=0.8',
    # 'cookie': 'as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; dssf=1; dssid2=44e1fba8-50c3-4f03-b70e-0282f216ba4f; as_dc=ucp5; s_fid=0CB86A3084024776-26A658113DDE232E; s_vi=[CS]v1|346D243D4179A454-600017AC22F53B93[CE]; sh_spksy=.; shld_bt_ck=9ZyBN7NghZtNMPjMX0PUMA|1759143070|DZKrzvLQtKc8vGCZzj1S_koBqM6q-JtRIHhrkIpm1aoKT9unDiQsrQc1-ZP7PTE9UeCBR275dOzyTUSd4crKBgnGnGwDp7sVjAxBkvpTYu7Yp4lde7rDOgybUM_Tq9xhHPgvfap1zrgZqR-lix0ZeIAs4qIzQk4F-ManledDRyRJFxir-JdNOJt043UJR-0A6fnWI-Zsrl8prTQv5JcTwGJrYv9bUDr9pRDw9CkOTeibcVcyV4QwrdAB7AsfpjcmRYAcqLZFjv9KzW4W0sn5j4cOFPO_gdZdwMdZ_YWCjOvBsKGTHJe5CVwehpffyUj3gcFzaKPnMOSIIINwKnJvew|rkVBpnLxjYRPh4CmJKnAPYEaAFk; as_uct=0; as_pcts=0QGZo5K_98R0e5cN-wvTd_o2u:S3O_X:6orywgOwg51r9j+du6yxD7FyQYarGIkJpB2B1VsfRq2d6D+:yd1SmJtnGNl6UbSlOCxlYFbYUyoHA0TUpaEJJGVVLvS7iVksETrrqjpHmgqXp:ZXuNu3uX; geo=PE; s_cc=true; as_rumid=308c56c1-00cc-43a9-bf5e-5484ecf56585; as_atb=1.0|MjAyNS0wOS0yOSAwMzowODoyMQ|b879c07aea9328e8660b90b1dd10381c2f61e801; shld_bt_m=Vxrbh8XH0tr29RUJDcLnOg|1759147730|JjAV0h-brNnEF7HL5Prmgw|tVjlMLWl5nghiv2IVnTyuHKmJfY; s_sq=applestoreww%3D%2526c.%2526a.%2526activitymap.%2526page%253DAOS%25253A%252520home%25252Fshop_iphone%25252Ffamily%25252Fiphone_17_pro%25252Fselect%2526link%253Diphone%252520availabilitycity%252520or%252520zip%252520resetm%252520%252528inner%252520text%252529%252520%25257C%252520no%252520href%252520%25257C%252520body%2526region%253Dbody%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c',
    'priority': 'u=1, i',
    'referer': 'https://www.apple.com/shop/buy-iphone/iphone-17-pro/6.9-inch-display-2tb-deep-blue-unlocked',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'x-aos-ui-fetch-call-1': 'uf0mvyliop-mg4yuu1q',
}

response = requests.get(
    'https://www.apple.com/shop/fulfillment-messages?fae=true&pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/US&parts.0=MFXJ4LL/A&location=33166',
    cookies=cookies,
    headers=headers,
)
print(response.status_code)