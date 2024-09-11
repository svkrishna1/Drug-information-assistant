import streamlit as st
import requests

# Your API Key
OPENFDA_API_KEY = "w3zN3cyCoBOGtVO7i32H09m0KWdbcPLSct3UVMth"

# Function to fetch drug information from OpenFDA
def fetch_openfda_drug_info(drug_name):
    base_url = "https://api.fda.gov/drug/label.json"
    params = {
        'api_key': OPENFDA_API_KEY,
        'search': f'openfda.brand_name:"{drug_name}"',
        'limit': 1
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to retrieve data: {response.status_code}"}

# Function to display detailed drug information in Streamlit
def display_drug_information(drug_name, data):
    if 'error' in data:
        st.error(data['error'])
    elif 'results' in data and data['results']:
        drug_info = data['results'][0]
        st.write(f"### Drug Information for {drug_name}:\n")
        
        # Display key details
        st.write("**Brand Name:**", drug_info.get('openfda', {}).get('brand_name', ['N/A'])[0])
        st.write("**Generic Name:**", drug_info.get('openfda', {}).get('generic_name', ['N/A'])[0])
        st.write("**Manufacturer:**", drug_info.get('openfda', {}).get('manufacturer_name', ['N/A'])[0])
        st.write("**Purpose:**", drug_info.get('purpose', ['N/A'])[0])
        st.write("**Indications and Usage:**", drug_info.get('indications_and_usage', ['N/A'])[0])
        st.write("**Warnings:**", drug_info.get('warnings', ['N/A'])[0])
        st.write("**Side Effects:**", drug_info.get('adverse_reactions', ['N/A'])[0])
        
        st.info("Note: Consult your healthcare provider for potential alternative treatments.")
    else:
        st.warning(f"No information found for {drug_name}.")

# Streamlit app main function
def main():
    st.title("Drug Information Finder")
    
    # Input field for drug name
    drug_name = st.text_input("Enter the drug name:")
    
    if st.button("Search"):
        if not drug_name:
            st.error("Please enter a drug name.")
        else:
            # Fetch data from OpenFDA API
            with st.spinner("Fetching drug information..."):
                openfda_data = fetch_openfda_drug_info(drug_name)
            # Display drug information
            display_drug_information(drug_name, openfda_data)

if __name__ == "__main__":
    main()
