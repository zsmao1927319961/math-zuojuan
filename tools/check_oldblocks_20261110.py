# -*- coding: utf-8 -*-
"""老年份多空块：每空的考点映射 + 题干对齐可行性核查"""
import json, re, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
z = json.load(open(os.path.join(ROOT, 'data', 'zhenti801.json'), encoding='utf-8'))
zkp = json.load(open(os.path.join(ROOT, 'data', 'z801_kp.json'), encoding='utf-8'))
QS = json.load(open(os.path.join(ROOT, 'data', 'z801_qstems.json'), encoding='utf-8'))

# 目标块：分题题干为"-"或缺题面的多空块
targets = ['y1998q1', 'y1999q1', 'y2000q1', 'y2001q1', 'y2003q1', 'y2005q1']
for y in z['years']:
    for b in y['qs']:
        bid = b.get('id')
        if bid not in targets:
            continue
        subs = b.get('subs') or []
        print('==== %s (%s) subs=%d' % (bid, (b.get('no') or '')[:24], len(subs)))
        print('  块stem前120:', repr((b.get('stem') or '')[:120]))
        for s in subs:
            sid = bid + '#' + str(s.get('n'))
            loc = zkp.get(sid)
            has_qs = sid in QS
            print('  n=%-3s t=%-14s 考点=%-28s QS题面=%s' % (
                s.get('n'), (s.get('t') or '')[:12], (loc[1][:24] if loc else 'MISSING!'), '✓' if has_qs else '✗'))
        # 小项行切分预览
        st = b.get('stem') or ''
        lines = [ln.strip() for ln in st.split('\n') if ln.strip()]
        item_lines = [ln for ln in lines if re.match(r'^\d{1,2}[\.、]', ln)]
        print('  可切出编号小项行: %d 行' % len(item_lines))
        for ln in item_lines[:8]:
            print('    ·', ln[:60])
