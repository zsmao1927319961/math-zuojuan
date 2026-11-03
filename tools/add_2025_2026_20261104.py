# -*- coding: utf-8 -*-
"""2025/2026 数二真题错题上架 mock.html 错题区（双录规则第三批）。
结构照 add_2023_2024_20261031.py；随后跑 localize_2025_2026_20261104.py 本地化。
2026 年题面图为中文路径 question/2026/数学二/T<N>/question.png（研可岸新格式）。幂等。"""
import json, sys

DATA = 'data/mock_errors.json'
TREE = 'tools/cxy_categories_cache.json'

with open(TREE, encoding='utf-8') as f:
    tree = json.load(f)
flat = set()
def walk(nodes):
    for n in nodes:
        flat.add(n.get('name'))
        walk(n.get('children') or [])
walk(tree)

with open(DATA, encoding='utf-8') as f:
    d = json.load(f)
ex = d['exams']
names = [e['paper']['name'] for e in ex]
if '2025数二真题错题' in names or '2026数二真题错题' in names:
    print('已存在，幂等退出')
    sys.exit(0)

def E(no, typ, score, subj, chap, kp, qurl, anas):
    assert kp in flat, f'kp 节点不存在: {kp}'
    assert chap in flat, f'chapter 节点不存在: {chap}'
    return {
        'no': no, 'type': typ, 'score': score, 'subject': subj,
        'chapter': chap, 'kp': kp,
        'qimg': qurl,
        'ztYear': None, 'ztCol': '真题',
        'anaimgs': anas,
    }

ex2025 = {
    'paper': {'name': '2025数二真题错题', 'date': '2025', 'group': '真题错题', 'taken': True,
              'sub': '真题错题 · 2025数学二 · 题面/解析源自研可岸真题网', 'answers': ''},
    'errors': [
        E(3,  '选择', 5,  '高数', '微分方程', '解微分方程',
          'https://oss.hzyankean.com/examMathQuestion/question/6cd0e97bb5964f5d9a1b328081a05430.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/fe9b23e9-8c46-41b4-894d-d8dbb6911f6c.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/9187420b-1cbb-47a9-b595-7a8a823d964b.png']),
        E(6,  '选择', 5,  '高数', '一元积分', '物理应用（数一二）',
          'https://oss.hzyankean.com/examMathQuestion/question/df01a8fc0aa843209f81775e20e37765.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/70d28f2d-5823-4325-b5fb-9fae4f44f701.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/a85aa3d7-9ee8-4f35-980c-dad0ec7e3be4.png']),
        E(18, '解答', 12, '高数', '一元微分', '微分中值定理',
          'https://oss.hzyankean.com/examMathQuestion/question/cf4c28a5ea054251be545fdf305a2cb1.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/b80b6fba-9a01-4961-b395-386d14cb229f.png']),
    ],
}

ex2026 = {
    'paper': {'name': '2026数二真题错题', 'date': '2026', 'group': '真题错题', 'taken': True,
              'sub': '真题错题 · 2026数学二 · 题面/解析源自研可岸真题网', 'answers': ''},
    'errors': [
        E(5,  '选择', 5,  '高数', '一元微分', '极值、最值与拐点',
          'https://oss.hzyankean.com/examMathQuestion/question/2026/数学二/T5/question.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2026/T5/2.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/62c73182-f681-4c69-a80e-cec88019900f.png']),
        E(7,  '选择', 5,  '高数', '一元积分', '奇偶性',
          'https://oss.hzyankean.com/examMathQuestion/question/2026/数学二/T7/question.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2026/T7/1.png']),
        E(10, '选择', 5,  '线代', '行列式', '行列式',
          'https://oss.hzyankean.com/examMathQuestion/question/2026/数学二/T10/question.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2026/T10/1.png']),
    ],
}

for e_, y in ((ex2025, 2025), (ex2026, 2026)):
    for er in e_['errors']:
        er['ztYear'] = y

d2 = json.loads(json.dumps(d))
d2['exams'] = ex + [ex2025, ex2026]
before = sum(len(e.get('errors', [])) for e in d2['exams'])
assert len(d2['exams']) == len(ex) + 2
assert before - sum(len(e.get('errors', [])) for e in ex) == 6
for e_ in (ex2025, ex2026):
    for er in e_['errors']:
        assert er['ztYear'] in (2025, 2026)
        assert er['qimg'].startswith('https://oss.hzyankean.com/')
        assert all(a.startswith('https://oss.hzyankean.com/') for a in er['anaimgs'])

with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(d2, f, ensure_ascii=False, indent=1)
print('OK: exams', len(ex), '->', len(d2['exams']),
      '| errors', sum(len(e.get('errors', [])) for e in ex), '->', before,
      '| 2025:', len(ex2025['errors']), '2026:', len(ex2026['errors']))
