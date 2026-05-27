# curl https://api.restful-api.dev/objects

import requests

url="https://api.restful-api.dev/objects"
response=requests.get(url)
print(response)
print("status_code=",response.status_code)
print("headers=",response.headers)
print("text=",response.text)
print("json=",response.json())
print(response.json())