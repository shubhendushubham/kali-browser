import streamlit as st
import requests
import json

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
st.title("KQL Query Generator for Microsoft and Azure Services")

# User inputs
service = st.selectbox("Select Service", ["Azure Monitor", "Microsoft Defender", "Log Analytics"])
query_type = st.selectbox("Select Query Type", ["Security", "Performance", "Usage"])

# Fetch queries from GitHub
repo_url = st.text_input("Enter GitHub Repository URL", "https://api.github.com/repos/yourusername/yourrepo/contents/queries.json")
queries = fetch_queries_from_github(repo_url)

if st.button("Generate KQL Query"):
    kql_query = generate_kql_query(service, query_type)
    st.code(kql_query, language='kql')

# Display fetched queries
if queries:
    st.subheader("Fetched Queries")
    for query in queries:
        st.write(query)
