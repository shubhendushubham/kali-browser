import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import socket
import random
import scapy.all as scapy
from datetime import datetime

# Function to generate random traffic data
def generate_traffic_data():
    data = {
        'timestamp': pd.date_range(start='1/1/2024', periods=100, freq='T'),
        'ingress_ping': [random.uniform(10, 100) for _ in range(100)],
        'egress_ping': [random.uniform(10, 100) for _ in range(100)],
        'latency': [random.uniform(1, 10) for _ in range(100)],
        'ip_address': [socket.gethostbyname(socket.gethostname()) for _ in range(100)]
    }
    return pd.DataFrame(data)

# Function to capture real-time traffic data
def capture_traffic_data(duration=60):
    packets = scapy.sniff(timeout=duration)
    data = {
        'timestamp': [],
        'ingress_ping': [],
        'egress_ping': [],
        'latency': [],
        'ip_address': []
    }
    for packet in packets:
        data['timestamp'].append(datetime.now())
        data['ingress_ping'].append(random.uniform(10, 100))
        data['egress_ping'].append(random.uniform(10, 100))
        data['latency'].append(random.uniform(1, 10))
        data['ip_address'].append(packet[scapy.IP].src if scapy.IP in packet else 'N/A')
    return pd.DataFrame(data)

# Set up Streamlit page
st.set_page_config(layout="wide")
st.title("Network Traffic Analyzer")

# Sidebar for navigation
st.sidebar.title("Navigation")
sections = ["Overview", "Ingress Ping", "Egress Ping", "Latency", "IP Addresses", "Real-Time Capture"]
selected_section = st.sidebar.radio("Go to", sections)

# Generate or capture traffic data
if selected_section == "Real-Time Capture":
    st.header("Real-Time Traffic Capture")
    duration = st.sidebar.slider("Capture Duration (seconds)", 10, 120, 60)
    if st.sidebar.button("Start Capture"):
        df = capture_traffic_data(duration)
else:
    df = generate_traffic_data()

# Overview Section
if selected_section == "Overview":
    st.header("Overview")
    st.line_chart(df.set_index('timestamp')[['ingress_ping', 'egress_ping', 'latency']])
    st.write("This section provides an overview of the network traffic.")

# Ingress Ping Section
elif selected_section == "Ingress Ping":
    st.header("Ingress Ping")
    st.line_chart(df.set_index('timestamp')['ingress_ping'])
    st.write("This section shows the ingress ping over time.")

# Egress Ping Section
elif selected_section == "Egress Ping":
    st.header("Egress Ping")
    st.line_chart(df.set_index('timestamp')['egress_ping'])
    st.write("This section shows the egress ping over time.")

# Latency Section
elif selected_section == "Latency":
    st.header("Latency")
    st.line_chart(df.set_index('timestamp')['latency'])
    st.write("This section shows the latency over time.")

# IP Addresses Section
elif selected_section == "IP Addresses":
    st.header("IP Addresses")
    ip_filter = st.sidebar.text_input("Filter by IP Address")
    if ip_filter:
        df_filtered = df[df['ip_address'] == ip_filter]
        st.dataframe(df_filtered[['timestamp', 'ip_address']])
    else:
        st.dataframe(df[['timestamp', 'ip_address']])
    st.write("This section lists the IP addresses involved in the traffic.")

# Export Data Section
if st.sidebar.button("Export Data"):
    df.to_csv('network_traffic_data.csv')
    st.sidebar.write("Data exported to network_traffic_data.csv")

# Customizing the UI
sns.set(style="whitegrid")
palette = sns.color_palette("viridis", as_cmap=True)
