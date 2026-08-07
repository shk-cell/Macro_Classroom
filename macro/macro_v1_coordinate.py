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
        log("좌표를 입력해주세요.")
        return

    log(f"3초 후 시작합니다. 브라우저로 이동하세요!")
    time.sleep(3)
    log(f"총 {len(coords)}개 좌표 클릭 시작")

    for i, (x, y) in enumerate(coords):
        if stop_event.is_set():
            log("중지됨.")
            return
        pyautogui.click(x, y)
        time.sleep(0.5)
        pyperclip.copy(name)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.15)
        pyautogui.press("enter")
        log(f"[{i+1}/{len(coords)}] ({x}, {y}) 완료")
        time.sleep(float(delay))

    log("완료!")


class App:
    def __init__(self, root):
        self.root = root
        self.stop_event = threading.Event()
        root.title("V1 — 고정 좌표 매크로")
        root.geometry("420x560")
        root.resizable(False, False)
        root.configure(bg="#1a1a1a")

        self._label("이름")
        self.name = self._entry("내이름")

        self._label("딜레이 (초)")
        self.delay = self._entry("0.5")

        self._label("좌표 목록 (x,y 한 줄씩)")
        self.coords = tk.Text(root, height=8, bg="#0d0d0d", fg="#00ff41",
                              font=("Consolas", 10), relief="flat", bd=4,
                              insertbackground="#00ff41")
        self.coords.insert("end", "300,250\n330,250\n360,250")
        self.coords.pack(fill="x", padx=14, pady=(0, 10))

        # 좌표 도우미 안내
        tk.Label(root, text="※ 좌표 확인: get_coordinates.py 실행 후 마우스 올리기",
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
        self.log("중지 요청됨.")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
