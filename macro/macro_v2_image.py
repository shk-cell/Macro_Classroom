import tkinter as tk
from tkinter import filedialog
import threading
import time
import pyautogui
import pyperclip

SITE_URL = "https://shk-cell.github.io/Macro_Classroom/"

def run(name, image_path, confidence, delay, log, stop_event):
    log(f"Starting in 3 seconds. Switch to browser!")
    time.sleep(3)
    log(f"Image recognition started: {image_path}")
    count = 0

    while not stop_event.is_set():
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=float(confidence))
        except Exception as e:
            log(f"Error: {e}")
            break

        if location is None:
            log("Image not found. Stopping.")
            break

        center = pyautogui.center(location)
        pyautogui.click(center)
        time.sleep(0.5)
        pyperclip.copy(name)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.15)
        pyautogui.press("enter")
        count += 1
        log(f"[{count}] Claimed! Position: {center}")
        time.sleep(float(delay))

    log(f"Finished! Total: {count}")


class App:
    def __init__(self, root):
        self.root = root
        self.stop_event = threading.Event()
        root.title("V2 - Image Recognition Macro")
        root.geometry("420x480")
        root.resizable(False, False)
        root.configure(bg="#1a1a1a")

        self._label("Name")
        self.name = self._entry("YourName")

        self._label("Image Path")
        f = tk.Frame(root, bg="#1a1a1a")
        f.pack(fill="x", padx=14, pady=(0, 4))
        self.img_var = tk.StringVar(value="images/empty_seat.png")
        tk.Entry(f, textvariable=self.img_var, bg="#0d0d0d", fg="#00ff41",
                 insertbackground="#00ff41", font=("Consolas", 10),
                 relief="flat", bd=4).pack(side="left", fill="x", expand=True)
        tk.Button(f, text="Browse", command=self._browse,
                  bg="#2a2a2a", fg="#00ff41", font=("Consolas", 9),
                  relief="flat", padx=8, cursor="hand2").pack(side="left", padx=(6, 0))

        tk.Label(root, text="* Capture an empty seat screenshot and save it first",
                 bg="#1a1a1a", fg="#555", font=("Consolas", 8)).pack()

        self._label("Confidence (0.0 ~ 1.0)")
        self.conf = self._entry("0.8")

        self._label("Delay (seconds)")
        self.delay = self._entry("0.4")

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

    def _browse(self):
        path = filedialog.askopenfilename(filetypes=[("Image", "*.png *.jpg")])
        if path:
            self.img_var.set(path)

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
            self.img_var.get(),
            self.conf.get(),
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
