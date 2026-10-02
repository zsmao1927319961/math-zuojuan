# -*- coding: utf-8 -*-
# 复核图片缺失：正确基准 data/images；并确认页面如何拼图片路径
import json, os

BASE = r'D:/考研数学/组卷网站_static'
d = json.load(open(os.path.join(BASE, 'data/questions.json'), encoding='utf-8'))

def exists(v):
    return os.path.exists(os.path.join(BASE, 'data', v.replace('/', os.sep)))

for name in ('qhzt', 'tk299'):
    qs = [x for x in d if x.get('source') == name]
    miss = []
    for x in qs:
        for f in ('question_img', 'answer_img'):
            v = x.get(f)
            if v and not exists(v):
                miss.append((x['id'], f, v))
    qimg = sum(1 for x in qs if x.get('question_img'))
    aimg = sum(1 for x in qs if x.get('answer_img'))
    print(name, '总', len(qs), '| 带题图', qimg, '| 带答案图', aimg, '| 真缺失引用', len(miss))
    for m in miss[:25]:
        print('  ', m[0], m[1], m[2])
    if len(miss) > 25:
        # 按目录归类看分布
        c = __import__('collections').Counter(os.path.dirname(m[2]) for m in miss)
        print('   缺失分布:', dict(c))
