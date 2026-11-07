// txbs 卡池 KaTeX 全量渲染验证: 所有卡 stem/ans/sol 的 $..$ 数学段
const path = require('path');
const fs = require('fs');
const BASE = 'D:/考研数学/组卷网站_static';
const katex = require(path.join(BASE, 'katex/katex.min.js'));
const DMACROS = { '\\frac': '\\dfrac' };
const src = fs.readFileSync(path.join(BASE, 'txbs_data.js'), 'utf8');
const data = JSON.parse(src.replace(/^window\.TXBS_DATA=/, '').replace(/;$/, ''));

function segments(str) {
  const out = [];
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;
  let m;
  while ((m = re.exec(str)) !== null) out.push({ tex: m[1] !== undefined ? m[1] : m[2], display: m[1] !== undefined });
  return out;
}

let totalSeg = 0, fails = [];
let oddDollar = 0;
for (const c of data.cards) {
  for (const f of ['stem', 'ans', 'sol']) {
    const t = c[f] || '';
    if (!t.includes('$')) continue;
    if (t.split('$').length % 2 === 0) { oddDollar++; fails.push({ id: c.id, f, kind: '$奇数', ctx: t.slice(0, 60) }); }
    for (const seg of segments(t)) {
      totalSeg++;
      try {
        katex.renderToString(seg.tex, { throwOnError: true, displayMode: seg.display, macros: DMACROS });
      } catch (e) {
        fails.push({ id: c.id, f, kind: 'KaTeX', tex: seg.tex.slice(0, 80), msg: String(e.message).slice(0, 90) });
      }
    }
  }
}
console.log('cards:', data.cards.length, ' segments:', totalSeg, ' oddDollar:', oddDollar, ' fails:', fails.length);
for (const x of fails.slice(0, 30)) console.log(JSON.stringify(x));
