#  made by nostorian, discord: @nostorian

import tls_client
import logging
import time
import json, os
from pystyle import *
from colorama import Fore, init

# Initialize colorama
init(autoreset=True, convert=True)

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt, symbol, symbol_color):
        self.symbol = symbol
        self.symbol_color = symbol_color
        super().__init__(fmt, datefmt)

    def format(self, record):
        # Inject the colored symbol into the log record
        record.symbol = f'{self.symbol_color}{self.symbol}{Fore.RESET}'
        record.msg = f'{Fore.MAGENTA}{record.msg}{Fore.RESET}'
        return super().format(record)
    
    @classmethod
    def setup_logger(cls, name, symbol, symbol_color):
        log_format = (
            f'{Fore.LIGHTBLACK_EX}[{Fore.RESET}{Fore.LIGHTBLUE_EX} %(asctime)s {Fore.RESET}{Fore.LIGHTBLACK_EX}]'
            f'{Fore.RESET} ( %(symbol)s ) | %(message)s'
        )
        datefmt = '%H:%M:%S'
        formatter = cls(log_format, datefmt, symbol, symbol_color)

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.handlers = []
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

class HamsterKombatClient:
    def __init__(self, token, base_url="https://api.hamsterkombat.io", cooldown_time=3):
        self.base_url = base_url
        self.upgrade_list = []
        self.session = tls_client.Session(client_identifier="okhttp4_android_11", random_tls_extension_order=True)
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {token}",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "api.hamsterkombat.io",
            "Origin": "https://hamsterkombat.io",
            "Referer": "https://hamsterkombat.io/clicker/mine",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-S908E Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.120 Safari/537.36",
            "X-Requested-With": "org.telegram.messenger.web"
        }
        self.cooldown_time = cooldown_time

        # Loggers setup
        self.logger_success = CustomFormatter.setup_logger('success', '+', Fore.GREEN)
        self.logger_error = CustomFormatter.setup_logger('error', '-', Fore.RED)
        self.logger_info = CustomFormatter.setup_logger('info', '>', Fore.CYAN)

    def _clear(self):
        system = os.name
        if system == 'nt':
            os.system('cls')
        elif system == 'posix':
            os.system('clear')
        else:
            print('\n'*120)
        return

    def fetch_upgrades(self):
        url = f"{self.base_url}/clicker/upgrades-for-buy"
        data = {}
        response = self.session.post(url, headers=self.headers, json=data)
        if response.status_code not in [200, 201]:
            self.logger_error.error(f"Failed to get upgrades: {response.status_code}")
            return []
        return response.json().get("upgradesForBuy", [])

    def display_upgrades(self):
        upgrades = self.fetch_upgrades()
        self.upgrade_list = []
        for upgrade in upgrades:
            upgrade_id = upgrade.get("id")
            name = upgrade.get("name")
            section = upgrade.get("section")
            price = upgrade.get("price")
            profit_per_hour = upgrade.get("profitPerHour")
            self.upgrade_list.append({"id": upgrade_id, "name": name, "section": section, "price": price, "profit_per_hour": profit_per_hour})
        
        sections = ["PR&Team", "Markets", "Legal", "Specials"]
        print(f"{Fore.LIGHTCYAN_EX}Available Upgrades {Fore.RESET}{Fore.LIGHTBLACK_EX}({len(self.upgrade_list)}){Fore.RESET}")
        print("-" * 50)
        
        for section in sections:
            section_list = [upgrade for upgrade in self.upgrade_list if upgrade["section"] == section]
            if section_list:
                print(f"{Fore.LIGHTCYAN_EX}{section}{Fore.RESET}")
                print("-" * 50)
                for upgrade in section_list:
                    print(f"{Fore.LIGHTBLACK_EX}ID: {Fore.RESET}{upgrade['id']} {Fore.LIGHTBLACK_EX}| Name: {Fore.RESET}{upgrade['name']} {Fore.LIGHTBLACK_EX}| Price: {Fore.RESET}{upgrade['price']} {Fore.LIGHTBLACK_EX}| Profit per hour: {Fore.RESET}{upgrade['profit_per_hour']}")
                print("-" * 50)

    def buy_upgrade(self, upgrade_id):
        url = f"{self.base_url}/clicker/buy-upgrade"
        data = {
            "upgradeId": upgrade_id,
            "timestamp": int(time.time() * 1000),
        }
        response = self.session.post(url, headers=self.headers, json=data)
        return response

    def handle_cooldown(self, cooldown, price):
        if cooldown > 60:
            self.logger_info.info(f"Cooldown: {cooldown // 60}m {cooldown % 60}s for {price}")
        elif cooldown == 0:
            self.logger_info.info(f"Cooldown is 0, defaulting to {self.cooldown_time}s to prevent detection.")
            cooldown = self.cooldown_time
        else:
            self.logger_info.info(f"Cooldown: {cooldown}s for {price}")
        time.sleep(cooldown)

    def check_status(self, resp):
        if resp.status_code == 422:
            self.logger_error.error("Invalid upgrade ID")
            return False
        resp_json = resp.json()
        error_code = resp_json.get("error_code")
        if error_code == "INSUFFICIENT_FUNDS":
            req_data = resp_json["error_message"]
            req_meta = req_data.split(", ")
            req_required = req_meta[1].split(": ")[1]
            req_balance = float(req_meta[0].split("balanceCoins ")[1]).__round__()
            self.logger_error.error(f"Insufficient funds: need {req_required}, have {req_balance}")
            return False
        elif error_code == "UPGRADE_NOT_AVAILABLE":
            msg = resp_json["error_message"]
            if "upgradeId" in json.dumps(resp_json):
                msge = msg.split("upgradeId ")[1]
                self.logger_error.error(f"Unavailable upgrade, complete the condition: {msge}")
            elif "moreReferralsCount" in json.dumps(resp_json):
                msge = msg.split("moreReferralsCount ")[1]
                reference = "people" if int(msge) > 1 else "person"
                self.logger_error.error(f"Refer {msge} more {reference} to unlock this upgrade")
            else:
                self.logger_error.error(f"Unable to buy upgrade: {msg}")
            return False
        else:
            try:
                resp_json["clickerUser"]
            except:
                self.logger_error.error(f"Unknown error: {resp_json}")
                return False
        return True

    def upgrade_repeatedly(self, upgrade_id, times):
        successful_upgrades = 0
        for _ in range(times):
            response = self.buy_upgrade(upgrade_id)
            check = self.check_status(response)
            if not check:
                break

            if response.status_code == 200:
                resp_json = response.json()
                with open("hamster.json", "w") as f:
                    f.write(json.dumps(resp_json, indent=4))
                meta = resp_json.get("upgradesForBuy", [])
                cooldown = 0
                price = "Unknown"
                for i in meta:
                    if i["id"] == upgrade_id:
                        cooldown = i.get("totalCooldownSeconds", 0)
                        price = i.get("price", "Unknown")
                        break
                successful_upgrades += 1
                self.logger_success.info(f"Upgrade successful: {upgrade_id} for {price}")
                self.handle_cooldown(cooldown, price)
            else:
                self.logger_error.error(f"Errored with status code: {response.status_code}")
                self.logger_error.error(response.text)
                break
        self.logger_success.info(f"Upgrades completed successfully: {successful_upgrades}")

    def run(self):
        while True:
            print(Center.XCenter(f"""{Fore.LIGHTCYAN_EX}
┏┓      ┓┏┓     ┓    
┣┫┓┏╋┏┓ ┃┫ ┏┓┏┳┓┣┓┏┓╋
┛┗┗┻┗┗┛ ┛┗┛┗┛┛┗┗┗┛┗┻┗             
{Fore.RESET}"""))
            print("\n")
            print(f"{Fore.CYAN}»{Fore.LIGHTGREEN_EX} Made by nostorian {Fore.RESET}")
            print(f"{Fore.CYAN}»{Fore.LIGHTGREEN_EX} feds.lol/ykreal {Fore.RESET}\n\n")
            print(f"{Fore.LIGHTCYAN_EX}({Fore.RESET}1{Fore.LIGHTCYAN_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Fetch Upgrades{Fore.RESET}")
            print(f"{Fore.LIGHTCYAN_EX}({Fore.RESET}2{Fore.LIGHTCYAN_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Start Upgrades{Fore.RESET}")
            print(f"{Fore.LIGHTCYAN_EX}({Fore.RESET}3{Fore.LIGHTCYAN_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Exit Program{Fore.RESET}")
            choice = input(f"\n{Fore.LIGHTBLACK_EX}➜ {Fore.RESET} {Fore.LIGHTWHITE_EX}Enter choice: {Fore.RESET}").lower()

            if choice == "1":
                self._clear()
                self.display_upgrades()
                input("\nPress Enter to continue...")
                self._clear()
            elif choice == "2":
                upgrade_id = input("Enter upgrade ID to buy: ")
                try:
                    times = int(input("Enter how many times to upgrade: "))
                except:
                    self.logger_error.error("Invalid input.")
                    input("Press Enter to continue...")
                    self._clear()
                    continue
                self.upgrade_repeatedly(upgrade_id, times)
                input("Press Enter to continue...")
                self._clear()
            elif choice == "3":
                self.logger_info.info("Exiting program...")
                input("Press Enter to exit.")
                break
            else:
                self.logger_error.error("Invalid choice.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    token = int(input("Enter your HK Bearer Token: "))
    client = HamsterKombatClient(token)
    client.run()
