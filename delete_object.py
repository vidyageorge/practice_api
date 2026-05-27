import requests

url = "https://api.restful-api.dev/objects/ff8081819d82fab6019e682d6eda0454"

response = requests.delete(url)

print(response.status_code)
print(response.text)
