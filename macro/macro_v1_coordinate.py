import pyautogui
import pyperclip
import time

# =============================================
#   설정
# =============================================
MY_NAME = "내이름"    # 본인 이름
DELAY   = 0.5         # 클릭 간격 (초)

# 클릭할 좌표 리스트 (x, y)
# 좌표 찾는 법: get_coordinates.py 실행 후 마우스를 원하는 칸에 올리면 좌표 출력됨
COORDINATES = [
    (300, 250),
    (330, 250),
    (360, 250),
    (390, 250),
    (420, 250),
]
# =============================================

print(f"[시작] {len(COORDINATES)}개 좌석 클릭 예정")
time.sleep(2)  # 준비 시간 (브라우저로 이동할 시간)

for i, (x, y) in enumerate(COORDINATES):
    # 좌석 클릭
    pyautogui.click(x, y)
    time.sleep(0.5)  # 팝업 뜨는 시간 대기

    # 이름 입력 (한글은 클립보드 붙여넣기 방식)
    pyperclip.copy(MY_NAME)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)
    pyautogui.press("enter")

    print(f"[{i+1}/{len(COORDINATES)}] ({x}, {y}) 클릭 완료")
    time.sleep(DELAY)

print("\n[완료]")
