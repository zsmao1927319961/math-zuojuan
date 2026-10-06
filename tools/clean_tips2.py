# -*- coding: utf-8 -*-
# 二次清理：tips 全变体（平界/平原 + 小马哥/小鸟哥/…）+ 尾部OCR碎片流
import json, re

P = r'D:/考研数学/组卷网站_static/data/questions.json'
raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)

re_tips = re.compile(r'^平[界原].{0,4}tips', re.I)
re_note = re.compile(r'^(本考点|本知识点|该考点)')
re_tail = re.compile(r'^(\d+\s*[、.]?|[(（]\d+[)）]?|[—\-·.]+|.{0,3})$')

hits = []
for x in d:
    if x.get('source') != 'tk299':
        continue
    t = (x.get('question_text') or '')
    lines = t.split('\n')
    keep, dropped = [], []
    for ln in lines:
        s = ln.strip()
        if re_tips.match(s):
            dropped.append(s[:24]); continue
        if re_note.match(s):
            dropped.append(s[:24]); continue
        keep.append(ln)
    # 尾部碎片流：从尾往回删（空行 / "1、" / "(1)" / 破折号 / ≤3字行）
    while keep:
        s = keep[-1].strip()
        if s == '' or re_tail.match(s):
            dropped.append(s[:24] if s else '(空行)')
            keep.pop()
        else:
            break
    while keep and not keep[0].strip():
        keep.pop(0)
    if dropped:
        x['question_text'] = '\n'.join(keep)
        hits.append((x['id'], dropped[:5], len(dropped)))

out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print('二次清理题数:', len(hits))
for h in hits[:30]:
    print(' ', h[0], '| 删', h[2], '行 |', ' || '.join(h[1]))
