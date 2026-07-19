const express = require('express');
const initSqlJs = require('sql.js');
const path = require('path');
const crypto = require('crypto');

const app = express();
const PORT = 3000;
const ADMIN_PASSWORD = 'jungboman';
const TOTAL_SEATS = 10;
const TOKEN_TTL = 60000; // 60초

// 토큰 저장소 (in-memory, 단일 사용)
const tokens = new Map(); // token -> createdAt

let db;

function dbGet(sql, params = []) {
  const stmt = db.prepare(sql);
  stmt.bind(params);
  const row = stmt.step() ? stmt.getAsObject() : null;
  stmt.free();
  return row;
}
function dbAll(sql, params = []) {
  const stmt = db.prepare(sql);
  stmt.bind(params);
  const rows = [];
  while (stmt.step()) rows.push(stmt.getAsObject());
  stmt.free();
  return rows;
}
function dbRun(sql, params = []) {
  db.run(sql, params);
}

function initDB() {
  db.run(`CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    seat_number INTEGER NOT NULL,
    reserved_at TEXT DEFAULT (datetime('now','localtime'))
  )`);
  db.run(`CREATE TABLE IF NOT EXISTS game_state (
    id INTEGER PRIMARY KEY DEFAULT 1,
    is_open INTEGER DEFAULT 0
  )`);
  const state = dbGet('SELECT id FROM game_state WHERE id=1');
  if (!state) db.run('INSERT INTO game_state (id, is_open) VALUES (1, 0)');
}

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// ────────────────────────────────────────
// 공개 API
// ────────────────────────────────────────

// 현재 예약 상태
app.get('/api/state', (req, res) => {
  const state = dbGet('SELECT * FROM game_state WHERE id=1');
  const reservations = dbAll('SELECT id, name, seat_number, reserved_at FROM reservations ORDER BY id ASC');
  res.json({
    is_open: !!state.is_open,
    total_seats: TOTAL_SEATS,
    seats_left: TOTAL_SEATS - reservations.length,
    reservations
  });
});

// 토큰 발급 (예약 전 필수)
app.get('/api/ticket', (req, res) => {
  const state = dbGet('SELECT is_open FROM game_state WHERE id=1');
  if (!state.is_open) return res.status(403).json({ error: '예약이 아직 시작되지 않았습니다.' });

  // 만료 토큰 정리
  for (const [t, ts] of tokens) {
    if (Date.now() - ts > TOKEN_TTL) tokens.delete(t);
  }

  const token = crypto.randomBytes(16).toString('hex');
  tokens.set(token, Date.now());
  res.json({ token });
});

// 예약 신청
app.post('/api/reserve', (req, res) => {
  const { name, token } = req.body;
  if (!name || !token) return res.status(400).json({ error: '이름과 토큰이 필요합니다.' });

  const state = dbGet('SELECT is_open FROM game_state WHERE id=1');
  if (!state.is_open) return res.status(403).json({ error: '예약이 마감되었습니다.' });

  // 토큰 검증 (단일 사용)
  const ts = tokens.get(token);
  if (!ts) return res.status(400).json({ error: '유효하지 않은 토큰입니다.' });
  if (Date.now() - ts > TOKEN_TTL) {
    tokens.delete(token);
    return res.status(400).json({ error: '토큰이 만료되었습니다. 다시 시도하세요.' });
  }
  tokens.delete(token);

  // 중복 이름 체크
  const existing = dbGet('SELECT id FROM reservations WHERE name=?', [name.trim()]);
  if (existing) return res.status(409).json({ error: '이미 예약된 이름입니다.' });

  // 좌석 체크
  const count = dbGet('SELECT COUNT(*) as c FROM reservations').c;
  if (count >= TOTAL_SEATS) {
    dbRun('UPDATE game_state SET is_open=0 WHERE id=1');
    return res.status(409).json({ error: '죄송합니다. 좌석이 모두 찼습니다.' });
  }

  const seat_number = count + 1;
  dbRun('INSERT INTO reservations (name, seat_number) VALUES (?,?)', [name.trim(), seat_number]);

  // 마지막 좌석이면 자동 마감
  if (seat_number >= TOTAL_SEATS) {
    dbRun('UPDATE game_state SET is_open=0 WHERE id=1');
  }

  res.json({ success: true, seat_number, message: `${name.trim()}님, ${seat_number}번 좌석 예약 완료!` });
});

// ────────────────────────────────────────
// 관리자 API
// ────────────────────────────────────────

function adminAuth(req, res, next) {
  const token = req.headers['x-admin-token'];
  if (token !== 'admin_' + Buffer.from(ADMIN_PASSWORD).toString('base64')) {
    return res.status(401).json({ error: '관리자 권한 없음' });
  }
  next();
}

app.post('/api/admin/login', (req, res) => {
  const { password } = req.body;
  if (password === ADMIN_PASSWORD) {
    res.json({ success: true, token: 'admin_' + Buffer.from(ADMIN_PASSWORD).toString('base64') });
  } else {
    res.status(401).json({ error: '비밀번호가 틀렸습니다.' });
  }
});

// 예약 열기
app.post('/api/admin/open', adminAuth, (req, res) => {
  dbRun('UPDATE game_state SET is_open=1 WHERE id=1');
  tokens.clear();
  res.json({ success: true });
});

// 예약 닫기
app.post('/api/admin/close', adminAuth, (req, res) => {
  dbRun('UPDATE game_state SET is_open=0 WHERE id=1');
  res.json({ success: true });
});

// 전체 초기화
app.post('/api/admin/reset', adminAuth, (req, res) => {
  dbRun('DELETE FROM reservations');
  dbRun('UPDATE game_state SET is_open=0 WHERE id=1');
  tokens.clear();
  res.json({ success: true });
});

// 관리자용 전체 상태
app.get('/api/admin/state', adminAuth, (req, res) => {
  const state = dbGet('SELECT * FROM game_state WHERE id=1');
  const reservations = dbAll('SELECT * FROM reservations ORDER BY id ASC');
  res.json({
    is_open: !!state.is_open,
    total_seats: TOTAL_SEATS,
    seats_left: TOTAL_SEATS - reservations.length,
    reservations
  });
});

// ────────────────────────────────────────
// 서버 시작
// ────────────────────────────────────────
async function startServer() {
  const SQL = await initSqlJs();
  db = new SQL.Database();
  initDB();
  console.log('[DB] 초기화 완료');

  return new Promise((resolve, reject) => {
    const server = app.listen(PORT, '0.0.0.0', () => {
      console.log(`[매크로실습실] 서버 시작: http://localhost:${PORT}`);
      resolve(server);
    });
    server.on('error', reject);
  });
}

if (require.main === module) {
  startServer().catch(console.error);
} else {
  module.exports = { startServer };
}
