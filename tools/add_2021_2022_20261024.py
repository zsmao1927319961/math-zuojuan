# -*- coding: utf-8 -*-
"""2021/2022 数二真题错题上架 mock.html 错题区（研可岸 oss 图链热链）。
字段结构照 tools/add_2019_2020_20261024.py 的 2020 卷册模式（qimg/ztCol/anaimgs，无 q/ans/sol 转录）。
exams 只追加不插队；kp/chapter 必须是 cxy 大观园分类树真实节点名，校验用内存对象，通过才落盘。
幂等：两卷册任一已存在即退出。
"""
import json, sys

DATA = 'data/mock_errors.json'
TREE = 'tools/cxy_categories_cache.json'
OSS_Q = 'https://oss.hzyankean.com/examMathQuestion/question/'
OSS_A = 'https://oss.hzyankean.com/examMathQuestion/analysis-v2/'

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
if '2021数二真题错题' in names or '2022数二真题错题' in names:
    print('已存在，幂等退出')
    sys.exit(0)

def E(no, typ, score, subj, chap, kp, qhash, anas):
    assert kp in flat, f'kp 节点不存在: {kp}'
    assert chap in flat, f'chapter 节点不存在: {chap}'
    return {
        'no': no, 'type': typ, 'score': score, 'subject': subj,
        'chapter': chap, 'kp': kp,
        'qimg': OSS_Q + qhash,
        'ztYear': None, 'ztCol': '真题',
        'anaimgs': [OSS_A + a for a in anas],
    }

def set_year(errors, year):
    for e in errors:
        e['ztYear'] = year

ex2021 = {
    'paper': {'name': '2021数二真题错题', 'date': '2021', 'group': '真题错题', 'taken': True,
              'sub': '真题错题 · 2021数学二 · 题面/解析源自研可岸真题网', 'answers': ''},
    'errors': [
        E(5,  '选择', 5,  '高数', '一元微分', '微分中值定理',
          'd9547592913a430d844a7a182c9b52de.png',
          ['math/math2/2021/T5/1.png', 'math/math2/2021/T5/2.png']),
        E(9,  '选择', 5,  '线代', '线性方程组', '方程组求解',
          '536c56a2aa594ff3a53050c54eac6caa.png',
          ['math/math2/2021/T9/1.png']),
        E(10, '选择', 5,  '线代', '矩阵', '初等变换与初等矩阵',
          '5a1d2e0d2e354a03bc97beb01924d32d.png',
          ['math/math2/2021/T10/1.png']),
        E(15, '填空', 5,  '高数', '微分方程', '解微分方程',
          '880b3f5789484bec916efb993ef061f2.png',
          ['math/math2/2021/T15/1.png']),
        E(22, '解答', 12, '线代', '特征值与特征向量', '相似对角化',
          'a8286f91d4054afcad59c36d95db7484.png',
          ['beaaaa24-b6e3-4b7e-8e75-d33f31e69db0.png']),
    ],
}
ex2022 = {
    'paper': {'name': '2022数二真题错题', 'date': '2022', 'group': '真题错题', 'taken': True,
              'sub': '真题错题 · 2022数学二 · 题面/解析源自研可岸真题网', 'answers': ''},
    'errors': [
        E(3,  '选择', 5,  '高数', '一元微分', '极值、最值与拐点',
          'be37d77cf25a4fb986943503b7b58b65.png',
          ['math/math2/2022/T3/1.png']),
        E(5,  '选择', 5,  '高数', '一元积分', '反常积分',
          '4ce8bf7ab8f749f4b59e8abfc7e53f7e.png',
          ['math/math2/2022/T5/1.png', 'math/math2/2022/T5/2.png']),
        E(6,  '选择', 5,  '高数', '极限', '数列极限',
          '05279690930e494787e788a022453b68.png',
          ['math/math2/2022/T6/1.png']),
        E(7,  '选择', 5,  '高数', '一元积分', '其他积分题型',
          '8b078df2cbca42feb4f2bcb327d4439a.png',
          ['math/math2/2022/T7/1.png']),
        E(8,  '选择', 5,  '线代', '特征值与特征向量', '相似对角化',
          'f87366f3c45b4340a11a92208fc72439.png',
          ['math/math2/2022/T8/1.png']),
        E(20, '解答', 12, '高数', '微分方程', '已知解反求微分方程（逆问题）',
          '91f402e84ef8447ead11f99fb7fee1b2.png',
          ['math/math2/2022/T20/1.png']),
        E(21, '解答', 12, '高数', '一元积分', '其他积分题型',
          'bde138930a37478989bf76f172cff5e7.png',
          ['math/math2/2022/T21/1.png']),
    ],
}
set_year(ex2021['errors'], 2021)
set_year(ex2022['errors'], 2022)

d2 = json.loads(json.dumps(d))          # 内存对象操作
d2['exams'] = ex + [ex2021, ex2022]     # 只追加不插队
before = sum(len(e.get('errors', [])) for e in d2['exams'])
assert len(d2['exams']) == len(ex) + 2
assert before - sum(len(e.get('errors', [])) for e in ex) == 12
for e in (ex2021, ex2022):              # 校验内存对象本身
    for er in e['errors']:
        assert er['ztYear'] in (2021, 2022)
        assert er['qimg'].startswith('https://oss.hzyankean.com/')
        assert all(a.startswith('https://oss.hzyankean.com/') for a in er['anaimgs'])

with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(d2, f, ensure_ascii=False, indent=1)
print('OK: exams', len(ex), '->', len(d2['exams']),
      '| errors', sum(len(e.get('errors', [])) for e in ex), '->', before,
      '| 2021:', len(ex2021['errors']), '2022:', len(ex2022['errors']))
