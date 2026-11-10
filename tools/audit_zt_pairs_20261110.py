# -*- coding: utf-8 -*-
"""2026-11-10 全量对账：zhenti801 subs 精解 ↔ txbs 独立答案 + 题面尾部泄露 + QS覆盖 + 块缺号"""
import json, re, io, sys, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
z = json.load(open(os.path.join(ROOT, 'data', 'zhenti801.json'), encoding='utf-8'))
tx = open(os.path.join(ROOT, 'txbs_data.js'), encoding='utf-8').read()
QS = json.load(open(os.path.join(ROOT, 'data', 'z801_qstems.json'), encoding='utf-8'))

tmap = {}
pat = re.compile(r'"id":"(zt(\d{4})-(选择|判断|填空|简答)(\d+))"(.{0,900}?)"ans":"((?:[^"\\]|\\.)*)"', re.S)
for m in pat.finditer(tx):
    tmap[(int(m.group(2)), m.group(3), int(m.group(4)))] = json.loads('"' + m.group(6) + '"')
print('txbs 卡可索引:', len(tmap))

def keyans(key):
    m = re.search(r'【答案】\*\*(.+?)\*\*', key or '')
    return m.group(1).strip() if m else ''

mism, nokey, tail_leak, qs_miss, emptystem = [], 0, [], [], []
gaps_report = []
for y in z['years']:
    yy = y['year']
    for b in y['qs']:
        subs = b.get('subs') or []
        if not subs:
            continue
        bid = b.get('id', '?')
        ns = [s.get('n') for s in subs]
        gaps = [n for n in range(1, max(ns) + 1) if n not in ns]
        if gaps:
            gaps_report.append((yy, bid, gaps))
        bno = b.get('no', '')
        typ = '选择' if '选择' in bno else ('判断' if '判断' in bno else None)
        for s in subs:
            n = s.get('n')
            stem = s.get('stem') or ''
            key = s.get('key') or ''
            ka = keyans(key)
            if not ka:
                nokey += 1
            if ka and len(ka) > 3 and stem.rstrip('。. ').endswith(ka.rstrip('。. ')):
                tail_leak.append((yy, bid, n, ka[:24]))
            sid = bid + '#' + str(n)
            if sid not in QS:
                qs_miss.append(sid)
            if not stem.strip():
                emptystem.append(sid)
            if typ and ka:
                tc = tmap.get((yy, typ, n))
                if tc is None:
                    mism.append((yy, typ, n, 'txbs缺卡', ka[:30]))
                else:
                    lm = re.match(r'([A-D])）?', ka.replace(' ', ''))
                    tl = re.match(r'([A-D])）?', tc.replace(' ', ''))
                    if lm and tl:
                        if lm.group(1) != tl.group(1):
                            mism.append((yy, typ, n, '字母不符 z=%s t=%s' % (ka[:20], tc[:20]), ''))
                    else:
                        norm = lambda x: re.sub(r'[\s，,、。；;（）()$\\*]', '', x)
                        a, b2 = norm(ka), norm(tc)
                        if a[:12] != b2[:12] and a not in b2 and b2 not in a:
                            mism.append((yy, typ, n, '文本不符 z=%r t=%r' % (ka[:24], tc[:24]), ''))

print('\n== 对账结果 ==')
print('key无答案标记:', nokey, '| 题面尾部泄露:', len(tail_leak), '| QS缺题面:', len(qs_miss), '| sub空题干:', len(emptystem))
for t in tail_leak[:12]:
    print('  泄露:', t)
print('txbs对账不符:', len(mism))
for m in mism[:40]:
    print('  ', m)
print('块缺号:', gaps_report[:12])
print('QS缺题面样例:', qs_miss[:25])
print('sub空题干样例:', emptystem[:25])

print('\n== 2016 选择填空块 QS ==')
for k in sorted([k for k in QS if k.startswith('y2016q1#')], key=lambda x: int(x.split('#')[1])):
    print(' ', k, '=>', repr(QS[k])[:100])
