# 🎮 Auto Macro

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> ⚡ A powerful Python macro tool to record, replay, and automate mouse & keyboard actions with spam and hold modes.

---

## ✨ Features

- 🎥 Record **mouse movements, clicks, and keyboard input**
- ▶️ Replay macros in loop (with real timing)
- ⏹ Toggle Play / Stop system
- ⚡ Spam mode with customizable delay
- 🔒 HOLD mode (0ms) for continuous key press
- 🖥 Clean Tkinter GUI interface
- ⌨ Global hotkeys (F6 / F7 / F8)
- 🎮 Lightweight automation tool for productivity or testing

---

## ⌨️ Hotkeys

| Action        | Key |
|--------------|-----|
| 🎥 Record     | F6  |
| ▶️ Play/Stop  | F7  |
| ⚡ Spam       | F8  |

---

## 🚀 Use

### 1. Clone the repository
```bash
git clone https://github.com/jeromepalos/auto-macro.git
cd auto-macro
```

### 2. Install dependencies
```bash
pip install pyautogui keyboard pynput
```

### 3. Run the app
```bash
python main.py
```

### 4. Build executable (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --hidden-import=pyautogui --hidden-import=keyboard --hidden-import=pynput main.py
```