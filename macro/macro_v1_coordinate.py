import tkinter as tk
import threading
import time
import pyautogui
import pyperclip

SITE_URL = "https://shk-cell.github.io/Macro_Classroom/"

def run(name, coords_text, delay, log, stop_event):
    coords = []
    for line in coords_text.strip().splitlines():
        try:
            x, y = map(int, line.strip().split(","))
            coords.append((x, y))
        except:
            continue

    if not coords:
        log("No coordinates entered.")
        return

    log(f"Starting in 3 seconds. Switch to browser!")
    time.sleep(3)
    log(f"Clicking {len(coords)} coordinates...")

    for i, (x, y) in enumerate(coords):
        if stop_event.is_set():
            log("Stopped.")
            return
        pyautogui.click(x, y)
        time.sleep(0.5)
        pyperclip.copy(name)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.15)
        pyautogui.press("enter")
        log(f"[{i+1}/{len(coords)}] ({x}, {y}) done")
        time.sleep(float(delay))

    log("Finished!")


class App:
    def __init__(self, root):
        self.root = root
        self.stop_event = threading.Event()
        root.title("V1 - Fixed Coordinate Macro")
        root.geometry("420x560")
        root.resizable(False, False)
        root.configure(bg="#1a1a1a")

        self._label("Name")
        self.name = self._entry("YourName")

        self._label("Delay (seconds)")
        self.delay = self._entry("0.5")

        self._label("Coordinates (x,y one per line)")
        self.coords = tk.Text(root, height=8, bg="#0d0d0d", fg="#00ff41",
                              font=("Consolas", 10), relief="flat", bd=4,
                              insertbackground="#00ff41")
        self.coords.insert("end", "300,250\n330,250\n360,250")
        self.coords.pack(fill="x", padx=14, pady=(0, 10))

        tk.Label(root, text="* Run get_coordinates.py to find coordinates",
                 bg="#1a1a1a", fg="#555", font=("Consolas", 8)).pack()

        self._btn_row()
        self._log_box()

    def _label(self, text):
        tk.Label(self.root, text=text, bg="#1a1a1a", fg="#00ff41",
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=14, pady=(10, 2))

    def _entry(self, default):
        v = tk.StringVar(value=default)
        tk.Entry(self.root, textvariable=v, bg="#0d0d0d", fg="#00ff41",
                 insertbackground="#00ff41", font=("Consolas", 11),
                 relief="flat", bd=4).pack(fill="x", padx=14, pady=(0, 4))
        return v

    def _btn_row(self):
        f = tk.Frame(self.root, bg="#1a1a1a")
        f.pack(pady=12)
        tk.Button(f, text="▶  START", command=self._start,
                  bg="#00aa33", fg="#000", font=("Consolas", 12, "bold"),
                  relief="flat", padx=24, pady=8, cursor="hand2",
                  activebackground="#00ff41").pack(side="left", padx=6)
        tk.Button(f, text="■  STOP", command=self._stop,
                  bg="#cc0033", fg="#fff", font=("Consolas", 12, "bold"),
                  relief="flat", padx=24, pady=8, cursor="hand2",
                  activebackground="#ff0040").pack(side="left", padx=6)

    def _log_box(self):
        tk.Label(self.root, text="LOG", bg="#1a1a1a", fg="#555",
                 font=("Consolas", 9)).pack(anchor="w", padx=14)
        self.log_box = tk.Text(self.root, height=7, bg="#0d0d0d", fg="#00cc33",
                                font=("Consolas", 9), relief="flat", bd=4, state="disabled")
        self.log_box.pack(fill="x", padx=12, pady=(0, 12))

    def log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _start(self):
        self.stop_event.clear()
        threading.Thread(target=run, args=(
            self.name.get(),
            self.coords.get("1.0", "end"),
            self.delay.get(),
            self.log,
            self.stop_event
        ), daemon=True).start()

    def _stop(self):
        self.stop_event.set()
        self.log("Stop requested.")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
