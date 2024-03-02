import requests

def get_ip_info(ip_address):
    try:
        url = f"https://api.facha.dev/v1/ip/{ip_address}"
        headers = {"User-Agent": "Your User-Agent"}  # Replace with your User-Agent
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Terminal-based output
print("IP Information Retrieval")

ip_address = input("Enter IP Address:")
if ip_address:
    api_data = get_ip_info(ip_address)

    if api_data:
        ip = api_data["ip"]
        subnet = api_data["subnet"]
        asn_number = api_data["asn"]["number"]
        asn_name = api_data["asn"]["name"]
        asn_description = api_data["asn"]["description"]
        country = api_data["country"]
        hosting = api_data["hosting"]

        print("IP Information:")
        print(f"- IP: {ip}")
        print(f"- Subnet: {subnet}")
        print(f"- ASN Number: {asn_number}")
        print(f"- ASN Name: {asn_name}")
        print(f"- ASN Description: {asn_description}")
        print(f"- Country: {country}")
        print(f"- Hosting: {hosting}")
    else:
        print("No data available")
