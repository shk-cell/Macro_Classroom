"""
[방법 2] 이미지 기반 매크로
화면에서 버튼 이미지를 찾아 자동으로 클릭하는 방식.
"""

import pyautogui
import time
import sys
import os

print("=" * 45)
print("   이미지 기반 자동 예약 매크로")
print("=" * 45)
print()

# exe로 실행될 때 기준 경로
BASE_DIR = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
BTN_PATH   = os.path.join(BASE_DIR, "images", "button.png")
INPUT_PATH = os.path.join(BASE_DIR, "images", "input.png")

# ── 이미지 파일 확인 ──
if not os.path.exists(BTN_PATH):
    print("❌ 버튼 이미지가 없습니다!")
    print(f"   아래 경로에 이미지를 저장하세요:")
    print(f"   {BTN_PATH}")
    print()
    print("캡처 방법: 브라우저에서 '지금 예매하기' 버튼만")
    print("           Win+Shift+S 로 캡처 → button.png 로 저장")
    input("엔터를 눌러 종료...")
    sys.exit()

# ── 이름 입력 ──
name = input("예매자 이름을 입력하세요: ").strip()
if not name:
    print("이름을 입력해야 합니다.")
    input("엔터를 눌러 종료...")
    sys.exit()

print()
print("3초 후 자동으로 예매를 진행합니다. 브라우저를 앞으로 가져오세요!")
time.sleep(3)

# ── 이름 입력창 찾기 ──
if os.path.exists(INPUT_PATH):
    print("▶ 이름 입력창 찾는 중...")
    loc = pyautogui.locateOnScreen(INPUT_PATH, confidence=0.8)
    if loc:
        pyautogui.click(pyautogui.center(loc))
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(name, interval=0.05)
        print(f"  → 이름 입력 완료: {name}")
    else:
        print("  ❌ 입력창을 찾지 못했습니다. 이미지를 다시 캡처하세요.")
        input("엔터를 눌러 종료...")
        sys.exit()
else:
    print("⚠ input.png 없음 → 입력창 클릭 건너뜀 (수동으로 이름 입력 후 진행)")
    input("이름을 직접 입력창에 입력한 뒤 엔터...")

time.sleep(0.2)

# ── 버튼 찾기 & 클릭 ──
print("▶ 예매 버튼 찾는 중...")
loc = pyautogui.locateOnScreen(BTN_PATH, confidence=0.8)
if loc:
    print(f"  → 버튼 발견! 클릭합니다.")
    pyautogui.click(pyautogui.center(loc))
    print()
    print("✅ 완료! 브라우저에서 결과를 확인하세요.")
else:
    print("❌ 버튼을 찾지 못했습니다.")
    print("  - button.png 를 다시 캡처해보세요")
    print("  - 브라우저 창 크기를 캡처 당시와 동일하게 맞춰보세요")

input("엔터를 눌러 종료...")
