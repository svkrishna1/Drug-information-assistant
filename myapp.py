import streamlit as st
import requests
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from huggingface_hub import login

# Log in to Hugging Face Hub
login("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")

# Initialize HuggingFaceEndpoint for drug recommendations
llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    task="text-generation",
    max_new_tokens=1024,
    do_sample=False,
    repetition_penalty=1.03,
    temperature=0.3
)

# Initialize the chat interface
chat = ChatHuggingFace(llm=llm, verbose=True)

# Your OpenFDA API Key
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

# Function to generate drug recommendations based on patient condition
def get_drug_recommendation(patient_condition):
    messages = [
        ("system", "You are a drug recommendation assistant. Your role is to provide appropriate drug recommendations based on patient conditions. For each drug, include dosage, potential side effects, drug interactions, overdose effects, and general uses. Always remind users to consult with healthcare professionals before taking any medication."),
        ("human", f"What would you recommend for a patient suffering from {patient_condition}?"),
    ]
    # Invoke the chat model with the given messages
    response = chat.invoke(messages)
    return response.content

# Streamlit app main function
def main():
    st.set_page_config(page_title="Drug Assistant", page_icon="💊", layout="wide")
    
    st.title("Drug Assistant")
    
    # Create sidebar for navigation
    choice = st.sidebar.selectbox("Choose Functionality", ["Drug Information", "Drug Recommendations"])
    
    if choice == "Drug Information":
        st.header("Drug Information Finder")
        
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

    elif choice == "Drug Recommendations":
        st.header("Drug Recommendation Assistant")
        st.write(
            "Enter a patient's condition, and we'll provide recommendations on appropriate drugs, "
            "including dosage, side effects, drug interactions, overdose effects, and uses."
        )
        
        # Input for patient condition
        patient_condition = st.text_input("Enter patient condition (e.g., 'skin rashes')", "")
        
        if st.button("Get Drug Recommendations"):
            if not patient_condition:
                st.error("Please enter a valid patient condition.")
            else:
                with st.spinner("Fetching drug recommendations..."):
                    response = get_drug_recommendation(patient_condition)
                # Output the response
                st.write("### Recommendations:")
                st.write(response)

if __name__ == "__main__":
    main()
