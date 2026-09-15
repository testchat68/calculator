# Calculator 1962 🧮

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%20Mint%2022.2-87CF3E?logo=linuxmint&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)

A retro-styled desktop calculator for **Linux Mint 22.2**, built with Python and Tkinter. It features a two-tier display (full expression on top, current value below), two independent memory slots (M1 / M2), thousands separators, and a warm 1962-inspired color palette.

![Calculator 1962 screenshot](calculator%201962.png)

## ✨ Features

- **Two-line display**
  - Top line: the full running expression (smaller font)
  - Bottom line: the current number / result (large font, mint-green digits)
- **Thousands separators** grouped every 3 digits from the right
- **Active operator highlight** — the last pressed operator (`+ − × ÷ =`) glows brighter until another operator from the same group or `C` is pressed
- **Two independent memories (M1 and M2)**
  - `+M1` / `+M2` — add the current value to the corresponding memory
  - `RM1` / `RM2` — **single click** recalls the memory value into the expression
  - `RM1` / `RM2` — **double click** clears (resets) that specific memory
  - Memory buttons change color and show the stored value once a memory is non-zero
- **Quick self-operations** — pressing `+` or `×` **twice in a row** immediately squares or doubles the current value (e.g. `5 + +` → `10`, `5 × ×` → `25`)
- Square root (`√`), percentage (`%`), sign toggle (`±`), backspace (`⌫`), and clear (`C`)
- Automatic `Error` handling for invalid operations (e.g. division by zero, square root of a negative number)
- Scientific notation fallback for very large or very small results

## 📦 Requirements

- Linux Mint 22.2 (or any modern Linux distribution)
- Python 3
- Tkinter (usually preinstalled; if not: `sudo apt install python3-tk`)

## 🚀 Installation

1. Download `calculator.py` and place it directly in your **home directory** (`~/calculator.py`).
2. Make the script executable:
   - Right-click the file → **Properties** → **Permissions** tab → check **"Allow executing file as program"**
   - Or from the terminal:
     ```bash
     chmod +x ~/calculator.py
     ```
3. (Optional) Add a desktop shortcut — see below.

## 🖥️ Desktop Shortcut

Create a file named `calculator.desktop` (e.g. on your Desktop or in `~/.local/share/applications/`) with the following content:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Calculator
Name[en]=Calculator
Comment=Прост калкулатор
Comment[en]=Simple Calculator
Exec=sh -c "python3 $HOME/calculator.py"
Icon=accessories-calculator
Terminal=false
Categories=Utility;Calculator;
StartupNotify=true
```

Then make the `.desktop` file executable as well (right-click → Properties → Permissions → "Allow executing file as program", or `chmod +x calculator.desktop`). Double-click it to launch the calculator.

## ▶️ Running from the terminal

```bash
python3 ~/calculator.py
```

## 🎨 Color Palette

| Element | Color |
|---|---|
| Top plate / operators | Pale pink `#EFAED0` |
| Active operator | Bright pink `#FF6EB8` |
| Window / keyboard background | Cream `#F7E8DF` |
| Memory buttons (M1/M2, inactive) | Teal `#00c3d9` |
| M1 active | Dark green `#1B5E20` |
| M2 active | Dark blue `#0D47A1` |
| C / ⌫ / ± / + | Magenta `#c70244` |
| Digits 0–9 and `.` | Light teal `#4EB8B4` |
| √ and % | Salmon `#F98F98` |
| Display background | Near-black `#1e1e1e` |
| Display digits | Mint green `#7fff00` |

## 📄 License

This project is released under the MIT License. Feel free to use, modify, and share it.
