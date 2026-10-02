# -*- coding: utf-8 -*-
# 题库修复：6题OCR截断补全（对照原书页转录）+ qhzt 82题 chapter_name 补齐
# 所有补录文本均转录自 _tk299_work/rot 书页照片：p187/p220/p221/p292/p320/p341/p342/p343
import json, re, sys

P = r'D:/考研数学/组卷网站_static/data/questions.json'
raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)
Q = {x['id']: x for x in d}
log = []

def tail_set(qid, field, old_tail, new_tail):
    """把字段末尾的 old_tail 替换为 new_tail"""
    x = Q[qid]
    t = x.get(field) or ''
    assert t.endswith(old_tail), (qid, field, '末尾不匹配:', t[-50:])
    x[field] = t[:-len(old_tail)] + new_tail
    log.append(f'{qid}.{field} 尾部替换 {len(old_tail)}->{len(new_tail)} 字符')

# ============ 1. tk299-21-05 题面补全（p187） ============
tail_set('tk299-21-05', 'question_text', '$x_4(t)=\\',
    '$x_4(t)=\\mathrm{sinc}(t)\\,\\mathrm{sinc}\\left(\\frac{t}{3}\\right)$。'
    '这四个系统的频带利用率依次是 (1)____，(2)____，(3)____，(4)____ Baud/Hz。'
    '（北京邮电大学 2024 年一、9）\n'
    '(1)(2)(3)(4)：A. 1　　B. 1.5　　C. 2　　D. 3')
x = Q['tk299-21-05']
log.append('tk299-21-05.question_text 补全（solution 原本完整，不动）')

# ============ 2. tk299-43-09 答案补尾（p292） ============
tail_set('tk299-43-09', 'answer_text', '可得 $\\dfrac{S}{N}=',
    '可得 $\\dfrac{S}{N}=2^{5.56}-1=46.23$\n'
    '$10\\lg\\dfrac{S}{N}=16.6\\,\\mathrm{dB}$\n'
    '（4）$\\eta=\\dfrac{\\log_2 M}{1+a}=\\dfrac{R_{\\text{总}}}{B}=\\dfrac{44492.8\\times10^3}{8\\times10^6}=5.56$\n'
    '由 $a=\\dfrac{\\log_2 M}{5.56}-1$，$0<a\\le 1$，解得 $M=64$。')

# ============ 3. tk299-61-05 题面重建（p220/p221） ============
x = Q['tk299-61-05']
x['question_text'] = ('5、设 $s(t)$ 是速率为 $R_b=2\\,\\mathrm{kbit/s}$ 的双极性不归零信号，'
    '其主瓣带宽是____kHz。令 $y(t)=s(t)+s(t-T_b)$，则 $y(t)$ 的主瓣带宽是____kHz。'
    '（北京邮电大学 2023 年一、9）\n'
    'A. 0.5　　B. 1　　C. 2　　D. 4')
print('61-05 原solution:', repr(x.get('solution')))
x['solution'] = ('5、C；B。解析：双极性 NRZ 码主瓣带宽 $B=R_b=2\\,\\mathrm{kHz}$，选 C；'
    '$y(t)$ 的功率谱乘因子 $\\left|1+e^{-j2\\pi fT_b}\\right|^2=4\\cos^2(\\pi fT_b)$，'
    '第一零点移至 $\\frac{1}{2T_b}$，主瓣带宽 $1\\,\\mathrm{kHz}$，选 B。')
log.append('tk299-61-05 question_text/solution 重建')

# ============ 4. tk299-72-05 答案重写（p320） ============
x = Q['tk299-72-05']
assert (x.get('answer_text') or '').endswith('$\\frac{1}{2}e^{-r')
x['answer_text'] = ('5、解：\n'
    '（1）曲线 1-5 依次为：非相干 $FSK$，相干 $FSK$，差分相干 $DPSK$，相干 $DPSK$，相干 $PSK$。\n'
    '（2）各种调制方式的误比特率计算公式如下：\n'
    '相干 $PSK$：$\\frac{1}{2}\\mathrm{erfc}\\sqrt{r}$　'
    '相干 $DPSK$：$\\mathrm{erfc}\\sqrt{r}$　'
    '差分相干 $DPSK$：$\\frac{1}{2}e^{-r}$\n'
    '相干 $FSK$：$\\frac{1}{2}\\mathrm{erfc}\\sqrt{\\frac{r}{2}}$　'
    '非相干 $FSK$：$\\frac{1}{2}e^{-\\frac{r}{2}}$\n'
    '其中信噪比 $r=\\dfrac{S}{N}=\\dfrac{S}{n_0B}=\\dfrac{S}{n_0\\cdot\\frac{2}{T}}=\\dfrac{ST}{2n_0}=\\dfrac{E_b}{2n_0}$，'
    '可以看出 $r$ 与 $\\dfrac{E_b}{n_0}$ 成正比。')
log.append('tk299-72-05.answer_text 重写')

# ============ 5. tk299-81-07 答案补全+题面去残留（p341） ============
x = Q['tk299-81-07']
t = x['question_text']
i = t.find('（右页边缘残缺）')
assert i > 0
x['question_text'] = t[:i].rstrip()
log.append('tk299-81-07.question_text 去残留碎片')
x['answer_text'] = ('7、解：\n'
    '(1) $E_s = E_g = \\int_{-\\infty}^{\\infty} g^2(t)\\,dt = \\int_0^1 \\left(\\frac{2}{\\sqrt{5}}\\right)^2 dt + \\int_1^2 \\left(\\frac{1}{\\sqrt{5}}\\right)^2 dt = 1$\n'
    '(2) 最佳抽样时刻 $t_0 = 2$，$h(t) = g(2-t)$：'
    '$h(t)=\\frac{1}{\\sqrt{5}}$（$0\\le t\\le 1$），$h(t)=\\frac{2}{\\sqrt{5}}$（$1\\le t\\le 2$）\n'
    '(3) 取样输出 $y = \\int_0^{T_b} \\left[ -g(t) + n_w(t) \\right] g(t)\\,dt = -E_g + Z$，'
    '其中 $Z = \\int_{-\\infty}^{+\\infty} n_w(t)g(t)\\,dt$ 为零均值高斯随机变量，$Z \\sim N(0, \\frac{N_0}{2})$，'
    '从而 $y \\sim N(-1, \\frac{N_0}{2})$，概率密度函数为：'
    '$p_y(x) = \\frac{1}{\\sqrt{\\pi N_0}} \\exp\\left[ -\\frac{(x+1)^2}{N_0} \\right]$\n'
    '(4) 由于等概，最佳判决门限为：$V_T = 0$\n'
    '(5) $P_e = P(1)P(e \\mid 1) + P(0)P(e \\mid 0) = \\frac{1}{2}\\,\\mathrm{erfc}\\sqrt{\\frac{1}{N_0}}$')
log.append('tk299-81-07.answer_text 重写（原截断于(1)中途）')

# ============ 6. tk299-81-09 答案补全（p342/p343） ============
x = Q['tk299-81-09']
t = x['answer_text']
old_fig = '冲激响应的波形图如下所示：\n【图】'
assert t.count(old_fig) == 1
x['answer_text'] = t.replace(old_fig,
    '冲激响应为 $h(t) = s_1(T-t) = -\\sin\\dfrac{2\\pi t}{T}$（$0\\le t\\le T$），与 $s_1(t)$ 反相。')
log.append('tk299-81-09 【图】→解析式')
tail_set('tk299-81-09', 'answer_text', '\\exp \\left[ -\\frac{(y - E_1)^2}{N_0 E_1} \\right]',
    '\\exp \\left[ -\\frac{(y - E_1)^2}{N_0 E_1} \\right]$\n'
    '发送 $s_2(t)$ 时：$y = 0 + Z$，其中 $Z \\sim N(0, \\frac{N_0}{2} E_1)$\n'
    '条件概率密度为：$p(y \\mid s_2) = \\frac{1}{\\sqrt{\\pi N_0 E_1}} \\exp \\left[ -\\frac{y^2}{N_0 E_1} \\right]$\n'
    '(3) 由于等概，最佳判决门限为两概率密度函数的交点：$V_T = \\frac{E_1}{2}$\n'
    '平均判错概率：$P_e = \\frac{1}{2}P(e \\mid s_1) + \\frac{1}{2}P(e \\mid s_2) = '
    '\\frac{1}{2}\\,\\mathrm{erfc}\\sqrt{\\frac{E_1}{4N_0}} = \\frac{1}{2}\\,\\mathrm{erfc}\\sqrt{\\frac{T}{8N_0}}$')

# ============ 7. qhzt 82题 chapter_name 补齐 ============
ZH = {6:'六',7:'七',8:'八',9:'九',10:'十',11:'十一',12:'十二',13:'十三',14:'十四',15:'十五',
      16:'十六',17:'十七',18:'十八',19:'十九',20:'二十',21:'二十一',22:'二十二',23:'二十三',
      24:'二十四',25:'二十五',26:'二十六',27:'二十七'}
filled = 0
for x in d:
    if x.get('source') != 'qhzt':
        continue
    if (x.get('chapter_name') or '').strip():
        continue
    m = re.match(r'专题(\d+)', x.get('chapter') or '')
    assert m, x['id']
    n = int(m.group(1))
    kp = (x.get('kp') or '').strip()
    assert kp, x['id']
    x['chapter_name'] = f'专题{ZH[n]} {kp}'
    filled += 1
log.append(f'qhzt chapter_name 补齐 {filled} 题')

# ============ 保存（保持 indent=1 + CRLF + 无尾换行） ============
out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print('\n'.join(log))
print('已写回', P)
