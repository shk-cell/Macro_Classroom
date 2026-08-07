import pyautogui
import pyperclip
import time

# =============================================
#   설정
# =============================================
MY_NAME    = "내이름"          # 본인 이름
IMAGE_PATH = "images/empty_seat.png"  # 빈 좌석 이미지 경로
CONFIDENCE = 0.8               # 이미지 유사도 (0~1, 낮을수록 대충 맞아도 인식)
DELAY      = 0.4               # 클릭 간격 (초)
# =============================================

# 이미지 인식에는 opencv 필요: pip install opencv-python

print("[시작] 이미지 인식 매크로")
print(f"인식 이미지: {IMAGE_PATH}")
time.sleep(2)  # 브라우저로 이동할 시간

count = 0

while True:
    # 화면에서 빈 좌석 이미지 찾기
    location = pyautogui.locateOnScreen(IMAGE_PATH, confidence=CONFIDENCE)

    if location is None:
        print("빈 좌석 이미지를 찾을 수 없습니다. 종료합니다.")
        break

    # 이미지 중앙 좌표 계산 후 클릭
    center = pyautogui.center(location)
    pyautogui.click(center)
    time.sleep(0.5)  # 팝업 대기

    # 이름 입력
    pyperclip.copy(MY_NAME)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)
    pyautogui.press("enter")

    count += 1
    print(f"[{count}번째] 좌석 점유 완료! 위치: {center}")
    time.sleep(DELAY)

print(f"\n[완료] 총 {count}개 점유")
