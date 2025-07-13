import requests

response = requests.get('http://34.12.84.239:8080/')
if response.status_code == 200:
    print("Website is up and running!")
else:
    print("Website is down or not reachable")