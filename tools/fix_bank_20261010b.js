// 62章HDB3组题修复 2026-10-10 (对照用户书照片p222; 锚点断言)
const fs = require('fs');
const FILE = 'D:/考研数学/组卷网站_static/data/questions.json';
const backup = 'C:/Users/19273/AppData/Local/Temp/questions_backup_20261010b.json';
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

// ===== 1. 62-04 题面: 一空 → 书上三空(用户照片p222) =====
rep('tk299-62-04', 'question_text',
  '4、若信息源为 1000000001，则 HDB3 码为 $(-v)$ ______。（南京邮电大学 2021 年二、1）',
  '4、若信息源为 1000000001，则 HDB3 码为 $(-v)$______，双相码为______；若 HDB3 码为 10-110010-10，则信息码为______。（南京邮电大学 2021 年二、1）');

// ===== 2. 62-04 答案: 补双相码(规则1→10、0→01, 经62-05书答1001101001核实约定) =====
rep('tk299-62-04', 'answer_text',
  '$+1000+1-100-1+1$; $10010101$',
  '$+1000+1-100-1+1$；双相码 $10010101010101010110$；$10010101$');

// ===== 3. 62-04 解析: 补双相码规则, 译码改称第三空 =====
rep('tk299-62-04', 'solution',
  '（4 连 0 以 000V 处理、V 极性交替）。第二空为 HDB3 译码',
  '（4 连 0 以 000V 处理、V 极性交替）。双相码：每个码元 1→10、0→01，故该信息源的双相码为 $10010101010101010110$。第三空为 HDB3 译码');

// ===== 4. 62-05 来源行: 书上为南邮2019年二2 =====
rep('tk299-62-05', 'question_text', '（西安科技大学 2010 年二、2）', '（南京邮电大学 2019 年二、2）');

// ===== 5. 尾部垃圾剥离 =====
rep('tk299-62-06', 'question_text', '\n2、若数\n（北京邮\nA. 采样\nC. 判决', '');
rep('tk299-62-07', 'question_text', '\n3、设某数\n干扰传输\n（北京', '');
rep('tk299-65-04', 'question_text', '\n2、时\n（南\n3、\n（北\n4、\n（\n5、\nx……', '');
rep('tk299-62-08', 'question_text', '\nA. 1\n4、考', '');

fs.writeFileSync(FILE, JSON.stringify(qs, null, 1));
console.log('全部修复成功 共' + done.length + ' 处:');
done.forEach(d => console.log(' ✓', d));
