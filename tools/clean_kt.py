# -*- coding: utf-8 -*-
# v4：只删题面开头的考点头栏目行（"考点N：xxx"，<40字），其余不动
import json, re

P = r'D:/考研数学/组卷网站_static/data/questions.json'
raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)

re_kt = re.compile(r'^考点\s*\d*\s*[：:，,]?\s*\S{0,30}$')
hits = []
for x in d:
    if x.get('source') != 'tk299':
        continue
    t = (x.get('question_text') or '')
    lines = t.split('\n')
    # 只删位于开头、连续的考点头行
    i = 0
    dropped = []
    while i < len(lines) and re_kt.match(lines[i].strip()) and len(lines[i].strip()) < 40:
        dropped.append(lines[i].strip()[:30])
        i += 1
    if dropped:
        newt = '\n'.join(lines[i:]).strip()
        if len(newt) > 30:  # 防止清空题面
            x['question_text'] = newt
            hits.append((x['id'], dropped))

out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print('清理题数:', len(hits))
for h in hits[:20]:
    print(' ', h[0], '| 删:', ' || '.join(h[1]))
