import tkinter as tk
import psutil
import time
import json
import os
import ctypes
import win32con
import win32gui
import sys
import winreg

APP_NAME = "NetSpeedMonitor"
APPDATA_DIR = os.path.join(os.environ["APPDATA"], APP_NAME)
POSITION_FILE = os.path.join(APPDATA_DIR, "position.json")
STARTUP_SHORTCUT = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup", f"{APP_NAME}.lnk")

# Ensure app data directory exists
os.makedirs(APPDATA_DIR, exist_ok=True)

# DPI awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    ctypes.windll.user32.SetProcessDPIAware()

# Auto-startup
def add_to_startup():
    exe_path = sys.executable  # Full path to .exe
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS) as regkey:
            try:
                existing, _ = winreg.QueryValueEx(regkey, APP_NAME)
                if existing == exe_path:
                    return  # Already set
            except FileNotFoundError:
                pass
            winreg.SetValueEx(regkey, APP_NAME, 0, winreg.REG_SZ, exe_path)
    except Exception as e:
        print("Startup registration failed:", e)

# First-run check
def ensure_startup_flag():
    if not os.path.exists(STARTUP_SHORTCUT):
        add_to_startup()
        with open(STARTUP_SHORTCUT, "w") as f:
            f.write("done")

# Save/load window position
def save_position(x, y):
    with open(POSITION_FILE, "w") as f:
        json.dump({"x": x, "y": y}, f)

def load_position():
    if os.path.exists(POSITION_FILE):
        with open(POSITION_FILE, "r") as f:
            pos = json.load(f)
            return pos.get("x", 100), pos.get("y", 100)
    return 100, 100

# Speed monitoring
def get_speed():
    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()
    return (net2.bytes_recv - net1.bytes_recv) / 1024, (net2.bytes_sent - net1.bytes_sent) / 1024

def update_speed():
    download, upload = get_speed()
    speed_label.config(text=f"↓ {download:.1f} KB/s\n↑ {upload:.1f} KB/s")
    root.after(1000, update_speed)

# Dragging
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_motion(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f'+{x}+{y}')
    save_position(x, y)

# Always-on-top
def force_topmost():
    hwnd = win32gui.FindWindow(None, "Internet Speed")
    if hwnd:
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
        )

def auto_refresh_topmost():
    force_topmost()
    root.after(2000, auto_refresh_topmost)

# Exit popup
def show_custom_popup(event):
    global popup
    if popup and popup.winfo_exists():
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    popup.configure(bg="black")

    exit_btn = tk.Button(popup, text="Exit", command=root.destroy, bg="red", fg="white", bd=0, padx=10, pady=2)
    exit_btn.pack()
    popup.geometry(f"+{event.x_root + 10}+{event.y_root - 20}")

# Initialize GUI
popup = None
root = tk.Tk()
root.title("Internet Speed")
root.overrideredirect(True)
root.attributes("-alpha", 0.92)
root.configure(bg="black")

speed_label = tk.Label(
    root,
    text="Loading...",
    font=("Segoe UI", 10, "bold"),
    fg="white",
    bg="black",
    justify="left"
)
speed_label.pack(padx=2, pady=2)
speed_label.bind("<Button-1>", start_move)
speed_label.bind("<ButtonRelease-1>", stop_move)
speed_label.bind("<B1-Motion>", on_motion)
speed_label.bind("<Button-3>", show_custom_popup)

# Apply position
x, y = load_position()
root.geometry(f"140x50+{x}+{y}")

# First-run logic
ensure_startup_flag()

# Start everything
update_speed()
auto_refresh_topmost()
root.mainloop()