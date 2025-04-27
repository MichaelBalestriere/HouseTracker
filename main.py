import requests
import csv
import tkinter as tk
from tkinter import messagebox, filedialog

# API details
url = "https://financialmodelingprep.com/stable/insider-trading/latest"
api_key = "1VmWVK5JNFhCrEekrP5FX4hj2EuNFdvG"

def fetch_trades():
    date = date_entry.get()
    response = requests.get(f"{url}?apikey={api_key}&date={date}")
    
    if response.status_code == 200:
        data = response.json()
        important_transaction_types = ['P-Purchase', 'S-Sale']
        exportable_trades.clear()
        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        
        for trade in data:
            if trade['transactionDate'] == date:
                total_cost = trade['securitiesTransacted'] * trade['price']
                if trade['transactionType'] in important_transaction_types:
                    formatted_total_cost = f"{total_cost:,.2f}"
                    
                    output_text.insert(tk.END, "\n-------------------------------\n")
                    output_text.insert(tk.END, f"Insider Name: {trade['reportingName']}\n")
                    output_text.insert(tk.END, f"Transaction Date: {trade['transactionDate']}\n")
                    output_text.insert(tk.END, f"Transaction Type: {trade['transactionType']}\n")
                    output_text.insert(tk.END, f"Shares Transacted: {trade['securitiesTransacted']}\n")
                    output_text.insert(tk.END, f"Price: ${trade['price']}\n")
                    output_text.insert(tk.END, f"Total Cost: ${formatted_total_cost}\n")
                    output_text.insert(tk.END, f"Relation to Trade: {trade['typeOfOwner']}\n")
                    
                    exportable_trades.append({
                        'Insider Name': trade['reportingName'],
                        'Transaction Date': trade['transactionDate'],
                        'Transaction Type': trade['transactionType'],
                        'Shares Transacted': trade['securitiesTransacted'],
                        'Price': trade['price'],
                        'Total Cost': total_cost,
                        'Relation to Trade': trade['typeOfOwner']
                    })
        
        if not exportable_trades:
            messagebox.showinfo("No Trades", "No matching trades to display or export.")
        output_text.config(state='disabled')
    else:
        messagebox.showerror("Error", f"Failed to fetch data: {response.status_code}")

def export_to_csv():
    if not exportable_trades:
        messagebox.showinfo("No Data", "No trades to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                              filetypes=[("CSV files", "*.csv")],
                                              initialfile=f"insider_trades_{date_entry.get()}.csv")
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=exportable_trades[0].keys())
            writer.writeheader()
            writer.writerows(exportable_trades)
        messagebox.showinfo("Success", f"Exported {len(exportable_trades)} trades to:\n{file_path}")

# GUI setup
root = tk.Tk()
root.title("Insider Trading Viewer")
root.geometry('800x600')
root.config(bg="#f0f2f5")

# Styles
entry_bg = "#ffffff"
button_bg = "#4CAF50"
button_fg = "#ffffff"
button_hover = "#45a049"
text_bg = "#ffffff"
frame_bg = "#ffffff"
font_main = ('Helvetica', 12)
font_title = ('Helvetica', 16, 'bold')

# Functions to create hover effect
def on_enter(e):
    e.widget['background'] = button_hover

def on_leave(e):
    e.widget['background'] = button_bg

# Layout
title_label = tk.Label(root, text="Insider Trading Viewer", font=font_title, bg="#f0f2f5")
title_label.pack(pady=20)

date_frame = tk.Frame(root, bg="#f0f2f5")
date_frame.pack(pady=10)

date_label = tk.Label(date_frame, text="Enter Date (YYYY-MM-DD):", font=font_main, bg="#f0f2f5")
date_label.pack(side=tk.LEFT, padx=5)

date_entry = tk.Entry(date_frame, font=font_main, bg=entry_bg, width=20, bd=2, relief="groove")
date_entry.pack(side=tk.LEFT, padx=5)

button_frame = tk.Frame(root, bg="#f0f2f5")
button_frame.pack(pady=10)

fetch_button = tk.Button(button_frame, text="Fetch Trades", command=fetch_trades,
                         font=font_main, bg=button_bg, fg=button_fg, activebackground=button_hover,
                         width=15, bd=0, relief="ridge", cursor="hand2")
fetch_button.pack(side=tk.LEFT, padx=10)

export_button = tk.Button(button_frame, text="Export to CSV", command=export_to_csv,
                          font=font_main, bg=button_bg, fg=button_fg, activebackground=button_hover,
                          width=15, bd=0, relief="ridge", cursor="hand2")
export_button.pack(side=tk.LEFT, padx=10)

fetch_button.bind("<Enter>", on_enter)
fetch_button.bind("<Leave>", on_leave)
export_button.bind("<Enter>", on_enter)
export_button.bind("<Leave>", on_leave)

output_frame = tk.Frame(root, bg=frame_bg, bd=2, relief="groove")
output_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

output_text = tk.Text(output_frame, wrap='word', font=('Courier', 10), bg=text_bg, state='disabled')
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

exportable_trades = []

root.mainloop()
