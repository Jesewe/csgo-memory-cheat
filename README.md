# CS:GO Memory Cheat

This project is a Python-based memory cheat for the game **Counter-Strike: Global Offensive (CS:GO)**. It provides togglable cheats like WallHack, RadarHack, and MoneyReveal using memory manipulation techniques.

---

## Features

- **WallHack**: See players through walls.
- **RadarHack**: Display all players on the radar.
- **MoneyReveal**: Show the money of all players.
- Configurable hotkeys for toggling cheats and exiting the program.
- Logging for actions and errors.
- Configuration stored in `config.json` for persistent customization.
- Console title updated to reflect the cheat's version.

---

## Requirements

### Python Dependencies:
Install the dependencies using `pip`:
```bash
pip install -r requirements.txt
```

**Dependencies:**
- `pymem`
- `keyboard`
- `requests`
- `colorama`

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Jesewe/csgo-memory-cheat.git
   cd csgo-memory-cheat
   ```

2. Install required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script as Administrator:
   ```bash
   python main.py
   ```

4. Launch CS:GO and use the configured hotkeys to toggle cheats.

---

## Configuration

### Default Hotkeys
The default configuration is saved in the `config.json` file:

```json
{
    "WallHack": "f4",
    "RadarHack": "f5",
    "MoneyReveal": "f6",
    "Exit": "f10"
}
```

You can edit this file to change the hotkeys as needed.

---

## Logging

Logs are stored in:
```
%LOCALAPPDATA%\Requests\ItsJesewe\csgo\logs\application.log
```
This contains all cheat actions and errors for debugging purposes.

---

## Disclaimer

This script is for educational purposes only. Using cheats or hacks in online games is against the terms of service of most games and can result in bans or other penalties. Use this script at your own risk.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
