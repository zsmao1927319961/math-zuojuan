# -*- coding: utf-8 -*-
"""三级: 邻题夹逼定位15题页码 (考点内题号单调不减)"""
import json, re

qs = json.load(open(r'D:/考研数学/组卷网站_static/data/questions.json', encoding='utf-8'))
qm = {q['id']: q for q in qs}
pages = json.load(open(r'D:/考研数学/_tk299_work/page_probe.json', encoding='utf-8'))
# 移除二级匹配的伪命中(选项段/考点说明段不可信)
for qid in ['tk299-31-01', 'tk299-34-07', 'tk299-71-04', 'tk299-82-02']:
    pages.pop(qid, None)

# 已知可靠的人工确认值(上轮照片工作)
pages['tk299-75-10'] = 240   # 书p240顶部第10题
pages['tk299-81-01'] = 244   # 第8章考点1第一题(考点起始页244)
pages['tk299-93-01'] = None  # 待夹逼
pages.pop('tk299-93-01', None)

by_ck = {}
for qid, pg in pages.items():
    q = qm[qid]
    m = re.match(r'第(\d+)章考点(\d+)', q['chapter'])
    key = (int(m.group(1)), int(m.group(2)))
    by_ck.setdefault(key, []).append((int(q['no']), pg))

missing = ['tk299-31-01','tk299-34-07','tk299-41-07','tk299-71-04','tk299-74-06','tk299-75-02',
           'tk299-75-06','tk299-75-10','tk299-81-01','tk299-81-04','tk299-81-07','tk299-82-01',
           'tk299-82-02','tk299-93-01','tk299-96-07']

for qid in missing:
    if qid in pages and pages[qid]:
        print(f'{qid}: 手工确认 p{pages[qid]}')
        continue
    q = qm[qid]
    m = re.match(r'第(\d+)章考点(\d+)', q['chapter'])
    key = (int(m.group(1)), int(m.group(2)))
    lst = sorted(by_ck.get(key, []))
    no = int(q['no'])
    lo = [p for n, p in lst if n < no and p]
    hi = [p for n, p in lst if n > no and p]
    p_lo = max(lo) if lo else None
    p_hi = min(hi) if hi else None
    if p_lo is not None and p_hi is not None and p_lo == p_hi:
        pages[qid] = p_lo
        print(f'{qid}: 夹逼同页确定 p{p_lo}')
    else:
        print(f'{qid}: 区间 p{p_lo} ~ p{p_hi} 需照片/裁剪确认')

json.dump(pages, open(r'D:/考研数学/_tk299_work/page_probe.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('pages total:', len([v for v in pages.values() if v]))
