import requests

# url="https://api.restful-api.dev/objects/7"
url="http://127.0.0.1:8000/expenses"
response=requests.get(url)
print(response.json())