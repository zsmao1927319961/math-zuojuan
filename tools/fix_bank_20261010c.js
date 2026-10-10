// 61-02 答案 τ→2 误读修复 2026-10-10 (用户书照+裁剪图核实; 锚点断言)
const fs = require('fs');
const FILE = 'D:/考研数学/组卷网站_static/data/questions.json';
const backup = 'C:/Users/19273/AppData/Local/Temp/questions_backup_20261010c.json';
const qs = JSON.parse(fs.readFileSync(FILE, 'utf8'));
fs.writeFileSync(backup, JSON.stringify(qs));
const q = qs.find(x => x.id === 'tk299-61-02');
if (!q) { console.log('61-02 不存在'); process.exit(1); }
const oldA = '2、$\\frac{1}{2}$，$\\frac{1}{2}$，$13.5\\,\\text{dB}$';
if (!q.answer_text.includes(oldA)) { console.log('答案锚点缺失: ' + JSON.stringify(q.answer_text)); process.exit(1); }
q.answer_text = q.answer_text.replace(oldA, '2、$\\frac{1}{\\tau}$，$\\frac{1}{\\tau}$，$13.5\\,\\text{dB}$');
if (q.solution && q.solution.includes('\\frac{1}{2}')) {
  q.solution = q.solution.replace(/\\frac\{1\}\{2\}/g, '\\frac{1}{\\tau}');
  console.log('解析同步修正');
}
if (!q.solution) {
  q.solution = '方波脉冲（宽度 $\\tau$ ms）频谱为 $G(f)=\\tau\\,\\mathrm{Sa}(\\pi f\\tau)$：第一零点在 $f=1/\\tau$（kHz），故主瓣宽度为 $1/\\tau$ kHz；第一旁瓣占据 $1/\\tau\\sim2/\\tau$，宽度也是 $1/\\tau$ kHz；第一旁瓣峰值 $|\\mathrm{Sa}|\\approx0.217$，$20\\lg 0.217\\approx-13.5$ dB，即比主瓣峰值降低约 13.5 dB。';
  console.log('补写解析');
}
fs.writeFileSync(FILE, JSON.stringify(qs, null, 1));
console.log('61-02 修复完成:', JSON.stringify(q.answer_text));
