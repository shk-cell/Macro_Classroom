import pyautogui
import time

# 마우스 현재 좌표를 실시간으로 출력해주는 도구
# 원하는 칸에 마우스 올리고 좌표 확인 후 macro_v1_coordinate.py 에 입력하면 됨

print("마우스를 원하는 위치로 이동하세요.")
print("Ctrl+C 로 종료\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"좌표: ({x}, {y})", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\n종료")
