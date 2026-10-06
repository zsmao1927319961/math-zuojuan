# -*- coding: utf-8 -*-
# 清理 tk299 question_text 里的书页栏头残留行（"计 算 题，要求……"等独立行）
import json, re

P = r'D:/考研数学/组卷网站_static/data/questions.json'
raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)
pat = re.compile(r'^(计\s*算\s*题|选\s*择\s*题|填\s*空\s*题|判\s*断\s*题|简\s*答\s*题)\s*[，,、]?\s*(要\s*求[\s…：:.]*)?$')
hits = []
for x in d:
    if x.get('source') != 'tk299':
        continue
    t = (x.get('question_text') or '')
    keep, dropped = [], []
    for ln in t.split('\n'):
        (dropped if pat.match(ln.strip()) else keep).append(ln)
    if dropped:
        x['question_text'] = '\n'.join(keep).strip()
        hits.append((x['id'], [s.strip()[:26] for s in dropped]))
out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print('清理题数:', len(hits))
for h in hits[:25]:
    print(' ', h[0], '| 删:', h[1])
