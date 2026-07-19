"""
[방법 1] 좌표 기반 매크로
화면의 X, Y 좌표를 직접 지정해서 클릭하는 방식.
"""

import pyautogui
import time
import sys

print("=" * 45)
print("   좌표 기반 자동 예약 매크로")
print("=" * 45)
print()

# ── 이름 입력 ──
name = input("예매자 이름을 입력하세요: ").strip()
if not name:
    print("이름을 입력해야 합니다.")
    input("엔터를 눌러 종료...")
    sys.exit()

print()
print("[ 좌표 찾기 ]")
print("마우스를 이름 입력창 위에 올려두세요.")
print("3초 후 좌표를 자동으로 읽습니다...")
time.sleep(3)
nx, ny = pyautogui.position()
print(f"  → 입력창 좌표: ({nx}, {ny})")

print()
print("마우스를 '지금 예매하기' 버튼 위에 올려두세요.")
print("3초 후 좌표를 자동으로 읽습니다...")
time.sleep(3)
bx, by = pyautogui.position()
print(f"  → 버튼 좌표: ({bx}, {by})")

print()
print(f"이름: {name}")
print(f"입력창: ({nx}, {ny})  |  버튼: ({bx}, {by})")
print()
go = input("이대로 예매를 시작할까요? (y/n): ").strip().lower()
if go != 'y':
    print("취소되었습니다.")
    input("엔터를 눌러 종료...")
    sys.exit()

print()
print("3초 후 자동으로 예매를 진행합니다. 브라우저를 앞으로 가져오세요!")
time.sleep(3)

# ── 자동 클릭 ──
print("▶ 이름 입력창 클릭...")
pyautogui.click(nx, ny)
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'a')
pyautogui.typewrite(name, interval=0.05)

time.sleep(0.2)
print("▶ 예매 버튼 클릭!")
pyautogui.click(bx, by)

print()
print("✅ 완료! 브라우저에서 결과를 확인하세요.")
input("엔터를 눌러 종료...")
