import streamlit as st
import requests

def query_blocklist(ip_address):
    base_url = 'http://api.blocklist.de/api.php'
    params = {'ip': ip_address}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}\n{response.text}"

def check_cins_blacklist(ip_address):
    try:
        cins_url = "https://cinsscore.com/list/ci-badguys.txt"
        cins_response = requests.get(cins_url)
        cins_response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        if ip_address in cins_response.text:
            return "Blacklisted by CINS"
        else:
            return "Not blacklisted by CINS"
    except requests.exceptions.RequestException as e:
        return f"Error fetching CINS Score data: {e}"

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

# Streamlit GUI
st.title("IP Information Query")

ip_address = st.text_input('Enter IP Address')

if st.button('Query'):
    if ip_address:
        blocklist_result = query_blocklist(ip_address)
        cins_result = check_cins_blacklist(ip_address)
        ip_info = get_ip_info(ip_address)

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

        st.subheader("CINS Status:")
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
    else:
        st.write("Please enter an IP address")
