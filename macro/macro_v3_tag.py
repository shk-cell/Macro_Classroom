import tkinter as tk
import threading
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

SITE_URL = "https://shk-cell.github.io/Macro_Classroom/"

def run(name, delay, log, stop_event):
    log("Launching browser...")
    driver = webdriver.Chrome()
    driver.get(SITE_URL)
    time.sleep(2)
    log("Connected. Searching for empty seats!")
    count = 0

    while not stop_event.is_set():
        seats = driver.find_elements(By.CSS_SELECTOR, ".seat:not(.claimed):not(.inactive)")
        if not seats:
            log("No empty seats found. Stopping.")
            break

        seat = random.choice(seats)
        try:
            driver.execute_script("arguments[0].click();", seat)
            result = driver.execute_script("""
                const modal = document.getElementById('name-modal');
                if (!modal || !modal.classList.contains('show')) return false;
                document.getElementById('name-input').value = arguments[0];
                window.confirmName();
                return true;
            """, name)
            if result:
                count += 1
                log(f"[{count}] Claimed!")
        except:
            pass

        time.sleep(float(delay))

    driver.quit()
    log(f"Finished! Total: {count}")


class App:
    def __init__(self, root):
        self.root = root
        self.stop_event = threading.Event()
        root.title("V3 - Tag-Based Macro (Selenium)")
        root.geometry("420x400")
        root.resizable(False, False)
        root.configure(bg="#1a1a1a")

        self._label("Name")
        self.name = self._entry("YourName")

        self._label("Delay (seconds)")
        self.delay = self._entry("0.3")

        tk.Label(root,
                 text="Finds empty seats by analyzing HTML tags.\nSelenium controls the browser directly.",
                 bg="#1a1a1a", fg="#555", font=("Consolas", 9), justify="left"
                 ).pack(anchor="w", padx=14, pady=(4, 0))

        self._btn_row()
        self._log_box()
        root.bind("<Escape>", lambda e: self._stop())

    def _label(self, text):
        tk.Label(self.root, text=text, bg="#1a1a1a", fg="#00ff41",
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=14, pady=(12, 2))

    def _entry(self, default):
        v = tk.StringVar(value=default)
        tk.Entry(self.root, textvariable=v, bg="#0d0d0d", fg="#00ff41",
                 insertbackground="#00ff41", font=("Consolas", 11),
                 relief="flat", bd=4).pack(fill="x", padx=14, pady=(0, 4))
        return v

    def _btn_row(self):
        f = tk.Frame(self.root, bg="#1a1a1a")
        f.pack(pady=14)
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
