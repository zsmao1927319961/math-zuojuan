# -*- coding: utf-8 -*-
"""
通信背诵卡池生成器 (2026-11-07):
来源A = 合订本 md 真题小题(与 gen_beisong_xiaoti_20261029.py 同一解析, 保留 $..$ LaTeX 供 KaTeX 渲染)
来源B = questions.json tk299 小题
输出 = txbs_data.js (仓库根): window.TXBS_DATA = {generated, cycle, cards, MAIN, GROUPS}
"""
import io, re, json, math
from collections import OrderedDict

BOOK = r"C:\Users\19273\Downloads\1998-2025年南邮通信原理真题及解析\南邮801通信原理历年真题答案精解_1998-2025合订本.md"
QJ = 'data/questions.json'
OUT = 'txbs_data.js'
CYCLE = 15


def light(t):
    if not t:
        return ''
    t = t.replace('**', '')
    t = t.replace('\\boxed', '')
    return t.strip()


s = io.open(BOOK, encoding='utf-8').read()
lines = s.split('\n')
years = []
for i, l in enumerate(lines):
    m = re.match(r'^#\s+(\d{4})年', l)
    if m:
        years.append((int(m.group(1)), i))
years.append((9999, len(lines)))

SEC_PAT = re.compile(r'^##\s*(一|二|三)、\s*(选择填空|选择|单选|填空|判断)')
ITEM1 = re.compile(r'^\*\*第(\d+)(?:题|空)(?:（([^）]*)）)?\*\*\s*(.*)')
ITEMG = re.compile(r'^\*\*第(\d+)(?:空)?[~～](?:第)?(\d+)空(?:（([^）]*)）)?\*\*\s*(.*)')
zt = []
TITEMS_ALL = {}
for (y, a), (_, b) in zip(years, years[1:]):
    if y == 9999:
        break
    cur_sec = None
    titems_by_sec = {}
    cur2 = None
    seen_item = False
    for i in range(a, b):
        l = lines[i]
        m_s = SEC_PAT.match(l)
        if m_s:
            cur2 = m_s.group(2)
            seen_item = False
            continue
        if re.match(r'^##\s', l):
            cur2 = None
            continue
        if not cur2:
            continue
        if re.match(r'^\*\*第\d+', l):
            seen_item = True
        if seen_item:
            continue
        if re.match(r'^\*\*', l) or re.match(r'^-\s*【', l):
            continue
        m_t = re.match(r'^\s*(\d+)[.、]\s*(.+)', l)
        if m_t:
            txt = m_t.group(2).strip()
            titems_by_sec.setdefault(cur2, {})[int(m_t.group(1))] = (
                txt, set(int(x) for x in re.findall(r'（(\d+)）', txt)))
    for sec_k, v in titems_by_sec.items():
        TITEMS_ALL[(y, sec_k)] = v
    for i in range(a, b):
        l = lines[i]
        m = SEC_PAT.match(l)
        if m:
            cur_sec = m.group(2)
            continue
        if re.match(r'^##\s', l):
            cur_sec = None
            continue
        if not cur_sec:
            continue
        mg, m1 = ITEMG.match(l), ITEM1.match(l)
        if not (mg or m1):
            continue
        if cur_sec == '填空':
            continue
        blk = []
        j = i + 1
        while j < b and not re.match(r'^\*\*第\d+', lines[j]) and not re.match(r'^#{2,3}\s', lines[j]):
            blk.append(lines[j])
            j += 1
        txt = '\n'.join(blk)
        if mg:
            ga, gb = int(mg.group(1)), int(mg.group(2))
            label = (mg.group(3) or '').strip()
            rest = (mg.group(4) or '').strip()
            am2 = re.search(r'-\s*【答案】\s*(.*)', txt)
            ans = am2.group(1).strip() if am2 else ''
            km = re.search(r'-\s*【知识点】\s*(.*)', txt)
            kp = km.group(1).strip() if km else ''
            sec_t = titems_by_sec.get(cur_sec, {})
            subj = [t for t, bl in sec_t.values() if bl and (bl & set(range(ga, gb + 1)))]
            if subj:
                stem = f"第{ga}~{gb}空 ｜ " + ' '.join(subj)
            else:
                stem = f"第{ga}~{gb}空 {re.sub(r'（答案[^）]*）', '', rest)}".strip()
            no = ga
        else:
            no = int(m1.group(1))
            label = (m1.group(2) or '').strip()
            stem = (m1.group(3) or '').strip()
            if cur_sec != '判断':
                titem = titems_by_sec.get(cur_sec, {}).get(no)
                if titem and titem[0]:
                    stem = titem[0]
                elif re.match(r'^（[^）]*）$', stem):
                    stem = ''
            ans = ''
            am = re.search(r'【答案】\s*(.*)', stem)
            if am:
                ans = am.group(1).strip()
                stem = stem[:am.start()].split('\n')[0].strip()
            if not ans:
                am2 = re.search(r'-\s*【答案】\s*(.*)', txt)
                if am2:
                    ans = am2.group(1).strip()
            if not stem or re.match(r'^（[^）]*选[^）]*）$', stem):
                am3 = re.search(r'-\s*【题目】\s*(.*)', txt)
                stem = am3.group(1).strip() if am3 else stem
            if not stem and no in titems_by_sec.get(cur_sec, {}):
                stem = re.sub(r'（\s*）\s*$', '', titems_by_sec[cur_sec][no][0]).strip()
            if not stem and label and cur_sec == '判断':
                stem = f"第{no}空（{label}）"
            km = re.search(r'-\s*【知识点】\s*(.*)', txt)
            kp = km.group(1).strip() if km else ''
        sol = '\n'.join(x.strip() for x in blk
                        if x.strip() and not re.match(r'^-\s*【(答案|知识点)】', x.strip())
                        and not re.match(r'^#{2,3}\s', x.strip()))
        zt.append({'year': y, 'sec': cur_sec, 'no': no, 'stem': stem,
                   'ans': ans, 'kp': kp, 'sol': sol})

# ---------- 主题-only 分组卡修复: 组序↔题目序对齐回填完整题干 (2018/2019 a~z选词年份) ----------
from collections import defaultdict
grp_by_ys = defaultdict(list)
for x in zt:
    if re.match(r'^第\d+~\d+空 ', x['stem']) and '｜' not in x['stem']:
        grp_by_ys[(x['year'], x['sec'])].append(x)
aligned = 0
for (yy, sec_k), cards_g in grp_by_ys.items():
    ti = TITEMS_ALL.get((yy, sec_k), {})
    items = [ti[k][0] for k in sorted(ti)]
    if len(items) != len(cards_g):
        continue
    for x, txt in zip(cards_g, items):
        m = re.match(r'^第(\d+)~(\d+)空 ', x['stem'])
        x['stem'] = f"第{m.group(1)}~{m.group(2)}空 ｜ " + txt
        aligned += 1
print('grouped stems aligned:', aligned)

q = json.load(io.open(QJ, encoding='utf-8'))
tk = [x for x in q if x.get('source') == 'tk299' and x.get('type') in ('选择', '填空', '判断')]

# ---------- 回填: 2022/2023 判断题题面 (合订本缺录, zhenti801.json 有 11-02 修好的转录) ----------
ZJ = 'data/zhenti801.json'


def split_numbered(txt):
    ms = list(re.finditer(r'(?:^|\n)\s*(\d+)\s*、', txt))
    out = {}
    for k, m in enumerate(ms):
        n = int(m.group(1))
        start = m.end()
        end = ms[k + 1].start() if k + 1 < len(ms) else len(txt)
        seg = txt[start:end].strip()
        if seg:
            out[n] = seg
    return out


zj = json.load(io.open(ZJ, encoding='utf-8'))
PD_FIX = {}
for yv in zj['years']:
    yv_year = yv.get('year')
    for qq in yv.get('qs', []):
        if '判断' in str(qq.get('no', '')) and qq.get('stem'):
            for n, seg in split_numbered(qq['stem']).items():
                PD_FIX[(yv_year, n)] = seg
fixed = 0
for x in zt:
    if not x['stem'] and PD_FIX.get((x['year'], x['no'])):
        x['stem'] = PD_FIX[(x['year'], x['no'])]
        fixed += 1
print('panduan stems backfilled:', fixed)

CALC_STEM = re.compile(r'((?<![要需请告要])求[^。]{0,12}(带宽|速率|门限|容量|熵|误码率|功率|码距|码字|监督|校正子|输出)|计算|画出|画一画|等于多少|为多少|是多少|多少\s*(dB|Hz|bps|bit|V|W|kHz|MHz)|试求|编码结果|写出.{0,8}(码字|编码|码组|HDB3|CMI))')
CALC_ANS = re.compile(r'\d')
UNIT = re.compile(r'(dB|Hz|bps|Baud|bit/s|kbit|Mbit|kHz|MHz|GHz|μs|μA|mV|kV|\bs\b)')


def is_calc(item):
    st = (item.get('stem') or item.get('question_text') or '') + ' ' + item.get('kp', '')
    an = item.get('ans') or item.get('answer_text') or ''
    if CALC_STEM.search(st):
        return True
    typ = item.get('sec', item.get('type'))
    if typ != '判断' and CALC_ANS.search(an) and UNIT.search(an):
        return True
    if re.match(r'^[\s\d.\s×*/+=<>≈-]+$', an) and CALC_ANS.search(an):
        return True
    return False


zt_keep = [x for x in zt if not is_calc(x)]
tk_keep = [x for x in tk if not is_calc(x)]
# 用户 2026-11-07 裁定: 只留真题第一大题(选择/选择填空/单选)+判断题, 填空题与299库卡全部删除
# (如需恢复 299 库小题卡: 删除下一行即可)
tk_keep = []

TYPE_MAP = {'选择填空': '选择', '选择': '选择', '单选': '选择', '填空': '填空', '判断': '判断'}
SHORT = {'选择': '选', '填空': '填', '判断': '判'}
cards = []
seen_ids = set()


def add_card(cid, src, year, typ, no, label, group, kp, stem, ans, sol, page):
    if cid in seen_ids:
        raise SystemExit('duplicate card id: ' + cid)
    seen_ids.add(cid)
    cards.append({
        'id': cid, 'src': src, 'year': year, 'type': typ, 'no': no,
        'label': label, 'group': group, 'kp': kp,
        'stem': light(stem), 'ans': light(ans),
        'sol': light(sol), 'page': page,
    })


for x in zt_keep:
    typ = TYPE_MAP[x['sec']]
    cid = 'zt' + str(x['year']) + '-' + x['sec'][:2] + str(x['no'])
    add_card(cid, 'zt', x['year'], typ, x['no'],
             str(x['year']) + '·' + SHORT[typ] + str(x['no']),
             str(x['year']) + '年',
             x['kp'], x['stem'], x['ans'], x.get('sol', ''), None)

for x in tk_keep:
    no = 0
    ns = str(x.get('no', ''))
    if ns.isdigit():
        no = int(ns)
    yr = None
    ys = str(x.get('year', ''))
    if ys.isdigit():
        yr = int(ys)
    typ = x['type']
    label = SHORT[typ] + str(no)
    add_card(x['id'], 't299', yr, typ, no, label,
             x.get('chapter_name') or '未分组',
             x.get('kp', ''), x.get('question_text', ''),
             x.get('answer_text', ''), x.get('solution') or '',
             x.get('book_page'))

groups = OrderedDict()
for c in cards:
    groups.setdefault(c['group'], []).append(c['id'])
MAIN = {}
queues = [list(v) for v in groups.values()]
inter = []
while any(queues):
    for qq in queues:
        if qq:
            inter.append(qq.pop(0))
per = int(math.ceil(len(inter) / float(CYCLE)))
for d in range(1, CYCLE + 1):
    MAIN[str(d)] = inter[(d - 1) * per: d * per]
GROUPS = [{'name': g, 'ids': v} for g, v in groups.items()]

data = {
    'generated': '2026-11-07',
    'cycle': CYCLE,
    'nzt': len(zt_keep),
    'ntk': len(tk_keep),
    'cards': cards,
    'MAIN': MAIN,
    'GROUPS': GROUPS,
}
js = 'window.TXBS_DATA=' + json.dumps(data, ensure_ascii=False,
                                      separators=(',', ':')) + ';'
io.open(OUT, 'w', encoding='utf-8').write(js)

empty_stem = [c['id'] for c in cards if not c['stem']]
empty_ans = [c['id'] for c in cards if not c['ans']]
print('zhenTi kept:', len(zt_keep), '/', len(zt))
print('tk299 kept:', len(tk_keep), '/', len(tk))
print('total cards:', len(cards), ' groups:', len(GROUPS))
print('MAIN per day:', [len(MAIN[str(d)]) for d in range(1, CYCLE + 1)])
print('empty stems:', len(empty_stem), empty_stem[:6])
print('empty answers:', len(empty_ans), empty_ans[:6])
