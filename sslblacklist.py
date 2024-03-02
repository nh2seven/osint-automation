import pandas as pd
import streamlit as st

# Load the data
df = pd.read_csv('sslblacklist.csv')

# Create Streamlit UI
st.title('Lookup SHA1 in DataFrame')

# Input field for SHA1
sha1_input = st.text_input('Enter SHA1')

# Function to find listing date and reason
def find_listing_info(sha1):
    result = df[df['SHA1'] == sha1]
    if not result.empty:
        listing_date = result.iloc[0]['Listingdate']
        listing_reason = result.iloc[0]['Listingreason']
        st.write(f'Listing Date: {listing_date}')
        st.write(f'Listing Reason: {listing_reason}')
    else:
        st.write('No matching SHA1 found.')

# Button to trigger lookup
if st.button('Lookup'):
    find_listing_info(sha1_input)
