import requests

url="https://api.restful-api.dev/objects"

payload={
"name":"Vidya Pixel 6 Pro",
"data":{"color":"Marble blue",
"capacity":"64 GB"}}

repose=requests.post(url,json=payload)
print(repose.json())

response=requests.get(url)
print("After posting the object, the response is: ",response.json())