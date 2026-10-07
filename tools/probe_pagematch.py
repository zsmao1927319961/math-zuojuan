# -*- coding: utf-8 -*-
"""探针: 用题号前缀(N、)在 crops_inventory segs 里匹配每题所在书页"""
import json, re

inv = json.load(open(r'D:/考研数学/_tk299_work/crops_inventory.json', encoding='utf-8'))
qs = json.load(open(r'D:/考研数学/组卷网站_static/data/questions.json', encoding='utf-8'))
tx = [q for q in qs if q.get('source') == 'tk299']

segs_by = {}
for c in inv:
    key = (c['c'], c['k'])
    segs_by.setdefault(key, [])
    for pg, seg in c['segs']:
        t = seg.get('t', '').strip()
        if t:
            segs_by[key].append((pg, int(seg['y0']), t))

hit = miss = 0
missing = []
pages = {}
for q in tx:
    ch, no = q['chapter'], str(q['no'])
    m = re.match(r'第(\d+)章考点(\d+)', ch)
    c_, k_ = int(m.group(1)), int(m.group(2))
    pool = segs_by.get((c_, k_), [])
    cand = [s for s in pool if re.match(rf'^\s*{no}[、.．,]\S', s[2])]
    if not cand:  # O/0 confusion
        cand = [s for s in pool if re.match(rf'^\s*{no.replace("0","[0O]")}[、.．,]\S', s[2])]
    if cand:
        cand.sort(key=lambda s: (s[0], s[1]))
        pages[q['id']] = cand[0][0]
        hit += 1
    else:
        miss += 1
        missing.append(q['id'])

print('hit', hit, 'miss', miss)
print('missing:', missing)
json.dump(pages, open(r'D:/考研数学/_tk299_work/page_probe.json', 'w', encoding='utf-8'), ensure_ascii=False)
