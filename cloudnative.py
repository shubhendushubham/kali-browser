import streamlit as st
import requests
import json

# GitHub repository URL
REPO_URL = "https://api.github.com/repos/yourusername/yourrepo/contents/queries.json"

# Function to fetch KQL queries from GitHub
def fetch_queries_from_github(repo_url):
    response = requests.get(repo_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch queries from GitHub")
        return []

# Function to generate KQL query based on user input
def generate_kql_query(service, query_type):
    # Placeholder for actual KQL query generation logic
    return f"Generated KQL query for {service} with type {query_type}"

# Streamlit UI
st.set_page_config(page_title="KQL Query Generator", page_icon=":mag:", layout="wide")

st.title("🔍 KQL Query Generator for Microsoft and Azure Services")
st.markdown("Generate KQL queries based on your inputs and fetch predefined queries from a GitHub repository.")

# User inputs
st.sidebar.header("Configuration")
service = st.sidebar.selectbox("Select Service", ["Azure Monitor", "Microsoft Defender", "Log Analytics"])
query_type = st.sidebar.selectbox("Select Query Type", ["Security", "Performance", "Usage"])

# Fetch queries from GitHub
queries = fetch_queries_from_github(REPO_URL)

if st.sidebar.button("Generate KQL Query"):
    kql_query = generate_kql_query(service, query_type)
    st.code(kql_query, language='kql')

# Display fetched queries
if queries:
    st.subheader("Fetched Queries")
    for query in queries:
        st.write(query)

# Footer
st.markdown("---")
st.markdown("Developed by Your Name")
