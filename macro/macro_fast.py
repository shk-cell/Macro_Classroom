import threading
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# =============================================
#   설정
# =============================================
MY_NAME    = "내이름"   # 본인 이름
NUM_BOTS   = 5          # 동시에 실행할 브라우저 수 (많을수록 빠름, PC 사양에 따라 조절)
# =============================================

SITE_URL = "https://shk-cell.github.io/Macro_Classroom/"

total_count = 0
lock = threading.Lock()

def run_bot(bot_id):
    global total_count

    # 헤드리스(백그라운드) 크롬 설정
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)
    driver.get(SITE_URL)
    time.sleep(2)  # Firebase 데이터 로딩 대기

    print(f"[Bot {bot_id}] 시작")

    while True:
        try:
            # 빈 좌석 목록
            seats = driver.find_elements(By.CSS_SELECTOR, ".seat:not(.claimed):not(.inactive)")
            if not seats:
                break

            # 랜덤 좌석 JS 클릭 (Selenium click보다 훨씬 빠름)
            seat = random.choice(seats)
            driver.execute_script("arguments[0].click();", seat)

            # 이름 입력 + 확인을 JS로 한방에 처리
            result = driver.execute_script("""
                const modal = document.getElementById('name-modal');
                if (!modal || !modal.classList.contains('show')) return false;
                const input = document.getElementById('name-input');
                input.value = arguments[0];
                window.confirmName();
                return true;
            """, MY_NAME)

            if result:
                with lock:
                    total_count += 1
                    print(f"[Bot {bot_id}] {total_count}번째 점유!")

        except Exception:
            time.sleep(0.1)

    driver.quit()
    print(f"[Bot {bot_id}] 종료")


# 멀티스레드로 동시 실행
start = time.time()
threads = [threading.Thread(target=run_bot, args=(i+1,)) for i in range(NUM_BOTS)]

for t in threads:
    t.start()
for t in threads:
    t.join()

elapsed = time.time() - start
print(f"\n[완료] 총 {total_count}개 점유 | 소요시간: {elapsed:.1f}초 | 평균: {total_count/elapsed:.1f}개/초")
