import requests
import json

def generate_webhook():
    """Step 1: Send initial POST request to generate webhook"""
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    payload = {
        "name": "Aman Rajput",
        "regNo": "0827IT221012",  # Last digit is 2 (even)
        "email": "amanrajput220712@acropolis.in"
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error generating webhook: {e}")
        return None

def solve_sql_problem():
    """Step 2: Solve the SQL problem (Question 2 for even regNo)"""
    sql_query = """
    SELECT 
        e1.EMP_ID,
        e1.FIRST_NAME,
        e1.LAST_NAME,
        d.DEPARTMENT_NAME,
        COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT
    FROM 
        EMPLOYEE e1
    JOIN 
        DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID
    LEFT JOIN 
        EMPLOYEE e2 ON e1.DEPARTMENT = e2.DEPARTMENT 
                    AND e2.DOB > e1.DOB
    GROUP BY 
        e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME
    ORDER BY 
        e1.EMP_ID DESC;
    """
    return sql_query.strip()

def submit_solution(webhook_url, access_token, sql_query):
    """Step 3: Submit the solution to the webhook"""
    payload = [{"finalQuery": sql_query}]
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error submitting solution: {e}")
        return None

def main():
    print("Starting Bajaj Finserv Health Qualifier 1 submission...")
    
    # Step 1: Generate webhook
    print("\nStep 1: Generating webhook...")
    webhook_data = generate_webhook()
    
    if not webhook_data:
        print("Failed to generate webhook. Exiting.")
        return
    
    webhook_url = webhook_data.get('webhook')
    access_token = webhook_data.get('accessToken')
    
    print(f"Webhook URL received: {webhook_url}")
    print(f"Access token received: {access_token[:5]}...")  # Show partial token for security
    
    # Step 2: Solve SQL problem
    print("\nStep 2: Solving SQL problem...")
    sql_query = solve_sql_problem()
    print("SQL Query prepared:")
    print(sql_query)
    
    # Step 3: Submit solution
    print("\nStep 3: Submitting solution...")
    response = submit_solution(webhook_url, access_token, sql_query)
    
    if response and response.status_code == 200:
        print("\nSubmission successful!")
        print("Response:", response.json())
    else:
        print("\nSubmission failed.")
        if response:
            print("Status code:", response.status_code)
            print("Response:", response.text)

if __name__ == "__main__":
    main()