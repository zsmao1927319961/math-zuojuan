# -*- coding: utf-8 -*-
"""
小题背诵手册生成器 (2026-10-29):
来源A = 1998-2025合订本 真题小题(一选择填空/二填空/三判断, 2007-2025)
来源B = questions.json 中 tk299 的 选择/填空/判断
过滤: 排除计算类题(求/计算/画波形/数值答案), 只留概念结论记忆题
输出: 桌面 HTML(点击显示答案, 提取式背诵), 含轻量 LaTeX→Unicode 清洗
"""
import io, re, json, html as H
from collections import OrderedDict

BOOK = r"C:\Users\19273\Downloads\1998-2025年南邮通信原理真题及解析\南邮801通信原理历年真题答案精解_1998-2025合订本.md"
QJ = 'data/questions.json'
OUT = r"C:\Users\19273\Desktop\考研通信_小题背诵手册_真题+299.html"

# ---------- LaTeX/标记 轻量清洗 ----------
SUBS = {'\\alpha':'α','\\beta':'β','\\omega':'ω','\\rho':'ρ','\\sigma':'σ','\\tau':'τ','\\Delta':'Δ',
        '\\delta':'δ','\\pi':'π','\\lambda':'λ','\\mu':'μ','\\eta':'η','\\theta':'θ','\\infty':'∞',
        '\\oplus':'⊕','\\times':'×','\\pm':'±','\\approx':'≈','\\le':'≤','\\ge':'≥','\\ne':'≠',
        '\\Rightarrow':'⇒','\\rightarrow':'→','\\leftrightarrow':'↔','\\in':'∈','\\cdot':'·',
        '\\log':'log','\\ln':'ln','\\lg':'lg','\\exp':'exp','\\sqrt':'√','\\sum':'Σ','\\int':'∫',
        '\\cos':'cos','\\sin':'sin','\\arg':'arg','\\max':'max','\\min':'min','\\mathrm':'',
        '\\left':'','\\right':'','\\,':' ','\\;':' ','\\!':'','\\ ': ' '}
def clean_tex(t):
    if not t: return ''
    t = re.sub(r'\$\$([^$]+)\$\$', r'\1', t)
    t = re.sub(r'\$([^$]+)\$', r'\1', t)
    t = t.replace('**', '').replace('\\boxed', '')
    # \frac{a}{b} / \dfrac
    for _ in range(3):
        t = re.sub(r'\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}', r'(\1)/(\2)', t)
    t = re.sub(r'\^\{([^{}]{1,4})\}', lambda m: sup(m.group(1)), t)
    t = re.sub(r'_\{([^{}]{1,6})\}', r'_\1', t)
    t = re.sub(r'\^(\w)', lambda m: sup(m.group(1)), t)
    for k in sorted(SUBS, key=len, reverse=True):  # 长键优先, 防 \le 吃掉 \left
        t = t.replace(k, SUBS[k])
    t = t.replace('{', '').replace('}', '')
    return t.strip()

_SUP = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','-':'⁻','+':'⁺','n':'ⁿ','k':'ᵏ','i':'ⁱ','j':'ʲ','T':'ᵀ','b':'ᵇ','e':'ᵉ','x':'ˣ','m':'ᵐ'}
def sup(s):
    return ''.join(_SUP.get(ch, ch) for ch in s)

def clean(t):
    return H.escape(clean_tex(t or ''))

# ---------- 来源A: 合订本真题小题 ----------
s = io.open(BOOK, encoding='utf-8').read()
lines = s.split('\n')
years = []
for i, l in enumerate(lines):
    m = re.match(r'^#\s+(\d{4})年', l)
    if m: years.append((int(m.group(1)), i))
years.append((9999, len(lines)))

SEC_PAT = re.compile(r'^##\s*(一|二|三)、\s*(选择填空|选择|单选|填空|判断)')
ITEM1 = re.compile(r'^\*\*第(\d+)(?:题|空)(?:（([^）]*)）)?\*\*\s*(.*)')
ITEMG = re.compile(r'^\*\*第(\d+)(?:空)?[~～](?:第)?(\d+)空(?:（([^）]*)）)?\*\*\s*(.*)')
zt = []
for (y, a), (_, b) in zip(years, years[1:]):
    if y == 9999: break
    cur_sec = None
    # 节级预扫: 收集"题目:"编号段(分组卡拼题干 + 单条目补题干), 容许前导空格
    titems_by_sec = {}  # sec -> {num: (text, blanks)}  按节隔离, 防不同节编号互覆
    cur2 = None
    seen_item = False  # 只收节内"逐空精解/条目"开始前的编号行(真题目块)
    for i in range(a, b):
        l = lines[i]
        m_s = SEC_PAT.match(l)
        if m_s: cur2 = m_s.group(2); seen_item = False; continue
        if re.match(r'^##\s', l): cur2 = None; continue
        if not cur2: continue
        if re.match(r'^\*\*第\d+', l): seen_item = True
        if seen_item: continue
        if re.match(r'^\*\*', l) or re.match(r'^-\s*【', l): continue
        m_t = re.match(r'^\s*(\d+)[.、]\s*(.+)', l)
        if m_t:
            txt = m_t.group(2).strip()
            titems_by_sec.setdefault(cur2, {})[int(m_t.group(1))] = (
                txt, set(int(x) for x in re.findall(r'（(\d+)）', txt)))
    for i in range(a, b):
        l = lines[i]
        m = SEC_PAT.match(l)
        if m: cur_sec = m.group(2); continue
        if re.match(r'^##\s', l): cur_sec = None; continue
        if not cur_sec: continue
        mg, m1 = ITEMG.match(l), ITEM1.match(l)
        if mg or m1:
            if mg:  # 分组制: 第a空～第b空 / 第a~b空
                ga, gb = int(mg.group(1)), int(mg.group(2))
                label = (mg.group(3) or '').strip()
                rest = (mg.group(4) or '').strip()
                blk = []
                j = i + 1
                while j < b and not re.match(r'^\*\*第\d+', lines[j]) and not re.match(r'^#{2,3}\s', lines[j]):
                    blk.append(lines[j]); j += 1
                txt = '\n'.join(blk)
                am2 = re.search(r'-\s*【答案】\s*(.*)', txt)
                ans = am2.group(1).strip() if am2 else ''
                km = re.search(r'-\s*【知识点】\s*(.*)', txt)
                kp = km.group(1).strip() if km else ''
                sec_t = titems_by_sec.get(cur_sec, {})
                subj = [t for t, bl in sec_t.values() if bl and (bl & set(range(ga, gb+1)))]
                if subj:
                    stem = f"第{ga}~{gb}空 ｜ " + ' '.join(subj)
                else:
                    stem = f"第{ga}~{gb}空 {label} {re.sub(r'（答案[^）]*）', '', rest)}".strip()
                zt.append({'year': y, 'sec': cur_sec, 'no': ga, 'stem': stem, 'ans': ans, 'kp': kp})
                continue
            no = int(m1.group(1))
            label = (m1.group(2) or '').strip()
            stem = (m1.group(3) or '').strip()
            blk = []
            j = i + 1
            while j < b and not re.match(r'^\*\*第\d+', lines[j]) and not re.match(r'^#{2,3}\s', lines[j]):
                blk.append(lines[j]); j += 1
            txt = '\n'.join(blk)
            ans = ''
            am = re.search(r'【答案】\s*(.*)', stem)
            if am:
                ans = am.group(1).strip()
                stem = stem[:am.start()].strip()
            if not ans:
                am2 = re.search(r'-\s*【答案】\s*(.*)', txt)
                if am2: ans = am2.group(1).strip()
            if not stem or re.match(r'^（[^）]*选[^）]*）$', stem):  # 2022式答案提示当头 → 用【题目】bullet
                am3 = re.search(r'-\s*【题目】\s*(.*)', txt)
                stem = am3.group(1).strip() if am3 else stem
            if not stem and no in titems_by_sec.get(cur_sec, {}):  # 判断/精解分组制: 按题号取本节"题目"编号行
                stem = re.sub(r'（\s*）\s*$', '', titems_by_sec[cur_sec][no][0]).strip()
            if not stem and label:
                stem = f"第{no}空（{label}）"
            km = re.search(r'-\s*【知识点】\s*(.*)', txt)
            kp = km.group(1).strip() if km else ''
            zt.append({'year': y, 'sec': cur_sec, 'no': no, 'stem': stem, 'ans': ans, 'kp': kp})

# ---------- 来源B: 299 小题 ----------
q = json.load(io.open(QJ, encoding='utf-8'))
tk = [x for x in q if x.get('source') == 'tk299' and x.get('type') in ('选择', '填空', '判断')]
for x in tk:
    x['stem'] = x.get('question_text', '')
    x['ans'] = x.get('answer_text', '')
    x['kp'] = x.get('kp', '') or ''
    x['sec'] = x['type']
    x['year'] = None
    x['no'] = x.get('no')

# ---------- 过滤计算类 ----------
CALC_STEM = re.compile(r'((?<![要需请告要])求[^。]{0,12}(带宽|速率|门限|容量|熵|误码率|功率|码距|码字|监督|校正子|输出)|计算|画出|画一画|等于多少|为多少|是多少|多少\s*(dB|Hz|bps|bit|V|W|kHz|MHz)|试求|编码结果|写出.{0,8}(码字|编码|码组|HDB3|CMI))')
CALC_ANS = re.compile(r'\d')
UNIT = re.compile(r'(dB|Hz|bps|Baud|bit/s|kbit|Mbit|kHz|MHz|GHz|μs|μA|mV|kV|\bs\b)')
def is_calc(item):
    st, an = item['stem'] + ' ' + item.get('kp',''), item['ans']
    if CALC_STEM.search(st): return True
    if item['sec'] != '判断' and CALC_ANS.search(an) and UNIT.search(an): return True
    if re.match(r'^[\s\d.\s×*/+=<>≈-]+$', an) and CALC_ANS.search(an): return True
    return False

zt_keep = [x for x in zt if not is_calc(x)]
tk_keep = [x for x in tk if not is_calc(x)]
print(f"真题小题: {len(zt)} → 保留 {len(zt_keep)}, 排除计算 {len(zt)-len(zt_keep)}")
print(f"299小题: {len(tk)} → 保留 {len(tk_keep)}, 排除计算 {len(tk)-len(tk_keep)}")
print("\n--- 真题被排除样例(查误杀) ---")
for x in [x for x in zt if is_calc(x)][:10]:
    print(' ', x['year'], x['sec'], x['no'], x['stem'][:55])
print("\n--- 299被排除样例 ---")
for x in [x for x in tk if is_calc(x)][:8]:
    print(' ', x['type'], x.get('chapter_name','')[:12], str(x['stem'])[:55])

# ---------- 生成 HTML ----------
def zt_group():
    out = []
    ys = sorted({x['year'] for x in zt_keep})
    for y in ys:
        items = sorted([x for x in zt_keep if x['year'] == y], key=lambda x: (x['sec'], x['no']))
        out.append(f'<h3>{y}年（{len(items)}题）</h3>')
        for x in items:
            out.append(card(f"{y}·{'选' if '选' in x['sec'] else ('填' if x['sec']=='填空' else '判')}{x['no']}", x['stem'], x['ans'], x['kp']))
    return '\n'.join(out)

def tk_group():
    out = []
    chs = OrderedDict()
    for x in tk_keep:
        chs.setdefault(x.get('chapter_name') or '未分组', []).append(x)
    for ch, items in chs.items():
        out.append(f'<h3>{H.escape(str(ch))}（{len(items)}题）</h3>')
        for x in sorted(items, key=lambda x: x.get('no') or 0):
            tag = f"{x['sec']}{x['no']}"
            out.append(card(tag, x['stem'], x['ans'], x.get('kp','')))
    return '\n'.join(out)

def card(tag, stem, ans, kp):
    a = clean(ans) or '（见合订本）'
    k = f'<div class="kp">考点：{clean(kp)}</div>' if kp else ''
    return (f'<div class="card"><div class="q"><span class="tag">{H.escape(tag)}</span>'
            f'{clean(stem)}</div>'
            f'<div class="ans"><b>答案</b>：{a}</div>{k}</div>')

css = """*{box-sizing:border-box}body{font-family:'Segoe UI','Microsoft YaHei',sans-serif;margin:0;background:#f5f6f8;color:#1a1a1a;font-size:14.5px;line-height:1.55}
header{background:#1d4ed8;color:#fff;padding:18px 22px}header h1{margin:0 0 4px;font-size:20px}header p{margin:2px 0;font-size:12.5px;opacity:.9}
.wrap{max-width:860px;margin:0 auto;padding:14px 16px 60px}
nav{position:sticky;top:0;background:#fff;border-bottom:2px solid #e2e5ea;padding:8px 12px;display:flex;gap:8px;flex-wrap:wrap;z-index:5}
nav a{text-decoration:none;color:#1d4ed8;font-size:13px;background:#eef2ff;padding:3px 10px;border-radius:12px}
h2{margin:26px 0 8px;padding:6px 12px;background:#1d4ed8;color:#fff;border-radius:6px;font-size:16px}
h3{margin:16px 0 6px;color:#1d4ed8;font-size:14.5px;border-left:4px solid #1d4ed8;padding-left:8px}
.card{background:#fff;border:1px solid #e2e5ea;border-radius:8px;padding:10px 12px;margin:8px 0}
.q{font-size:14.5px}.tag{display:inline-block;background:#eef2ff;color:#1d4ed8;font-size:11px;border-radius:4px;padding:1px 6px;margin-right:6px;vertical-align:2px}
.ans{margin-top:6px;padding:6px 10px;background:#ecfdf5;border-left:3px solid #10b981;border-radius:4px;font-size:13.5px;display:none}
.card.open .ans{display:block}
.kp{margin-top:4px;font-size:12px;color:#6b7280}
.hint{background:#fffbe8;border:1px solid #f0e0a0;border-radius:6px;padding:8px 12px;font-size:13px;margin:12px 0}
@media print{.ans{display:block!important}nav{display:none}body{background:#fff}h2{-webkit-print-color-adjust:exact}}"""
js = """document.addEventListener('click',e=>{const c=e.target.closest('.card');if(c)c.classList.toggle('open');});
function ex(show){document.querySelectorAll('.card').forEach(c=>c.classList.toggle('open',show));}"""

n1, n2 = len(zt_keep), len(tk_keep)
page = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>考研通信·小题背诵手册（真题+299·免计算）</title><style>{css}</style></head><body>
<header><h1>考研通信 · 小题背诵手册</h1>
<p>真题小题 {n1} 道（2007–2025 选择/填空/判断）＋ 299题库小题 {n2} 道 ｜ 已剔除计算题 ｜ {len(zt_keep)+len(tk_keep)} 道纯记忆</p>
<p>用法：看题 → 脑中作答 → 点卡片显示答案核对（提取式背诵）。打印版自动展开全部答案。</p></header>
<nav><a href="#zt">真题小题（{n1}）</a><a href="#tk">299题库小题（{n2}）</a>
<a href="javascript:ex(1)">全部展开</a><a href="javascript:ex(0)">全部收起</a></nav>
<div class="wrap">
<div class="hint">背诵优先级建议：①近年（2020–2025）真题小题 → ②2014–2019（你正做的一刷区间）→ ③2008–2013 高频滚一轮 → ④299 按章查漏。判断题全卷都是概念对错，适合睡前过。</div>
<h2 id="zt">一、历年真题小题（{n1} 道）</h2>
{zt_group()}
<h2 id="tk">二、299 题库小题（{n2} 道）</h2>
{tk_group()}
</div><script>{js}</script></body></html>"""

io.open(OUT, 'w', encoding='utf-8').write(page)
print(f"\n已生成: {OUT}  ({len(page)//1024} KB)")
EOF_MARKER = None
