import os
import streamlit as st

st.title("🔍 Debugging MySQL Connection in Streamlit")

# Check if MYSQL_CONNECTION_STRING is correctly passed to Streamlit
mysql_connection_string = os.getenv("MYSQL_CONNECTION_STRING")

if mysql_connection_string:
    st.success("✅ MYSQL_CONNECTION_STRING is loaded!")
    st.write(f"🔍 Debug: {mysql_connection_string[:50]}...")  # Show part of the connection string
else:
    st.error("❌ MYSQL_CONNECTION_STRING is missing! Check GitHub Secrets and Deployment.")
    st.stop()

