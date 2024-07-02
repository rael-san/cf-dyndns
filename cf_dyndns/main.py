import requests
import time
import os
from yaml import load, Loader
import sys
import logging

# API endpoints
CF_API_URL = "https://api.cloudflare.com/client/v4/zones/%s/dns_records"
IP_CHECK_URL = "https://api.ipify.org"

def get_external_ip():
    """Fetch the current external IP address."""
    logging.debug(f"Fetching external IP address: {IP_CHECK_URL}")
    response = requests.get(IP_CHECK_URL)
    return response.text.strip()

def get_dns_record(token: str, record_name: str, zone_id: str):
    """Fetch the current DNS record from Cloudflare."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {
        "type": "A",
        "name": record_name
    }
    url = CF_API_URL % zone_id
    logging.debug(f"Fetching DNS record: {url}")

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    logging.debug(f"Response: {data}")
    
    if data["success"] and data["result"]:
        return data["result"][0]
    return None

def update_dns_record(token: str, record_name: str, zone_id: str, record_id: str, new_ip: str):
    """Update the DNS record on Cloudflare."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": record_name,
        "content": new_ip,
        "ttl": 1,  # Automatic
        "proxied": False,
        "id": record_id
    }
    url = (CF_API_URL % zone_id) + "/" + record_id
    logging.debug(f"Updating DNS record: {url}")

    response = requests.put(url, headers=headers, json=data)

    resp = response.json()
    logging.debug(f"Response: {resp}")

    return resp["success"]

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help="Config file path")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.debug or os.environ.get("DEBUG") == "1":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not args.config:
        logging.error("No config file provided. Exiting...")
        sys.exit(1)

    if not os.path.isfile(args.config):
        logging.error("Config file not found. Exiting...")
        sys.exit(1)

    # Load config
    config = load(open(args.config), Loader=Loader)

    token = config.get("CF_API_TOKEN")
    zone_id = config.get("ZONE_ID")
    record_name = config.get("RECORD_NAME")

    if not token or not zone_id or not record_name:
        logging.error("Invalid config. Exiting...")
        sys.exit(1)

    logging.debug("Config loaded successfully.")
    logging.debug(f"Token: {token}, Zone ID: {zone_id}, Record Name: {record_name}")

    while True:
        current_ip = get_external_ip()
        dns_record = get_dns_record(token, record_name, zone_id)

        if dns_record and dns_record["content"] != current_ip:
            logging.info(f"IP change detected. Updating DNS record...")
            if update_dns_record(token, record_name, zone_id, dns_record["id"], current_ip):
                logging.info(f"DNS record updated successfully. New IP: {current_ip}")
            else:
                logging.error("Failed to update DNS record.")
        else:
            logging.info(f"No IP change detected. Current IP: {current_ip}")

        # Wait for 5 minutes before checking again
        time.sleep(300)
