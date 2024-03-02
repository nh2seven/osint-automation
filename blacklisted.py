import requests


def check_cins_blacklist(ip_address):
    try:
        cins_url = "https://cinsscore.com/list/ci-badguys.txt"
        cins_response = requests.get(cins_url)
        cins_response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        if ip_address in cins_response.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CINS Score data: {e}")
        return None


# Example usage:
ip_address = "188.126.94.176"
blacklisted = check_cins_blacklist(ip_address)
if blacklisted is not None:
    print(
        f"The IP address {ip_address} is {'blacklisted' if blacklisted else 'not blacklisted'} in the CINS Score blacklist."
    )
