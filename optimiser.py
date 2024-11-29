import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the FirewallRule class
class FirewallRule:
    def __init__(self, rule_id, protocol, src_ip, dest_ip, src_port, dest_port, action):
        self.rule_id = rule_id
        self.protocol = protocol
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.src_port = src_port
        self.dest_port = dest_port
        self.action = action

    def __repr__(self):
        return f"Rule({self.rule_id}, {self.protocol}, {self.src_ip}, {self.dest_ip}, {self.src_port}, {self.dest_port}, {self.action})"

# Function to detect conflicts
def detect_conflicts(rules):
    conflicts = []
    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            if (rules[i].src_ip == rules[j].src_ip and
                rules[i].dest_ip == rules[j].dest_ip and
                rules[i].protocol == rules[j].protocol and
                rules[i].src_port == rules[j].src_port and
                rules[i].dest_port == rules[j].dest_port and
                rules[i].action != rules[j].action):
                conflicts.append((rules[i], rules[j]))
    return conflicts

# Function to optimize rules
def optimize_rules(rules):
    optimized_rules = []
    seen = set()
    for rule in rules:
        rule_tuple = (rule.protocol, rule.src_ip, rule.dest_ip, rule.src_port, rule.dest_port, rule.action)
        if rule_tuple not in seen:
            seen.add(rule_tuple)
            optimized_rules.append(rule)
    return optimized_rules

# Streamlit app
st.title("Firewall Policy Optimizer")

uploaded_file = st.file_uploader("Upload Firewall Rules", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    rules = [FirewallRule(row['rule_id'], row['protocol'], row['src_ip'], row['dest_ip'], row['src_port'], row['dest_port'], row['action']) for index, row in df.iterrows()]
    st.write("Uploaded Firewall Rules:")
    st.write(df)

    # Filter options
    protocol_filter = st.selectbox("Filter by Protocol", options=["All"] + list(df['protocol'].unique()))
    action_filter = st.selectbox("Filter by Action", options=["All"] + list(df['action'].unique()))

    filtered_df = df
    if protocol_filter != "All":
        filtered_df = filtered_df[filtered_df['protocol'] == protocol_filter]
    if action_filter != "All":
        filtered_df = filtered_df[filtered_df['action'] == action_filter]

    st.write("Filtered Firewall Rules:")
    st.write(filtered_df)

    if st.button("Detect Conflicts"):
        conflicts = detect_conflicts(rules)
        if conflicts:
            st.write("Conflicts detected:")
            for conflict in conflicts:
                st.write(conflict)
        else:
            st.write("No conflicts detected.")

    if st.button("Optimize Rules"):
        optimized_rules = optimize_rules(rules)
        st.write("Optimized Rules:")
        for rule in optimized_rules:
            st.write(rule)

    # Graph options
    st.write("Firewall Rules Visualization:")
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x='protocol', hue='action', ax=ax)
    st.pyplot(fig)
