import pymem, pymem.process, re, os, ctypes, logging, json, keyboard
from requests import get
from colorama import init, Fore

# Initialize colorama for colored console output
init(autoreset=True)

class Logger:
    """Handles logging setup."""
    LOG_DIRECTORY = os.path.expandvars(r'%LOCALAPPDATA%\Requests\ItsJesewe\csgo\logs')
    LOG_FILE = os.path.join(LOG_DIRECTORY, 'application.log')

    @staticmethod
    def setup_logging():
        os.makedirs(Logger.LOG_DIRECTORY, exist_ok=True)
        with open(Logger.LOG_FILE, 'w') as f:
            pass

        logging.basicConfig(
            level=logging.INFO,
            format='[%(levelname)s]: %(message)s',
            handlers=[logging.FileHandler(Logger.LOG_FILE), logging.StreamHandler()]
        )

class ConfigManager:
    """Handles configuration management."""
    CONFIG_DIRECTORY = os.path.expandvars(r'%LOCALAPPDATA%\Requests\ItsJesewe\csgo')
    CONFIG_FILE = os.path.join(CONFIG_DIRECTORY, 'config.json')
    DEFAULT_CONFIG = {
        "WallHack": "f4",
        "RadarHack": "f5",
        "MoneyReveal": "f6",
        "Exit": "f10"
    }

    @staticmethod
    def load_config():
        os.makedirs(ConfigManager.CONFIG_DIRECTORY, exist_ok=True)
        if not os.path.exists(ConfigManager.CONFIG_FILE):
            ConfigManager.save_config(ConfigManager.DEFAULT_CONFIG)
        try:
            with open(ConfigManager.CONFIG_FILE, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            logging.error("Failed to load configuration. Using defaults.")
            return ConfigManager.DEFAULT_CONFIG

    @staticmethod
    def save_config(config):
        with open(ConfigManager.CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)

class Utility:
    """Utility functions."""
    @staticmethod
    def set_console_title(title):
        ctypes.windll.kernel32.SetConsoleTitleW(title)

class Cheat:
    """Handles cheat functionalities."""

    VERSION="Release-1.5.4"

    def __init__(self):
        self.config = ConfigManager.load_config()
        self.wallhack_status = False
        self.radarhack_status = False
        self.moneyreveal_status = False

    def wallhack(self):
        """Toggle WallHack."""
        self._toggle_feature(
            feature_name="WallHack",
            status_attr="wallhack_status",
            pattern=rb'\x33\xC0\x83\xFA.\xB9\x20'
        )

    def radarhack(self):
        """Toggle RadarHack."""
        self._toggle_feature(
            feature_name="RadarHack",
            status_attr="radarhack_status",
            pattern=rb'\x74\x15\x8B\x47\x08\x8D\x4F\x08'
        )

    def moneyreveal(self):
        """Toggle MoneyReveal."""
        self._toggle_feature(
            feature_name="MoneyReveal",
            status_attr="moneyreveal_status",
            pattern=rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF'
        )

    def _toggle_feature(self, feature_name, status_attr, pattern):
        try:
            pm = pymem.Pymem('csgo.exe')
            client = pymem.process.module_from_name(pm.process_handle, 'client.dll')
            client_module = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
            address = client.lpBaseOfDll + re.search(pattern, client_module).start()
            pm.write_uchar(address, 1 if not getattr(self, status_attr) else 0)
            pm.close_process()
            setattr(self, status_attr, not getattr(self, status_attr))
            logging.info(Fore.LIGHTMAGENTA_EX + f"{feature_name} {'ON' if getattr(self, status_attr) else 'OFF'}")
        except Exception as e:
            logging.error(Fore.LIGHTRED_EX + f"Error toggling {feature_name}: {e}")

    def start(self):
        Utility.set_console_title(f"CS:GO Memory Cheat | {self.VERSION}")
        logging.info(Fore.LIGHTCYAN_EX + f"Welcome to CS:GO Memory Cheat {self.VERSION}")

        keyboard.add_hotkey(cheat.config["WallHack"], cheat.wallhack)
        keyboard.add_hotkey(cheat.config["RadarHack"], cheat.radarhack)
        keyboard.add_hotkey(cheat.config["MoneyReveal"], cheat.moneyreveal)
        keyboard.add_hotkey(cheat.config["Exit"], cheat.exit)

        keyboard.wait()

    def exit(self):
        """Exit program."""
        logging.info("Exiting program.")
        os.abort()

if __name__ == '__main__':
    Logger.setup_logging()
    cheat = Cheat()
    cheat.start()