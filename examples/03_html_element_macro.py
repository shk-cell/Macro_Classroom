"""
[방법 3] HTML 요소 기반 매크로
Python으로 직접 서버 API를 호출하는 방식. 가장 빠르고 강력함.
"""

import requests
import time
import sys

print("=" * 45)
print("   HTML 요소 기반 자동 예약 매크로")
print("=" * 45)
print()

# ── 입력 ──
server = input("서버 주소를 입력하세요 (예: http://192.168.0.1:3000): ").strip().rstrip('/')
if not server:
    print("서버 주소를 입력해야 합니다.")
    input("엔터를 눌러 종료...")
    sys.exit()

name = input("예매자 이름을 입력하세요: ").strip()
if not name:
    print("이름을 입력해야 합니다.")
    input("엔터를 눌러 종료...")
    sys.exit()

print()

# ── STEP 1: 상태 확인 & 예매 열릴 때까지 대기 ──
print("▶ STEP 1: 서버 연결 및 예매 상태 확인...")
try:
    res = requests.get(f"{server}/api/state", timeout=5)
    state = res.json()
except Exception as e:
    print(f"  ❌ 서버 연결 실패: {e}")
    print("  서버 주소를 다시 확인하세요.")
    input("엔터를 눌러 종료...")
    sys.exit()

print(f"  예매 열림: {'예' if state['is_open'] else '아니오'}")
print(f"  남은 좌석: {state['seats_left']} / {state['total_seats']}")

if state['seats_left'] == 0:
    print("  ❌ 이미 매진되었습니다.")
    input("엔터를 눌러 종료...")
    sys.exit()

if not state['is_open']:
    print()
    print("  ⏳ 예매가 아직 열리지 않았습니다.")
    print("  예매가 열릴 때까지 자동으로 기다립니다... (0.3초마다 확인)")
    while not state['is_open']:
        time.sleep(0.3)
        try:
            state = requests.get(f"{server}/api/state", timeout=5).json()
        except:
            pass
    print("  🟢 예매 시작! 즉시 예약합니다!")

# ── STEP 2: 토큰 발급 ──
print()
print("▶ STEP 2: 토큰 발급 중...")
try:
    res = requests.get(f"{server}/api/ticket", timeout=5)
    if res.status_code != 200:
        print(f"  ❌ 토큰 발급 실패: {res.json().get('error')}")
        input("엔터를 눌러 종료...")
        sys.exit()
    token = res.json()['token']
    print(f"  토큰 발급 성공!")
except Exception as e:
    print(f"  ❌ 오류: {e}")
    input("엔터를 눌러 종료...")
    sys.exit()

# ── STEP 3: 예약 신청 ──
print()
print("▶ STEP 3: 예약 신청 중...")
try:
    res = requests.post(
        f"{server}/api/reserve",
        json={"name": name, "token": token},
        timeout=5
    )
    data = res.json()
    print()
    if data.get('success'):
        print("🎉 " + "=" * 35)
        print(f"   예약 성공!")
        print(f"   이름     : {name}")
        print(f"   좌석번호 : {data['seat_number']}번")
        print("=" * 37)
    else:
        print(f"❌ 예약 실패: {data.get('error')}")
except Exception as e:
    print(f"  ❌ 오류: {e}")

input("\n엔터를 눌러 종료...")
