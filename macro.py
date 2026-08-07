from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

# =============================================
#   설정 — 여기만 수정하면 됩니다!
# =============================================
MY_NAME = "내이름"       # 본인 이름으로 변경
DELAY   = 0.3            # 클릭 간격 (초) — 줄이면 빠름, 너무 줄이면 오류남
# =============================================

SITE_URL = "https://shk-cell.github.io/Macro_Classroom/"

# 브라우저 열기
driver = webdriver.Chrome()
driver.get(SITE_URL)
wait = WebDriverWait(driver, 5)

print(f"[시작] 이름: {MY_NAME}")
time.sleep(2)  # 페이지 로딩 대기

count = 0

while True:
    # 빈 좌석 목록 가져오기 (이미 선택된 칸, 비활성 칸 제외)
    seats = driver.find_elements(By.CSS_SELECTOR, ".seat:not(.claimed):not(.inactive)")

    if not seats:
        print("빈 좌석이 없거나 게임이 시작되지 않았습니다.")
        break

    # 랜덤으로 빈 좌석 하나 선택
    seat = random.choice(seats)

    try:
        seat.click()

        # 이름 입력 팝업 대기
        name_input = wait.until(EC.visibility_of_element_located((By.ID, "name-input")))
        name_input.clear()
        name_input.send_keys(MY_NAME)
        name_input.send_keys(Keys.ENTER)

        count += 1
        print(f"[{count}번째] 좌석 점유 완료!")
        time.sleep(DELAY)

    except Exception as e:
        # 팝업이 안 뜨거나 다른 사람이 먼저 선택한 경우 — 그냥 넘어감
        time.sleep(0.5)

print(f"\n[종료] 총 {count}개 점유했습니다.")
driver.quit()
