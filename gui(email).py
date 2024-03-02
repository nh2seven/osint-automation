import requests
import streamlit as st

def check_temporary_email(domain):
    try:
        url = f"https://api.facha.dev/v1/temporary-email/{domain}"
        headers = {
            "User-Agent": "Your User-Agent"  # Replace with your User-Agent
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Streamlit GUI
st.title("Check Temporary Email Address")

email = st.text_input("Enter Email Address:")
if email:
    # Extract domain part from email address
    domain = email.split('@')[-1]
    api_data = check_temporary_email(domain)

    if api_data:
        temporary = api_data["temporary"]

        st.write("### Result:")
        if temporary:
            st.write(f"The email address '{email}' is a temporary email.")
        else:
            st.write(f"The email address '{email}' is not a temporary email.")
