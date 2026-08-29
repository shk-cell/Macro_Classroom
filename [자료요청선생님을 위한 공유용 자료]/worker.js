import HTML from './index.html';

// ⚠️ 본인의 Firebase Realtime Database URL로 바꾸세요.
// Firebase 콘솔 > Realtime Database 페이지 상단에 표시되는 주소입니다.
// 예: https://YOUR_PROJECT_ID-default-rtdb.YOUR_REGION.firebasedatabase.app
const FIREBASE_DB_URL = 'https://YOUR_PROJECT_ID-default-rtdb.YOUR_REGION.firebasedatabase.app';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'POST' && url.pathname === '/claim') {
      try {
        return await handleClaim(request, env);
      } catch (e) {
        return json({ error: 'Server error' }, 500);
      }
    }

    return new Response(HTML, {
      headers: { 'Content-Type': 'text/html; charset=utf-8' }
    });
  }
};

async function handleClaim(request, env) {
  // ── 요청 파싱 ──
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid JSON' }, 400);
  }
  const { seatId, name, color } = body;
  if (seatId === undefined || !name || !color) {
    return json({ error: 'Missing fields' }, 400);
  }

  // env.FIREBASE_SECRET 은 코드에 직접 쓰지 말고 아래 명령으로 Cloudflare에 등록하세요:
  //   wrangler secret put FIREBASE_SECRET
  // (Firebase 콘솔 > 프로젝트 설정 > 서비스 계정 > 데이터베이스 보안 비밀 에서 발급)
  const secret = env.FIREBASE_SECRET;

  // ── gameActive 확인 ──
  const activeRes = await fetch(`${FIREBASE_DB_URL}/gameActive.json?auth=${secret}`);
  const isActive = await activeRes.json();
  if (!isActive) {
    return json({ error: 'Game not active' }, 403);
  }

  // ── 이미 예매된 좌석 확인 ──
  const seatRes = await fetch(`${FIREBASE_DB_URL}/seats/${seatId}.json?auth=${secret}`);
  const existing = await seatRes.json();
  if (existing !== null) {
    return json({ error: 'Already claimed' }, 409);
  }

  // ── Firebase에 좌석 기록 ──
  const writeRes = await fetch(`${FIREBASE_DB_URL}/seats/${seatId}.json?auth=${secret}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, color })
  });

  const data = await writeRes.json();
  return json(data, writeRes.status);
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}
