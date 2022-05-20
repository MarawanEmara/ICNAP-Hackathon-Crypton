import requests
import json
import pandas as pd

data = requests.get("http://192.168.178.132:8090/getFactory").json()
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


print(data)

