import requests


def get_data(api_endpoint):
    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


# Base URL
base_url = "https://phishstats.info:2096/api/phishing"

# API endpoints
endpoints = {
    "id": "(id, eq,",
    "asn": "(asn, eq,",
    "ip": "(ip, eq,",
    "country": "(countrycode,eq,",
    "tld": "(tld,eq,",
}

# User selection
selected_endpoint = input("Select API Endpoint: " + ", ".join(endpoints.keys()) + ": ")

enable_sorting = input("Enable Sorting (y/n): ").lower() == "y"

input_value = input("Enter Value for Query: ")

if input("Get Data (y/n): ").lower() == "y":
    if enable_sorting:
        api_endpoint = f"{base_url}?_where={endpoints[selected_endpoint]}{input_value})&_sort=-Type"
    else:
        api_endpoint = f"{base_url}?_where={endpoints[selected_endpoint]}{input_value})"

    api_data = get_data(api_endpoint)

    if api_data:
        print("Data:")
        print(api_data)
