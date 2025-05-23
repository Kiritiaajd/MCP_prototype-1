# backend/mcp_router.py

from backend.handlers.loan_handler import load_loan_data, parse_query, query_loan_data

loan_df = load_loan_data()

def run_query_loop():
    print("\n--- MCP Router Ready ---")
    while True:
        user_query = input("Ask your question (or type 'exit'): ").strip()
        if user_query.lower() in ['exit', 'quit']:
            print("Exiting MCP Router.")
            break

        parsed = parse_query(user_query, loan_df)
        cust_id = parsed.get("Cust_ID")
        field = parsed.get("Field")

        if not cust_id:
            print("Customer ID not found in dataset.")
            continue

        result = query_loan_data(loan_df, cust_id, field)
        if result is None:
            print(f"No record found for Cust_ID: {cust_id}")
        else:
            if field:
                print(f"{field} for {cust_id}: {result}")
            else:
                print("Matching record:")
                print(result)

if __name__ == "__main__":
    run_query_loop()
