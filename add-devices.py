import requests
import json
import urllib3

# Disable SSL verification warning for testing purposes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
url = "https://10.100.16.10/api/dcim/devices/"

payload = json.dumps([
  {
    "name": "AP3",
    "device_type": 19,
    "role": 8,
    "site": 3,
    "status": "planned",
    "primary_ip4": "10.42.1.1/32",
  }
])
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token ea0a07d37b5b07cc0a77b6ff7c127fd4077c5ebc'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)
