// ensureToday 剔除已掌握+补新 逻辑模拟测试（不入库，仅本地验证）
const fs = require('fs');
const src = fs.readFileSync('app.js', 'utf8');
const grab = n => {
  const m = src.match(new RegExp('function ' + n + '([\\s\\S]*?\\n})'));
  if (!m) throw new Error(n + ' not found');
  return 'function ' + n + m[1];
};
let QUESTIONS = [];
let STATE = {};
const toasts = [];
globalThis.toast = s => toasts.push(s);
globalThis.saveState = () => {};
for (const n of ['todayISO', 'addDays', 'qstate', 'isDone', 'dueIds', 'recentIds', 'pick', 'shuffle', 'pickAuto', 'ensureToday']) {
  eval(grab(n));
}
// 构造题库: 10道高数ch1 + 10道线代880 + 10道线代讲义
const qs = [];
for (let i = 1; i <= 10; i++) qs.push({ id: 'gd1-' + i, source: 'gaoshu880', chapter: '第一章', level: '基础', no: String(i) });
for (let i = 1; i <= 10; i++) qs.push({ id: 'ld880-' + i, source: 'xian_dai880', chapter: '', no: String(i) });
for (let i = 1; i <= 10; i++) qs.push({ id: 'xd-' + i, source: 'xian_dai', chapter: '', no: String(i) });
QUESTIONS = qs;
STATE = {
  question_state: { 'gd1-1': { status: 'done' }, 'gd1-2': { status: 'done' }, 'ld880-1': { status: 'done' } },
  paper_history: [{ date: '2026-10-09', ids: ['gd1-3', 'ld880-2'] }],
  papers: []
};
// 旧卷(10-09): 3道已掌握 + 3道未做
STATE.today_paper = { date: '2026-10-09', ids: ['gd1-1', 'gd1-2', 'ld880-1', 'gd1-4', 'ld880-3', 'xd-5'] };
const ids = ensureToday();
const doneIds = new Set(['gd1-1', 'gd1-2', 'ld880-1']);
console.log('新卷:', ids.join(','));
console.log('已掌握全被剔除:', ids.every(i => !doneIds.has(i)));
console.log('未做的旧题保留:', ['gd1-4', 'ld880-3', 'xd-5'].every(i => ids.includes(i)));
console.log('长度保持(3旧+3新):', ids.length === 6);
console.log('toast:', toasts);
// 当天卷不动的分支
STATE.today_paper = { date: new Date().toISOString().slice(0, 10), ids: ['gd1-1'] };
toasts.length = 0;
console.log('当天卷含已掌握也原样保留:', ensureToday().join(',') === 'gd1-1', '| 无toast:', toasts.length === 0);
