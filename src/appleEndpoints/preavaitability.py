import re
import requests
import json

r = requests.get('https://www.apple.com')
print(r.status_code)
# Convert cookies to a dictionary before saving as JSON
data = r.cookies.get_dict()
print(data)
with open('src/appleEndpoints/data.json', 'w') as f:
    json.dump(data, f, indent=4)