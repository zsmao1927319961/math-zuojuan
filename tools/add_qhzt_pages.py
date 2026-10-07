# -*- coding: utf-8 -*-
"""qhzt 113题页码: 解析《原题整理笔记.md》的 'X. 例（pNN）' 精确页 + 专题范围兜底"""
import json, re

NOTE = r"C:/Users/19273/Desktop/强化专题/原题整理笔记.md"
text = open(NOTE, encoding='utf-8').read()

# 1) 逐节解析: 当前专题号 + 'N. 例（pNN）'
exact = {}   # (topic, qno) -> page
cur = None
for line in text.split('\n'):
    m = re.match(r'^##\s*专题([一二三四五六七八九十]+)', line.strip())
    if m:
        cn = m.group(1)
        d = '零一二三四五六七八九'
        if cn in d[1:]: cur = d.index(cn)
        elif cn == '十': cur = 10
        elif cn.startswith('十'): cur = 10 + d.index(cn[1])
        elif cn.endswith('十'): cur = d.index(cn[0]) * 10
        elif '十' in cn:
            a, b = cn.split('十'); cur = d.index(a) * 10 + d.index(b)
        continue
    if cur is None: continue
    m = re.match(r'^(\d{1,2})[\.、]\s*例（p(\d{1,3})', line.strip())
    if m:
        exact[(cur, int(m.group(1)))] = int(m.group(2))

# 2) 专题范围兜底 (讲义书页, 由照片号↔书页映射推断)
RANGE = {1:'3~6',2:'7~8',3:'9~11',4:'12~13',5:'14~17',6:'19~24',7:'25~27',8:'28~30',
         9:'33~35',10:'36~37',11:'38~44',12:'45~47',13:'48~54',14:'55~58',15:'59~64',
         16:'65~69',17:'70~71',18:'72~73',19:'75~79',20:'77~79',21:'80~81',22:'82~86',
         23:'87~89',24:'90~91',25:'92',26:'93~94',27:'95~96'}
# 3) 专题二十(重组)强制精确页
T20 = {1:77, 2:78, 3:78, 4:79, 5:79}

qs = json.load(open(r"D:/考研数学/组卷网站_static/data/questions.json", encoding='utf-8'))
qh = [q for q in qs if q.get('source') == 'qhzt']
n_exact = n_range = 0
by_topic = {}
for q in qh:
    m = re.match(r'qhzt-(\d+)-(\d+)$', q['id'])
    t, no = int(m.group(1)), int(m.group(2))
    if t == 20:
        pg = T20.get(no)
    else:
        pg = exact.get((t, no))
    if pg:
        q['book_page'] = pg; n_exact += 1
    else:
        q['book_page'] = RANGE.get(t, ''); n_range += 1
    by_topic.setdefault(t, []).append((no, q['book_page']))

json.dump(qs, open(r"D:/考研数学/组卷网站_static/data/questions.json", 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f'qhzt 113题: 精确页 {n_exact}, 专题范围 {n_range}')
for t in sorted(by_topic):
    row = sorted(by_topic[t])
    marks = ''.join(str(p) if isinstance(p, int) else '[' + str(p) + ']' for _, p in row)
    print(f'  专题{t:2d}({len(row)}题): {marks}')
