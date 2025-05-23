# backend/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.handlers.loan_handler import load_loan_data, parse_query, query_loan_data

app = FastAPI()

loan_df = load_loan_data()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_loan_application(req: QueryRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    parsed = parse_query(query, loan_df)
    cust_id = parsed.get("Cust_ID")
    field = parsed.get("Field")

    if not cust_id:
        return {"answer": "Customer ID not found in dataset."}

    result = query_loan_data(loan_df, cust_id, field)

    if result is None:
        return {"answer": f"No record found for Customer_ID: {cust_id}"}

    if field:
        return {"answer": f"{field} for {cust_id}: {result}"}
    else:
        return {"answer": f"Matching record:\n{result}"}
