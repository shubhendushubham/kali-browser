import streamlit as st

# Custom CSS for colorful UI
def load_css():
    st.markdown(
        """
        <style>
        .stSelectbox, .stButton {
            background-color: #f0f0f5;
            color: #333;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Load custom CSS
load_css()

# Set the title and description
st.title("Serverless Security Framework Generator")
st.markdown("### Generate a customized serverless security framework based on your inputs")

# User inputs
vm_size = st.selectbox("Select VM Size", ["Small", "Medium", "Large"])
deployment_region = st.selectbox("Select Deployment Region", ["US East", "US West", "Europe", "Asia"])
pricing_tier = st.selectbox("Select Pricing Tier", ["Free", "Standard", "Premium"])

# Display user inputs
st.markdown(f"**VM Size:** {vm_size}")
st.markdown(f"**Deployment Region:** {deployment_region}")
st.markdown(f"**Pricing Tier:** {pricing_tier}")

# Function to generate security framework
def generate_framework(vm_size, deployment_region, pricing_tier):
    framework = {
        "VM Size": vm_size,
        "Deployment Region": deployment_region,
        "Pricing Tier": pricing_tier,
        "Best Practices": [
            "Ensure least privilege access",
            "Implement strong input validation",
            "Set up comprehensive logging and monitoring",
            "Use encryption for data at rest and in transit",
            "Manage secrets securely"
        ]
    }
    return framework

# Generate framework button
if st.button("Generate Framework"):
    framework = generate_framework(vm_size, deployment_region, pricing_tier)
    st.success("Framework generated successfully!")
    st.json(framework)
