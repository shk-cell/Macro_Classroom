import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui
import pyperclip

SITE_URL = "https://shk-cell.github.io/Macro_Classroom/"

def run(name, coords, delay, log, stop_event):
    if not coords:
        log("No coordinates added.")
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
        self.coords = []  # (x, y) list

        root.title("V1 - Fixed Coordinate Macro")
        root.geometry("500x580")
        root.resizable(False, False)
        root.configure(bg="#1a1a1a")

        # ── Name / Delay ──
        top = tk.Frame(root, bg="#1a1a1a")
        top.pack(fill="x", padx=14, pady=(12, 4))

        tk.Label(top, text="Name", bg="#1a1a1a", fg="#00ff41",
                 font=("Consolas", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.name = tk.StringVar(value="YourName")
        tk.Entry(top, textvariable=self.name, bg="#0d0d0d", fg="#00ff41",
                 insertbackground="#00ff41", font=("Consolas", 11),
                 relief="flat", bd=4, width=16).grid(row=0, column=1, padx=8, sticky="w")

        tk.Label(top, text="Delay (s)", bg="#1a1a1a", fg="#00ff41",
                 font=("Consolas", 10, "bold")).grid(row=0, column=2, sticky="w")
        self.delay = tk.StringVar(value="0.5")
        tk.Entry(top, textvariable=self.delay, bg="#0d0d0d", fg="#00ff41",
                 insertbackground="#00ff41", font=("Consolas", 11),
                 relief="flat", bd=4, width=6).grid(row=0, column=3, padx=8, sticky="w")

        # ── Coordinate Manager ──
        tk.Label(root, text="Coordinates", bg="#1a1a1a", fg="#00ff41",
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=14, pady=(10, 4))

        coord_frame = tk.Frame(root, bg="#1a1a1a")
        coord_frame.pack(fill="x", padx=14)

        # Listbox
        list_frame = tk.Frame(coord_frame, bg="#1a1a1a")
        list_frame.pack(side="left", fill="both", expand=True)

        self.listbox = tk.Listbox(list_frame, bg="#0d0d0d", fg="#00ff41",
                                   font=("Consolas", 10), relief="flat", bd=4,
                                   selectbackground="#00aa33", selectforeground="#000",
                                   height=10, activestyle="none")
        self.listbox.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        sb.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=sb.set)

        # Buttons (right of listbox)
        btn_frame = tk.Frame(coord_frame, bg="#1a1a1a")
        btn_frame.pack(side="left", padx=(10, 0), fill="y")

        btn_cfg = dict(bg="#2a2a2a", fg="#00ff41", font=("Consolas", 9, "bold"),
                       relief="flat", width=10, cursor="hand2", pady=6,
                       activebackground="#3a3a3a", activeforeground="#00ff41")

        tk.Button(btn_frame, text="Capture", command=self._capture, **btn_cfg).pack(pady=(0, 4))
        tk.Button(btn_frame, text="Add Manual", command=self._add_manual, **btn_cfg).pack(pady=(0, 4))
        tk.Button(btn_frame, text="Delete", command=self._delete,
                  bg="#2a2a2a", fg="#ff4444", font=("Consolas", 9, "bold"),
                  relief="flat", width=10, cursor="hand2", pady=6,
                  activebackground="#3a3a3a").pack(pady=(0, 4))
        tk.Button(btn_frame, text="Clear All", command=self._clear_all,
                  bg="#2a2a2a", fg="#ff4444", font=("Consolas", 9, "bold"),
                  relief="flat", width=10, cursor="hand2", pady=6,
                  activebackground="#3a3a3a").pack(pady=(0, 4))
        tk.Button(btn_frame, text="Move Up", command=self._move_up, **btn_cfg).pack(pady=(0, 4))
        tk.Button(btn_frame, text="Move Down", command=self._move_down, **btn_cfg).pack()

        # Capture hint
        tk.Label(root, text="* Capture: click button, move mouse to seat, wait 3s",
                 bg="#1a1a1a", fg="#555", font=("Consolas", 8)).pack(anchor="w", padx=14, pady=(4, 0))

        # Coord count
        self.count_var = tk.StringVar(value="0 coordinates")
        tk.Label(root, textvariable=self.count_var, bg="#1a1a1a", fg="#00aa33",
                 font=("Consolas", 9)).pack(anchor="w", padx=14)

        # START / STOP
        self._btn_row()
        self._log_box()
        root.bind("<Escape>", lambda e: self._stop())

    # ── Coordinate Actions ──

    def _capture(self):
        """3초 카운트다운 후 현재 마우스 위치 캡처"""
        def countdown():
            for i in range(3, 0, -1):
                self.log(f"Capturing in {i}...")
                time.sleep(1)
            x, y = pyautogui.position()
            self.coords.append((x, y))
            self.listbox.insert("end", f"  ({x}, {y})")
            self._update_count()
            self.log(f"Captured: ({x}, {y})")
        threading.Thread(target=countdown, daemon=True).start()

    def _add_manual(self):
        """팝업으로 x, y 직접 입력"""
        win = tk.Toplevel(self.root)
        win.title("Add Coordinate")
        win.geometry("260x140")
        win.configure(bg="#1a1a1a")
        win.resizable(False, False)

        entry_cfg = dict(bg="#0d0d0d", fg="#00ff41", insertbackground="#00ff41",
                         font=("Consolas", 11), relief="flat", bd=4, width=8)

        tk.Label(win, text="X", bg="#1a1a1a", fg="#00ff41",
                 font=("Consolas", 10, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        x_var = tk.StringVar()
        tk.Entry(win, textvariable=x_var, **entry_cfg).grid(row=0, column=1, padx=4)

        tk.Label(win, text="Y", bg="#1a1a1a", fg="#00ff41",
                 font=("Consolas", 10, "bold")).grid(row=1, column=0, padx=10, sticky="w")
        y_var = tk.StringVar()
        tk.Entry(win, textvariable=y_var, **entry_cfg).grid(row=1, column=1, padx=4)

        def confirm():
            try:
                x, y = int(x_var.get()), int(y_var.get())
                self.coords.append((x, y))
                self.listbox.insert("end", f"  ({x}, {y})")
                self._update_count()
                self.log(f"Added: ({x}, {y})")
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Enter valid numbers.", parent=win)

        tk.Button(win, text="Add", command=confirm,
                  bg="#00aa33", fg="#000", font=("Consolas", 10, "bold"),
                  relief="flat", padx=16, pady=4, cursor="hand2").grid(
                  row=2, column=0, columnspan=2, pady=12)

    def _delete(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.listbox.delete(idx)
        self.coords.pop(idx)
        self._update_count()
        self.log(f"Deleted index {idx+1}.")

    def _clear_all(self):
        self.listbox.delete(0, "end")
        self.coords.clear()
        self._update_count()
        self.log("All coordinates cleared.")

    def _move_up(self):
        sel = self.listbox.curselection()
        if not sel or sel[0] == 0:
            return
        idx = sel[0]
        self.coords[idx], self.coords[idx-1] = self.coords[idx-1], self.coords[idx]
        text = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx-1, text)
        self.listbox.selection_set(idx-1)

    def _move_down(self):
        sel = self.listbox.curselection()
        if not sel or sel[0] == len(self.coords)-1:
            return
        idx = sel[0]
        self.coords[idx], self.coords[idx+1] = self.coords[idx+1], self.coords[idx]
        text = self.listbox.get(idx)
        self.listbox.delete(idx)
        self.listbox.insert(idx+1, text)
        self.listbox.selection_set(idx+1)

    def _update_count(self):
        self.count_var.set(f"{len(self.coords)} coordinates")

    # ── UI Helpers ──

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
        self.log_box = tk.Text(self.root, height=6, bg="#0d0d0d", fg="#00cc33",
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
            list(self.coords),
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
