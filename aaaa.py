import streamlit as st
import openai
import requests
import os  # Import the os module

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Hardcoded GitHub repository URL
REPO_URL = 'https://raw.githubusercontent.com/your_username/your_repo/main/kql_queries/'

# Function to fetch KQL queries from a GitHub repository
def fetch_kql_query(query_name):
    try:
        response = requests.get(f"{REPO_URL}{query_name}.kql")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return None

# Function to convert natural language to KQL using OpenAI GPT-3.5-turbo
def natural_language_to_kql(natural_language):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Convert the following natural language to KQL:\n\n{natural_language}"}
            ],
            max_tokens=150
        )
        kql_query = response.choices[0].message["content"].strip()
        return kql_query
    except Exception as e:
        return f"Error converting to KQL: {e}"

# Streamlit web application
st.title("Natural Language to KQL Converter")

# Input field for natural language query
natural_language = st.text_area("Enter your query in natural language:")

if st.button("Convert to KQL"):
    if natural_language:
        # Convert the natural language query to KQL
        converted_kql = natural_language_to_kql(natural_language)
        if "Error" not in converted_kql:
            st.subheader("Converted KQL Query:")
            st.code(converted_kql, language='kql')
            
            # Check if the converted KQL query exists in the GitHub repository
            kql_query = fetch_kql_query(converted_kql)
            if kql_query:
                st.subheader("Fetched KQL Query from GitHub:")
                st.code(kql_query, language='kql')
            else:
                st.warning("KQL query not found in the specified GitHub repository.")
                st.text_area("Submit your KQL query:", value=converted_kql, height=200)
        else:
            st.error(converted_kql)
    else:
        st.error("Please enter a query in natural language.")
