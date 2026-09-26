/* 生成 data/knowledge.json
 * 知识树结构完全取自 cxyonly.fans 的 /api/categories（高数 7 章 + 线代 7 章），
 * 本地题库按 source|kp_sub 映射到它的知识点节点；通信原理无对应树，按 26 个专题自建。
 * 重新生成：node tools/gen_knowledge.js
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');

const qs = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'questions.json'), 'utf8'));

/* ---------- 高数：kp_sub → 节点id（对照 cxyonly 知识树） ---------- */
const M = {
  /* 极限 */
  'gaoshu880|函数极限的应用（渐近线、间断点、无穷小比阶、反求参数）': 329,
  'gaoshu880|函数极限定义和性质': 332,
  'gaoshu880|函数/数列极限的计算': 333,
  'gaoshu880|函数极限的应用（间断点）': 341,
  'gaoshu880|函数极限的应用（无穷小比阶）': 749,
  'gaoshu880|导数的计算（麦克劳林展开）': 339,
  'gaoshu880|导数的计算（泰勒展开）': 339,
  /* 一元微分 */
  'gaoshu880|导数的定义': 367,
  'gaoshu880|导数的计算（高阶导数、反函数、参数方程、分段函数）': 366,
  'gaoshu880|导数的计算': 366,
  'gaoshu880|隐函数求导': 376,
  'gaoshu880|导数的应用（凹凸性）': 458,
  'gaoshu880|导数的应用（极值）': 443,
  'gaoshu880|导数的应用（极值、拐点、单调性、凹凸性）': 382,
  'gaoshu880|导数的应用（切线）': 381,
  'gaoshu880|曲率、曲率半径、物理应用': 365,
  'gaoshu880|微分中值定理': 368,
  /* 一元积分 */
  'gaoshu880|不定积分/定积分的计算': 2321,
  'gaoshu880|不定积分/定积分计算': 2321,
  'gaoshu880|定积分计算（对称性）': 2360,
  'gaoshu880|定积分的定义与性质': 2538,
  'gaoshu880|定积分的定义与比较大小': 2538,
  'gaoshu880|定积分的比较大小': 2556,
  'gaoshu880|变上限积分函数': 2557,
  'gaoshu880|含参积分': 2538,
  'gaoshu880|反常积分敛散性判断': 2472,
  'gaoshu880|定积分的几何应用': 2382,
  /* 微分方程 */
  'gaoshu880|微分方程求解': 762,
  'gaoshu880|微分方程解的结构和性质': 760,
  'gaoshu880|解的结构和性质': 760,
  /* 多元微分 */
  'gaoshu880|二元泰勒公式': 324,
  'gaoshu880|连续、偏导、可微存在性': 483,
  'gaoshu880|连续性、偏导数、可微性': 483,
  'gaoshu880|一元函数微分学：全微分；多元函数微分学：可微性；一元函数积分学：定积分的计算': 483,
  'gaoshu880|一元函数微分学：全微分；多元函数微分学：可微性': 483,
  'gaoshu880|一元函数微分学：可微性；多元函数微分学：偏导数': 483,
  'gaoshu880|一元函数微分学：全微分；一元函数积分学：定积分的计算': 483,
  'gaoshu880|一元函数微分学：全微分；多元函数微分学：偏导数': 483,
  'gaoshu880|偏导数的计算': 484,
  'gaoshu880|极值和最值问题': 486,
  'gaoshu880|极值和最值': 486,
  'gaoshu880|极值和最值（条件极值）': 500,
  /* 二重积分 */
  'gaoshu880|二重积分的概念和性质': 563,
  'gaoshu880|二重积分的计算（对称性、交换次序、坐标系、分区域）': 562,
  'gaoshu880|综合应用': -223,
  /* 线代讲义 xian_dai */
  'xian_dai|行列式': 2,
  'xian_dai|矩阵': 3,
  'xian_dai|伴随矩阵': 25,
  'xian_dai|代数余子式与伴随矩阵': 11,
  'xian_dai|矩阵的逆': 24,
  'xian_dai|逆矩阵': 24,
  'xian_dai|矩阵高次幂': 28,
  'xian_dai|初等矩阵': 29,
  'xian_dai|矩阵的秩': 27,
  'xian_dai|分块矩阵': 30,
  'xian_dai|向量基础': 4,
  'xian_dai|线性相关': 120,
  'xian_dai|向量组的线性相关性': 120,
  'xian_dai|极大线性无关组': 122,
  'xian_dai|向量组等价': 121,
  'xian_dai|向量空间': 4,
  'xian_dai|线性方程组解的判定': 132,
  'xian_dai|解的判定': 132,
  'xian_dai|方程组求解': 135,
  'xian_dai|线性方程组的求解': 135,
  'xian_dai|线性方程组解的结构': 135,
  'xian_dai|解的结构': 135,
  'xian_dai|同解与公共解': 157,
  'xian_dai|公共解与同解问题': 157,
  'xian_dai|特征值与特征向量': 177,
  'xian_dai|特征值与特征向量的概念与性质': 177,
  'xian_dai|秩1矩阵': 60,
  'xian_dai|相似对角化': 179,
  'xian_dai|矩阵相似对角化': 179,
  'xian_dai|等价、相似、合同的判定': 6,
  'xian_dai|实对称矩阵的性质': 180,
  'xian_dai|二次型的表示与矩阵': 201,
  'xian_dai|配方法求标准形、正交变换法求标准形': 202,
  'xian_dai|惯性指数与正定判定': 210,
  'xian_dai|二次型等于0的求解': 205,
  'xian_dai|矩阵等价、相似、合同': 6,
  /* 线代880 xian_dai880 */
  'xian_dai880|行列式的性质、展开定理（余子式、代数余子式）': 2,
  'xian_dai880|抽象行列式的计算': 10,
  'xian_dai880|矩阵运算、逆矩阵、伴随矩阵': 3,
  'xian_dai880|相关无关性与表出问题': 4,
  'xian_dai880|解的结构、判定、性质': 5,
  'xian_dai880|特征值与特征向量的概念与性质': 177,
  'xian_dai880|抽象与带参数方程组求解': 135,
  'xian_dai880|矩阵相似对角化': 179,
  'xian_dai880|惯性指数与正定判定': 210,
  'xian_dai880|等价、相似、合同的判定': 6,
  'xian_dai880|正交变换法求标准形': 212,
  'xian_dai880|正交矩阵': 57,
  'xian_dai880|正定矩阵': 210,
  'xian_dai880|微分方程解的结构和性质': -1
};

/* 线代880 无 kp_sub 的题按章节回退 */
const FB880 = { '第七章': 2, '第八章': 3, '第九章': 4, '第十章': 5, '第十一章': 6, '第十二章': 7 };

/* ---------- 抓取过的 cxyonly 分类树（缓存文件，可用 curl 重新拉） ---------- */
let cats;
const cache = path.join(__dirname, 'cxy_categories_cache.json');
if (fs.existsSync(cache)) cats = JSON.parse(fs.readFileSync(cache, 'utf8'));
else {
  const out = require('child_process').execSync('curl -s "https://cxyonly.fans/api/categories"', { encoding: 'utf8', maxBuffer: 30 * 1024 * 1024 });
  cats = JSON.parse(out);
  fs.writeFileSync(cache, out);
}
function prune(node) {
  return { id: node.id, n: node.name, c: (node.children || []).map(prune) };
}
const gsTree = prune(cats.find(d => d.name === '高等数学'));
const xdTree = prune(cats.find(d => d.name === '线性代数'));

/* 通信原理：26 专题自建树 */
const txChapters = [];
{
  const seen = new Map();
  qs.filter(q => q.source === 'qhzt').forEach(q => {
    if (!seen.has(q.chapter)) { seen.set(q.chapter, { id: 'qhzt-' + String(q.chapter).replace('专题', ''), n: q.chapter_name || q.chapter, ch: q.chapter, c: [] }); txChapters.push(seen.get(q.chapter)); }
  });
  txChapters.sort((a, b) => parseInt(a.ch.replace('专题', ''), 10) - parseInt(b.ch.replace('专题', ''), 10));
}
const txTree = { id: -999, n: '通信原理 · 强化专题', c: txChapters };

/* 校验：每道题必须能解析到节点 */
const noneId = { 'gaoshu880': -223, 'xian_dai880': -1, 'xian_dai': -1, 'qhzt': -999 };
const unresolved = [];
const counts = {};
for (const q of qs) {
  const key = q.source + '|' + (q.kp_sub || '');
  let nid = M[key];
  if (nid === undefined && q.source === 'xian_dai880' && !q.kp_sub) nid = FB880[q.chapter];
  if (nid === undefined) { nid = noneId[q.source]; unresolved.push(key + ' #' + q.id); }
  counts[nid] = (counts[nid] || 0) + 1;
}
/* 未细分桶也要有名字：挂在各科树根下 */
gsTree.c = gsTree.c.concat([{ id: -223, n: '未细分（按 kp 对照不到）', c: [] }]);
xdTree.c = xdTree.c.concat([{ id: -1, n: '未细分（按 kp 对照不到）', c: [] }]);

const data = {
  generated: new Date().toISOString().slice(0, 10),
  origin: 'tree from cxyonly.fans /api/categories; questions mapped by kp_sub',
  tree: [gsTree, xdTree, txTree],
  sources: {
    'gaoshu880': { root: 223 },
    'xian_dai': { root: 1 },
    'xian_dai880': { root: 1 },
    'qhzt': { root: -999 }
  },
  assign: M,
  fallback880: FB880
};
fs.writeFileSync(path.join(ROOT, 'data', 'knowledge.json'), JSON.stringify(data));

console.log('knowledge.json 写入完成，大小:', (fs.statSync(path.join(ROOT, 'data', 'knowledge.json')).size / 1024).toFixed(1) + 'KB');
console.log('未映射条目数:', unresolved.length, unresolved.slice(0, 10));
const total = Object.entries(counts).reduce((s, [, v]) => s + v, 0);
console.log('已归属题数:', total, '/', qs.length);
console.log('未细分桶: 高数', counts[-223] || 0, '线代', counts[-1] || 0);
