# -*- coding: utf-8 -*-
# 合并批次解析写回 questions.json 的 solution 字段 + 校验
import json, importlib.util, os

BASE = r'D:/考研数学/组卷网站_static'
P = os.path.join(BASE, 'data/questions.json')
merged = {}
for b in ['sol_b1', 'sol_b2', 'sol_b3', 'sol_b4', 'sol_b5', 'sol_b6']:
    spec = importlib.util.spec_from_file_location(b, os.path.join(BASE, 'tools', b + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for k, v in m.SOL.items():
        if k in merged:
            print('重复id警告:', k)
        merged[k] = v
print('批次解析合计:', len(merged))

# 校验：KaTeX 平衡 + 无 Unicode 上下标
import re
bad = []
for qid, s in merged.items():
    if s.count('$') % 2:
        bad.append((qid, '$奇数'))
    for seg in re.findall(r'\$([^$]+)\$', s):
        if seg.count('{') != seg.count('}'):
            bad.append((qid, '括号不平衡:' + seg[:36]))
    if re.search(r'[⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉]', s):
        bad.append((qid, 'Unicode上下标'))
print('格式问题:', bad or '无')

raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)
n = 0
for x in d:
    if x['id'] in merged:
        x['solution'] = merged[x['id']]
        n += 1
print('写回 solution:', n, '题')
out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print('已写回')
