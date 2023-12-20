import ipcalc
import requests
from netmiko import ConnectHandler
import urllib3
import subprocess

# Disable SSL verification warning for testing purposes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#NetBox API URL and Token
NETBOX_URL = "https://10.100.16.10/api"
NETBOX_TOKEN = "ea0a07d37b5b07cc0a77b6ff7c127fd4077c5ebc"

# Netmiko device credentials
NETMIKO_USERNAME = "AliDoski"
NETMIKO_PASSWORD = "Al!$osk!22"

def is_pingable(ip_address):
    # Use subprocess to ping the IP address
    result = subprocess.run(['ping', '-c', '1', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def ip_exists_in_netbox(ip_address):
    nb_url = f"{NETBOX_URL}/ipam/ip-addresses/?address={ip_address}"

    response = requests.get(nb_url, headers={"Authorization": f"Token {NETBOX_TOKEN}"}, verify=False)

    return response.status_code == 200 and response.json()["count"] > 0

def get_hostname_from_device(ip_address):
    netmiko_device = {
        "device_type": "cisco_ios",
        "ip": ip_address,
        "username": NETMIKO_USERNAME,
        "password": NETMIKO_PASSWORD,
    }

    with ConnectHandler(**netmiko_device) as net_connect:
        # Retrieve the hostname from the device
        hostname = net_connect.send_command("show running-config | include hostname").split()[-1]

        return hostname

def add_ip_to_netbox(ip_address, status):
    if status == "active" and not ip_exists_in_netbox(ip_address):
        nb_url = f"{NETBOX_URL}/ipam/ip-addresses/"

        # Get the hostname from the reachable device
        hostname = get_hostname_from_device(ip_address)

        # Provide additional data as needed based on NetBox API requirements
        payload = {
            "address": ip_address,
            "status": status,
            "tenant": None,  # Adjust as needed
            "interface": None,  # Adjust as needed
            "device": None,  # Adjust as needed
            "description": f"Device hostname: {hostname}",
            # Add other fields as needed
        }

        response = requests.post(nb_url, json=payload, headers={"Authorization": f"Token {NETBOX_TOKEN}"}, verify=False)

        if response.status_code == 201:
            print(f"Added IP address {ip_address} to NetBox with status {status} and hostname {hostname}")
        else:
            print(f"Failed to add IP address {ip_address} to NetBox. Status Code: {response.status_code}")
            print(response.text)

def main():
    network = ipcalc.Network('10.42.5.0/29')

    for ip in network:
        ip_address = str(ip)
        if is_pingable(ip_address):
            add_ip_to_netbox(ip_address, "active")
        # Else do nothing for non-pingable addresses

if __name__ == "__main__":
    main()
