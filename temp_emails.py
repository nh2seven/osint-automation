import requests

def check_temporary_email(domain):
    try:
        url = f"https://api.facha.dev/v1/temporary-email/{domain}"
        headers = {"User-Agent": "Your User-Agent"}  # Replace with your User-Agent
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


# Terminal-based output
print("Check Temporary Email Address")

email = input("Enter Email Address:")
if email:
    # Extract domain part from email address
    domain = email.split("@")[-1]
    api_data = check_temporary_email(domain)

    if api_data:
        temporary = api_data["temporary"]

        print("Result:")
        if temporary:
            print(f"The email address '{email}' is a temporary email.")
        else:
            print(f"The email address '{email}' is not a temporary email.")
