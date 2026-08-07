import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

SITE_URL = "https://shk-cell.github.io/Macro_Classroom/"

# ─────────────────────────────────────────────
#  버전 1 — 고정 좌표
# ─────────────────────────────────────────────
def run_v1(name, coords_text, delay, log):
    coords = []
    for line in coords_text.strip().splitlines():
        line = line.strip()
        if not line: continue
        try:
            x, y = map(int, line.split(","))
            coords.append((x, y))
        except:
            log(f"좌표 파싱 오류: {line}")
            return

    log(f"[V1] {len(coords)}개 좌표 클릭 시작")
    time.sleep(1.5)

    for i, (x, y) in enumerate(coords):
        pyautogui.click(x, y)
        time.sleep(0.5)
        pyperclip.copy(name)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.15)
        pyautogui.press("enter")
        log(f"[V1] {i+1}/{len(coords)} 완료 ({x},{y})")
        time.sleep(float(delay))

    log("[V1] 완료!")

# ─────────────────────────────────────────────
#  버전 2 — 이미지 인식
# ─────────────────────────────────────────────
def run_v2(name, image_path, confidence, delay, log):
    log(f"[V2] 이미지 인식 시작: {image_path}")
    time.sleep(1.5)
    count = 0

    while True:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=float(confidence))
        except Exception as e:
            log(f"[V2] 오류: {e}")
            break

        if location is None:
            log("[V2] 이미지를 찾을 수 없습니다. 종료.")
            break

        center = pyautogui.center(location)
        pyautogui.click(center)
        time.sleep(0.5)
        pyperclip.copy(name)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.15)
        pyautogui.press("enter")
        count += 1
        log(f"[V2] {count}번째 점유! 위치: {center}")
        time.sleep(float(delay))

    log(f"[V2] 완료! 총 {count}개")

# ─────────────────────────────────────────────
#  버전 3 — 태그 기반 (Selenium)
# ─────────────────────────────────────────────
def run_v3(name, delay, log):
    import random
    log("[V3] 브라우저 실행 중...")

    driver = webdriver.Chrome()
    driver.get(SITE_URL)
    time.sleep(2)
    count = 0

    while True:
        seats = driver.find_elements(By.CSS_SELECTOR, ".seat:not(.claimed):not(.inactive)")
        if not seats:
            log("[V3] 빈 좌석 없음. 종료.")
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
                log(f"[V3] {count}번째 점유!")
        except:
            pass
        time.sleep(float(delay))

    driver.quit()
    log(f"[V3] 완료! 총 {count}개")

# ─────────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────────
class App:
    def __init__(self, root):
        self.root = root
        root.title("매크로 런처")
        root.geometry("520x620")
        root.resizable(False, False)
        root.configure(bg="#1a1a1a")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",        background="#1a1a1a", borderwidth=0)
        style.configure("TNotebook.Tab",    background="#2a2a2a", foreground="#aaa",
                         padding=[12, 6], font=("Consolas", 10, "bold"))
        style.map("TNotebook.Tab",          background=[("selected", "#00aa33")],
                                            foreground=[("selected", "#000")])
        style.configure("TFrame",           background="#1a1a1a")
        style.configure("TLabel",           background="#1a1a1a", foreground="#00ff41",
                         font=("Consolas", 10))
        style.configure("TEntry",           fieldbackground="#0d0d0d", foreground="#00ff41",
                         insertcolor="#00ff41", font=("Consolas", 10))

        # 공통 이름 입력
        top = tk.Frame(root, bg="#1a1a1a")
        top.pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(top, text="이름", bg="#1a1a1a", fg="#00ff41",
                 font=("Consolas", 10, "bold")).pack(side="left")
        self.name_var = tk.StringVar(value="내이름")
        tk.Entry(top, textvariable=self.name_var, bg="#0d0d0d", fg="#00ff41",
                 insertbackground="#00ff41", font=("Consolas", 11),
                 relief="flat", bd=4, width=20).pack(side="left", padx=8)

        # 탭
        nb = ttk.Notebook(root)
        nb.pack(fill="both", expand=True, padx=12, pady=6)

        self.tab1 = self._make_tab(nb, "V1 좌표")
        self.tab2 = self._make_tab(nb, "V2 이미지")
        self.tab3 = self._make_tab(nb, "V3 태그")
        self._build_v1(self.tab1)
        self._build_v2(self.tab2)
        self._build_v3(self.tab3)

        # 로그
        tk.Label(root, text="LOG", bg="#1a1a1a", fg="#555",
                 font=("Consolas", 9)).pack(anchor="w", padx=16)
        self.log_box = tk.Text(root, height=8, bg="#0d0d0d", fg="#00cc33",
                               font=("Consolas", 9), relief="flat", bd=4,
                               state="disabled")
        self.log_box.pack(fill="x", padx=12, pady=(0, 12))

    def _make_tab(self, nb, title):
        f = ttk.Frame(nb)
        nb.add(f, text=title)
        return f

    def _label(self, parent, text, row, col=0):
        tk.Label(parent, text=text, bg="#1a1a1a", fg="#00ff41",
                 font=("Consolas", 10)).grid(row=row, column=col, sticky="w",
                                              padx=10, pady=4)

    def _entry(self, parent, default, row, col=1, width=18):
        v = tk.StringVar(value=default)
        tk.Entry(parent, textvariable=v, bg="#0d0d0d", fg="#00ff41",
                 insertbackground="#00ff41", font=("Consolas", 10),
                 relief="flat", bd=3, width=width).grid(row=row, column=col,
                                                         padx=10, pady=4, sticky="w")
        return v

    def _start_btn(self, parent, cmd, row):
        tk.Button(parent, text="▶  START", command=cmd,
                  bg="#00aa33", fg="#000", font=("Consolas", 12, "bold"),
                  relief="flat", bd=0, padx=20, pady=8, cursor="hand2",
                  activebackground="#00ff41").grid(row=row, column=0,
                                                    columnspan=2, pady=14)

    # ── V1 ──
    def _build_v1(self, f):
        f.configure(style="TFrame")
        self._label(f, "딜레이 (초)", 0)
        self.v1_delay = self._entry(f, "0.5", 0)
        tk.Label(f, text="좌표 목록 (x,y 한 줄씩)", bg="#1a1a1a",
                 fg="#00ff41", font=("Consolas", 10)).grid(row=1, column=0,
                 columnspan=2, sticky="w", padx=10, pady=(8,2))
        self.v1_coords = tk.Text(f, height=7, bg="#0d0d0d", fg="#00ff41",
                                  font=("Consolas", 10), relief="flat", bd=3,
                                  insertbackground="#00ff41")
        self.v1_coords.insert("end", "300,250\n330,250\n360,250")
        self.v1_coords.grid(row=2, column=0, columnspan=2, padx=10, sticky="ew")
        self._start_btn(f, self._start_v1, 3)

    def _start_v1(self):
        t = threading.Thread(target=run_v1, args=(
            self.name_var.get(),
            self.v1_coords.get("1.0", "end"),
            self.v1_delay.get(),
            self.log), daemon=True)
        t.start()

    # ── V2 ──
    def _build_v2(self, f):
        self._label(f, "이미지 경로", 0)
        self.v2_img = self._entry(f, "images/empty_seat.png", 0, width=24)
        self._label(f, "유사도 (0~1)", 1)
        self.v2_conf = self._entry(f, "0.8", 1)
        self._label(f, "딜레이 (초)", 2)
        self.v2_delay = self._entry(f, "0.4", 2)
        self._start_btn(f, self._start_v2, 3)

    def _start_v2(self):
        t = threading.Thread(target=run_v2, args=(
            self.name_var.get(),
            self.v2_img.get(),
            self.v2_conf.get(),
            self.v2_delay.get(),
            self.log), daemon=True)
        t.start()

    # ── V3 ──
    def _build_v3(self, f):
        self._label(f, "딜레이 (초)", 0)
        self.v3_delay = self._entry(f, "0.3", 0)
        tk.Label(f, text="Selenium으로 태그를 분석해\n빈 좌석을 자동으로 찾아 클릭합니다.",
                 bg="#1a1a1a", fg="#555", font=("Consolas", 9),
                 justify="left").grid(row=1, column=0, columnspan=2,
                                      padx=10, pady=6, sticky="w")
        self._start_btn(f, self._start_v3, 2)

    def _start_v3(self):
        t = threading.Thread(target=run_v3, args=(
            self.name_var.get(),
            self.v3_delay.get(),
            self.log), daemon=True)
        t.start()

    # ── 로그 ──
    def log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
