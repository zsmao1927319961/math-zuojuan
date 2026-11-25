#!/usr/bin/env node
/* 公式默写卡数据生成器: gsbs_src/*.txt -> gsbs_data.js
   用法: node tools/build_gsbs_data.js [源目录] [输出文件]   (默认 tools/gsbs_src 与仓库根的 gsbs_data.js)
   源文件是行格式, 见 gsbs_src/_format.txt。改卡只改源文件再重跑本脚本, 不要手改 gsbs_data.js。 */
'use strict';
const fs = require('fs'), path = require('path');
const DEF_SRC = path.join(__dirname, 'gsbs_src');
const DEF_OUT = path.join(__dirname, '..', 'gsbs_data.js');
const srcDir = process.argv[2] || DEF_SRC;
const outFile = process.argv[3] || DEF_OUT;
const CYCLE = 13;                 // 首轮天数
const SRC_OK = { gs: 1, xd: 1, fl: 1 };
const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.txt') && !f.startsWith('_')).sort();
if (!files.length) { console.error('源目录里没有 .txt: ' + srcDir); process.exit(2); }

const cards = [], groups = [], MAIN = {}, fail = [], ids = {};
let sec = null, card = null, ord = 0;

function badDollars(where, field, text) {
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;
  const rest = text.replace(re, '');
  if (rest.indexOf('$') >= 0) { fail.push(where + ' ' + field + ': 有落单的 $ -> ' + JSON.stringify(rest.slice(0, 60))); return; }
  let m;
  while ((m = re.exec(text)) !== null) {
    const tex = m[1] !== undefined ? m[1] : m[2];
    if (!tex.trim()) fail.push(where + ' ' + field + ': 空公式 $$');
    if (m[1] === undefined && /\n/.test(tex)) fail.push(where + ' ' + field + ': 行内公式跨行');
  }
}
function flushCard() {
  if (!card) return;
  const where = '[' + sec.num + ' ' + card.no + ']';
  if (!card.q.length) fail.push(where + ' 缺 Q');
  if (!card.a.length) fail.push(where + ' 缺 A');
  const stem = card.q.join('\n') + (sec.pre && !card.nopre ? '\n' + sec.pre : '');
  const ans = card.a.join('\n');
  const sol = card.n.join('\n');
  badDollars(where, 'Q', stem); badDollars(where, 'A', ans); if (sol) badDollars(where, 'N', sol);
  const key = card.no.replace(/[()（）]/g, '');
  const id = (sec.src === 'fl' ? 'fl' : 's' + sec.num) + '-' + key;
  if (ids[id]) fail.push(where + ' id 重复: ' + id);
  ids[id] = 1;
  const label = (sec.src === 'fl' ? '附录' : '§' + sec.num) + '·' + card.no;
  cards.push({
    id, src: sec.src, label, kp: card.tag, group: sec.group, sec: sec.short,
    stem, ans, sol, page: sec.page, hot: sec.hot ? 1 : 0, dict: sec.day === 0 ? 1 : 0, ord: ++ord
  });
  sec.ids.push(id);
  if (sec.day > 0) (MAIN[sec.day] = MAIN[sec.day] || []).push(id);
  card = null;
}
for (const f of files) {
  const lines = fs.readFileSync(path.join(srcDir, f), 'utf8').split(/\r?\n/);
  lines.forEach((raw, i) => {
    const line = raw.replace(/\s+$/, '');
    if (!line || line.indexOf('//') === 0) return;
    if (line.indexOf('## ') === 0) {
      flushCard();
      if (!sec) { fail.push(f + ':' + (i + 1) + ' 卡出现在节之前'); return; }
      const p = line.slice(3).split(/\s+\|\s*/);
      card = { no: p[0].trim(), tag: (p[1] || '').trim(), q: [], a: [], n: [], nopre: false };
      if (!/^[（(].+[)）]$/.test(card.no)) fail.push(f + ':' + (i + 1) + ' 题号应带括号: ' + card.no);
      return;
    }
    if (line.indexOf('# ') === 0) {
      flushCard();
      const p = line.slice(2).split(/\s+\|\s*/).map(x => x.trim());
      if (p.length !== 7) { fail.push(f + ':' + (i + 1) + ' 节头应有 7 个字段: ' + line); return; }
      const [num, title, short, src, page, day, hot] = p;
      if (!SRC_OK[src]) fail.push(f + ':' + (i + 1) + ' 来源应为 gs/xd/fl: ' + src);
      const d = +day;
      if (!(d >= 0 && d <= CYCLE)) fail.push(f + ':' + (i + 1) + ' 首轮天应在 0~' + CYCLE + ': ' + day);
      if (src === 'fl' ? d !== 0 : d === 0) fail.push(f + ':' + (i + 1) + ' 只有附录的首轮天可以是 0: ' + line);
      sec = { num, title, short, src, page, day: d, hot: hot === 'hot', ids: [],
        pre: '', group: (src === 'gs' ? '高数 §' : src === 'xd' ? '线代 §' : '附录 ') + (src === 'fl' ? '' : num + ' ') + title };
      sec.short = (src === 'fl' ? '' : '§' + num + ' ') + short;
      groups.push(sec);
      return;
    }
    const m = /^(Q|A|N|P):(?: ?)(.*)$/.exec(line);
    if (m) {
      if (m[1] === 'P') { if (sec) sec.pre = m[2]; return; }
      if (!card) { fail.push(f + ':' + (i + 1) + ' 字段出现在卡之外'); return; }
      card[m[1].toLowerCase()].push(m[2]);
      return;
    }
    if (line === 'NOPRE') { if (card) card.nopre = true; return; }
    fail.push(f + ':' + (i + 1) + ' 无法识别的行: ' + line.slice(0, 50));
  });
}
flushCard();
for (const g of groups) if (!g.ids.length) fail.push('[' + g.num + '] 节里没有卡');
if (fail.length) { console.error('源文件有 ' + fail.length + ' 处问题:'); fail.forEach(x => console.error('  - ' + x)); process.exit(1); }

const now = new Date();
const today = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
const data = {
  generated: today, cycle: CYCLE, newCap: 60,
  note: '茶楠Cian《考研数学公式默写》数二范围: 高数21节+线代25节按13天首轮排期, 附录初等公式速查只浏览不排期(dict=1)。hot=按模考失分点标出的重点节。由 tools/build_gsbs_data.js 生成。',
  cards,
  MAIN,
  GROUPS: groups.map(g => ({ name: g.group, ids: g.ids }))
};
fs.writeFileSync(outFile, '/* 公式默写卡数据 · 由 tools/build_gsbs_data.js 从 tools/gsbs_src/ 生成, 勿手改 */\nwindow.GSBS_DATA=' + JSON.stringify(data) + ';\n', 'utf8');

/* ---- 汇总 ---- */
const perDay = {};
let hot = 0, dict = 0;
for (const c of cards) { if (c.dict) dict++; else hot += c.hot; }
for (let d = 1; d <= CYCLE; d++) perDay[d] = (MAIN[d] || []).length;
console.log('写出 ' + outFile + '  (' + Math.round(fs.statSync(outFile).size / 1024) + ' KB)');
console.log('卡总数 ' + cards.length + ' = 排期 ' + (cards.length - dict) + ' + 速查 ' + dict + ' ; 重点 ' + hot + ' ; 节 ' + groups.length);
for (let d = 1; d <= CYCLE; d++) {
  const secs = [...new Set(MAIN[d].map(id => cards.find(c => c.id === id).sec))];
  console.log('  D' + String(d).padStart(2) + ' ' + String(perDay[d]).padStart(3) + ' 张  ' + secs.join('、'));
}
