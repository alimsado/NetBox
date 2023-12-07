import requests
import json
import urllib3

# Disable SSL verification warning for testing purposes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
url = "https://10.100.16.10/api/dcim/devices/"

payload = json.dumps([
  {
    "name": "AP2",
    "device_type": 4,
    "role": 8,
    "site": 1,
    "status": "planned"
  }
])
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Token ea0a07d37b5b07cc0a77b6ff7c127fd4077c5ebc'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)
