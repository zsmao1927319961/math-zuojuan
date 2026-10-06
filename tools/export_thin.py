# -*- coding: utf-8 -*-
# 导出 57 道薄解析题清单（id/题面/速答/考点）供主模型直接撰写详解
import json

d = json.load(open(r'D:/考研数学/组卷网站_static/data/questions.json', encoding='utf-8'))
targets = [x for x in d if x.get('source') == 'tk299'
           and len((x.get('answer_text') or '')) < 40
           and not (x.get('solution') or '').strip()]
out = [{'id': x['id'], 'type': x.get('type'), 'kp': x.get('kp'), 'kp_sub': x.get('kp_sub', ''),
        'qt': x.get('question_text') or '', 'ans': x.get('answer_text') or ''} for x in targets]
json.dump(out, open(r'D:/考研数学/组卷网站_static/tools/thin_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('导出', len(out), '题')
# 摘要打印：id | 题面(压缩) | 答案
for x in out:
    qt = x['qt'].replace('\n', ' ')[:110]
    print(x['id'], '|', qt, '|| 答案:', x['ans'][:40])
