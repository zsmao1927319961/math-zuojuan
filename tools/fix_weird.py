# -*- coding: utf-8 -*-
# 修复 qhzt solution 里的 11 处 OCR 怪字符（对照上下文语义还原）
import json

P = r'D:/考研数学/组卷网站_static/data/questions.json'
raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)
Q = {x['id']: x for x in d}

FIX = {
    'qhzt-3-3':  [('sin(\\pi fT)=0', '\\sin(\\pi fT)=0'), ('​', '')],  # ZWSP 移除
    'qhzt-16-5': [('Sa}^2(ƒ\\pi T_b)', 'Sa}^2(f\\pi T_b')],
    'qhzt-21-1': [('Ɠ=[0,0,π,π,0,0]', '\\varphi=[0,0,π,π,0,0]')],
    'qhzt-21-2': [('Ɠ=[0,0,π,π,0]', '\\varphi=[0,0,π,π,0]')],
    'qhzt-22-6': [('ē x_k=\\bar x_k', '\\mathrm{E}[x_k]=\\bar x_k'),
                  ('ēx=1=y_2', '\\mathrm{E}[x]=1=y_2'),
                  ('ēx=3=y_3', '\\mathrm{E}[x]=3=y_3')],
    'qhzt-27-1': [('m^2+ĥm^2', 'm^2+\\hat{m}^2'),
                  ('m^2-ĥm^2', 'm^2-\\hat{m}^2'),
                  ('m^2-ĥm^2', 'm^2-\\hat{m}^2'),
                  ('mĥm\\sin2ω_ct', 'm\\hat{m}\\sin2ω_ct')],
}
n = 0
for qid, subs in FIX.items():
    x = Q[qid]
    t = x['solution']
    for old, new in subs:
        if old == '​':
            assert '​' in t
            t = t.replace('​', '')
            n += 1
            continue
        assert old in t, (qid, old)
        t = t.replace(old, new, 1)
        n += 1
    x['solution'] = t
print('替换完成', n, '处')

out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print('已写回')
