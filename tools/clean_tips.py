# -*- coding: utf-8 -*-
# 清理 tk299 question_text 里的考点头/栏目残留：
# ①"考点N[：:]xxx"行 ②"平界小马哥tips[：:]"行 ③tips 说明行("本考点…"直到首个题号行) ④尾部孤立碎片("平界"/"本"/"裁少"等)
import json, re

P = r'D:/考研数学/组卷网站_static/data/questions.json'
raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)

re_kt = re.compile(r'^考点\s*\d*')
re_tips = re.compile(r'^平界(小马哥)?\s*tips', re.I)
re_note = re.compile(r'^(本考点|本知识点|该考点)')
re_junk = re.compile(r'^(平界|本|裁少|必是精品|品[,，]?必是精品)$')

hits = []
for x in d:
    if x.get('source') != 'tk299':
        continue
    t = (x.get('question_text') or '')
    lines = t.split('\n')
    keep, dropped, in_tips = [], [], False
    for ln in lines:
        s = ln.strip()
        if re_kt.match(s) and len(s) < 40:
            dropped.append(s[:30]); in_tips = True; continue
        if re_tips.match(s):
            dropped.append(s[:30]); in_tips = True; continue
        if in_tips and re_note.match(s):
            dropped.append(s[:30]); continue
        if in_tips and re.match(r'^\d+\s*[、.]\s*[^、.]', s):
            in_tips = False  # 到达第一个题号，说明段结束
        if re_junk.match(s):
            dropped.append(s[:30]); continue
        keep.append(ln)
    # 去掉首尾空行
    while keep and not keep[0].strip():
        keep.pop(0)
    while keep and not keep[-1].strip():
        keep.pop()
    if dropped:
        x['question_text'] = '\n'.join(keep)
        hits.append((x['id'], dropped[:6]))

out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print('清理题数:', len(hits))
for h in hits[:30]:
    print(' ', h[0], '| 删:', ' || '.join(h[1]))
