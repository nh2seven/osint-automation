import requests
import streamlit as st

def query_blocklist(ip_address):
    base_url = 'http://api.blocklist.de/api.php'
    params = {'ip': ip_address}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)  # Print the error message
        return None

# Streamlit GUI
st.title("Blocklist.de IP Query")

ip_address = st.text_input('Enter IP Address', value='78.46.91.239')

if st.button('Query'):
    result = query_blocklist(ip_address)
    if result:
        st.write("IP Query Result:")
        parts = result.split('<br />')
        for part in parts:
            key_value = part.split(': ')
            if len(key_value) == 2:
                key, value = key_value
                st.write(f"{key.capitalize()}: {value}")
            else:
                st.write(part)
