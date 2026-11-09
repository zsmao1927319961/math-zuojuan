// KaTeX 全量渲染验证：data/yz40.json（压轴40）stem/sol 的数学段 + z801_kp 考点名合法性
const path = require('path');
const fs = require('fs');
const BASE = 'D:/考研数学/组卷网站_static';
const katex = require(path.join(BASE, 'katex/katex.min.js'));
const DMACROS = { '\\frac': '\\dfrac' };
const d = JSON.parse(fs.readFileSync(path.join(BASE, 'data/yz40.json'), 'utf8'));
const tree = JSON.parse(fs.readFileSync(path.join(BASE, 'data/kp_tree.json'), 'utf8'));
const KSN = {};
tree.chapters.forEach(c => { KSN[c.n] = new Set(c.ks); });

function segments(str) {
  const out = [];
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;
  let m;
  while ((m = re.exec(str)) !== null) out.push({ tex: m[1] !== undefined ? m[1] : m[2], display: m[1] !== undefined });
  return out;
}
let totalSeg = 0, fails = [], oddDollar = [], svgBad = [];
for (const it of d.items) {
  for (const f of ['stem', 'sol']) {
    const t = it[f] || '';
    if (!t.includes('$')) continue;
    if (t.split('$').length % 2 === 0) oddDollar.push({ id: it.id, f, ctx: t.slice(t.length - 60) });
    for (const s of segments(t)) {
      totalSeg++;
      try { katex.renderToString(s.tex, { throwOnError: true, displayMode: s.display, macros: DMACROS }); }
      catch (e) { fails.push({ id: it.id, f, tex: s.tex.slice(0, 80), err: String(e.message).slice(0, 80) }); }
    }
    const o = (t.match(/<svg/g) || []).length, c = (t.match(/<\/svg>/g) || []).length;
    if (o !== c) svgBad.push({ id: it.id, f, o, c });
  }
  if (!KSN[it.ch] || !KSN[it.ch].has(it.kp)) fails.push({ id: it.id, kind: '考点不在树中', ch: it.ch, kp: it.kp });
}
console.log('yz40 数学段', totalSeg, '段');
console.log('渲染失败', fails.length, JSON.stringify(fails.slice(0, 10), null, 1));
console.log('$奇数', oddDollar.length, JSON.stringify(oddDollar.slice(0, 6)));
console.log('svg不配对', svgBad.length, JSON.stringify(svgBad.slice(0, 6)));
console.log(totalSeg && !fails.length && !oddDollar.length && !svgBad.length ? 'YZ40 ALL PASS' : 'YZ40 HAS FAILURES');
