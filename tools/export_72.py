# -*- coding: utf-8 -*-
# 导出 72 道速答型选择/判断题清单（题面+选项+速答+考点）
import json

BASE = r'D:/考研数学/组卷网站_static'
dxy = json.load(open(BASE + '/data/tk299_dxy.json', encoding='utf-8'))
qj = {x['id']: x for x in json.load(open(BASE + '/data/questions.json', encoding='utf-8'))}

out = []
for q in dxy['questions']:
    expl = (q.get('explanation_md') or '').strip()
    if len(expl) >= 10:
        continue
    src = qj.get(q['question_id'], {})
    opts = ''
    if q.get('options'):
        opts = ' | '.join(o['label'] + '.' + o['content_md'] for o in q['options'])
    out.append({'id': q['question_id'], 'ans': expl, 'opts': opts,
                'qt': (src.get('question_text') or ''), 'kp': src.get('kp') or ''})

json.dump(out, open(BASE + '/tools/thin72.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('导出', len(out), '题')
for x in out:
    qt = x['qt'].replace('\n', ' ')[:100]
    print(x['id'], '|', qt, '| 速答:', x['ans'][:20], '|', (x['opts'] or '')[:40])
