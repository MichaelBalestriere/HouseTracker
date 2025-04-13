import requests

# API endpoint
url = "https://financialmodelingprep.com/stable/insider-trading/latest"

# Your API key
api_key = "1VmWVK5JNFhCrEekrP5FX4hj2EuNFdvG"

# Ask the user to enter a date in the format YYYY-MM-DD
date = input("Enter the date (YYYY-MM-DD): ")

# Make the GET request with the user-provided date
response = requests.get(f"{url}?apikey={api_key}&date={date}")

# Check if the request was successful
if response.status_code == 200:
    # Parse the response data
    data = response.json()
    
    # Define the transaction types to filter (Purchase and Sale)
    important_transaction_types = ['P-Purchase', 'S-Sale']  # Purchases and Sales
    
    # Filter and display the relevant facts for each trade
    for trade in data:
        # Check if the transaction date matches the user-provided date
        if trade['transactionDate'] == date:
            # Calculate total cost
            total_cost = trade['securitiesTransacted'] * trade['price']
            
            # Check if the transaction type is either 'P' (Purchase) or 'S' (Sale)
            if trade['transactionType'] in important_transaction_types:
                # Format the total cost with commas
                formatted_total_cost = f"{total_cost:,.2f}"
                
                print("\n-------------------------------")
                print(f"Insider Name: {trade['reportingName']}")
                print(f"Transaction Date: {trade['transactionDate']}")
                print(f"Transaction Type: {trade['transactionType']}")
                print(f"Shares Transacted: {trade['securitiesTransacted']}")
                print(f"Price: ${trade['price']}")
                print(f"Total Cost: ${formatted_total_cost}")
                print(f"Relation to Trade: {trade['typeOfOwner']}")
                
else:
    print(f"Error: {response.status_code}")
