import ipaddress
from ping3 import ping, verbose_ping
import requests
import urllib3

# Disable SSL verification warning for testing purposes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NETBOX_URL = "https://10.100.16.10/api"
NETBOX_TOKEN = "ea0a07d37b5b07cc0a77b6ff7c127fd4077c5ebc"

def is_reachable(ip_address):
    try:
        # Use ping to check if the IP address is reachable
        response = ping(ip_address, timeout=1)
        return response is not None and response < 1.0
    except Exception as e:
        print(f"Error checking reachability for {ip_address}: {e}")
        return False

def add_ip_to_netbox(ip_address, status="active"):
    url = f"{NETBOX_URL}/ipam/ip-addresses/"
    payload = {
        "address": str(ip_address),
        "status": status,
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {NETBOX_TOKEN}',
    }
    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)
        if response.status_code == 201:
            print(f"Added IP address {ip_address} to NetBox with status {status}")
        else:
            print(f"Failed to add IP address {ip_address} to NetBox. Status Code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error adding IP address {ip_address} to NetBox: {e}")

def scan_and_add_to_netbox(ip_range):
    network = ipaddress.IPv4Network(ip_range, strict=False)
    for ip in network.hosts():
        if is_reachable(str(ip)):
            add_ip_to_netbox(ip)

if __name__ == "__main__":
    # Replace the IP range with your desired range
    scan_and_add_to_netbox("10.42.0.0/16")
