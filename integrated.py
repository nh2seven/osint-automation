import streamlit as st
import requests
import pandas as pd
import re

# Load SSL blacklist data
df_ssl = pd.read_csv('sslblacklist.csv')

# Function to query Blocklist.de for IP addresses
def query_blocklist(ip_address):
    base_url = 'http://api.blocklist.de/api.php'
    params = {'ip': ip_address}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}\n{response.text}"

# Function to check CINS Score blacklist for IP addresses
def check_cins_blacklist(ip_address):
    try:
        cins_url = "https://cinsscore.com/list/ci-badguys.txt"
        cins_response = requests.get(cins_url)
        cins_response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        if ip_address in cins_response.text:
            return "Blacklisted in CINS Score"
        else:
            return "Not blacklisted in CINS Score"
    except requests.exceptions.RequestException as e:
        return f"Error fetching CINS Score data: {e}"

# Function to get information about an IP address
def get_ip_info(ip_address):
    try:
        url = f"https://api.facha.dev/v1/ip/{ip_address}"
        headers = {"User-Agent": "Your User-Agent"}  # Replace with your User-Agent
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"

# Function to check if an email is a temporary one
def check_temporary_email(domain):
    try:
        url = f"https://api.facha.dev/v1/temporary-email/{domain}"
        headers = {"User-Agent": "Your User-Agent"}  # Replace with your User-Agent
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"

# Function to validate IP address
def validate_ip(ip):
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(ip_pattern, ip) is not None

# Function to validate email address
def validate_email(email):
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_pattern, email) is not None

# Function to validate SHA1 hash
def validate_sha1(sha1):
    sha1_pattern = r"^[a-fA-F0-9]{40}$"
    return re.match(sha1_pattern, sha1) is not None

# Function to query SHA1 information from CSV
def query_sha1_from_csv(sha1_hash):
    result = df_ssl[df_ssl['SHA1'] == sha1_hash]
    if not result.empty:
        listing_date = result.iloc[0]['Listingdate']
        listing_reason = result.iloc[0]['Listingreason']
        return f"Listing Date: {listing_date}\nListing Reason: {listing_reason}"
    else:
        return "No matching SHA1 found in the CSV."

# Streamlit GUI
st.title("Data Query Tool")

# Input field for user query
query_input = st.text_input("Enter Data:")

# Button to trigger the query
if st.button('Query'):
    if query_input:
        if validate_ip(query_input):
            # IP Address query
            ip_address = query_input
            blocklist_result = query_blocklist(ip_address)
            cins_result = check_cins_blacklist(ip_address)
            ip_info = get_ip_info(ip_address)

            st.subheader("IP Address Query Result:")
            st.write(f"IP Address: {ip_address}")

            st.subheader("Blocklist.de Result:")
            if blocklist_result:
                parts = blocklist_result.split('<br />')
                for part in parts:
                    key_value = part.split(': ')
                    if len(key_value) == 2:
                        key, value = key_value
                        st.write(f"- {key.capitalize()}: {value}")
                    else:
                        st.write(part)
            else:
                st.write("No data available")

            st.subheader("CINS Score Result:")
            st.write(cins_result)

            st.subheader("IP Information:")
            if ip_info:
                st.write(f"- IP: {ip_info['ip']}")
                st.write(f"- Subnet: {ip_info['subnet']}")
                st.write(f"- ASN Number: {ip_info['asn']['number']}")
                st.write(f"- ASN Name: {ip_info['asn']['name']}")
                st.write(f"- ASN Description: {ip_info['asn']['description']}")
                st.write(f"- Country: {ip_info['country']}")
                st.write(f"- Hosting: {ip_info['hosting']}")
            else:
                st.write("No data available")

        elif validate_email(query_input):
            # Email Address query
            email = query_input
            domain = email.split("@")[-1]
            api_data = check_temporary_email(domain)

            st.subheader("Email Address Query Result:")
            st.write(f"Email Address: {email}")

            if api_data:
                temporary = api_data["temporary"]
                st.write("Result:")
                if temporary:
                    st.write(f"The email address '{email}' is a temporary email.")
                else:
                    st.write(f"The email address '{email}' is not a temporary email.")
            else:
                st.write("Error fetching data")

        elif validate_sha1(query_input):
            # SHA1 Hash query
            sha1_hash = query_input
            sha1_result = query_sha1_from_csv(sha1_hash)
            st.subheader("SHA1 Hash Query Result:")
            st.write(sha1_result)

        else:
            st.write("Invalid input. Please enter a valid IP Address, Email Address, SHA1 Hash, or ICAO Hex Code.")
    else:
        st.write("Please enter a query.")
