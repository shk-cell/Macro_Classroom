import HTML from './index.html';

const FIREBASE_DB_URL = 'https://macro-classroom-default-rtdb.asia-southeast1.firebasedatabase.app';
const COOLDOWN_MS = 1000; // IP당 최소 예매 간격 (ms)

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
  // ── 속도 제한: IP당 1초에 1개 ──
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const key = `rl:${ip}`;
  const last = await env.RATE_LIMIT.get(key);

  if (last && Date.now() - parseInt(last) < COOLDOWN_MS) {
    return json({ error: 'Too fast' }, 429);
  }
  await env.RATE_LIMIT.put(key, String(Date.now()), { expirationTtl: 10 });

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
