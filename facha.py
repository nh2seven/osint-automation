import requests
import streamlit as st

# Function to fetch data from API
def get_data(api_url):
    try:
        headers = {"User-Agent": "Your User-Agent"}  # Replace with your User-Agent
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Streamlit GUI
st.title("Facha API Data")

# Base URL
base_url = "https://api.facha.dev/v1"

# API endpoints
endpoints = {
    "Aircraft Details by ICAO HEX Code": "/aircraft/detail/icao/",
    "Aircraft Details by Registration/Tail Number": "/aircraft/detail/reg/",
    "Total Number of Known Aircraft": "/aircraft/detail/stats"
}

# User selection
selected_endpoint = st.selectbox("Select API Endpoint", list(endpoints.keys()))

# Input field based on selected endpoint
input_value = st.text_input(f"Enter {'ICAO HEX Code' if selected_endpoint.startswith('Aircraft Details by ICAO') else 'Registration/Tail Number'}:")

if st.button("Get Data"):
    if selected_endpoint.startswith("Total Number"):
        api_url = base_url + endpoints[selected_endpoint]
    else:
        api_url = base_url + endpoints[selected_endpoint] + input_value

    api_data = get_data(api_url)

    if api_data:
        if selected_endpoint.startswith("Total Number"):
            st.write(f"Total number of known aircraft: {api_data['total']}")
        else:
            st.write("### Aircraft Details:")
            for key, value in api_data.items():
                st.write(f"- {key}: {value}")