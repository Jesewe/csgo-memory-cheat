import pymem, re, keyboard, datetime, configparser, ctypes, requests, time, random, os
import pymem.process
from colorama import Fore, init
init()

statusWH = False
statusRH = False
statusMR = False
config = configparser.ConfigParser()

try:
    config.read("config.ini")
    key1 = config["DEFAULT"]["WallHack"]
    key2 = config["DEFAULT"]["RadarHack"]
    key3 = config["DEFAULT"]["MoneyReveal"]
    key4 = config["DEFAULT"]["Exit"]
except:
    config["DEFAULT"] = {"WallHack": "f4", "RadarHack": "f5", "MoneyReveal": "f6", "Exit": "f10"}
    with open("config.ini", "w") as config_file:
        config.write(config_file)
    key1 = "f4"
    key2 = "f5"
    key3 = "f6"
    key4 = "f10"

def time():
    return datetime.datetime.now().strftime('[%H:%M:%S]')

def exit_program():
    print(Fore.RED + "Exit...")
    os.abort()

def check_for_updates(version):
    server_url = 'https://raw.githubusercontent.com/Jesewe/csgo-memory-cheat/main/version.json'
    try:
        response = requests.get(server_url)
        latest_version = response.text.strip()
        if latest_version == version:
            return "You already have the latest version of the project installed."
        else:
            return Fore.GREEN + f"A new version of the project is available: {latest_version}. Please update."

    except requests.RequestException as e:
        return Fore.RED + f"Error checking for updates: {str(e)}"

def wallhack():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'\x33\xC0\x83\xFA.\xB9\x20',clientModule).start() + 4
        pm.write_uchar(address, 2 if pm.read_uchar(address) == 1 else 1)
        pm.close_process()
    except Exception:
        print(Fore.YELLOW + time(), Fore.RED + '[WallHack] ERROR: csgo.exe process is not running!')
    else:
        global statusWH
        statusWH = not statusWH
        print(Fore.YELLOW + time(), Fore.GREEN + "WallHack is ON" if statusWH else Fore.RED + "WallHack is OFF")

def radarhack():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'\x74\x15\x8B\x47\x08\x8D\x4F\x08',clientModule).start() - 1
        pm.write_uchar(address, 0 if pm.read_uchar(address) != 0 else 2)
        pm.close_process()
    except Exception:
        print(Fore.YELLOW + time(), Fore.RED + '[RadarHack] ERROR: csgo.exe process is not running!')
    else:
        global statusRH
        statusRH = not statusRH
        print(Fore.YELLOW + time(), Fore.GREEN + "RadarHack is ON" if statusRH else Fore.RED + "RadarHack is OFF")

def moneyreveal():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF',clientModule).start()
        pm.write_uchar(address, 0xEB if pm.read_uchar(address) == 0x75 else 0x75)
        pm.close_process()
    except Exception:
        print(Fore.YELLOW + time(), Fore.RED + '[MoneyReveal] ERROR: csgo.exe process is not running!')
    else:
        global statusMR
        statusMR = not statusMR
        print(Fore.YELLOW + time(), Fore.GREEN + "MoneyReveal is ON" if statusMR else Fore.RED + "MoneyReveal is OFF")

version='1.5.2'
fake_programs = ["WinBooster", "GameBooster", "DataAnalyzer", "CodeOptimizer", "TaskManagerPro", "SystemGuardian"]
random_program = random.choice(fake_programs)
banner=f'''
\t\t\t  {random_program}

                Made by Jesewe      Version: {version}
'''

if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW(f'{random_program} v{version}')
    print(Fore.YELLOW + banner)
    print(check_for_updates(version))
    print(Fore.LIGHTGREEN_EX + f'\n[{key1}] - WallHack\n[{key2}] - RadarHack\n[{key3}] - MoneyReveal\n[{key4}] - Exit\n')
    keyboard.add_hotkey(key1, wallhack)
    keyboard.add_hotkey(key2, radarhack)
    keyboard.add_hotkey(key3, moneyreveal)
    keyboard.add_hotkey(key4, exit_program)
    keyboard.wait()