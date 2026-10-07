# -*- coding: utf-8 -*-
"""二级匹配: 15题未命中题号前缀的, 用题面文字指纹在 segs 里找"""
import json, re

inv = json.load(open(r'D:/考研数学/_tk299_work/crops_inventory.json', encoding='utf-8'))
qs = json.load(open(r'D:/考研数学/组卷网站_static/data/questions.json', encoding='utf-8'))
qm = {q['id']: q for q in qs}
pages = json.load(open(r'D:/考研数学/_tk299_work/page_probe.json', encoding='utf-8'))

segs_by = {}
for c in inv:
    key = (c['c'], c['k'])
    segs_by.setdefault(key, [])
    for pg, seg in c['segs']:
        t = seg.get('t', '').strip()
        if t:
            segs_by[key].append((pg, int(seg['y0']), t))

def norm(s):
    s = re.sub(r'\$[^$]*\$', '', s)          # 去公式
    s = s.replace('（', '(').replace('）', ')')
    s = re.sub(r'[^\u4e00-\u9fff\w]', '', s)
    return s

missing = ['tk299-31-01','tk299-34-07','tk299-41-07','tk299-71-04','tk299-74-06','tk299-75-02',
           'tk299-75-06','tk299-75-10','tk299-81-01','tk299-81-04','tk299-81-07','tk299-82-01',
           'tk299-82-02','tk299-93-01','tk299-96-07']

for qid in missing:
    q = qm[qid]
    m = re.match(r'第(\d+)章考点(\d+)', q['chapter'])
    pool = sorted(segs_by.get((int(m.group(1)), int(m.group(2))), []), key=lambda s: (s[0], s[1]))
    fp = norm(q.get('question_text') or '')[2:10]   # 跳过题号"N、"
    found = None
    if len(fp) >= 4:
        for n in (8, 6, 5, 4):
            if n > len(fp): continue
            key = fp[:n]
            hits = [s for s in pool if key in norm(s[2])]
            if len(hits) >= 1:
                # 多命中时取包含位置最靠段首的
                hits.sort(key=lambda s: (s[0], s[1]))
                found = (n, hits[0])
                break
    if found:
        n, s = found
        print(f'{qid}: fp[{fp[:n]}] -> p{s[0]}  seg: {s[2][:40]}')
        pages[qid] = s[0]
    else:
        print(f'{qid}: fp[{fp}] NO MATCH  题面: {(q.get("question_text") or "")[:40]!r}')

json.dump(pages, open(r'D:/考研数学/_tk299_work/page_probe.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('total pages:', len(pages))
