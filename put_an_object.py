import requests

url="https://api.restful-api.dev/objects/ff8081819d82fab6019e682d6eda0454"

payload={"name":"Vidya George Pixel 6 Pro",
"data":{"color":"Marble blue",
"capacity":"128 GB"}}

repose=requests.put(url,json=payload)
print(repose.json())
