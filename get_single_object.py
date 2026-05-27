import requests

url="https://api.restful-api.dev/objects/7"
response=requests.get(url)
print(response.json())