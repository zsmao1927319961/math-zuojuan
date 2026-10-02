// KaTeX 全量渲染验证：qhzt + tk299 所有文本字段的数学段
// 用站点自带 katex（与线上一致），宏 DMACROS = {\frac: \dfrac}
const path = require('path');
const fs = require('fs');
const BASE = 'D:/考研数学/组卷网站_static';
const katex = require(path.join(BASE, 'katex/katex.min.js'));
const DMACROS = { '\\frac': '\\dfrac' };
const d = JSON.parse(fs.readFileSync(path.join(BASE, 'data/questions.json'), 'utf8'));

function segments(str) {
  const out = [];
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;
  let m;
  while ((m = re.exec(str)) !== null) out.push({ tex: m[1] !== undefined ? m[1] : m[2], display: m[1] !== undefined });
  return out;
}

let totalSeg = 0, fails = [];
const banks = { qhzt: [], tk299: [] };
for (const q of d) {
  if (q.source === 'qhzt') banks.qhzt.push(q);
  if (q.source === 'tk299') banks.tk299.push(q);
}
for (const [bank, qs] of Object.entries(banks)) {
  let segN = 0, fN = 0;
  for (const q of qs) {
    for (const f of ['question_text', 'answer_text', 'solution']) {
      const t = q[f] || '';
      if (!t.includes('$')) continue;
      if (t.split('$').length % 2 === 0) fails.push({ id: q.id, f, kind: '$奇数', ctx: t.slice(0, 60) });
      for (const seg of segments(t)) {
        segN++;
        try {
          katex.renderToString(seg.tex, { throwOnError: true, displayMode: seg.display, macros: DMACROS });
        } catch (e) {
          fN++;
          fails.push({ id: q.id, f, kind: 'KaTeX', tex: seg.tex.slice(0, 80), msg: String(e.message).slice(0, 90) });
        }
      }
    }
  }
  totalSeg += segN;
  console.log(bank, '题数', qs.length, '| 数学段', segN, '| 失败', fN);
}
console.log('合计数学段', totalSeg, '| 真实失败', fails.filter(x => x.kind === 'KaTeX').length, '| $奇数题', fails.filter(x => x.kind === '$奇数').length);
for (const x of fails) console.log('---', x.id, x.f, x.kind, x.msg || '', '|', (x.tex || x.ctx || '').replace(/\n/g, ' '));
