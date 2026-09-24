// /api/atoms — la constellation.
//   GET  /api/atoms                  → les atomes visibles (mis en cache 20 s sur le CDN)
//   GET  /api/atoms?challenge=1      → un petit calcul à résoudre avant d'écrire (preuve de travail)
//   POST /api/atoms                  → ajouter son atome
//   POST /api/atoms?report=<id>      → signaler un atome (masqué à partir de 3 signalements)
// Variables d'environnement : SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, ATOMS_SECRET (sel et signature),
// facultatives : TURNSTILE_SECRET_KEY (Cloudflare), ATOMS_MODERATION=1 (tout passe en attente), ATOMS_ORIGINS.
const crypto = require('crypto');

const LIMIT = 600, POW_BITS = 16, CHALLENGE_TTL = 10 * 60e3, MIN_FILL_MS = 2500;
const PER_10MIN = 2, PER_DAY = 6;
const ORIGINS = (process.env.ATOMS_ORIGINS || 'https://areweai.dev,https://www.areweai.dev').split(',').map(s => s.trim()).filter(Boolean);
const BLOCK = ['nigger', 'nigga', 'faggot', 'kike', 'retard', 'pute', 'salope', 'enculé', 'encule', 'connard', 'fdp', 'ntm', 'viagra', 'casino', 'porn', 'xxx', 'onlyfans', 'crypto giveaway', 'airdrop', 'bitcoin', 'forex', 'telegram', 'whatsapp'];

const secret = () => process.env.ATOMS_SECRET || 'dev-secret-change-me';
const sha = s => crypto.createHash('sha256').update(s).digest('hex');
const hmac = s => crypto.createHmac('sha256', secret()).update(s).digest('hex').slice(0, 32);
const json = (res, code, body, cache) => {
  res.statusCode = code;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', cache || 'no-store');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.end(JSON.stringify(body));
};

function db(path, opts = {}) {
  const url = process.env.SUPABASE_URL, key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw Object.assign(new Error('database not configured'), { code: 503 });
  return fetch(`${url.replace(/\/$/, '')}/rest/v1/${path}`, {
    ...opts,
    headers: { apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json', ...(opts.headers || {}) }
  });
}

const clientIp = req => String(req.headers['x-real-ip'] || (req.headers['x-forwarded-for'] || '').split(',')[0] || req.socket?.remoteAddress || '0').trim();
const ipHash = req => sha(clientIp(req) + '|' + secret()).slice(0, 40);

// texte propre : pas de caractères de contrôle ni invisibles, espaces normalisés
const clean = s => String(s || '').normalize('NFC').replace(/[\u0000-\u001f\u007f-\u009f​-‏‪-‮⁠-⁯﻿]/g, ' ').replace(/\s+/g, ' ').trim();

function checkText(name, message) {
  if (name.length < 1 || name.length > 24) return 'name';
  if (message.length < 3 || message.length > 140) return 'message';
  const both = (name + ' ' + message).toLowerCase();
  if (/(https?:\/\/|www\.|\b[a-z0-9-]+\.(com|net|org|io|ru|cn|xyz|top|link|click|ly|gg|me|co|app|dev|fr|de)\b|@[a-z0-9_]{3,}\.|<\s*\/?\s*[a-z])/i.test(both)) return 'link';
  if (/(.)\1{7,}/.test(both)) return 'spam';
  if (BLOCK.some(w => both.includes(w))) return 'words';
  const letters = message.replace(/[^A-Za-z]/g, '');
  if (letters.length > 20 && letters === letters.toUpperCase()) return 'caps';
  return null;
}

function newChallenge() {
  const c = `${Date.now()}.${crypto.randomBytes(8).toString('hex')}`;
  return { challenge: `${c}.${hmac(c)}`, bits: POW_BITS };
}
function checkPow(challenge, nonce) {
  const parts = String(challenge || '').split('.');
  if (parts.length !== 3) return false;
  const [ts, rnd, sig] = parts, c = `${ts}.${rnd}`;
  if (hmac(c) !== sig || !(Date.now() - +ts < CHALLENGE_TTL)) return false;
  const h = sha(`${challenge}:${nonce}`);
  let zeros = 0;
  for (const ch of h) { const v = parseInt(ch, 16); if (v === 0) { zeros += 4; continue; } zeros += Math.clz32(v) - 28; break; }
  return zeros >= POW_BITS;
}

async function turnstileOk(token, req) {
  const key = process.env.TURNSTILE_SECRET_KEY; if (!key) return true;
  if (!token) return false;
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ secret: key, response: token, remoteip: clientIp(req) }) });
  const d = await r.json().catch(() => ({})); return !!d.success;
}

async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') return JSON.parse(req.body || '{}');
  let raw = ''; for await (const ch of req) { raw += ch; if (raw.length > 4096) throw Object.assign(new Error('too large'), { code: 413 }); }
  return JSON.parse(raw || '{}');
}

async function recentCount(ip, sinceMs) {
  const since = new Date(Date.now() - sinceMs).toISOString();
  const r = await db(`atoms?select=id&ip_hash=eq.${ip}&created_at=gte.${encodeURIComponent(since)}`, { method: 'HEAD', headers: { Prefer: 'count=exact' } });
  const cr = r.headers.get('content-range') || '*/0'; return +cr.split('/')[1] || 0;
}

module.exports = async function handler(req, res) {
  try {
    const q = new URL(req.url, 'http://x').searchParams;
    if (req.method === 'GET' && q.get('challenge')) return json(res, 200, newChallenge());
    if (req.method === 'GET') {
      const r = await db(`atoms?select=id,created_at,name,country,message,shape,color&status=eq.visible&order=id.desc&limit=${LIMIT}`);
      if (!r.ok) return json(res, 502, { error: 'db' });
      return json(res, 200, { atoms: await r.json() }, 'public, s-maxage=20, stale-while-revalidate=120');
    }
    if (req.method !== 'POST') { res.setHeader('Allow', 'GET, POST'); return json(res, 405, { error: 'method' }); }

    // les écritures ne viennent que du site
    const origin = req.headers.origin || '';
    if (ORIGINS.length && origin && !ORIGINS.includes(origin) && !/^http:\/\/localhost(:\d+)?$/.test(origin)) return json(res, 403, { error: 'origin' });
    if (!/application\/json/.test(req.headers['content-type'] || '')) return json(res, 415, { error: 'type' });
    const body = await readBody(req), ip = ipHash(req);

    if (q.get('report')) {
      const id = parseInt(q.get('report'), 10); if (!(id > 0)) return json(res, 400, { error: 'id' });
      if (!checkPow(body.challenge, body.nonce)) return json(res, 400, { error: 'pow' });
      const r = await db('rpc/report_atom', { method: 'POST', body: JSON.stringify({ aid: id, ip }) });
      return json(res, r.ok ? 200 : 502, { ok: r.ok });
    }

    // 1. le pot de miel, le temps de remplissage, la preuve de travail, Turnstile si configuré
    if (body.website) return json(res, 200, { ok: true, ignored: true });
    if (!(+body.elapsed >= MIN_FILL_MS)) return json(res, 400, { error: 'fast' });
    if (!checkPow(body.challenge, body.nonce)) return json(res, 400, { error: 'pow' });
    if (!(await turnstileOk(body.turnstile, req))) return json(res, 400, { error: 'captcha' });

    // 2. le contenu
    const name = clean(body.name), message = clean(body.message);
    const bad = checkText(name, message); if (bad) return json(res, 422, { error: bad });
    const shape = parseInt(body.shape, 10), color = parseInt(body.color, 10);
    if (!(shape >= 0 && shape <= 5) || !(color >= 0 && color <= 7)) return json(res, 422, { error: 'style' });
    const cc = String(req.headers['x-vercel-ip-country'] || '').toUpperCase();
    const country = body.hideCountry || !/^[A-Z]{2}$/.test(cc) ? null : cc;
    const lang = /^[a-z]{2}$/.test(body.lang || '') ? body.lang : null;

    // 3. le rythme : quelques atomes par personne, pas de doublon
    if (await recentCount(ip, 10 * 60e3) >= PER_10MIN || await recentCount(ip, 24 * 3600e3) >= PER_DAY) return json(res, 429, { error: 'rate' });
    const dup = await db(`atoms?select=id&message=eq.${encodeURIComponent(message)}&created_at=gte.${encodeURIComponent(new Date(Date.now() - 24 * 3600e3).toISOString())}&limit=1`);
    if (dup.ok && (await dup.json()).length) return json(res, 409, { error: 'duplicate' });

    const status = process.env.ATOMS_MODERATION === '1' ? 'pending' : 'visible';
    const r = await db('atoms?select=id,created_at,name,country,message,shape,color,status', { method: 'POST', headers: { Prefer: 'return=representation' }, body: JSON.stringify({ name, message, shape, color, country, lang, ip_hash: ip, status }) });
    if (!r.ok) return json(res, 502, { error: 'db' });
    const [atom] = await r.json();
    return json(res, 201, { atom });
  } catch (e) {
    return json(res, e.code === 413 ? 413 : e.code === 503 ? 503 : e instanceof SyntaxError ? 400 : 500, { error: e.code === 503 ? 'unconfigured' : 'server' });
  }
};
module.exports.config = { maxDuration: 10 };
