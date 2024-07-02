import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cloudflare API configuration
CF_API_TOKEN = os.getenv('CF_API_TOKEN')
ZONE_ID = os.getenv('ZONE_ID')
RECORD_NAME = os.getenv('RECORD_NAME')

# API endpoints
CF_API_URL = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
IP_CHECK_URL = "https://api.ipify.org"

def get_external_ip():
    """Fetch the current external IP address."""
    response = requests.get(IP_CHECK_URL)
    return response.text.strip()

def get_dns_record():
    """Fetch the current DNS record from Cloudflare."""
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "type": "A",
        "name": RECORD_NAME
    }
    response = requests.get(CF_API_URL, headers=headers, params=params)
    data = response.json()
    
    if data["success"] and data["result"]:
        return data["result"][0]
    return None

def update_dns_record(record_id, new_ip):
    """Update the DNS record on Cloudflare."""
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": RECORD_NAME,
        "content": new_ip,
        "ttl": 1,  # Automatic
        "proxied": False,
        "id": record_id
    }
    response = requests.put(f"{CF_API_URL}/{record_id}", headers=headers, json=data)
    return response.json()["success"]

def main():
    while True:
        current_ip = get_external_ip()
        dns_record = get_dns_record()

        if dns_record and dns_record["content"] != current_ip:
            print(f"IP change detected. Updating DNS record...")
            if update_dns_record(dns_record["id"], current_ip):
                print(f"DNS record updated successfully. New IP: {current_ip}")
            else:
                print("Failed to update DNS record.")
        else:
            print(f"No IP change detected. Current IP: {current_ip}")

        # Wait for 5 minutes before checking again
        time.sleep(300)

if __name__ == "__main__":
    main()
