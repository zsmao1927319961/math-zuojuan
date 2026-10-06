# -*- coding: utf-8 -*-
# tk299 记录补 school/year 字段（从题面尾部"（XX大学 YYYY 年…）"抽取）
import json, re, collections

P = r'D:/考研数学/组卷网站_static/data/questions.json'
raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)

pat = re.compile(r'（(?:判\s*断\s*题|选\s*择\s*题|计\s*算\s*题|填\s*空\s*题|简\s*答\s*题)\s*[，,]?\s*([^（）]*?(?:大学|学院))\s*(\d{4})?\s*年?[^（）]*）\s*$')
pat2 = re.compile(r'（([^（）]*?(?:大学|学院))\s*(\d{4})?\s*年?[^（）]*）\s*$')

n = 0
schools = collections.Counter()
for x in d:
    if x.get('source') != 'tk299':
        continue
    t = (x.get('question_text') or '').strip()
    m = pat.search(t) or pat2.search(t)
    if m:
        x['school'] = m.group(1).strip()
        x['year'] = m.group(2) or ''
        schools[x['school']] += 1
        n += 1
    else:
        x['school'] = ''
        x['year'] = ''

out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print('标注完成:', n, '/', sum(1 for x in d if x.get('source') == 'tk299'))
print(dict(schools.most_common(10)))
# 南邮题按章分布
c2 = collections.Counter(x['chapter'] for x in d if x.get('source') == 'tk299' and x.get('school') == '南京邮电大学')
print('南邮题章分布:', dict(sorted(c2.items())))
