// fix_txbs_2016_alignment.js — 2026-11-16
// 修复 txbs 2016年选择题 11 张主卡的"题答错位"(答案按第k空配第k卡的错位 bug),
// 删除 11 张补丁碎片卡(选12/13/14/15/16/19/20/21/23/24/25), 清洗 MAIN/GROUPS 引用。
// 用法: node tools/fix_txbs_2016_alignment.js
const fs = require('fs');
const path = require('path');
const FILE = path.join(__dirname, '..', 'txbs_data.js');

const o = JSON.parse(fs.readFileSync(FILE, 'utf8').slice(
  fs.readFileSync(FILE, 'utf8').indexOf('{'),
  fs.readFileSync(FILE, 'utf8').lastIndexOf('}') + 1));

const DEL = ['zt2016-选择12','zt2016-选择13','zt2016-选择14','zt2016-选择15',
  'zt2016-选择16','zt2016-选择19','zt2016-选择20','zt2016-选择21',
  'zt2016-选择23','zt2016-选择24','zt2016-选择25'];

const PATCH = {
  'zt2016-选择1': {
    ans: 'x（信源）、v（信道）',
    kp: '信源编码与信道编码',
    sol: '【要点】模拟信号数字化属于信源编码；差错控制编码属于信道编码。' },
  'zt2016-选择2': {
    ans: 'r（平稳）',
    kp: '遍历性',
    sol: '【要点】随机过程具有遍历性(各态历经)的前提是它必须是平稳的。' },
  'zt2016-选择3': {
    ans: 'z（自相关函数）、l（功率谱密度）',
    kp: '维纳-辛钦定理',
    sol: '【要点】维纳-辛钦定理：Rx(τ) 与 Px(ω) 是一对傅里叶变换(时域↔频域)。' },
  'zt2016-选择4': {
    ans: 'm（恒参）、t（随参）',
    kp: '恒参/随参信道',
    sol: '【要点】特性不随时间变化=恒参信道(存在幅度-频率、相位-频率失真)；随时间变化=随参信道(时延随时间变、衰减随时间变、存在多径传播)。' },
  'zt2016-选择5': {
    ans: 'b（Gauss）、d（Rayleigh）、o（均匀）、b（Gauss）、e（Rice）',
    kp: '窄带高斯噪声统计分布',
    sol: '【要点】窄带高斯白噪声：同相/正交分量呈Gauss(正态)分布，包络呈Rayleigh分布，相位呈均匀分布；余弦+窄带高斯噪声：同相/正交分量仍呈Gauss分布，包络呈Rice(莱斯)分布。' },
  'zt2016-选择6': {
    ans: 'q（门限效应）、j（非相干解调）',
    kp: '门限效应',
    sol: '【要点】输入信噪比下降到门限以下无法解调=门限效应，是非相干解调(包络检波)特有的现象；相干解调无门限效应。' },
  'zt2016-选择7': {
    ans: 'u（消除码间干扰）、y（余弦滚降）、f（部分响应）、p（理想低通）',
    kp: '码间干扰与传输特性',
    sol: '【要点】设计传输特性的目的是消除码间干扰(ISI)；三种常用传输特性：理想低通、余弦滚降、部分响应。' },
  'zt2016-选择8': {
    ans: 'h（多进制调制）、i（多载波调制）',
    kp: '多进制/多载波调制',
    sol: '【要点】不增加信号带宽而提高信息速率→多进制调制；无线多径衰落信道实现高速传输→多载波调制(OFDM)。' },
  'zt2016-选择9': {
    ans: 'n（接收机模型）、w（信号形式）',
    kp: '最佳接收',
    sol: '【要点】最佳接收研究：最佳信号形式 + 最佳接收机模型(由相关器/匹配滤波器实现)。' },
  'zt2016-选择10': {
    ans: 'c（PCM30/32）、a（A律十三折线）',
    kp: 'PCM30/32与A律十三折线',
    sol: '【要点】我国数字通信制式=PCM30/32路(E体系)；压缩特性=A律十三折线。' },
  'zt2016-选择11': {
    ans: 'g（低）、s（强）',
    kp: '码率与纠错能力',
    sol: '【要点】纠错编码中校验位越多→码率越低→纠错能力越强。' },
};

let patched = 0;
for (const c of o.cards) {
  if (PATCH[c.id]) {
    c.ans = PATCH[c.id].ans;
    c.kp = PATCH[c.id].kp;
    c.sol = PATCH[c.id].sol;
    patched++;
  }
}
const before = o.cards.length;
o.cards = o.cards.filter(c => !DEL.includes(c.id));
const removed = before - o.cards.length;

// 清洗 MAIN / GROUPS 中的失效 id 引用(递归)
let scrubbed = 0;
function scrub(x) {
  if (Array.isArray(x)) {
    const kept = x.filter(v => !(typeof v === 'string' && DEL.includes(v)));
    scrubbed += x.length - kept.length;
    kept.forEach(scrub);
    return kept;
  }
  if (x && typeof x === 'object') {
    for (const k of Object.keys(x)) x[k] = scrub(x[k]);
  }
  return x;
}
o.MAIN = scrub(o.MAIN);
o.GROUPS = scrub(o.GROUPS);

o.nzt = o.cards.length;
o.generated = '2026-11-16';
o.note = '2016-11-16: 修复2016年选择题11卡题答错位(答案按空号错配), 删除11张碎片补丁卡; 全量398→' + o.cards.length + '卡审计通过';

fs.writeFileSync(FILE, 'window.TXBS_DATA=' + JSON.stringify(o) + ';', 'utf8');
console.log('patched:', patched, '| removed:', removed, '| total cards:', o.cards.length, '| scrubbed refs:', scrubbed);

// 复扫审计: 空数vs答案数 + 2016残留碎片检查
const s2 = fs.readFileSync(FILE, 'utf8');
const o2 = JSON.parse(s2.slice(s2.indexOf('{'), s2.lastIndexOf('}') + 1));
let bad = [];
for (const c of o2.cards) {
  const blanks = [...String(c.stem || '').matchAll(/（(\d{1,2})）/g)].map(m => +m[1]);
  const nB = new Set(blanks).size;
  const nA = String(c.ans || '').split(/[、；;]/).filter(x => x.trim() && !/见下方|勘误|第\d+/.test(x)).length;
  if (nB > 0 && c.year !== 2024 && c.year !== 2025 && nA !== nB) bad.push(c.id + ' [空' + nB + '/答' + nA + ']');
}
console.log('复扫残留错位:', bad.length ? bad.join(', ') : '0 ✓');
const left2016 = o2.cards.filter(c => c.year === 2016 && c.type === '选择').map(c => c.label);
console.log('2016选择卡(', left2016.length, '张):', left2016.join(', '));
