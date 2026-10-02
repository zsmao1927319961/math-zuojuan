# -*- coding: utf-8 -*-
# 定位数学段里的可疑字符：ZWSP(8203)/Ɠ/ē/ĥ 等
import json, re, sys

d = json.load(open(r'D:/考研数学/组卷网站_static/data/questions.json', encoding='utf-8'))
susp = re.compile(r'[\u200b\u0193\u0113\u0125\u0192]')
found = 0
for x in d:
    if x.get('source') not in ('qhzt', 'tk299'):
        continue
    for f in ('question_text', 'answer_text', 'solution'):
        t = x.get(f) or ''
        for m in susp.finditer(t):
            found += 1
            s = max(0, m.start() - 40)
            print(x['id'], f, repr(m.group()), 'U+%04X' % ord(m.group()))
            print('   ...' + t[s:m.start() + 40].replace('\n', '⏎') + '...')
print('可疑字符总数:', found)
