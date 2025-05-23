import streamlit as st
import requests

API_URL = "http://localhost:8000/query"  # Update if your API runs elsewhere

def query_backend(question):
    """Send question to backend API and get response."""
    try:
        response = requests.post(API_URL, json={"query": question})
        if response.status_code == 200:
            return response.json().get("answer", "No answer found.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error connecting to backend: {e}"

def main():
    st.title("Loan Application Query Interface")

    st.write(
        "Ask questions about loan applications, for example:\n"
        "- What is the application status of CUST021?\n"
        "- How much exposure is proposed for CUST-1010?"
    )

    question = st.text_input("Enter your question:")

    if st.button("Ask"):
        if question.strip():
            answer = query_backend(question)
            st.success(answer)
        else:
            st.warning("Please enter a question before submitting.")

if __name__ == "__main__":
    main()
