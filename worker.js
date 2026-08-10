import HTML from './index.html';

const FIREBASE_DB_URL = 'https://macro-classroom-default-rtdb.asia-southeast1.firebasedatabase.app';
const WINDOW_MS   = 10000; // 10초 윈도우
const MAX_REQUESTS = 50;   // 윈도우당 최대 요청 수 (학생 40명 + 여유)

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'POST' && url.pathname === '/claim') {
      return handleClaim(request, env);
    }

    return new Response(HTML, {
      headers: { 'Content-Type': 'text/html; charset=utf-8' }
    });
  }
};

async function handleClaim(request, env) {
  // ── 속도 제한: IP당 10초에 50개 ──
  const ip     = request.headers.get('CF-Connecting-IP') || 'unknown';
  const window = Math.floor(Date.now() / WINDOW_MS);
  const key    = `rl:${ip}:${window}`;

  const count = parseInt(await env.RATE_LIMIT.get(key) || '0');
  if (count >= MAX_REQUESTS) {
    return json({ error: 'Rate limited' }, 429);
  }
  await env.RATE_LIMIT.put(key, String(count + 1), { expirationTtl: 20 });

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
