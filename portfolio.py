import streamlit as st
import os

st.title("🔍 Debugging Streamlit Deployment")

# Check if secrets are loading correctly
mysql_connection_string = os.getenv("MYSQL_CONNECTION_STRING")
st.write(f"🔍 MYSQL_CONNECTION_STRING: {mysql_connection_string[:50]}...")

if mysql_connection_string is None:
    st.error("❌ MYSQL_CONNECTION_STRING is missing! Check GitHub Secrets.")

# Add a basic test output
st.success("✅ Streamlit is running!")
