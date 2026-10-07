# -*- coding: utf-8 -*-
# 合并 c1~c6 写回 questions.json 的 solution（仅覆盖原 solution 长度<10 的速答），并同步 tk299_dxy.json
import json, importlib.util, os

BASE = r'D:/考研数学/组卷网站_static'
P = os.path.join(BASE, 'data/questions.json')
merged = {}
for b in ['sol_c1', 'sol_c2', 'sol_c3', 'sol_c4', 'sol_c5', 'sol_c6']:
    spec = importlib.util.spec_from_file_location(b, os.path.join(BASE, 'tools', b + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    merged.update(m.SOL)
print('批次解析合计:', len(merged))

import re
bad = []
for qid, s in merged.items():
    if s.count('$') % 2:
        bad.append((qid, '$奇数'))
    for seg in re.findall(r'\$([^$]+)\$', s):
        if seg.count('{') != seg.count('}'):
            bad.append((qid, '括号不平衡:' + seg[:36]))
print('格式问题:', bad or '无')

raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)
n = 0
for x in d:
    if x['id'] in merged:
        cur = (x.get('solution') or '').strip()
        if len(cur) >= 10:
            print('跳过（已有详解）:', x['id'])
            continue
        x['solution'] = merged[x['id']]
        n += 1
print('写回 solution:', n, '题')
out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
