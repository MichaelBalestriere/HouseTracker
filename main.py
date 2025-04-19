import requests
import csv

url = "https://financialmodelingprep.com/stable/insider-trading/latest"
api_key = "1VmWVK5JNFhCrEekrP5FX4hj2EuNFdvG"

date = input("Enter the date (YYYY-MM-DD): ")
response = requests.get(f"{url}?apikey={api_key}&date={date}")

if response.status_code == 200:
    data = response.json()
    important_transaction_types = ['P-Purchase', 'S-Sale']
    exportable_trades = []  # Store trades to potentially export

    for trade in data:
        if trade['transactionDate'] == date:
            total_cost = trade['securitiesTransacted'] * trade['price']
            if trade['transactionType'] in important_transaction_types:
                formatted_total_cost = f"{total_cost:,.2f}"
                
                print("\n-------------------------------")
                print(f"Insider Name: {trade['reportingName']}")
                print(f"Transaction Date: {trade['transactionDate']}")
                print(f"Transaction Type: {trade['transactionType']}")
                print(f"Shares Transacted: {trade['securitiesTransacted']}")
                print(f"Price: ${trade['price']}")
                print(f"Total Cost: ${formatted_total_cost}")
                print(f"Relation to Trade: {trade['typeOfOwner']}")
                
                exportable_trades.append({
                    'Insider Name': trade['reportingName'],
                    'Transaction Date': trade['transactionDate'],
                    'Transaction Type': trade['transactionType'],
                    'Shares Transacted': trade['securitiesTransacted'],
                    'Price': trade['price'],
                    'Total Cost': total_cost,
                    'Relation to Trade': trade['typeOfOwner']
                })

    # Ask if the user wants to export the filtered trades to a CSV file
    if exportable_trades:
        should_export = input("\nWould you like to export these trades to a CSV file? (yes/no): ").lower()
        if should_export == 'yes':
            filename = r"C:\Users\Mabal\OneDrive\Documents\MyVsCode\Programming II\FinalProject\insider_trades_" + date + ".csv"
            with open(filename, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=exportable_trades[0].keys())
                writer.writeheader()
                writer.writerows(exportable_trades)
            print(f"\nExported {len(exportable_trades)} trades to {filename}")
    else:
        print("No matching trades to export.")
else:
    print(f"Error: {response.status_code}")
