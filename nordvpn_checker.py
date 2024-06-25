# NordVPN Account Checker

print("""
  _______
 /        \
|  NORD  |
 _|  VPN  |_
  |       |
  |  _____  |
  | /      \ |
  |/_______\|
""")

print("NordVPN Account Checker")
print("-----------------------")

username = input("Enter username: ")
password = input("Enter password: ")
proxy = input("Enter proxy (e.g., 123.456.789.012:8080): ")

import requests

url = "https://nordvpn.com/wp-admin/admin-ajax.php?action=login"
post_fields = {"username": username, "password": password}

proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

try:
    response = requests.post(url, data=post_fields, proxies=proxies)
    if "success" in response.text:
        print("Account is valid!")
    else:
        print("Account is invalid.")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
