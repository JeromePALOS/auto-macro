import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import keyboard
from pynput import mouse, keyboard as kb

# ---------------------------------
# STATES (FIXED)
# ---------------------------------
recording = False
spam_running = False

play_event = threading.Event()
play_thread = None

events = []
start_time = 0

last_play_start  = 0

# ---------------------------------
# UTILS
# ---------------------------------
def log(msg):
    status_var.set(msg)


def get_key_name(key):
    try:
        return key.char.lower()
    except:
        return str(key).replace("Key.", "").lower()


def parse_keys(text):
    return text.lower().replace(" ", "").split("+")


# ---------------------------------
# SAFETY LOCKS (FIXED)
# ---------------------------------
def can_record():
    return not play_event.is_set() and not spam_running


def can_play():
    return not recording and not spam_running


def can_spam():
    return not recording and not play_event.is_set()


# ---------------------------------
# RECORD (MOUSE + KEYBOARD)
# ---------------------------------
def on_move(x, y):
    if recording:
        events.append(("move", time.time() - start_time, x, y))


def on_click(x, y, button, pressed):
    if recording:
        events.append(("click", time.time() - start_time, x, y, button.name, pressed))


def on_press(key):
    if recording:
        name = get_key_name(key)
        events.append(("key_down", time.time() - start_time, name))


def on_release(key):
    if recording:
        name = get_key_name(key)
        events.append(("key_up", time.time() - start_time, name))


# ---------------------------------
# RECORD CONTROL
# ---------------------------------
def start_record():
    global recording, events, start_time

    if not can_record():
        log("⛔ Cannot record now")
        return

    events = []
    recording = True
    start_time = time.time()

    btn_record.config(text="⏹ Stop (F6)", bg="#e53935", fg="white")
    log("🔴 Recording...")


def stop_record():
    global recording
    recording = False

    btn_record.config(text="🔴 Record (F6)", bg="#eee", fg="black")
    btn_play.config(text="▶ Play (F7)", bg="#eee", fg="black", state="normal")
    log("✅ Recording stopped")


def toggle_record():
    if recording:
        stop_record()
    else:
        start_record()


# ---------------------------------
# PLAY MACRO (FIXED)
# ---------------------------------
def play_macro():
    prev = 0

    while play_event.is_set():
        for event in events:
            if not play_event.is_set():
                break

            time.sleep(max(0, event[1] - prev))
            prev = event[1]

            if not play_event.is_set():
                break

            etype = event[0]

            if etype == "move":
                _, _, x, y = event
                pyautogui.moveTo(x, y, _pause=False)

            elif etype == "click":
                _, _, x, y, button, pressed = event
                if pressed:
                    pyautogui.mouseDown(x, y, button=button)
                else:
                    pyautogui.mouseUp(x, y, button=button)

            elif etype == "key_down":
                _, _, key = event
                pyautogui.keyDown(key)

            elif etype == "key_up":
                _, _, key = event
                pyautogui.keyUp(key)

    btn_play.config(text="▶ Play (F7)", bg="#eee", fg="black")
    log("⏹ Stopped")


# ---------------------------------
# PLAY TOGGLE (FIXED)
# ---------------------------------
def toggle_play():
    global play_thread, last_play_start

    if play_event.is_set():
        play_event.clear()
        log("⏹ Stopped")
        return

    # cooldown
    now = time.time()
    if now - last_play_start < 1:
        return

    last_play_start = now

    if not events:
        log("⚠️ No macro")
        return

    if not can_play():
        log("⛔ Can't play now")
        return

    play_event.set()

    btn_play.config(text="⏹ Stop (F7)", bg="#43a047", fg="white")
    log("⚠️ If it doesn't stop, keep holding F7")

    play_thread = threading.Thread(target=play_macro, daemon=True)
    play_thread.start()


# ---------------------------------
# SPAM (FIXED)
# ---------------------------------
def press_combo(keys):
    for k in keys:
        pyautogui.keyDown(k)


def release_combo(keys):
    for k in keys:
        pyautogui.keyUp(k)


def spam_loop():
    global spam_running

    keys = parse_keys(entry_keys.get())

    try:
        delay = int(entry_ms.get())
    except:
        delay = 100

    spam_running = True
    log("⚡ Spam actif")

    if delay == 0:
        log("🔒 HOLD MODE")

        if len(keys) == 1 and len(keys[0]) == 1:
            while spam_running:
                keyboard.press(keys[0])
                time.sleep(0.01)
            return

        press_combo(keys)

        while spam_running:
            time.sleep(0.01)

        release_combo(keys)
        log("⏹ Spam stopped")
        return

    while spam_running:
        for k in keys:
            pyautogui.press(k)

        time.sleep(delay / 1000)


def toggle_spam():
    global spam_running

    if spam_running:
        spam_running = False
        btn_spam.config(text="⚡ Spam (F8)", bg="#eee", fg="black")
        log("⏹ Spam stopped")
        return

    if can_spam():
        spam_running = True
        btn_spam.config(text="⏹ Stop Spam (F8)", bg="#43a047", fg="white")
        threading.Thread(target=spam_loop, daemon=True).start()
    else:
        log("⛔ Can't spam now")


# ---------------------------------
# GUI
# ---------------------------------
root = tk.Tk()
root.title("Auto Macro")
root.geometry("560x470")

title = tk.Label(root, text="🎮 Auto Macro", font=("Arial", 20, "bold"))
title.pack(pady=10)

btn_record = tk.Button(root, text="🔴 Record (F6)", bg="#eee", fg="black", command=toggle_record)
btn_record.pack(pady=5, ipadx=10, ipady=6)

btn_play = tk.Button(root, text="▶ Play (F7)", bg="#eee", fg="black", state="disabled", command=toggle_play)
btn_play.pack(pady=5, ipadx=10, ipady=6)

ttk.Separator(root).pack(fill="x", pady=10)

tk.Label(root, text="Keys to spam").pack()
entry_keys = tk.Entry(root, justify="center")
entry_keys.pack()
entry_keys.insert(0, "e")

tk.Label(root, text="Delay ms (0 = HOLD)").pack()
entry_ms = tk.Entry(root, justify="center")
entry_ms.pack()
entry_ms.insert(0, "0")

btn_spam = tk.Button(root, text="⚡ Spam (F8)", bg="#eee", fg="black", command=toggle_spam)
btn_spam.pack(pady=5, ipadx=10, ipady=6)

status_var = tk.StringVar()
status_var.set("Ready")

tk.Label(root, textvariable=status_var).pack(pady=10)
footer = tk.Frame(root)
footer.pack(fill="both", expand=True)

tk.Label(
    footer,
    text="♥",
    fg="#ff69b4",
    font=("Arial", 14, "bold")
).place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

# ---------------------------------
# LISTENERS
# ---------------------------------
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
keyboard_listener = kb.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

# HOTKEYS
keyboard.add_hotkey("f6", lambda: root.after(0, toggle_record))
keyboard.add_hotkey("f7", lambda: root.after(0, toggle_play))
keyboard.add_hotkey("f8", lambda: root.after(0, toggle_spam))

root.mainloop()
