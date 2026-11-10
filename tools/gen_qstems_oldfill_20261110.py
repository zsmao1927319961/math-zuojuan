# -*- coding: utf-8 -*-
"""
老年份多空块补每空题面（2026-11-10）：
2000/2001/2003 填空块分题题干当年转录为"-"，但块 stem 的编号小项行完整——
按空号顺序消耗小项行空位数分配题面，空名关键词做双重校验，不过校验的不写。
2005q1 简答连排块：sub stem 里【答案要点】等切出并入 key，题面段入 QS。
幂等：已有 QS 的 sid 跳过。
"""
import json, re, io, sys, os, shutil, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BK = r'C:\Users\19273\.zcode\workspace\535ea3dd-0465-49eb-aba2-34497bac154e\_oldfill_backup'
os.makedirs(BK, exist_ok=True)

ZT_P = os.path.join(ROOT, 'data', 'zhenti801.json')
QS_P = os.path.join(ROOT, 'data', 'z801_qstems.json')
z = json.load(open(ZT_P, encoding='utf-8'))
QS = json.load(open(QS_P, encoding='utf-8'))

BLANK = re.compile(r'（\s*）')
MARK = re.compile(r'^[ \t]*[-*>]?[ \t]*【(?:知识点|对应课件|切入点|要点|答案要点|答案|解题过程|易错点|备注|考点)】', re.M)

def label_core(t):
    m = re.search(r'（([^（）]+)）', t or '')
    return m.group(1) if m else ''

def fuzzy_in(core, line):
    lc = re.sub(r'\s+', '', line)
    c = re.sub(r'\s+', '', core)
    for L in (6, 5, 4, 3):
        if len(c) >= L and c[:L] in lc:
            return True
    return False

def lcs_len(a, b):
    """最长公共连续子串长度（去空白后）"""
    a = re.sub(r'\s+', '', a)
    b = re.sub(r'\s+', '', b)
    best = 0
    for i in range(len(a)):
        for j in range(len(b)):
            k = 0
            while i + k < len(a) and j + k < len(b) and a[i + k] == b[j + k]:
                k += 1
            if k > best:
                best = k
    return best

report = []
shutil.copy(QS_P, os.path.join(BK, 'z801_qstems.json.bak'))
shutil.copy(ZT_P, os.path.join(BK, 'zhenti801.json.bak'))

# 人工确认的三条显式覆盖（自动匹配不确定，语义归属唯一：信息熵簇/最佳接收ρ簇/采样簇）
OVERRIDES = {'y2000q1#3': 0, 'y2001q1#16': 4, 'y2003q1#5': 3}

for y in z['years']:
    for b in y['qs']:
        bid = b.get('id')
        if bid not in ('y2000q1', 'y2001q1', 'y2003q1'):
            continue
        subs = b.get('subs') or []
        st = b.get('stem') or ''
        lines = [ln.strip() for ln in st.split('\n') if ln.strip()]
        items = [ln for ln in lines if re.match(r'^\d{1,2}[\.、]', ln)]
        blanks = [len(BLANK.findall(ln)) for ln in items]
        total = sum(blanks)
        submap = {int(s['n']): s for s in subs if s.get('n') is not None}
        for n, s in submap.items():
            sid = bid + '#' + str(n)
            if sid in OVERRIDES and sid not in QS and len(items) > OVERRIDES[sid]:
                QS[sid] = items[OVERRIDES[sid]]
                report.append((sid, 'override', '人工确认指定行', items[OVERRIDES[sid]][:36]))
        cursor = 0
        ok = miss = 0
        for ln, k in zip(items, blanks):
            if k == 0:
                continue
            nums = list(range(cursor + 1, cursor + k + 1))
            cursor += k
            for n in nums:
                s = submap.get(n)
                if not s:
                    continue  # 卷面缺号（如 2001 的 10/11）
                sid = bid + '#' + str(n)
                if sid in QS:
                    ok += 1
                    continue
                core = label_core(s.get('t'))
                if core and fuzzy_in(core, ln):
                    QS[sid] = ln
                    ok += 1
                elif core:
                    # 顺序校验不过 → 空名与各行最长公共子串兜底（≥3字，或2字且全块唯一）
                    best, bestL, ties = None, 0, 0
                    for ln2 in items:
                        L = lcs_len(core, ln2)
                        if L > bestL:
                            best, bestL, ties = ln2, L, 1
                        elif L == bestL:
                            ties += 1
                    if bestL >= 3 and ties == 1:
                        QS[sid] = best
                        ok += 1
                        report.append((sid, core, 'LCS兜底(%d字)' % bestL, best[:36]))
                    elif bestL == 2 and ties == 1:
                        QS[sid] = best
                        ok += 1
                        report.append((sid, core, 'LCS兜底(2字唯一)', best[:36]))
                    else:
                        miss += 1
                        report.append((sid, core, '仍不确定未写入(best=%d,ties=%d)' % (bestL, ties), (best or '')[:36]))
                else:
                    miss += 1
                    report.append((sid, core, '无空名', ln[:40]))
        report.append((bid, '汇总', 'subs=%d 写入=%d 未写=%d 小项行=%d 空位=%d' % (len(subs), ok, miss, len(items), total), ''))

# ---- 2005q1 简答连排：切【答案要点】等到 key，题面入 QS ----
for y in z['years']:
    for b in y['qs']:
        if b.get('id') != 'y2005q1':
            continue
        for s in b.get('subs') or []:
            sid = 'y2005q1#' + str(s.get('n'))
            st = s.get('stem') or ''
            if not st.strip():
                report.append((sid, s.get('t'), '题干为空(第2题题干缺转录)，保持紧凑行', ''))
                continue
            mm = MARK.search(st)
            if not mm:
                continue
            m = mm.start()
            head = st[:m].strip()
            tail = st[m:].strip()
            s['stem'] = head
            if tail:
                s['key'] = tail + (('\n\n' + s['key']) if s.get('key') else '')
            if head and sid not in QS:
                QS[sid] = head
            report.append((sid, s.get('t'), '连排切分: 题面%d字→QS, 解析%d字→key' % (len(head), len(tail)), head[:40]))

json.dump(QS, open(QS_P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(z, open(ZT_P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('== 补题面报告 ==')
for r in report:
    print(' ', r)
qs2 = json.load(open(QS_P, encoding='utf-8'))
for bid in ('y2000q1', 'y2001q1', 'y2003q1', 'y2005q1'):
    have = [k for k in qs2 if k.startswith(bid + '#')]
    print(bid, 'QS 覆盖:', len(have))
