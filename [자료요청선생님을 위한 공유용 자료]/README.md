# 매크로 교육용 자료 — 설정 가이드

이 폴더는 "매크로 완전 이해" 수업에 쓰인 자료를 공유용으로 정리한 것입니다.
원본과 달리 Firebase/Cloudflare 관련 설정값은 전부 `YOUR_...` 형태의
자리표시자(placeholder)로 바꿔두었습니다. 실제로 실습을 진행하려면
**본인 소유의 Firebase 프로젝트 + Cloudflare Workers**를 새로 만들어
아래 값을 채워 넣어야 합니다. (원본 프로젝트를 그대로 쓰면 다른 학교 학생들과
같은 데이터베이스·같은 사이트를 공유하게 되어 실습이 서로 충돌합니다.)

## 폴더 구성

```
index.html        - 좌석 예매 게임 페이지 (Firebase 클라이언트 SDK 사용)
worker.js         - Cloudflare Worker (좌석 등록 API, Firebase에 직접 씀)
wrangler.toml     - Cloudflare Workers 배포 설정
macro/            - 매크로 실습 예제 3종 (V1 좌표 / V2 이미지 / V3 태그 기반)
macro_guide.txt   - 매크로 원리 + CSS 셀렉터 실습 가이드 (수업 자료)
requirements.txt  - 매크로 실행에 필요한 파이썬 패키지 목록
```

## 1. Firebase 프로젝트 만들기

1. [Firebase 콘솔](https://console.firebase.google.com)에서 새 프로젝트 생성
2. **Realtime Database** 생성 (테스트 모드로 시작해도 되지만, 수업 전 보안 규칙을
   반드시 점검하세요 — 아래 "보안 규칙" 항목 참고)
3. **Authentication** 메뉴에서 이메일/비밀번호 로그인 방식을 활성화하고,
   관리자로 쓸 계정 하나를 직접 생성 (예: `admin@yourschool.com` + 원하는 비밀번호)
4. **프로젝트 설정 > 일반 > 내 앱**에서 웹 앱을 추가하면 `firebaseConfig` 객체가
   나옵니다. 이 값을 [index.html](index.html)의 `firebaseConfig` 부분에 그대로
   붙여넣으세요.
5. [index.html](index.html)의 `ADMIN_EMAIL`을 3번에서 만든 관리자 이메일로 바꾸세요.
6. [worker.js](worker.js)의 `FIREBASE_DB_URL`을 Realtime Database 콘솔 상단에
   표시된 주소로 바꾸세요.
7. Realtime Database용 **비밀 키(Database Secret)**를 발급받으세요
   (프로젝트 설정 > 서비스 계정 > 데이터베이스 보안 비밀). 이 값은 절대
   코드에 직접 적지 말고 아래 3단계에서 Cloudflare Secret으로만 등록합니다.

## 2. Cloudflare Workers 배포

1. Cloudflare 계정 생성 후 `npm install -g wrangler`, `wrangler login`
2. `wrangler kv:namespace create RATE_LIMIT` 실행 → 발급된 id를
   [wrangler.toml](wrangler.toml)의 `id` 자리에 채우기
3. Cloudflare 대시보드에서 확인한 `account_id`를 [wrangler.toml](wrangler.toml)에 채우기
4. Firebase Database Secret을 환경변수로 등록:
   ```bash
   wrangler secret put FIREBASE_SECRET
   ```
   (여기서 값을 붙여넣으면 Cloudflare 서버에만 저장되고 코드/git에는 남지 않습니다)
5. `wrangler deploy` 로 배포 → 발급된 `https://xxxx.workers.dev/` 주소가 실습 사이트 URL

## 3. 매크로 스크립트에 사이트 주소 반영

`macro/macro_v1_coordinate.py`, `macro_v2_image.py`, `macro_v3_tag.py` 상단의
```python
SITE_URL = "https://YOUR-WORKER-SUBDOMAIN.workers.dev/"
```
를 2단계에서 배포한 실제 주소로 바꾸세요.

## 4. Firebase 보안 규칙 점검 (중요)

클라이언트가 Firebase SDK로 직접 `seats`, `gameActive`를 **읽는** 것은 의도된
동작이지만, **쓰기(write)**는 반드시 Worker(`/claim`)를 통해서만 이뤄지도록
막아야 합니다. 그렇지 않으면 학생이 Worker를 거치지 않고 Firebase SDK로
직접 좌석을 등록해 쿨다운/검증 로직을 우회할 수 있습니다. Realtime Database
규칙 예시:

```json
{
  "rules": {
    "seats": { ".read": true, ".write": false },
    "gameActive": { ".read": true, ".write": "auth != null" }
  }
}
```

(`.write`를 서버 시크릿 기반 쓰기만 허용하도록 막고, Start/Stop/Reset은
로그인한 관리자만 가능하도록 `auth != null` 조건을 유지)

## 5. 설치 및 실행

```bash
pip install -r requirements.txt
python macro/macro_v1_coordinate.py
python macro/macro_v2_image.py
python macro/macro_v3_tag.py
```

또는 `macro/install.bat`으로 Python + 패키지를 한 번에 설치할 수 있습니다.

수업 진행 방식과 매크로 원리 설명은 [macro_guide.txt](macro_guide.txt)를 참고하세요.
