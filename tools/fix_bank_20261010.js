// 430题三轮体检修复 2026-10-10 (对照书后答案区p277-370 OCR + P81视频帧; 锚点断言, MISS即整体不保存)
const fs = require('fs');
const FILE = 'D:/考研数学/组卷网站_static/data/questions.json';
const backup = 'C:/Users/19273/AppData/Local/Temp/questions_backup_20261010.json';
const qs = JSON.parse(fs.readFileSync(FILE, 'utf8'));
fs.writeFileSync(backup, JSON.stringify(qs));
const M = new Map(qs.map(q => [q.id, q]));
const done = [];
function must(c, m) { if (!c) throw new Error(m); }
function rep(id, field, oldStr, newStr) {
  const q = M.get(id); must(q, id + ' 不存在');
  const s = q[field] || '';
  must(s.includes(oldStr), `${id}.${field} 锚点缺失: ${JSON.stringify(oldStr.slice(0, 40))}`);
  must(s.indexOf(oldStr) === s.lastIndexOf(oldStr), `${id}.${field} 锚点不唯一`);
  q[field] = s.replace(oldStr, newStr);
  done.push(`${id}.${field}`);
}
function tailRep(id, field, tailOld, tailNew) {
  const q = M.get(id); must(q, id + ' 不存在');
  const s = q[field] || '';
  must(s.endsWith(tailOld), `${id}.${field} 尾锚点不匹配: …${JSON.stringify(s.slice(-50))}`);
  q[field] = s.slice(0, -tailOld.length) + tailNew;
  done.push(`${id}.${field} 尾部补全`);
}

// ===== 1. 34-02 答案: QQ残渣+占位符垃圾 → 书p284原文 =====
rep('tk299-34-02', 'answer_text',
  '\n18696\nB. D. A. 解析 由于（文字被截断，无法完整辨认）', '');
done.push('tk299-34-02 答案垃圾清除');

// ===== 2. 42-04 解析: 占位符 → 书p290原文("称之为多普勒扩展") =====
rep('tk299-42-04', 'solution',
  '4、C。解析：相干时间的倒数我们常常称……（该行文字在图片中被截断，后半部分不可辨认）',
  '4、C。解析：相干时间的倒数我们常常称之为多普勒扩展。');

// ===== 3. 44-04 答案: 中途截断 → 书p294-295全文重写 =====
{
  const q = M.get('tk299-44-04');
  must(q.answer_text.startsWith('4、解：'), '44-04 头锚点不符');
  q.answer_text = '4、解：\n（1）$H(X)=-\\sum_{i=1}^{4}p(x_i)\\log_2 p(x_i)=-\\left[2\\times\\frac{1}{4}\\log_2\\frac{1}{4}+\\frac{3}{8}\\log_2\\frac{3}{8}+\\frac{1}{8}\\log_2\\frac{1}{8}\\right]=1.91$ bit/符号\n（2）$I(X,Y)=H(Y)-H(Y|X)$。令 $\\mu_1=\\frac{125}{128},\\ \\mu_2=\\frac{1}{128}$，则 $H(Y|X)=-\\left[\\mu_1\\log_2\\mu_1+3\\mu_2\\log_2\\mu_2\\right]=0.1974$\n可求得 $P_Y=\\left[\\frac{1}{4},\\ \\frac{1}{4},\\ \\frac{95}{256},\\ \\frac{33}{256}\\right]$，$H(Y)=1.912$ bit\n故当前信源下信道的传输速率 $I(X,Y)=H(Y)-H(Y|X)=1.7146$ bit/符号\n（3）信道容量：$C=\\max I(X,Y)=\\max(H(Y)-H(Y|X))$。由于 $H(Y|X)$ 为定值 0.1974，只需 $H(Y)$ 取最大值即可\n$$C=2+\\mu_1\\log_2\\mu_1+3\\mu_2\\log_2\\mu_2=1.8026\\text{ bit/符号}$$';
  done.push('tk299-44-04 答案按书p294-295重写');
}

// ===== 4. 63-11 解析 / 65-02 答案 / 95-04 答案: QQ残渣行删除 =====
rep('tk299-63-11', 'solution', '\n18696\n', '\n');
rep('tk299-65-02', 'answer_text', '\n9418696\n', '\n');
rep('tk299-95-04', 'answer_text', '\n418696', '');

// ===== 5. 81-03 book_page 核实: 库值245已正确(裁剪图印刷页63+偏移182), 无需修改 =====

// ===== 6. 81-10 答案: 中途截断 → 按P81视频帧续完 =====
tailRep('tk299-81-10', 'answer_text',
  '$$= -\\int_0^T s_2(t)h_2(t)\\,dt + \\int_0^T n_w(t)h_1(t)\\,dt - \\int',
  '$$= -\\int_0^T s_2(t)h_2(t)\\,dt + \\int_0^T n_w(t)h_1(t)\\,dt - \\int_0^T n_w(t)h_2(t)\\,dt$$\n令：$Z\' = \\int_0^T n_w(t)h_1(t)\\,dt - \\int_0^T n_w(t)h_2(t)\\,dt$，则 $y = -\\sqrt{2T_b} + Z\'$，$Z\' \\sim N(0, N_0)$，$E[y] = -\\sqrt{2T_b}$\n（3）判决 y 中的噪声功率：$D[y] = N_0$（由 $Z, Z\' \\sim N(0, N_0)$）\n（4）等概发送时最佳判决门限 $V_T = 0$\n（5）平均误比特率 $P_e = \\frac{1}{2}P(y<0|s_1) + \\frac{1}{2}P(y>0|s_2) = \\frac{1}{2}\\,\\mathrm{erfc}\\left(\\sqrt{\\frac{T_b}{N_0}}\\right)$');

// ===== 7. 102-11 答案: 截断 → 书p363续完(校验方程+伴随式译码) =====
tailRep('tk299-102-11', 'answer_text',
  '$$\\begin{cases}c_9\\oplus c_8\\oplus c_7\\oplus c_6\\oplus',
  '$$\\begin{cases}c_9\\oplus c_8\\oplus c_7\\oplus c_6\\oplus c_5=0\\\\c_9\\oplus c_4=0\\\\c_8\\oplus c_3=0\\\\c_7\\oplus c_2=0\\\\c_6\\oplus c_1=0\\\\c_9\\oplus c_8\\oplus c_7\\oplus c_6\\oplus c_0=0\\end{cases}$$\n(3) 伴随式 $s=Hy^\\mathrm{T}=(000001)$，可看出 000001 刚好是监督矩阵的第 10 列，则最可能的错误图样为 $e=[0000000001]$，译码结果为 $[1100011001]+[0000000001]=[1100011000]$。');

// ===== 8. 102-12 答案: 矩阵中途截断 → 书p363-364续完 =====
tailRep('tk299-102-12', 'answer_text',
  '$$G=\\begin{bmatrix}1&0&0&0&1&1&1\\\\0&1&0&0&1&0&1\\\\0&0&1&0&0',
  '$$G=\\begin{bmatrix}1&0&0&0&1&1&1\\\\0&1&0&0&1&0&1\\\\0&0&1&0&0&1&1\\\\0&0&0&1&1&1&0\\end{bmatrix}$，监督矩阵 $H=\\begin{bmatrix}1&1&0&1&1&0&0\\\\1&1&0&0&0&1&0\\\\1&0&1&0&0&0&1\\end{bmatrix}$\n(3) $s=eH^\\mathrm{T}=[101]$，校正子不为零，接收码字不正确；从校正子可以看出其刚好为监督矩阵的第二列，从而错误图样 $e=[0100000]$，正确码字 $c=r+e=[1110001]$\n(4) 依题意 $bH^\\mathrm{T}=rH^\\mathrm{T}$，令 $b=r+a$，则 $aH^\\mathrm{T}=0$，$a$ 必定是该线性分组码的一个码字；要求 $b$ 和 $r$ 的最小汉明距离，即求码字 $a$ 的最小码重，显然 $W(a)=3$，因此 $b$ 和 $r$ 汉明距离的最小值为 3。');

fs.writeFileSync(FILE, JSON.stringify(qs, null, 1));
console.log('全部修复成功 共' + done.length + ' 处:');
done.forEach(d => console.log(' ✓', d));
