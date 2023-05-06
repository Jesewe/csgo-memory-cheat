# importing modules
import pymem, re, logging, keyboard, os, datetime, configparser, ctypes
import pymem.process
from colorama import Fore, init
init()

# status
statusWH = False
statusRH = False
statusMR = False
# config
config = configparser.ConfigParser()
# logging
logging.basicConfig(
    filename='logs.txt', 
    level=logging.DEBUG, 
    format='%(asctime)s %(message)s', 
    datefmt='%Y-%m-%d [%H:%M:%S]')
# file config.ini
try:
    config.read("config.ini")
    key1 = config["DEFAULT"]["WallHack"]
    key2 = config["DEFAULT"]["RadarHack"]
    key3 = config["DEFAULT"]["MoneyReveal"]
    key4 = config["DEFAULT"]["Exit"]
    logging.debug('Configuration file found')
except:
    logging.debug('The configuration file has been created')
    config["DEFAULT"] = {"WallHack": "f4", "RadarHack": "f5", "MoneyReveal": "f6", "Exit": "f10"}
    with open("config.ini", "w") as config_file:
        config.write(config_file)
    key1 = "f4"
    key2 = "f5"
    key3 = "f6"
    key4 = "f10"
# time display on the screen
def time():
    return datetime.datetime.now().strftime('[%H:%M:%S]')
# exiting the program
def exit():
    logging.debug("I'm exiting the program")
    print(Fore.YELLOW + time(), Fore.CYAN + 'Exiting the program...')
    os.abort()
# function wallhack
def wallhack():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'\x33\xC0\x83\xFA.\xB9\x20',clientModule).start() + 4
        pm.write_uchar(address, 2 if pm.read_uchar(address) == 1 else 1)
        pm.close_process()
    except Exception:
        logging.error('[WallHack] ERROR: csgo.exe process is not running!')
        print(Fore.YELLOW + time(), Fore.RED + '[WallHack] ERROR: csgo.exe process is not running!')
    else:
        global statusWH
        statusWH = not statusWH
        logging.debug("WallHack is ON" if statusWH else "WallHack is OFF")
        print(Fore.YELLOW + time(), Fore.GREEN + "WallHack is ON" if statusWH else Fore.RED + "WallHack is OFF")
# function radarhack
def radarhack():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'\x74\x15\x8B\x47\x08\x8D\x4F\x08',clientModule).start() - 1
        pm.write_uchar(address, 0 if pm.read_uchar(address) != 0 else 2)
        pm.close_process()
    except Exception:
        logging.error('[RadarHack] ERROR: csgo.exe process is not running!')
        print(Fore.YELLOW + time(), Fore.RED + '[RadarHack] ERROR: csgo.exe process is not running!')
    else:
        global statusRH
        statusRH = not statusRH
        logging.debug("RadarHack is ON" if statusRH else "RadarHack is OFF")
        print(Fore.YELLOW + time(), Fore.GREEN + "RadarHack is ON" if statusRH else Fore.RED + "RadarHack is OFF")
# function moneyreveal
def moneyreveal():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF',clientModule).start()
        pm.write_uchar(address, 0xEB if pm.read_uchar(address) == 0x75 else 0x75)
        pm.close_process()
    except Exception:
        logging.error('[MoneyReveal] ERROR: csgo.exe process is not running!')
        print(Fore.YELLOW + time(), Fore.RED + '[MoneyReveal] ERROR: csgo.exe process is not running!')
    else:
        global statusMR
        statusMR = not statusMR
        logging.debug("MoneyReveal is ON" if statusMR else "MoneyReveal is OFF")
        print(Fore.YELLOW + time(), Fore.GREEN + "MoneyReveal is ON" if statusMR else Fore.RED + "MoneyReveal is OFF")

banner='''
_  _ ____ _  _ ____ ____ _   _    ____ _  _ ____ ____ ___
|\/| |___ |\/| |  | |__/  \_/     |    |__| |___ |__|  |
|  | |___ |  | |__| |  \   |      |___ |  | |___ |  |  |

            MADE BY JESEWE      Version: 1.3.0

You can change the configuration file and set any hotkeys for each function, 
if there is no configuration file, the program will easily create it!
'''
# main
if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleW('Memory Cheat 1.3.0')
    print(Fore.YELLOW + banner + Fore.GREEN + f'\n[{key1}] - WallHack Console\n[{key2}] - RadarHack Console\n[{key3}] - MoneyReveal\n[{key4}] - Exiting the program\n')
    keyboard.add_hotkey(key1, wallhack)
    keyboard.add_hotkey(key2, radarhack)
    keyboard.add_hotkey(key3, moneyreveal)
    keyboard.add_hotkey(key4, exit)
    keyboard.wait()