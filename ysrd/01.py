import requests

base_url = 'http://123.127.175.45:8082/ajax/GwtWaterHandler.ashx'
body = {
    'Method': 'SelectRealData',
}
req = requests.post(base_url, data=body)
html = req.content.decode('utf-8')
print(html, type(html))

import json
html = json.loads(html)
print(html, type(html))

for data in html:
    print(data)


import time
print(time.time())
