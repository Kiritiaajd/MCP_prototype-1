import streamlit as st
import requests

st.title("MCP Prototype Query Interface")

query = st.text_input("Enter your financial query:")

if st.button("Submit Query"):
    if query.strip():
        try:
            response = requests.post("http://localhost:8000/query", json={"query": query})
            if response.status_code == 200:
                st.success(response.json().get("answer"))
            else:
                st.error(f"Error: Server returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: Could not retrieve data from server. Details: {e}")
    else:
        st.warning("Please enter a valid query before submitting.")
