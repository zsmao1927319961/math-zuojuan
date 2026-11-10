# -*- coding: utf-8 -*-
"""全站其余板块体检：题面泄答案 / 空字段 / 结构异常（2026-11-10）"""
import json, re, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def leak_check(stem, ans):
    """返回泄露描述或 None"""
    if not stem or not ans or len(ans) < 2:
        return None
    st = stem.strip()
    a = ans.strip()
    # 判断类短答案（对/错/√/×）不查
    if len(a) < 2:
        return None
    marks = set(x[0] for x in re.findall(r'[A-D][）)、]', st))
    if a in st:
        # 完整选项题面（≥2个选项字母且结尾不是答案）算正常；否则算泄露
        line = st.split('\n')[0]
        if len(marks) >= 2 and not line.rstrip('。. ').endswith(a.rstrip('。. ')):
            return None
        return 'stem含ans(选项字母%d种)' % len(marks)
    return None

report = {}

# ---------- 1) questions.json：qhzt(讲义113) + tk299(299题317) ----------
qs = json.load(open(os.path.join(ROOT, 'data', 'questions.json'), encoding='utf-8'))
if isinstance(qs, dict):
    qs = qs.get('questions', [])
for src in ['qhzt', 'tk299']:
    rows = [q for q in qs if q.get('source') == src]
    leak, empty_ans, empty_sol = [], 0, 0
    for q in rows:
        stem = (q.get('question_text') or '')
        ans = (q.get('answer_text') or '')
        sol = (q.get('solution') or '')
        lk = leak_check(stem, ans)
        if lk:
            leak.append((q.get('id'), q.get('chapter_name', ''), lk, ans[:26], stem[-50:]))
        if not ans.strip():
            empty_ans += 1
        if not sol.strip():
            empty_sol += 1
    report[src] = dict(n=len(rows), leak=len(leak), empty_ans=empty_ans, empty_sol=empty_sol, leak_rows=leak[:12])

# ---------- 2) yz40.json ----------
yz = json.load(open(os.path.join(ROOT, 'data', 'yz40.json'), encoding='utf-8'))
items = yz.get('items', yz if isinstance(yz, list) else [])
yz_leak, yz_nostem, yz_nosol = [], 0, 0
for it in items:
    stem = it.get('stem') or ''
    sol = it.get('sol') or ''
    lk = leak_check(stem, sol.split('\n')[0][:80] if sol else '')
    if lk:
        yz_leak.append((it.get('id'), it.get('no'), lk))
    if not stem.strip():
        yz_nostem += 1
    if not sol.strip():
        yz_nosol += 1
report['yz40'] = dict(n=len(items), leak=len(yz_leak), no_stem=yz_nostem, no_sol=yz_nosol, leak_rows=yz_leak[:8])

# ---------- 3) txbs_data.js 全卡（含判断题） ----------
tx = open(os.path.join(ROOT, 'txbs_data.js'), encoding='utf-8').read()
pat = re.compile(r'"id":"([^"]+)"(.{0,1200}?)"ans":"((?:[^"\\]|\\.)*)"', re.S)
tx_leak, tx_noans, tx_n = [], 0, 0
for m in pat.finditer(tx):
    cid, mid, ans_raw = m.group(1), m.group(2), m.group(3)
    sm = re.search(r'"stem":"((?:[^"\\]|\\.)*)"', mid)
    if not sm:
        continue
    tx_n += 1
    stem = json.loads('"' + sm.group(1) + '"')
    ans = json.loads('"' + ans_raw + '"')
    if not ans.strip():
        tx_noans += 1
    lk = leak_check(stem, ans)
    if lk:
        tx_leak.append((cid, lk, ans[:24], stem[-46:]))
report['txbs'] = dict(n=tx_n, leak=len(tx_leak), no_ans=tx_noans, leak_rows=tx_leak[:14])

# ---------- 4) zhenti801.json 大题块（q.stem 含【答案】等） ----------
z = json.load(open(os.path.join(ROOT, 'data', 'zhenti801.json'), encoding='utf-8'))
big_stem_mark, big_stem_n = [], 0
MARK = re.compile(r'【(答案|知识点|对应课件|切入点|要点|解题过程)】')
for y in z['years']:
    for b in y['qs']:
        subs = b.get('subs') or []
        if len(subs) < 2:
            big_stem_n += 1
            st = b.get('stem') or ''
            if st and MARK.search(st):
                big_stem_mark.append((y['year'], b.get('id'), MARK.search(st).group(1), st[:60]))
report['zhenti_big'] = dict(n=big_stem_n, stem_has_mark=len(big_stem_mark), rows=big_stem_mark[:12])

# ---------- 5) z801_split.json ----------
try:
    SP = json.load(open(os.path.join(ROOT, 'data', 'z801_split.json'), encoding='utf-8'))
    sp_leak, sp_n = [], 0
    for qid, sp in SP.items():
        for p in sp.get('parts', []):
            sp_n += 1
            lk = leak_check(p.get('stem') or '', p.get('key') or '')
            if lk:
                sp_leak.append((qid, p.get('n'), lk))
    report['z801_split'] = dict(n=sp_n, leak=len(sp_leak), rows=sp_leak[:8])
except FileNotFoundError:
    report['z801_split'] = 'missing'

for k, v in report.items():
    print('==', k)
    if isinstance(v, dict):
        meta = {kk: vv for kk, vv in v.items() if not kk.endswith('_rows')}
        print('  ', meta)
        for r in v.get('leak_rows', v.get('rows', []))[:12]:
            print('   -', r)
    else:
        print('  ', v)
