import pymem, re
import pymem.process
import keyboard
import os, datetime

status = False

def time():
    return datetime.datetime.now().strftime('[%H:%M:%S]')

def exit():
    os.abort()

def wallhack():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,
                                                'client.dll')

        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'\x33\xC0\x83\xFA.\xB9\x20',
                                                 clientModule).start() + 4

        pm.write_uchar(address, 2 if pm.read_uchar(address) == 1 else 1)
        pm.close_process()
    except Exception:
        print(time(), '[WallHack] ERROR: csgo.exe process is not running!')
    else:
        global status
        status = not status
        print(time(), "WallHack is ON" if status else "WallHack is OFF")

def radarhack():
    try:
        pm = pymem.Pymem('csgo.exe')
        client = pymem.process.module_from_name(pm.process_handle,
                                        'client.dll')

        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        address = client.lpBaseOfDll + re.search(rb'\x74\x15\x8B\x47\x08\x8D\x4F\x08',
                                         clientModule).start() - 1

        pm.write_uchar(address, 0 if pm.read_uchar(address) != 0 else 2)
        pm.close_process()
    except Exception:
        print(time(), '[RadarHack] ERROR: csgo.exe process is not running!')
    else:
        global status
        status = not status
        print(time(), "RadarHack is ON" if status else "RadarHack is OFF")

if __name__ == '__main__':
    print('F4 - R_DrawOtherModels 2\nF5 - RadarHack Console\nF10 - Exit')
    keyboard.add_hotkey('F4', wallhack)
    keyboard.add_hotkey('F5', radarhack)
    keyboard.add_hotkey('F10', exit)
    keyboard.wait()