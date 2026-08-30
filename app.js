/* ============================================================
   纯静态版：无 Python 后端，全部逻辑在浏览器运行
   - questions.json / progress.json 通过 fetch 加载
   - 做题进度、笔记存 localStorage（首次自动导入现有 progress.json）
   - 出卷：高数5 + 线代5，排除已掌握，7天/15天到期优先
   ============================================================ */
let QUESTIONS = [];
let CUOTI = [];
let TODAY = [];
let STATE = null;          // progress 对象（localStorage）
let cuotiMode = 'chapter';
let cuotiSrc = '';
let cuotiReason = '';
let morePane = 'bank';

const SOURCE_NAMES = { gaoshu880: '高数880', xian_dai: '线代讲义', xian_dai880: '线代880' };
const $ = s => document.querySelector(s);
const LS_KEY = 'shuxue_progress_v1';
// 固定今日卷：8/28 那套 10 道题（用户要求恢复）
const DEFAULT_PAPER_IDS = ["gd-5-tk-9","gd-4-tk-11","gd-5-tk-11","gd-4-jd-11","gd-6-jd-4","ld-3.5-l5","ld-1.9-l2","ld-3.3-l9","ld-2.6-l4","ld-4.1-l3"];

function todayISO() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}
function addDays(iso, days) {
  const d = new Date(iso + 'T00:00:00');
  d.setDate(d.getDate() + days);
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

/* ---------- 持久化 ---------- */
function loadState() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) { /* ignore */ }
  return null;
}
function saveState() {
  try { localStorage.setItem(LS_KEY, JSON.stringify(STATE)); } catch (e) { /* 超限时忽略 */ }
}

async function init() {
  setTodayDate();
  registerSW();
  // 加载题库 + 初始化进度（优先 localStorage，否则导入 data/progress.json）
  try {
    const qr = await fetch('data/questions.json');
    QUESTIONS = await qr.json();
  } catch (e) { console.error('题库加载失败', e); }

  STATE = loadState();
  if (!STATE) {
    try {
      const pr = await fetch('data/progress.json');
      STATE = await pr.json();
      if (!STATE || typeof STATE !== 'object') STATE = { papers: [], notes: {}, question_state: {} };
      saveState();
      console.log('已导入现有 progress.json 到本地');
    } catch (e) {
      STATE = { papers: [], notes: {}, question_state: {} };
      saveState();
    }
  }
  // 一次性迁移：旧版本(无 version)时，把"今日卷"替换为 28 号那套 10 道题，
  // 然后标记版本号。之后不再强制干预（跨天/一键拼卷都按新逻辑正常走）。
  if (!STATE.version) {
    const today = todayISO();
    const old = STATE.today_paper;
    STATE.today_paper = { date: '2026-08-28', ids: DEFAULT_PAPER_IDS.slice() };
    if (old && old.ids && old.ids.length) {
      STATE.paper_history = STATE.paper_history || [];
      STATE.paper_history.push({ date: today, ids: DEFAULT_PAPER_IDS.slice(), restored: true });
      STATE.paper_history = STATE.paper_history.slice(-60);
    }
    STATE.version = 2;
    saveState();
    console.log('已将今日卷替换为 8/28 那套 10 道题');
  }

  await Promise.all([refreshCuoti(), refreshStats(), refreshWeekly()]);
  fillFilters();
  bindEvents();
  bindBackup();
  renderBank();
  renderCuoti();
  await refreshToday();
  if (TODAY.length === 0) {
    toast('今天还没出卷，正在自动生成…');
    autoGenerate(false);
  }
}

function setTodayDate() {
  const d = new Date();
  const wd = ['日','一','二','三','四','五','六'][d.getDay()];
  $('#today-date').textContent = `${d.getFullYear()}年${d.getMonth()+1}月${d.getDate()}日 · 周${wd}`;
}

function registerSW() {
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === '127.0.0.1' || location.hostname === 'localhost')) {
    navigator.serviceWorker.register('./sw.js').then((reg) => {
      // 检测是否有新版本 SW 等待激活；有则在其激活后刷新一次，强制更新缓存
      if (reg.waiting) {
        reg.waiting.postMessage({ type: 'SKIP_WAITING' });
      }
      reg.addEventListener('updatefound', () => {
        const nw = reg.installing;
        if (!nw) return;
        nw.addEventListener('statechange', () => {
          if (nw.state === 'installed' && navigator.serviceWorker.controller) {
            // 有控制器说明是旧版页面，新 SW 已装好：刷新一次加载新版
            nw.postMessage({ type: 'SKIP_WAITING' });
          }
        });
      });
      // 当新 SW 控制本页时自动 reload（仅一次），确保用户看到的是最新代码
      let refreshed = false;
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (!refreshed) { refreshed = true; location.reload(); }
      });
    }).catch(() => {});
  }
}

/* ---------- 状态派生（移植 progress.py） ---------- */
function qstate() { return STATE.question_state || (STATE.question_state = {}); }
function notes() { return STATE.notes || (STATE.notes = {}); }

function isDone(qid) { return qstate()[qid] && qstate()[qid].status === 'done'; }
function wrongIds() {
  const st = qstate();
  const done = new Set(Object.keys(st).filter(k => st[k].status === 'done'));
  const ids = new Set();
  for (const [qid, s] of Object.entries(st)) {
    if (s.status === 'review') ids.add(qid);
    else if (s.status !== 'done' && s.wrong_date) ids.add(qid);
  }
  for (const p of (STATE.papers || [])) {
    for (const [qid, r] of Object.entries(p.results || {})) {
      if (r === 'wrong' && !done.has(qid)) ids.add(qid);
    }
  }
  for (const qid of (STATE.cuoti_manual || [])) if (!done.has(qid)) ids.add(qid);
  return [...ids].sort();
}

function dueIds(today) {
  today = today || todayISO();
  const st = qstate();
  return Object.entries(st)
    .filter(([, s]) => (s.status === 'todo' && s.due && s.due <= today) || (s.status === 'review' && s.review_due && s.review_due <= today))
    .map(([qid]) => qid);
}

function recentIds(today) {
  today = today || todayISO();
  const cutoff = addDays(today, -6);
  const ids = new Set();
  for (const p of (STATE.paper_history || [])) {
    const d = p.date || '';
    if (d && cutoff <= d && d <= today) (p.ids || []).forEach(i => ids.add(i));
  }
  const tp = STATE.today_paper;
  if (tp && tp.date === today) (tp.ids || []).forEach(i => ids.add(i));
  return ids;
}

function computeStats() {
  const st = qstate();
  const done = new Set(), review = new Set(), wrong = new Set();
  for (const [qid, s] of Object.entries(st)) {
    if (s.status === 'done') done.add(qid);
    else if (s.status === 'review') review.add(qid);
    else if (s.status === 'todo' && s.wrong_date) wrong.add(qid);
  }
  for (const p of (STATE.papers || [])) {
    for (const [qid, r] of Object.entries(p.results || {})) {
      if (qid in st) continue;
      if (r === 'wrong') wrong.add(qid);
      else if (r === 'right') done.add(qid);
    }
  }
  const mastered = new Set([...done, ...review]);
  return {
    total: QUESTIONS.length,
    wrong_count: wrong.size,
    done_count: mastered.size,
    review_count: review.size,
    remaining: Math.max(0, QUESTIONS.length - mastered.size - wrong.size),
  };
}

/* ---------- 出卷（移植 autopaper.py） ---------- */
function pick(pool, n, done, due, recent) {
  const avail = pool.filter(q => !done.has(q.id) && !String(q.no || '').includes('('));
  const dueQs = avail.filter(q => due.has(q.id) && !recent.has(q.id));
  shuffle(dueQs);
  let picks = dueQs.slice(0, n);
  if (picks.length < n) {
    const have = new Set(picks.map(q => q.id));
    const others = avail.filter(q => !have.has(q.id) && !recent.has(q.id));
    shuffle(others);
    picks = picks.concat(others.slice(0, n - picks.length));
  }
  return picks;
}
function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

function pickAuto() {
  const today = todayISO();
  const st = qstate();
  const done = new Set(Object.keys(st).filter(k => st[k].status === 'done'));
  const recent = recentIds(today);
  const due = new Set(dueIds(today));
  const gaoshu = QUESTIONS.filter(q => q.source === 'gaoshu880' && (q.level || '基础') === '基础');
  const xd = QUESTIONS.filter(q => q.source === 'xian_dai');
  return pick(gaoshu, 5, done, due, recent).concat(pick(xd, 5, done, due, recent));
}

function ensureToday() {
  // 不因跨天自动换卷：只要已有今日卷就固定复用（除非用户点「一键拼卷」手动换）。
  // 这样打开网站始终显示用户上次/固定那套，避免"每天自动换题"。
  if (STATE.today_paper && STATE.today_paper.ids && STATE.today_paper.ids.length) {
    const cur = new Set(STATE.today_paper.ids);
    return STATE.today_paper.ids.filter(id => QUESTIONS.some(q => q.id === id));
  }
  const today = todayISO();
  const qs = pickAuto();
  const ids = qs.map(q => q.id);
  STATE.today_paper = { date: today, ids };
  STATE.paper_history = STATE.paper_history || [];
  STATE.paper_history.push({ date: today, ids });
  STATE.paper_history = STATE.paper_history.slice(-60);
  saveState();
  return ids;
}

function rerollToday() {
  // 手动换一套：强制重新抽 10 道，并替换今日卷（保留做题历史）
  const today = todayISO();
  const qs = pickAuto();
  const ids = qs.map(q => q.id);
  STATE.today_paper = { date: today, ids };
  STATE.paper_history = STATE.paper_history || [];
  STATE.paper_history.push({ date: today, ids, reroll: true });
  STATE.paper_history = STATE.paper_history.slice(-60);
  saveState();
  return ids;
}

/* ---------- 今日卷 ---------- */
function withLive(q) {
  const s = qstate()[q.id] || {};
  // 状态只来自做题记录(progress)；无记录才算"未做"(todo)。
  // 不再用题库自带 status 字段,避免"未做"无法变更/显示被题库 todo 覆盖。
  const st = s.status || 'todo';
  return { ...q, live: {
    status: st, wrong_date: s.wrong_date, due: s.due, review_due: s.review_due,
    right_count: s.right_count, reason: s.reason, note: notes()[q.id] || '',
    in_cuoti: wrongIds().includes(q.id),
  }};
}

async function refreshToday() {
  const ids = ensureToday();
  const qmap = new Map(QUESTIONS.map(q => [q.id, q]));
  TODAY = ids.map(id => qmap.get(id)).filter(Boolean).map(withLive);
  renderToday();
  renderTodayActions();
}

function renderToday() {
  $('#today-count').textContent = TODAY.length ? `（${TODAY.length} 题）` : '';
  $('#today-empty').hidden = TODAY.length > 0;
  const list = $('#today-list'); list.innerHTML = '';
  TODAY.forEach(q => list.appendChild(todayRow(q)));
}

function renderTodayActions() {
  const btn = $('#btn-reroll');
  if (btn) {
    btn.onclick = () => {
      if (!confirm('确定换一套新的 10 道题吗？当前题的做对/做错记录会保留。')) return;
      const ids = rerollToday();
      const qmap = new Map(QUESTIONS.map(q => [q.id, q]));
      TODAY = ids.map(id => qmap.get(id)).filter(Boolean).map(withLive);
      renderToday();
      toast('已换一套新题');
    };
  }
}

function todayRow(q) {
  const lv = q.live || {};
  let tag = '<span class="tag">未标记</span>';
  if (lv.status === 'done') tag = '<span class="tag ok">已掌握</span>';
  else if (lv.status === 'review') tag = '<span class="tag review">待巩固</span>';
  else if (lv.status === 'todo' && lv.wrong_date) tag = '<span class="tag bad">已标记做错</span>';
  const r = document.createElement('div'); r.className = 'today-row'; r.dataset.qid = q.id;
  const sub = [q.chapter_name || '', q.kp_sub || '', q.page_hint || ''].filter(Boolean).join(' · ');
  const qimg = q.question_img ? `<img class="today-qimg" src="data/${q.question_img}" alt="题目">` : '';
  const noteTxt = (lv.note || '').trim();
  r.innerHTML = `
    <div class="today-info"><div class="qname">${q.label}${tag}</div>
      <div class="qsub">${sub || SOURCE_NAMES[q.source] || ''}</div></div>
    ${qimg}
    <div class="today-note-line">${noteTxt ? `<span class="note-preview">${noteTxt.replace(/</g,'&lt;').slice(0,120)}</span>` : '<span class="note-empty">暂无笔记</span>'}</div>
    <div class="today-btns"><button class="tbtn ok">做对</button><button class="tbtn bad">做错</button></div>
    <div class="today-reasons" hidden>
      <div class="today-reason-title">这道题错在哪？（可不选）</div>
      <div class="today-chips">
        <button class="chip" data-reason="概念不清">概念不清</button>
        <button class="chip" data-reason="计算失误">计算失误</button>
        <button class="chip" data-reason="方法不会">方法不会</button>
        <button class="chip" data-reason="审题踩坑">审题踩坑</button>
      </div>
      <button class="chip cancel">直接确认</button>
    </div>`;
  const qimgEl = r.querySelector('.today-qimg');
  if (qimgEl) qimgEl.onclick = () => showModal(q);
  r.querySelector('.tbtn.ok').onclick = () => markResult(q.id, 'right');
  r.querySelector('.tbtn.bad').onclick = () => { r.querySelector('.today-reasons').hidden = false; };
  r.querySelectorAll('.today-reasons .chip[data-reason]').forEach(c => c.onclick = () => markResult(q.id, 'wrong', c.dataset.reason));
  const cancel = r.querySelector('.today-reasons .cancel');
  if (cancel) cancel.onclick = () => { r.querySelector('.today-reasons').hidden = true; };
  return r;
}

/* 更新今日列表中某题的笔记预览，避免重新打开弹窗时还是旧内容 */
function syncNotePreview(q) {
  const row = document.querySelector(`.today-row[data-qid="${CSS.escape(q.id)}"] .today-note-line`);
  if (!row) return;
  const txt = (notes()[q.id] || '').trim();
  row.innerHTML = txt
    ? `<span class="note-preview">${txt.replace(/</g, '&lt;').slice(0, 120)}</span>`
    : '<span class="note-empty">暂无笔记</span>';
}

/* 离开/刷新页面前，把还在编辑框里的笔记立即保存（防止 600ms 防抖未触发） */
window.__noteFlush = null;
window.addEventListener('pagehide', () => { if (window.__noteFlush) window.__noteFlush(); });
window.addEventListener('beforeunload', () => { if (window.__noteFlush) window.__noteFlush(); });

function markResult(id, val, reason) {
  const st = qstate();
  const prev = st[id] || {};
  const today = todayISO();
  if (val === 'right') {
    // 已在"已掌握"则不动
    if (prev.status === 'done') return;
    // 防误触/连点：同一天内已做过"做对"(review)的题，再点做对不升级为 done(已掌握)
    // 二刷确认(done)必须发生在 review_due 到期之后(至少隔天)，避免"连点两次就掌握"
    if (prev.status === 'review') {
      if (prev.right_date === today) {
        // 当天重复点"做对"：保持 review，不做任何状态变化
        toast('今天已标记做对，进入待巩固；二刷确认将在到期后');
        return;
      }
      const cnt = (prev.right_count || 0) + 1;
      st[id] = { status: 'done', right_date: today, right_count: cnt };
    } else {
      const cnt = (prev.right_count || 0) + 1;
      st[id] = { status: 'review', right_date: today, review_due: addDays(today, 15), right_count: cnt };
    }
  } else {
    // 做错：始终覆盖为待重做（todo），无论之前是 review 还是别的
    const s = { status: 'todo', wrong_date: today, due: addDays(today, 7) };
    if (reason) s.reason = reason;
    st[id] = s;
  }
  STATE.papers = STATE.papers || [];
  STATE.papers.push({ id: 'web-' + Date.now(), date: today, results: { [id]: val }, reasons: reason ? { [id]: reason } : {} });
  saveState();
  refreshCuoti(); refreshStats(); refreshWeekly(); refreshToday();
  if (val === 'right') {
    toast(st[id].status === 'done' ? '二刷确认，已彻底掌握' : '已做对，进入待巩固（15天后二刷）');
  } else {
    toast('已标记做错，进入错题本');
  }
}

async function autoGenerate(with_answer) {
  // 「一键拼卷」：生成一套新的今日卷（换新题），不生成 PDF
  const ids = rerollToday();
  const qmap = new Map(QUESTIONS.map(q => [q.id, q]));
  TODAY = ids.map(id => qmap.get(id)).filter(Boolean).map(withLive);
  renderToday();
  toast('已拼好新卷（10题），需要PDF请点「生成PDF」');
}

/* ---------- 题库（更多页） ---------- */
function fillFilters() {
  const sources = [...new Set(QUESTIONS.map(q => q.source))];
  const chapters = [...new Set(QUESTIONS.map(q => q.chapter))];
  const types = [...new Set(QUESTIONS.map(q => q.type).filter(Boolean))];
  fillSelect('#f-source', sources.map(s => ({ value: s, text: SOURCE_NAMES[s] || s })));
  fillGroupedSelect('#f-chapter', [
    { label: '高数', items: chapters.filter(c => QUESTIONS.some(q => q.chapter === c && q.source === 'gaoshu880'))
        .map(c => ({ value: c, text: QUESTIONS.find(q => q.chapter === c && q.source === 'gaoshu880').chapter_name })) },
    { label: '线代讲义', items: chapters.filter(c => QUESTIONS.some(q => q.chapter === c && q.source === 'xian_dai'))
        .map(c => ({ value: c, text: QUESTIONS.find(q => q.chapter === c && q.source === 'xian_dai').chapter_name })) },
    { label: '线代880', items: chapters.filter(c => QUESTIONS.some(q => q.chapter === c && q.source === 'xian_dai880'))
        .map(c => ({ value: c, text: QUESTIONS.find(q => q.chapter === c && q.source === 'xian_dai880').chapter_name })) },
  ]);
  fillSelect('#f-type', types.map(t => ({ value: t, text: t })));
  const kps = [...new Set(QUESTIONS.map(q => q.kp_sub).filter(Boolean))].sort();
  fillSelect('#f-kp', kps.map(k => ({ value: k, text: k })));
  const levels = [...new Set(QUESTIONS.map(q => q.level).filter(Boolean))];
  fillSelect('#f-level', [{ value: '基础', text: '基础' }, { value: '综合', text: '综合' }, { value: '拓展', text: '拓展' }].filter(o => levels.includes(o.value)));
}
function fillSelect(sel, options) {
  const el = document.querySelector(sel); if (!el) return;
  options.forEach(o => { const n = document.createElement('option'); n.value = o.value; n.textContent = o.text; el.appendChild(n); });
}
function fillGroupedSelect(sel, groups) {
  const el = document.querySelector(sel); if (!el) return;
  groups.forEach(g => {
    const og = document.createElement('optgroup'); og.label = g.label;
    g.items.forEach(o => { const n = document.createElement('option'); n.value = o.value; n.textContent = o.text; og.appendChild(n); });
    el.appendChild(og);
  });
}
function groupBy(items, keyFn) {
  const map = new Map();
  items.forEach(it => { const k = keyFn(it); if (!map.has(k)) map.set(k, []); map.get(k).push(it); });
  return [...map.entries()].map(([name, arr]) => ({ name, items: arr }));
}

function renderBank() {
  if (!QUESTIONS.length) return;
  const f = { source: $('#f-source').value, chapter: $('#f-chapter').value, type: $('#f-type').value, kp: $('#f-kp').value, level: $('#f-level').value };
  const qs = QUESTIONS.filter(q => (!f.source || q.source === f.source) && (!f.chapter || String(q.chapter) === String(f.chapter)) && (!f.type || q.type === f.type) && (!f.kp || q.kp_sub === f.kp) && (!f.level || q.level === f.level));
  const list = $('#list'); if (!list) return; list.innerHTML = '';
  const order = ['基础', '综合', '拓展'];
  const levels = [...new Set(qs.map(q => q.level).filter(Boolean))].sort((a, b) => order.indexOf(a) - order.indexOf(b));
  levels.forEach(lv => {
    const lg = qs.filter(q => q.level === lv);
    const lhead = document.createElement('div'); lhead.className = 'group-head level-head';
    lhead.innerHTML = `<span>${lv}题</span><span class="tag">${lg.length}</span>`;
    list.appendChild(lhead);
    groupBy(lg, q => q.chapter_name || q.chapter).forEach(g => {
      const head = document.createElement('div'); head.className = 'group-head';
      const srcTag = g.items[0] && g.items[0].source === 'xian_dai' ? '线代' : '高数';
      head.innerHTML = `<span>${g.name}</span><span class="tag">${srcTag} · ${g.items.length}</span>`;
      list.appendChild(head);
      const byType = {};
      g.items.forEach(q => { const t = q.type || '题目'; (byType[t] = byType[t] || []).push(q); });
      Object.keys(byType).forEach(t => {
        const sub = document.createElement('div'); sub.className = 'type-head'; sub.textContent = t + '题';
        list.appendChild(sub);
        byType[t].forEach(q => list.appendChild(qrow(withLive(q))));
      });
    });
  });
}

function qrow(q) {
  const r = document.createElement('div'); const lv = q.live || {};
  let tags = '';
  if (lv.status === 'done') tags += '<span class="tag ok">已掌握</span>';
  else if (lv.status === 'review') tags += '<span class="tag review">待巩固</span>';
  else if (lv.due) tags += '<span class="tag bad">待重做</span>';
  else if (lv.status === 'todo' && lv.wrong_date) tags += '<span class="tag bad">已标记做错</span>';
  else tags += '<span class="tag">未做</span>';
  if (lv.reason) tags += `<span class="tag reason">${lv.reason}</span>`;
  if (q.kp_sub) tags += `<span class="tag">${q.kp_sub}</span>`;
  r.innerHTML = `<div class="qinfo"><div class="qname">${q.label}${tags}</div><div class="qsub">${SOURCE_NAMES[q.source] || ''}${q.page_hint ? ' · ' + q.page_hint : ''}</div></div>`;
  r.onclick = () => showModal(q);
  return r;
}

/* ---------- 错题本 ---------- */
async function refreshCuoti() {
  const wids = wrongIds();
  const qmap = new Map(QUESTIONS.map(q => [q.id, q]));
  CUOTI = wids.map(id => qmap.get(id)).filter(Boolean).map(withLive);
  const badge = $('#cuoti-badge');
  if (badge) { badge.hidden = CUOTI.length === 0; badge.textContent = CUOTI.length > 99 ? '99+' : CUOTI.length; }
}

function renderCuoti() {
  const qs = CUOTI.filter(q => (!cuotiSrc || q.source === cuotiSrc) && (!cuotiReason || (q.live && q.live.reason) === cuotiReason));
  const cnt = $('#cuoti-count'), list = $('#cuoti-list'), empty = $('#cuoti-empty');
  if (!list) return;
  if (cnt) cnt.textContent = `全部 ${qs.length} 道题`;
  if (empty) empty.hidden = qs.length > 0;
  list.innerHTML = '';
  const groups = cuotiMode === 'kp' ? groupBy(qs, q => q.kp_sub || '未分类') : groupBy(qs, q => q.chapter_name || q.chapter);
  groups.forEach(g => {
    const head = document.createElement('div'); head.className = 'group-head';
    head.innerHTML = `<span>${g.name}</span><span class="tag">${g.items.length}</span>`;
    list.appendChild(head);
    g.items.forEach(q => list.appendChild(cuotiRow(q)));
  });
}
function cuotiRow(q) {
  const r = document.createElement('div'); r.className = 'qrow'; const lv = q.live || {};
  let tags = `<span class="tag">${SOURCE_NAMES[q.source] || ''}</span>`;
  if (lv.status === 'review') tags += '<span class="tag review">待巩固</span>';
  if (lv.due) tags += '<span class="tag bad">第7天重做</span>';
  if (lv.reason) tags += `<span class="tag reason">${lv.reason}</span>`;
  if (q.kp_sub) tags += `<span class="tag">${q.kp_sub}</span>`;
  r.innerHTML = `<div class="qinfo"><div class="qname">${q.label}${tags}</div><div class="qsub">${lv.wrong_date ? '错题日期 ' + lv.wrong_date : ''}${lv.due ? ' · ' + lv.due + ' 重做' : ''}${lv.review_due ? ' · ' + lv.review_due + ' 二刷' : ''}</div></div>`;
  r.onclick = () => showModal(q);
  return r;
}

/* ---------- 我的 / 统计 / 周报 ---------- */
async function refreshStats() {
  const s = computeStats();
  const el = $('#stats');
  if (el) el.innerHTML = `<div style="font-size:15px;font-weight:700;">学习统计</div>
    <div class="stat-nums">
      <div class="stat-item"><b>${s.total}</b><span>题库总数</span></div>
      <div class="stat-item"><b>${s.done_count}</b><span>已做对</span></div>
      <div class="stat-item"><b>${s.review_count}</b><span>待巩固</span></div>
      <div class="stat-item"><b>${s.wrong_count}</b><span>做错过</span></div>
      <div class="stat-item"><b>${s.remaining}</b><span>未做</span></div>
    </div>`;
}

async function refreshWeekly() {
  const el = $('#weekly'); if (!el) return;
  const today = todayISO(), start = addDays(today, -6);
  const qmap = new Map(QUESTIONS.map(q => [q.id, q]));
  const wrongCnt = {}, reasonCnt = {}, kpCnt = {}, chCnt = {};
  const seen = new Set();
  for (const p of (STATE.papers || [])) {
    const d = p.date || '';
    if (!(start <= d && d <= today)) continue;
    for (const [qid, r] of Object.entries(p.results || {})) {
      if (r !== 'wrong' || seen.has(qid + '|' + d)) continue;
      seen.add(qid + '|' + d);
      const q = qmap.get(qid) || {};
      const reason = (p.reasons || {})[qid] || '未标注';
      wrongCnt[qid] = (wrongCnt[qid] || 0) + 1;
      reasonCnt[reason] = (reasonCnt[reason] || 0) + 1;
      const kp = q.kp_sub || q.kp || '未分类'; kpCnt[kp] = (kpCnt[kp] || 0) + 1;
      const ch = q.chapter_name || q.chapter || '未分类'; chCnt[ch] = (chCnt[ch] || 0) + 1;
    }
  }
  const byReason = Object.entries(reasonCnt).sort((a,b)=>b[1]-a[1]);
  const byKp = Object.entries(kpCnt).sort((a,b)=>b[1]-a[1]).slice(0,8);
  const byChapter = Object.entries(chCnt).sort((a,b)=>b[1]-a[1]);
  const total = Object.values(wrongCnt).reduce((a,b)=>a+b,0);
  let html = `<div class="wk-card"><h3>本周总结</h3><div class="wk-sub">${start} ~ ${today}</div>`;
  if (!total) html += '<p style="color:var(--sub);font-size:13px;margin:8px 0;">本周还没有错题记录，继续保持！</p>';
  else {
    const maxC = Math.max(...byChapter.map(x=>x[1]),1), maxK = Math.max(...byKp.map(x=>x[1]),1), maxR = Math.max(...byReason.map(x=>x[1]),1);
    html += `<div class="wk-nums"><div class="wk-num"><b>${total}</b><span>做错次数</span></div><div class="wk-num"><b>${Object.keys(wrongCnt).length}</b><span>涉及题目</span></div></div>`;
    if (byChapter.length) { html += `<div class="wk-section"><b>错得最多的章节</b>`; byChapter.forEach(([ch,c])=>{ html += `<div class="wk-row"><span class="wk-label">${ch}</span><span class="wk-cnt">${c} 次</span></div><div class="wk-bar"><i style="width:${Math.round(c/maxC*100)}%"></i></div>`; }); html += '</div>'; }
    if (byKp.length) { html += `<div class="wk-section"><b>错题涉及的知识点</b>`; byKp.forEach(([k,c])=>{ html += `<div class="wk-row"><span class="wk-label">${k}</span><span class="wk-cnt">${c} 次</span></div><div class="wk-bar"><i style="width:${Math.round(c/maxK*100)}%"></i></div>`; }); html += '</div>'; }
    if (byReason.length) { html += `<div class="wk-section"><b>错因分布</b>`; byReason.forEach(([r,c])=>{ html += `<div class="wk-row"><span class="wk-label">${r}</span><span class="wk-cnt">${c} 次</span></div><div class="wk-bar"><i style="width:${Math.round(c/maxR*100)}%"></i></div>`; }); html += '</div>'; }
  }
  html += '</div>';
  el.innerHTML = html;
}

/* ---------- 导出 / 导入进度备份 ---------- */
function bindBackup() {
  const btnExp = $('#btn-export'), btnImp = $('#btn-import'), file = $('#import-file');
  if (!btnExp) return;
  btnExp.onclick = () => {
    const blob = new Blob([JSON.stringify(STATE, null, 1)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `数学组卷备份_${todayISO()}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    toast('已导出备份，请存到 iPad 文件/iCloud');
  };
  btnImp.onclick = () => file.click();
  file.onchange = () => {
    const f = file.files[0];
    if (!f) return;
    const rd = new FileReader();
    rd.onload = () => {
      try {
        const obj = JSON.parse(rd.result);
        if (!obj || typeof obj !== 'object') throw new Error('格式不对');
        STATE = obj;
        saveState();
        refreshCuoti(); refreshStats(); refreshWeekly(); refreshToday(); renderBank();
        toast('导入成功');
      } catch (e) { toast('导入失败：' + e.message); }
    };
    rd.readAsText(f);
    file.value = '';
  };
}

/* ---------- 题目弹窗 + 笔记 ---------- */
function showModal(q) {
  const m = $('#modal'); const lv = q.live || {};
  let tags = `<span class="tag">${SOURCE_NAMES[q.source] || ''}</span>`;
  if (lv.status === 'done') tags += '<span class="tag ok">已掌握</span>';
  else if (lv.status === 'review') tags += '<span class="tag review">待巩固</span>';
  else if (lv.due) tags += '<span class="tag bad">待重做</span>';
  if (q.kp_sub) tags += `<span class="tag">${q.kp_sub}</span>`;
  const img = q.question_img ? `<img src="data/${q.question_img}" alt="题目">` : '<div class="placeholder">本题无图</div>';
  const ans = q.answer_img ? `<img src="data/${q.answer_img}" alt="答案">`
    : (q.answer_text ? `<div class="answer-text katex-render" id="katex-answer"></div>`
      : (q.note ? `<div class="answer-text">方法：${q.note}</div>` : ''));
  m.innerHTML = `
    <div id="modal-mask"></div>
    <div id="modal-box">
      <div id="modal-head"><span id="modal-label">${q.label}</span><button id="modal-close">×</button></div>
      <div id="modal-tags">${tags}</div>
      <div id="modal-img">${img}</div>
      ${ans ? `<div id="modal-ans-box"><div class="today-reason-title">答案</div>${ans}</div>` : ''}
      <div id="modal-note-box">
        <div class="today-reason-title">我的笔记（可写思路/易错点，自动保存）</div>
        <textarea id="modal-note" rows="3" placeholder="例如：这题不能硬算，先观察对称性……">${(notes()[q.id] || lv.note || '').replace(/</g,'&lt;')}</textarea>
        <div class="note-save-hint" id="note-save-hint">上次保存：--</div>
      </div>
      <div id="modal-actions">
        <button class="btn ok" data-act="right">做对</button>
        <button class="btn bad" data-act="wrong">做错</button>
        <button class="btn" data-act="close">关闭</button>
      </div>
    </div>`;
  // 答案公式：katex.render 直接渲染；KaTeX 未加载时降级为纯文本（保证可见）
  const kr = m.querySelector('#katex-answer');
  if (kr && q.answer_text) {
    if (window.katex) {
      try { window.katex.render(q.answer_text, kr, { throwOnError: false }); }
      catch(e) { kr.textContent = q.answer_text; }
    } else {
      // KaTeX CDN 未加载/离线：显示原始文本（比空白好）
      let txt = q.answer_text.replace(/\$|\\(frac|sqrt|ln|pi|sin|cos|tan|left|right|cdot|begin|end|pmatrix|int|theta|arcsin|arctan|cosh|Big|O|and|or|text)\{?/g, m => (m[1] ? {frac:'/',sqrt:'√',ln:'ln',pi:'π',sin:'sin',cos:'cos',tan:'tan',left:'',right:'',cdot:'·',begin:'',end:'',pmatrix:'矩阵',int:'∫',theta:'θ',arcsin:'arcsin',arctan:'arctan',cosh:'cosh',Big:'',O:'O',text:''}[m[1]] || '' : m));
      kr.textContent = txt || q.answer_text;
    }
  }
  const noteEl = m.querySelector('#modal-note'), hintEl = m.querySelector('#note-save-hint');
  let timer = null;
  const saveNote = () => {
    clearTimeout(timer);
    notes()[q.id] = noteEl.value;
    if (q.live) q.live.note = noteEl.value;
    saveState();
    syncNotePreview(q);
    const d = new Date();
    hintEl.textContent = `上次保存：${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
  };
  window.__noteFlush = saveNote;
  noteEl.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(saveNote, 600); });
  m.hidden = false;
  m.querySelector('#modal-close').onclick = () => { saveNote(); closeModal(); };
  m.querySelector('#modal-mask').onclick = () => { saveNote(); closeModal(); };
  m.querySelector('[data-act="right"]').onclick = () => { saveNote(); closeModal(); markResult(q.id, 'right'); };
  m.querySelector('[data-act="wrong"]').onclick = () => { saveNote(); closeModal(); markResult(q.id, 'wrong'); };
  m.querySelector('[data-act="close"]').onclick = () => { saveNote(); closeModal(); };
}
function closeModal() {
  $('#modal').hidden = true;
  window.__noteFlush = null;
}

/* ---------- 导航 / 事件 ---------- */
function switchTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('#tabbar .tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === name));
  const tab = $('#tab-' + name); if (tab) tab.classList.add('active');
  $('#page-title').textContent = { zuojuan: '今日拼卷', more: '更多' }[name];
}
function switchMorePane(name) {
  morePane = name;
  document.querySelectorAll('#more-nav .chip').forEach(c => c.classList.toggle('active', c.dataset.more === name));
  document.querySelectorAll('.more-pane').forEach(p => p.classList.toggle('active', p.id === 'more-' + name));
  if (name === 'bank') renderBank();
  if (name === 'cuoti') renderCuoti();
}
function bindEvents() {
  $('#btn-auto').onclick = () => autoGenerate(false);
  $('#btn-print').onclick = () => window.print();
  ['#f-source','#f-chapter','#f-type','#f-kp','#f-level'].forEach(s => $(s).onchange = renderBank);
  document.querySelectorAll('#tabbar .tab-btn').forEach(b => b.onclick = () => switchTab(b.dataset.tab));
  document.querySelectorAll('#more-nav .chip').forEach(c => c.onclick = () => switchMorePane(c.dataset.more));
  document.querySelectorAll('#cuoti-mode .chip').forEach(c => c.onclick = () => { cuotiMode = c.dataset.mode; document.querySelectorAll('#cuoti-mode .chip').forEach(x => x.classList.toggle('active', x === c)); renderCuoti(); });
  document.querySelectorAll('#cuoti-source .chip').forEach(c => c.onclick = () => { cuotiSrc = c.dataset.src; document.querySelectorAll('#cuoti-source .chip').forEach(x => x.classList.toggle('active', x === c)); renderCuoti(); });
  document.querySelectorAll('#cuoti-reason .chip').forEach(c => c.onclick = () => { cuotiReason = c.dataset.reason; document.querySelectorAll('#cuoti-reason .chip').forEach(x => x.classList.toggle('active', x === c)); renderCuoti(); });
}
function toast(msg) {
  const t = $('#toast'); t.textContent = msg; t.hidden = false;
  clearTimeout(t._timer); t._timer = setTimeout(() => { t.hidden = true; }, 2600);
}

init();
