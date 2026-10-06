# -*- coding: utf-8 -*-
# 保守清理 v3：①tips全变体栏目头 ②紧随tips的"本考点…"说明段 ③尾部OCR碎片（白名单严格：
#   只删 空行/孤立"1、"/孤立"(1)"/纯破折号/长度<=2的行——【图】、选项字母行(A. B. C. D. 或孤立A-D)一律保留）
import json, re

P = r'D:/考研数学/组卷网站_static/data/questions.json'
raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)

re_tips = re.compile(r'^平[界原]\S{0,4}tips', re.I)
re_note = re.compile(r'^(本考点|本知识点|该考点)')
re_tail_num = re.compile(r'^\d+\s*[、.]?$')
re_tail_paren = re.compile(r'^[(（]\d+[)）][,，，]?$')
re_tail_dash = re.compile(r'^[—\-–·]+$')

def is_short_junk(s):
    # <=2字的孤立行；排除选项字母（孤立A-D 或 A. B. 形态）与【图】
    if len(s) > 2:
        return False
    if re.match(r'^[A-DＡ-Ｄ]\s*[、.．]?$', s):
        return False
    if s in ('【图】',):
        return False
    return True

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
    while keep:
        s = keep[-1].strip()
        if (s == '' or re_tail_num.match(s) or re_tail_paren.match(s)
                or re_tail_dash.match(s) or is_short_junk(s)):
            dropped.append((s[:20] if s else '(空行)'))
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
fig_total = sum((x.get('question_text') or '').count('【图】') for x in d if x.get('source') == 'tk299')
print('清理题数:', len(hits), '| 清理后【图】总数:', fig_total, '(基线42)')
for h in hits[:30]:
    print(' ', h[0], '| 删', h[2], '行 |', ' || '.join(h[1]))
