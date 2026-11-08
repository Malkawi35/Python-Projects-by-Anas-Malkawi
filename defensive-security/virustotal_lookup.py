import requests
import json
import os

API_Key = os.environ["VT_API_KEY"]  # export VT_API_KEY=... (free key from virustotal.com)

def check_hash(hash_value):
    url = f"https://www.virustotal.com/api/v3/files/{hash_value}"
    headers = {"x-apikey": API_Key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print("VirusTotal Result:")
        print(json.dumps(result, indent=4))
    else:
        print(f"Error: {response.status_code}: {response.text}")

def check_ip(ip_to_check):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_to_check}"
    headers = {"x-apikey": API_Key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print("VirusTotal Result:")
        print(json.dumps(result, indent=4))
    else:
        print(f"Error: {response.status_code}: {response.text}")

if __name__ == "__main__":
    indicator =input("Enter a hash or IP Address: ").strip()
    kind = input("Type 'ip' or 'hash' to select:").strip()

    if kind == "hash":
        check_hash(indicator)
    elif kind == "ip":
        check_ip(indicator)
    else:
        print("Please enter a valid choice.")

