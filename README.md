🖼️ Screenshot
 ![screenshot](performance.png)

# 💻 Internet Speed Monitor for Windows

A lightweight, draggable floating overlay that displays real-time internet download and upload speeds. Designed to stay **above the taskbar**, **auto-start with Windows**, and **remember its position**.

---

## 📦 Features

- 🔼 Shows **upload and download speed** in KB/s
- 📌 Always-on-top overlay, even above the taskbar
- 🎛️ Minimalist, transparent, and draggable UI
- 💾 Remembers last window position across reboots
- 🚀 Auto-starts with Windows on first run
- 🖱️ Right-click menu to **Exit**
- 🧱 Uses native Windows APIs for reliable behavior

---

## 🛠️ How It Works

- Built with **Python**, using:
  - `Tkinter` for UI  
  - `psutil` for network monitoring  
  - `ctypes` and `winreg` for Windows API interaction  
- Compiled into `.exe` using **PyInstaller**
- Saves config (position, startup settings) in: %APPDATA%\InternetSpeedMonitor

- Sets up auto-start using the Windows Registry: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run


---

## 📁 Files Created

| File / Key Name              | Purpose                         | Location                                         |
|-----------------------------|----------------------------------|--------------------------------------------------|
| `InternetSpeedMonitor.exe`  | Main executable                 | Anywhere you run it                              |
| `position.json`             | Saves last window position      | `%APPDATA%\InternetSpeedMonitor\position.json`   |
| `InternetSpeedMonitor` key  | Enables auto-start on boot      | Windows Registry (`HKCU\...\Run`)                |

---

## 🚀 How to Use

1. **Download & extract** the `.zip` containing `InternetSpeedMonitor.exe`
2. **Run** `InternetSpeedMonitor.exe`
3. On first launch:
 - It will appear on-screen showing live speed
 - It saves its position in `%APPDATA%`
 - It registers itself to auto-start at boot
4. You can **drag** the window to reposition
5. **Right-click** on it to see the **Exit** option

> ✅ The app will now auto-run and restore position every time your PC starts.

---

## 🔁 Running from Any Folder

You can copy or run the `.exe` from **any directory** (e.g., Desktop, Documents, Downloads). It will:

- Automatically write config to `%APPDATA%`
- Automatically register for startup in Windows Registry

You **do not** need to run it from a specific install path.

---

## 🧹 How to Uninstall

1. Press `Win + R`, type `regedit`, and open: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
2. Delete the entry named: InternetSpeedMonitor
3. Delete the folder: %APPDATA%\InternetSpeedMonitor
4. Delete the `.exe` file from wherever you placed it.

---

## 💡 Developer Notes

> The `.exe` was created using [PyInstaller](https://pyinstaller.org/)

### Build Command:
```bash
pyinstaller --onefile --noconsole --name NetSpeedMonitor --icon=neticon.ico main.py

