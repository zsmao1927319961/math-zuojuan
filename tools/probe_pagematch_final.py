# -*- coding: utf-8 -*-
"""最终页码解析: crops_inventory 块首题号+pages / step3 PATCHES / 手工确认 三源合一
输出 _tk299_work/page_final.json {qid: page} 并校验考点内单调"""
import json, re

inv = json.load(open(r'D:/考研数学/_tk299_work/crops_inventory.json', encoding='utf-8'))
qs = json.load(open(r'D:/考研数学/组卷网站_static/data/questions.json', encoding='utf-8'))
tx = [q for q in qs if q.get('source') == 'tk299']

# step3_split.py 的人工补丁: 页 -> [(y, 题号)]
PATCHES = {196: [7], 199: [3], 200: [7], 201: [3], 202: [4], 210: [5],
           233: [4], 235: [3, 6], 237: [2], 238: [6], 240: [10], 242: [2],
           246: [4], 248: [7], 251: [1], 252: [2], 264: [7], 232: [4]}
# 手工确认(上轮照片工作)
MANUAL = {'tk299-75-06': 238, 'tk299-75-10': 240, 'tk299-81-01': 244}

pages = {}
# 源1: 块首题号 -> 块首页码 (id格式: tk299-<c><k>-<no两位>, k不补零)
def qid_of(c, k, n):
    return f'tk299-{c}{k}-{n:02d}'
for blk in inv:
    nums = blk.get('nums') or []
    pgs = sorted(set(blk.get('pages') or []))
    if not nums or not pgs:
        continue
    first = min(nums)
    qid = qid_of(blk['c'], blk['k'], first)
    pages[qid] = pgs[0]
# 源1b: 块内 segs 里题号行开头匹配的段页(补缺)
for blk in inv:
    for pg, seg in blk['segs']:
        m = re.match(r'^\s*(\d{1,2})[、.．]\S', seg.get('t', '').strip())
        if m:
            qid = qid_of(blk['c'], blk['k'], int(m.group(1)))
            if qid not in pages:
                pages[qid] = pg
# 源2: PATCHES
valid_ids = {q['id'] for q in tx}
for pg, nums in PATCHES.items():
    for n in nums:
        # 需定位是哪章考点: 用块归属(该页属于哪个考点的pages)
        for blk in inv:
            if pg in (blk.get('pages') or []):
                qid = qid_of(blk['c'], blk['k'], n)
                if qid in valid_ids:
                    pages[qid] = pg
                break
# 源3: 手工
pages.update(MANUAL)

# 汇总+校验
res = {}
for q in tx:
    p = pages.get(q['id'])
    res[q['id']] = p
have = {k: v for k, v in res.items() if v}
print(f'解析 {len(have)}/{len(tx)}')
# 单调校验
by_ck = {}
for q in tx:
    m = re.match(r'第(\d+)章考点(\d+)', q['chapter'])
    by_ck.setdefault((int(m.group(1)), int(m.group(2))), []).append((int(q['no']), res[q['id']], q['id']))
bad = []
for key, lst in sorted(by_ck.items()):
    lst.sort()
    prev = 0
    for no, pg, qid in lst:
        if pg is None: continue
        if pg < prev:
            bad.append((qid, pg, prev))
        prev = pg if pg else prev
print('单调违例:', bad if bad else '无')
missing = [k for k, v in res.items() if not v]
print('未解析:', missing)
json.dump(res, open(r'D:/考研数学/_tk299_work/page_final.json', 'w', encoding='utf-8'), ensure_ascii=False)
