# -*- coding: utf-8 -*-
"""补丁前核对：合并分组影响面 / 无QS行的 s.stem 可用性 / 头部行识别"""
import json, re, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
z = json.load(open(os.path.join(ROOT, 'data', 'zhenti801.json'), encoding='utf-8'))
QS = json.load(open(os.path.join(ROOT, 'data', 'z801_qstems.json'), encoding='utf-8'))

# 1) 2016q1 subs 字段
y16 = [y for y in z['years'] if y['year'] == 2016][0]
b = y16['qs'][0]
print('2016q1 subs 字段样例:')
for s in b['subs'][:4]:
    print('  n=%s t=%r k=%r keyans=%r' % (s.get('n'), s.get('t'), s.get('k'), (re.search(r'【答案】\*\*(.{0,18})', s.get('key') or '') or [None,''])[1] if re.search(r'【答案】\*\*(.{0,18})', s.get('key') or '') else None))

# 2) 合并分组统计（同 QS stem 连续组，subs 和 split 两分支）
try:
    SP = json.load(open(os.path.join(ROOT, 'data', 'z801_split.json'), encoding='utf-8'))
except FileNotFoundError:
    SP = {}
tot_groups, tot_merged = 0, 0
for y in z['years']:
    for blk in y['qs']:
        subs = blk.get('subs') or []
        bid = blk.get('id')
        if len(subs) >= 2:
            run = None
            for s in subs:
                st = QS.get(bid + '#' + str(s.get('n')), '')
                if st and run and run[0] == st:
                    run[1].append(s)
                else:
                    if run and len(run[1]) > 1:
                        tot_groups += 1; tot_merged += len(run[1])
                    run = [st, [s]]
            if run and len(run[1]) > 1:
                tot_groups += 1; tot_merged += len(run[1])
        elif bid in SP:
            parts = SP[bid].get('parts', [])
            run = None
            for p in parts:
                st = p.get('stem') or ''
                if st and run and run[0] == st:
                    run[1].append(p)
                else:
                    if run and len(run[1]) > 1:
                        tot_groups += 1; tot_merged += len(run[1])
                    run = [st, [p]]
            if run and len(run[1]) > 1:
                tot_groups += 1; tot_merged += len(run[1])
print('同题干连续组:', tot_groups, '组，涉及', tot_merged, '个分题')

# 3) QS 缺失行中 s.stem 非空的数量与样例（检查是否带答案填充）
miss_have, miss_clean = [], []
for y in z['years']:
    for blk in y['qs']:
        subs = blk.get('subs') or []
        if len(subs) < 2: continue
        bid = blk.get('id')
        for s in subs:
            sid = bid + '#' + str(s.get('n'))
            if sid in QS: continue
            st = (s.get('stem') or '').strip()
            if st:
                miss_have.append(sid)
                if not re.search(r'（[^（）]{1,12}）', st):  # 无括号填充
                    miss_clean.append(sid)
print('QS缺失但有s.stem:', len(miss_have), '| 其中无括号填充(干净):', len(miss_clean))
for sid in miss_have[:8]:
    bid, n = sid.rsplit('#', 1)
    for y in z['years']:
        blk = next((bb for bb in y['qs'] if bb.get('id') == bid), None)
        if blk:
            sub = next((ss for ss in blk['subs'] if str(ss.get('n')) == n), None)
            if sub:
                print('  ', sid, repr(sub['stem'][:70]))
            break

# 4) 头部行（key 无【答案】且 stem 空的小题 subs）
hdr = []
for y in z['years']:
    for blk in y['qs']:
        subs = blk.get('subs') or []
        if len(subs) < 2: continue
        for s in subs:
            key = s.get('key') or ''
            if not s.get('stem') and '【答案】' not in key:
                hdr.append((blk.get('id'), s.get('n'), key[:40]))
print('疑似头部行:', len(hdr))
for h in hdr[:10]:
    print('  ', h)

# 5) split 块里同 stem 组明细
for qid, sp in (SP.items() if isinstance(SP, dict) else []):
    parts = sp.get('parts', [])
    runs = []
    run = None
    for p in parts:
        st = p.get('stem') or ''
        if st and run and run[0] == st:
            run[1].append(p.get('n'))
        else:
            if run and len(run[1]) > 1: runs.append(run)
            run = [st, [p.get('n')]]
    if run and len(run[1]) > 1: runs.append(run)
    for r in runs:
        print('SPLIT 同题干组:', qid, 'parts', r[1], repr(r[0][:50]))
