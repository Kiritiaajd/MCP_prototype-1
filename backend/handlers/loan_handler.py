# backend/handlers/loan_handler.py

import os
import pandas as pd

def load_loan_data():
    base_dir = os.getcwd()
    data_path = os.path.join(base_dir, 'data', 'loan_application.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Loan data file not found at {data_path}")
    df = pd.read_csv(data_path)
    return df

def parse_query(query: str, loan_df: pd.DataFrame):
    query = query.lower()
    cust_id = None

    for cust in loan_df["Customer_ID"].astype(str).tolist():
        if cust.lower() in query:
            cust_id = cust
            break

    if "status" in query:
        field = "Application_Status"
    elif "application number" in query or "app no" in query:
        field = "Application_No"
    elif "name" in query:
        field = "Customer_Name"
    elif "exposure" in query:
        field = "Proposed_Exposure"
    else:
        field = None

    return {
        "Cust_ID": cust_id,
        "Field": field
    }

from typing import Optional

def query_loan_data(loan_df: pd.DataFrame, cust_id: str, field: Optional[str] = None):
    match = loan_df[loan_df["Customer_ID"] == cust_id]
    if match.empty:
        return None
    if field and field in match.columns:
        return match.iloc[0][field]
    else:
        return match.to_string(index=False)
