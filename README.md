# Simple Calculator

[![Python](https://img.shields.io/badge/python-3-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational?logo=python&logoColor=white)](https://docs.python.org/3/library/tkinter.html)
[![Standard library](https://img.shields.io/badge/deps-stdlib%20only-success)](#how-to-install--run)
[![No pip](https://img.shields.io/badge/pip-not%20required-lightgrey)](#how-to-install--run)
[![Linux Mint](https://img.shields.io/badge/Linux%20Mint-22.2-green?logo=linuxmint&logoColor=white)](https://linuxmint.com/)
[![Platform](https://img.shields.io/badge/platform-Linux-orange?logo=linux&logoColor=white)](#how-to-install--run)
[![Desktop](https://img.shields.io/badge/type-desktop%20app-blueviolet)](#how-to-install--run)
[![.desktop launcher](https://img.shields.io/badge/launcher-.desktop-critical)](#how-to-install--run)
[![Memory slots](https://img.shields.io/badge/memory-2%20slots%20(M1%20%2B%20M2)-3a7bd5)](#memory-slots-m1-and-m2)
[![Dark UI](https://img.shields.io/badge/theme-dark-2d2d2d)](#simple-calculator)
[![Size](https://img.shields.io/badge/window-400×580-inactive)](#simple-calculator)
[![Font](https://img.shields.io/badge/font-Ubuntu-e95420)](https://design.ubuntu.com/font)
[![Display font](https://img.shields.io/badge/display%20font-DS--Digital%20(optional)-9c27b0)](#optional-ds-digital-font)
[![Language](https://img.shields.io/badge/UI-EN%20%2B%20BG-yellow)](#simple-calculator)
[![Forever Free](https://img.shields.io/badge/license-Forever%20Free-brightgreen)](#license)
[![Use](https://img.shields.io/badge/use-private%20%7C%20public%20%7C%20business-green)](#license)
[![Modify](https://img.shields.io/badge/modify-yes-success)](#license)
[![Issues](https://img.shields.io/badge/contact-good.vibes.github%40gmail.com-red)](#license)

A retro-styled desktop calculator (up to 14 digits) for **Linux Mint 22.2**, built entirely with Python's standard library (Tkinter — no `pip install` needed). It features a two-tier display (full expression on top, current value below), two independent memory slots (M1 / M2), thousands separators, and a warm 1962-inspired color palette.

![Calculator 1962 screenshot](calculator%201962.png)

## Features

- **Two-line display**
  - Top line: the full running expression (smaller font)
  - Bottom line: the current number / result (large font, mint-green digits on a dark screen)
- **Thousands separators**, grouped every 3 digits from the right
- **Active operator highlight** — the last pressed operator (`+ − × ÷ =`) glows brighter until another operator from the same group or `C` is pressed
- **Quick self-operations** — pressing `+` or `×` **twice in a row** instantly doubles or squares the current value (e.g. `5 + +` → `10`, `5 × ×` → `25`)
- Square root (`√`), percentage (`%`), sign toggle (`±`), backspace (`⌫`), and clear (`C`)
- Automatic `Error` handling for invalid operations (e.g. division by zero, square root of a negative number)
- Scientific notation fallback for very large or very small results
- Bilingual interface labels (Bulgarian window title / comments, English translations included)


## Repeated `=` Operation (New Features)

This additional mode can be used by accountants or engineers for cases where a single number needs to be repeatedly added to or multiplied by other numbers.
After a normal calculation is completed with `=`, **the calculator remembers the first operand and the operator**.
When a new number is entered and `=` is pressed again, that new number becomes the second operand while the original first operand remains unchanged.

**Example (Addition):**
Instead of writing:

* `2563+163=`
* `2563+176=`
* `2563+419=`
* `2563+9919=`
* 
You can simply enter `2563+163=` first, and then continue with:

* `176=`
* `419=`
* `9919=`
  
**Example (Multiplication):**
Instead of writing:

* `1316*14=`
* `1316*76=`
* `1316*17=`
* `1316*77=`
* 
You can enter `116*14=` first, and then continue with:

* `76=`
* `17=`
* `77=`
* 
This allows the following sequence:

`first operand` `operator` `second operand` `=` → result  
`new number` `=` → first operand `operator` new number → result  
`another number` `=` → first operand `operator` another number → result

The repeated `=` mode works with all four basic operators.

### Addition `+`

1. `5 + 5 =` → `10`; then `10 =` → `15`; then `15 =` → `20`;
2. `6 + 6 =` → `12`; then `10 =` → `16`; then `15 =` → `21`;

### Multiplication `×`

1. `2 × 3 =` → `6`;   then `4 =` → `8`;  then `5 =` → `10`
2. `3 × 4 =` → `12`;  then `5 =` → `15`; then `6 =` → `18`

### Subtraction `−`

1. `20 − 2 =` → `18`; then `3 =` → `17`; then `6 =` → `14`
2. `18 − 4 =` → `14`; then `6 =` → `12`; then `8 =` → `10`

### Division `÷`

1. `20 ÷ 2 =` → `10`; then `4 =` → `5`; then `5 =` → `4`
2. `18 ÷ 3 =` → `6`;  then `6 =` → `3`; then `2 =` → `9`


### Example matching the calculator's intended workflow

`2 + 2 =` → `4`  
`8 =` → `10`  
`26 =` → `28`

The same principle applies to `×`, `−`, and `÷`.

- **Pressing `C` clears the current calculation and also resets this repeated `=` mode, so the calculator starts fresh**

## Memory Slots (M1 and M2)

The calculator has two fully independent memory registers:

- **`+M1` / `+M2`** — add the current value to the corresponding memory
- **`RM1` / `RM2` — single click** — recalls the stored memory value into the expression
- **`RM1` / `RM2` — double click** — clears (resets) that specific memory back to zero
- Memory buttons change color and display the stored value as soon as a memory becomes non-zero, so you can always see at a glance what's stored in M1 and M2

![Calculator 1962 memory slots screenshot](calculator%201962%20%28Memory%29.png)

## How to Install / Run

### Requirements

- Linux Mint 22.2 (or any modern Linux distribution)
- Python 3
- Tkinter (usually preinstalled; if missing: `sudo apt install python3-tk`)

No third-party packages and no `pip install` are required — everything runs on the Python standard library.

Both files below (`calculator.py` and `Calculator.desktop`) are included in this repository.

### Steps

1. Download `calculator.py` and place it directly in your **home directory** (`~/calculator.py`).
2. Make the script executable:
   - Right-click the file → **Properties** → **Permissions** tab → check **"Allow executing file as program"**
3. Download `Calculator.desktop` and place it directly in your **desktop directory**.
4. Right-click on the `Calculator.desktop` file → **Properties → Permissions** and check all **Execute** boxes, then double-click it to launch the calculator like any other app.

That's it — now you can use the program.

## Optional: DS-Digital Font

The display uses the **DS-Digital** font for that authentic digital-clock look. It's optional — if the font isn't installed, the calculator automatically falls back to Courier, and everything still works exactly the same.

To install it:

1. Download `font ds_digital.zip` from this repository and extract it (it contains the `.ttf` font files).
2. Double-click each `.ttf` file to open it in the **Font Viewer**, then click **Install**.
   - Alternatively, copy the `.ttf` files into `~/.local/share/fonts/` (create the folder if it doesn't exist), then run `fc-cache -f -v` in a terminal to refresh the font cache.
3. Restart the calculator so it picks up the newly installed font.

## Color Palette

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

## License

**Forever Free.** This project is free to use, copy, and modify for private, public, or business purposes, with no fees, restrictions, or warranty.


Questions, bugs, or suggestions: **good.vibes.github@gmail.com**
