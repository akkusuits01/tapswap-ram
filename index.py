import requests
import requests
import json
import time
from colorama import init, Fore, Style
import sys
import os
import random
init(autoreset=True)

from keep_alive import keep_alive
keep_alive()

with open('data.txt', 'r') as file:
    doc_data = file.readlines()
#with open('auth.txt', 'r') as file1:
#    auth_data = file1.readlines()

        
def get_access_token(tao_data_dc):
    chr_value, query_id, cacheId = tao_data_dc.split('|')
    
    url = "https://api.tapswap.ai/api/account/login"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en,en-IN;q=0.9,en-US;q=0.8",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Origin": "https://app.tapswap.club",
        "Referer": "https://app.tapswap.club/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Samsung S21 Build/JMB1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.2478.371 Mobile Safari/537.36",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "x-app": "tapswap_server",
        "x-cv": "632",
#        "x-bot": "no",

        "Cache-Id": cacheId, #"s8ZHx0EJ",
        "x-touch": "1",
        "X-Requested-With": "org.telegram.messenger",
        "Accept-Encoding": ""
    }
    
    payload = {
        "init_data": query_id,
        "referrer": "",
        "bot_key": "app_bot_0",
        "chr" : int(chr_value)
    }
  #  print(headers)
   # print(json.dumps(payload))
  #  response1 = requests.post(url, headers=headers, data=json.dumps(payload1))
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response)
    if response.status_code == 201:
        data = response.json()
        if 'access_token' in data:
            access_token = data['access_token']
            name = data['player']['full_name']
            coin = data['player']['shares']
            energy = data['player']['energy']
            level_energy = data['player']['energy_level']
            level_charge = data['player']['charge_level']
            level_tap = data['player']['tap_level']
            boosts = data['player']['boost']
            energy_boost = next((b for b in boosts if b["type"] == "energy"), None)
            turbo_boost = next((b for b in boosts if b["type"] == "turbo"), None)
            boost_ready = turbo_boost['cnt']
            energy_ready = energy_boost['cnt']

            print(f"{Fore.BLUE+Style.BRIGHT}\n==========================\n")  
            print(f"{Fore.GREEN+Style.BRIGHT}[*] Name: {name}")    
            print(f"{Fore.YELLOW+Style.BRIGHT}[*] Balance: {coin}")
            print(f"{Fore.YELLOW+Style.BRIGHT}[*] Energy: {energy}")
            print(f"{Fore.CYAN+Style.BRIGHT}[*] Level tap/energy/recharge: {level_tap}/{level_energy}/{level_charge}")
            print(f"{Fore.MAGENTA+Style.BRIGHT}[*] Boost: Acceleration {turbo_boost['cnt']} | Full Energy : {energy_boost['cnt']}")

            return access_token, energy, boost_ready, energy_ready
        else:
            print("Access Token no reply")
            return None, None, None, None
    elif response.status_code == 408:
        print("Request timeout")
    else:
        print(response.json())
        print(f"Unable to get access token and status code: {response.status_code}")
    
    return None, None, None, None
turbo_activated = False    
def apply_turbo_boost(access_token, tao_data_dc):
    chr_value, query_id, cacheId = tao_data_dc.split('|')
    
    global turbo_activated
    url = "https://api.tapswap.ai/api/player/apply_boost"
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "*/*",
            "Accept-Language": "en,en-IN;q=0.9,en-US;q=0.8",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; Samsung S21 Build/JMB1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.2478.371 Mobile Safari/537.36",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "x-app": "tapswap_server",
            "x-cv": "632",
       #     "x-bot": "no",
            
       #     Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjUxMTA0MDQyMDcsImlhdCI6MTcyMDUwMjk3MywiZXhwIjoxNzIwNTA2NTczfQ.luVwUB5bEgAw4Vhhm5YHHaQYJl7R9h3hWBruAjRIo8o
            "Cache-Id": cacheId, #"s8ZHx0EJ",
            "x-touch": "1",
       #     "Content-Id": "5110325848",
            "X-Requested-With": "org.telegram.messenger",
            "Accept-Encoding": ""
        }
    payload = {"type": "turbo"}
    if turbo_activated == False:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:

            print(f"\r{Fore.GREEN+Style.BRIGHT}Turbo is activated successfully", flush=True)
            turbo_activated = True
            return True

        else:
            print(f"{Fore.RED+Style.BRIGHT}Unable to activate turbo, status code: {response.json()}")
            return False
    else:
        print(f"\r{Fore.GREEN+Style.BRIGHT}Turbo activated")
        return True


not_enough_balance = {
    "tap": False,
    "energy": False,
    "charge": False
}
def upgrade_level(headers, upgrade_type):

    global not_enough_balance
    if not_enough_balance[upgrade_type]:
        return False
    for i in range(5):
        print(f"\r{Fore.WHITE+Style.BRIGHT}To be upgrading {upgrade_type} {'.' * (i % 4)}", end='', flush=True)
    url = "https://api.tapswap.ai/api/player/upgrade"
    payload = {"type": upgrade_type}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"\r{Fore.GREEN+Style.BRIGHT}Upgrade {upgrade_type} success", flush=True)
        return True
    else:
        response_json = response.json()
        if 'message' in response_json and 'not_enough_shares' in response_json['message']:
            print(f"\r{Fore.RED+Style.BRIGHT}Not enough balance to upgrade {upgrade_type}", flush=True)
            not_enough_balance[upgrade_type] = True
            return False
        else:
            print(f"\r{Fore.RED+Style.BRIGHT}Error while upgrading {upgrade_type}: {response_json['message']}", flush=True)
        return False



use_booster = 'y' # input("Use automatic booster? (Y/N): ").strip().lower()
if use_booster in ['y', 'n', '']:
    use_booster = use_booster or 'n'
else:
    print("Must be 'Y' or 'N'")
    sys.exit()


use_upgrade = 'y' # input("Automatic upgrade? (Y/N): ").strip().lower()
if use_upgrade in ['y', 'n', '']:
    use_upgrade = use_upgrade or 'n'
else:
    print("Must be 'Y' or 'N'")
    sys.exit()

def submit_taps(access_token, energy, boost_ready, energy_ready, content_id, time_stamp, tao_data_dc):
    global turbo_activated
    turbo_not_ready_notified = False 
    chr_value, query_id, cacheId = tao_data_dc.split('|')
    
    while True:
        url = "https://api.tapswap.ai/api/player/submit_taps"

        if use_booster == 'y' and boost_ready > 0:
            if not turbo_activated:
                print(f"\r{Fore.WHITE+Style.BRIGHT}Turbo ready, buy turbo", end='', flush=True)
                apply_turbo_boost(access_token, tao_data_dc)
            else:
                print(f"\r{Fore.WHITE+Style.BRIGHT}Turbo activated", end='', flush=True)
        elif use_booster == 'y' and boost_ready == 0 and not turbo_not_ready_notified:
            turbo_not_ready_notified = True

        if energy < 50:
            print(f"\r{Fore.RED+Style.BRIGHT}Low energy", end='', flush=True)
            if use_booster == 'y' and energy_ready > 0:
                print(f"\r{Fore.WHITE+Style.BRIGHT}Ready energy, buy energy", end='', flush=True)
                if apply_energy_boost(access_token):
                    energy = 300  
                    continue  
                else:
                    print(f"\r{Fore.RED+Style.BRIGHT}Cannot buy energy, transfer accounts", end='', flush=True)
                    return
            else:
                time.sleep(3)
                print(f"\r{Fore.RED+Style.BRIGHT}Move to the next account", end='', flush=True)
                return
        else:
            print(f"\r{Fore.WHITE+Style.BRIGHT}Start tapping", end='', flush=True)

        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {access_token}",
            "Connection": "keep-alive",
            "Content-Id": content_id,
            "Content-Type": "application/json",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-bot": "no",
            "x-cv": "632",
            "Cache-Id": cacheId, #"s8ZHx0EJ",
            "x-touch": "1",
            "X-Requested-With": "org.telegram.messenger",
            "Accept-Encoding": ""
        }

        total_taps = random.randint(100000, 1000000) if turbo_activated else random.randint(50, 250)
        payload = {"taps": total_taps, "time": int(time_stamp)}

        if turbo_activated:
            for _ in range(22):
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 201:
                    response_data = response.json()
                    energy_dc = response_data.get("player", {}).get("energy", 0)
                    coin_balance = response_data.get("player", {}).get("shares", 0)
                    print(f"\r{Fore.GREEN+Style.BRIGHT}Tap successfully: balance {coin_balance} / remaining energy {energy_dc}", flush=True)
                else:
                    print(f"\r{Fore.RED+Style.BRIGHT}Unable to tap, status code: {response.status_code}")
            turbo_activated = False
        else:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                response_data = response.json()
                energy_dc = response_data.get("player", {}).get("energy", 0)
                coin_balance = response_data.get("player", {}).get("shares", 0)
                print(f"\r{Fore.GREEN+Style.BRIGHT}Tap successfully: balance {coin_balance} / remaining energy {energy_dc}", flush=True)

                if use_upgrade == 'y':
                    if not not_enough_balance["tap"]:
                        upgrade_level(headers, "tap")
                    if not not_enough_balance["energy"]:
                        upgrade_level(headers, "energy")
                    if not not_enough_balance["charge"]:
                        upgrade_level(headers, "charge")
                energy = energy_dc  
                if energy < 50:
                    if use_booster == 'y' and energy_ready > 0:
                        print(f"\r{Fore.WHITE+Style.BRIGHT} Ready energy, buy energy", end='', flush=True)
                        if apply_energy_boost(access_token):
                            energy = 300 
                        else:
                            print(f"\r{Fore.RED+Style.BRIGHT}Cannot buy energy, transfer accounts", end='', flush=True)
                            return
                    else:
                        print(f"\r{Fore.RED+Style.BRIGHT}Low energy, checking account\n", end='', flush=True)
                        return
            else:
                print(f"\n\r{Fore.RED+Style.BRIGHT}Unable to tap, status code: {response.status_code}")
                print(response.text)

def clear_console():

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
def apply_energy_boost(access_token):
    chr_value, query_id, cacheId = tao_data_dc.split('|')
    
    url = "https://api.tapswap.ai/api/player/apply_boost"
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Origin": "https://app.tapswap.club",
            "Referer": "https://app.tapswap.club/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "x-app": "tapswap_server",
            "x-cv": "632",
            "Cache-Id": cacheId, #"s8ZHx0EJ",
            "x-touch": "1",
            "X-Requested-With": "org.telegram.messenger",
            "Accept-Encoding": ""
        }

    payload = {"type": "energy"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"\r{Fore.GREEN+Style.BRIGHT}Purchased energy", flush=True)
        submit_taps(access_token, 100, 0, 0, content_id, time_stamp, tao_data_dc)  
        return True

    else:
        print(f"{Fore.RED+Style.BRIGHT}Cannot buy energy, status code: {response.status_code}")
        return False

while True:
    for xuly_data_dc in doc_data:
        parts = xuly_data_dc.strip().split('|')
        if len(parts) != 5:
            print(f"Invalid data: {xuly_data_dc}")
            continue
        content_id = parts[0]
        time_stamp = parts[1]
        chr_value = parts[2]
        query_id = parts[3]
        cacheId= parts[4]
        tao_data_dc = chr_value + '|' + query_id+'|'+cacheId 
        access_token, energy, boost_ready, energy_ready = get_access_token(tao_data_dc.strip())
        if access_token:
            submit_taps(access_token, energy, boost_ready, energy_ready, content_id, time_stamp, tao_data_dc.strip())

    print(f"\n\n{Fore.CYAN+Style.BRIGHT}==============All accounts have been processed=================\n")
    for giay in range(1800, 0, -1):
        print(f"\r Start again in {giay} seconds...", end='')
        time.sleep(1)
    clear_console()