# -*- coding: utf-8 -*-
import json, collections

d = json.load(open(r'D:/考研数学/组卷网站_static/data/questions.json', encoding='utf-8'))
tk = [x for x in d if x.get('source') == 'tk299']
thin = [x for x in tk if len((x.get('answer_text') or '')) < 40 and not (x.get('solution') or '').strip()]
thin_sol = [x for x in tk if len((x.get('answer_text') or '')) < 40 and (x.get('solution') or '').strip()]
print('tk299 总', len(tk))
print('解析薄(answer_text<40字 且无solution):', len(thin), '| 题型:', dict(collections.Counter(x.get('type') for x in thin)))
print('answer_text<40字但有solution兜底:', len(thin_sol), dict(collections.Counter(x.get('type') for x in thin_sol)))
print('中等(40-120字):', sum(1 for x in tk if 40 <= len((x.get('answer_text') or '')) < 120))
print('详细(>=120字):', sum(1 for x in tk if len((x.get('answer_text') or '')) >= 120))
print('薄解析样例:')
for x in thin[:10]:
    print(' ', x['id'], x.get('type'), '|', repr((x.get('answer_text') or '')[:44]))
