import streamlit as st
import openai
import requests
import os

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to fetch KQL queries from a GitHub repository
def fetch_kql_query(repo_url, query_name):
    try:
        response = requests.get(f"{repo_url}/{query_name}.kql")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching query: {e}"

# Function to convert natural language to KQL using OpenAI GPT-3
def natural_language_to_kql(natural_language):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Convert the following natural language to KQL:\n\n{natural_language}",
            max_tokens=150
        )
        kql_query = response.choices[0].text.strip()
        return kql_query
    except Exception as e:
        return f"Error converting to KQL: {e}"

# Streamlit web application
st.title("Natural Language to KQL Converter")

# Input fields for user inputs
repo_url = st.text_input("Enter the GitHub repository URL containing KQL queries:")
query_name = st.text_input("Enter the name of the KQL query file (without extension):")
natural_language = st.text_area("Enter your query in natural language:")

# Button to trigger the conversion process
if st.button("Convert to KQL"):
    if repo_url and query_name and natural_language:
        # Fetch the KQL query from GitHub
        kql_query = fetch_kql_query(repo_url, query_name)
        if "Error" not in kql_query:
            st.subheader("Fetched KQL Query from GitHub:")
            st.code(kql_query, language='kql')
        else:
            st.error(kql_query)
        
        # Convert the natural language query to KQL
        converted_kql = natural_language_to_kql(natural_language)
        if "Error" not in converted_kql:
            st.subheader("Converted KQL Query:")
            st.code(converted_kql, language='kql')
            
            # Option to save the converted KQL query
            if st.button("Save Converted KQL Query"):
                with open(f"{query_name}_converted.kql", "w") as file:
                    file.write(converted_kql)
                st.success(f"Converted KQL query saved as {query_name}_converted.kql")
        else:
            st.error(converted_kql)
    else:
        st.error("Please provide all inputs.")
