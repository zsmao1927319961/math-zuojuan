// 430题二轮体检修复 2026-10-08 (锚点断言, 任一MISS即不保存)
const fs = require('fs');
const FILE = 'D:/考研数学/组卷网站_static/data/questions.json';
const backup = 'C:/Users/19273/AppData/Local/Temp/questions_backup_20261008c.json';
const qs = JSON.parse(fs.readFileSync(FILE, 'utf8'));
fs.writeFileSync(backup, JSON.stringify(qs));
const M = new Map(qs.map(q => [q.id, q]));
const errors = [], done = [];

function must(cond, msg) { if (!cond) throw new Error(msg); }

function stripHead(id, frag) {
  const q = M.get(id);
  must(q, id + ' 不存在');
  must(q.question_text.startsWith(frag), `${id} 头部锚点不匹配: ${JSON.stringify(q.question_text.slice(0,30))}`);
  q.question_text = q.question_text.slice(frag.length);
  done.push(`${id} 剥离头部 ${JSON.stringify(frag)}`);
}
function appendTail(id, tail) {
  const q = M.get(id);
  must(q, id + ' 不存在');
  must(!q.question_text.includes(tail), `${id} 尾部已含待追加内容`);
  q.question_text += tail;
  done.push(`${id} 追加尾部 ${JSON.stringify(tail.slice(0,30))}`);
}
function replaceOnce(id, field, oldStr, newStr) {
  const q = M.get(id);
  must(q, id + ' 不存在');
  const s = q[field] || '';
  must(s.includes(oldStr), `${id}.${field} 锚点不匹配: ${JSON.stringify(s.slice(0,40))}`);
  must(s.indexOf(oldStr) === s.lastIndexOf(oldStr), `${id}.${field} 锚点不唯一`);
  q[field] = s.replace(oldStr, newStr);
  done.push(`${id}.${field} 替换 ${JSON.stringify(oldStr.slice(0,25))} -> ${JSON.stringify(newStr.slice(0,25))}`);
}

// ===== A. 头部碎片剥离 =====
[
  ['tk299-31-02', '（北京…\n'],
  ['tk299-32-01', '径程；以及平稳性与\n'],
  ['tk299-33-06', '通信原理精\n'],
  ['tk299-34-03', '中求出，或是……\n'],
  ['tk299-34-04', '(2)(3)(4) A. 瑞利\n'],
  ['tk299-41-09', 'A、时延　　B、相频\n'],
  ['tk299-52-02', 'A. AM    B. DS\n'],
  ['tk299-54-01', '合调制后信号带宽。\n'],
  ['tk299-62-06', '（南京邮电大学 2019 年一、\n'],
  ['tk299-64-02', 'B. 频谱较窄\n'],
  ['tk299-67-02', '（北京交通大学 202\n'],
  ['tk299-81-11', '和\n'],
  ['tk299-91-01', '包括最低抽样速率、抽样后信号频谱的变\n'],
  ['tk299-112-10', '…京邮电大学 2011 年一、8)\n'],
  ['tk299-121-02', '（判断题，南京邮电大学 2022\n'],
  ['tk299-121-06', '……信息　　D. 群同步信息\n'],
  ['tk299-121-07', 'D. 网同步\n'],
].forEach(([id, frag]) => stripHead(id, frag));

// ===== B. 碎片接回正确归属 =====
// 33-07头 -> 33-06尾 (包络服|从____分布)
stripHead('tk299-33-07', '从____分布。（北京交通大学 2022 年一、4）\n');
appendTail('tk299-33-06', '从____分布。（北京交通大学 2022 年一、4）');
// 34-02: 碎片是自己尾巴 -> 剥头接自己尾 (河北工业|工业大学 2023 年 二、7）)
stripHead('tk299-34-02', '工业大学 2023 年 二、7）\n');
appendTail('tk299-34-02', '工业大学 2023 年 二、7）');
// 112-09头 -> 112-08尾 (D、1|01100111100010)
stripHead('tk299-112-09', 'D、101100111100010\n');
{
  const q = M.get('tk299-112-08');
  must(q.question_text.endsWith('D、1'), '112-08 尾锚点不匹配: ' + JSON.stringify(q.question_text.slice(-20)));
  q.question_text += '01100111100010';
  done.push('tk299-112-08 尾补全选项D');
}
// 112-09 尾截断补全 (北京邮电大学2011年 -> 北京邮电大学 2011 年一、8）)
replaceOnce('tk299-112-09', 'question_text', '（北京邮电大学2011年', '（北京邮电大学 2011 年一、8）');
// 76-02头(2017来源) -> 76-01尾
stripHead('tk299-76-02', '（北京交通大学2017年一、3）\n');
appendTail('tk299-76-01', '\n（北京交通大学 2017 年一、3）');

// ===== C. 82-01 整体重建(碎片拼合) =====
{
  const q = M.get('tk299-82-01');
  must(q.question_text.startsWith('简单。\nA 电\n'), '82-01 头锚点不符');
  must(q.question_text.includes('系统总的传输函数') === false, '82-01 不应已含碎片');
  q.question_text = '1、在理想信道下的最佳基带系统中，发送滤波器 $G_T(\\omega)$、接收滤波器 $G_R(\\omega)$ 和连接网络的系统总的传输函数 $H(\\omega)$ 三者之间满足_______。（河北工业大学 2022 年二、12）';
  done.push('tk299-82-01 题面重建');
}
stripHead('tk299-82-02', '系统总的传输函数 $H(\\omega)$ 三者之间满足_______。（河北工业大学 2022 年二、12）\n');

// ===== D. 101-01 整题重建(书p266) =====
{
  const q = M.get('tk299-101-01');
  must(q.question_text === '（北京交通大学2022年一、10）', '101-01 题面现状不符');
  q.question_text = '1、最小距离为 5 的线性分组码，纠错能力为______。（北京交通大学 2022 年一、10）';
  q.answer_text = '1、纠正 2 位错码。解析：根据公式 $d_{\\min} \\geq 2t + 1$，$5 \\geq 2t+1 \\Rightarrow t \\leq 2$，故最多能纠正 2 位错。';
  done.push('tk299-101-01 题面+答案重建');
}

// ===== E. 112-10: 残渣清理 + 答案重建 + 接图 =====
{
  const q = M.get('tk299-112-10');
  must(q.question_text.includes('\n…8696\n'), '112-10 QQ残渣行锚点不符');
  q.question_text = q.question_text.replace('\n…8696\n', '\n');
  q.answer_text = '10、解：\n（1）$f(x)$ 为既约的；$f(x)$ 可整除 $x^m+1$（$m=2^n-1=2^3-1=7$）；$f(x)$ 除不尽 $x^q+1$（$q<m$）。\n（2）LFSR 结构图：\n【图】\n（3）$\\underline{0011101}00111$（下划线为一个周期）。\n（4）$n=3$，周期 $T=2^3-1=7$，是 m 序列。';
  q.answer_img = 'images/t299/a_tk299-112-10.jpg';
  done.push('tk299-112-10 残渣清理+答案重建+答案图');
}

// ===== F. 43章四题 =====
// 43-03 解析补全(书p291两个极限结论)
replaceOnce('tk299-43-03', 'solution',
  '当给定 $\\frac{S}{N_0}$，B 趋于无穷时：',
  '当给定 $\\frac{S}{N_0}$，B 趋于无穷时：\n$$C=\\lim_{B\\to\\infty}B\\log_2\\left(1+\\frac{S}{N_0B}\\right)=\\frac{S}{N_0\\ln 2}=1.44\\frac{S}{N_0}$$\n当给定 $\\frac{S}{N_0 B}$（信噪比恒定），B 趋于无穷时：$C=\\lim_{B\\to\\infty}B\\log_2\\left(1+\\frac{S}{N_0B}\\right)=\\infty$。');
// 43-04 type 纠正(带ABCD选项的选空题)
replaceOnce('tk299-43-04', 'type', '计算', '选择');
// 43-10 答案尾部补全(书p293) — 尾锚点(同一公式在(b)段也出现,故按结尾断言)
{
  const q = M.get('tk299-43-10');
  const tailOld = '$$C_2 = B\\log_2\\left(1+\\frac{S}{N}\\right) = 1000\\';
  must(q.answer_text.endsWith(tailOld), '43-10 尾锚点不匹配: …' + JSON.stringify(q.answer_text.slice(-50)));
  q.answer_text = q.answer_text.slice(0, -tailOld.length) +
    '$$C_2 = B\\log_2\\left(1+\\frac{S}{N}\\right) = 1000\\log_2\\left(1+\\frac{1\\times2}{1}\\right) = \\log_2 3\\ kbit/s$$\n$$C_3 = B\\log_2\\left(1+\\frac{S}{N}\\right) = 1000\\log_2\\left(1+\\frac{1.5\\times3}{1}\\right) = \\log_2 5.5\\ kbit/s$$\n$$C = C_1 + C_2 + C_3 = \\log_2\\frac{99}{4}\\ kbit/s$$';
  done.push('tk299-43-10 答案尾部补全(C2/C3/总容量)');
}
// 44-07 QQ残渣行删除
replaceOnce('tk299-44-07', 'answer_text', '\n2919418696\n', '\n');

// ===== G. 76-02 接答案图 + 34-04 接题图 =====
{
  const q = M.get('tk299-76-02');
  must(q.question_text.includes('（2）画出相位路径网格图'), '76-02 题面应含(2)问');
  must(q.answer_text.endsWith('（2）相位路径图如下：'), '76-02 答案尾锚点不符');
  q.answer_img = 'images/t299/a_tk299-76-02.jpg';
  done.push('tk299-76-02 接答案图(相位路径)');
}
{
  const q = M.get('tk299-34-04');
  must(q.question_text.includes('下图所示系统'), '34-04 题面应引用下图');
  q.question_img = 'images/t299/q_tk299-34-04.jpg';
  done.push('tk299-34-04 接题图(延迟T框图)');
}

// ===== 保存 =====
if (errors.length) { console.log('ERRORS:', errors); process.exit(1); }
fs.writeFileSync(FILE, JSON.stringify(qs, null, 1));
console.log('全部修复成功 共' + done.length + ' 处:');
done.forEach(d => console.log(' ✓', d));
