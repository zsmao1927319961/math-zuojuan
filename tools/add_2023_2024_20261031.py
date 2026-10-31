# -*- coding: utf-8 -*-
"""2023/2024 数二真题错题上架 mock.html 错题区（研可岸 oss 图链热链）。
结构照 add_2021_2022_20261024.py 的模式（qimg/ztCol/anaimgs 图链，无 q/ans/sol 转录）。
数据源特性：2024-7 的题面图研可岸存成了 analysis-v2 路径（内容已肉眼核验是题面，照用）。
exams 只追加不插队；kp/chapter 必须 cxy 树真实节点；校验用内存对象，通过才落盘。幂等。
"""
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
if '2023数二真题错题' in names or '2024数二真题错题' in names:
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

ex2023 = {
    'paper': {'name': '2023数二真题错题', 'date': '2023', 'group': '真题错题', 'taken': True,
              'sub': '真题错题 · 2023数学二 · 题面/解析源自研可岸真题网', 'answers': ''},
    'errors': [
        E(3,  '选择', 5,  '高数', '极限', '无穷小比阶',
          'https://oss.hzyankean.com/examMathQuestion/question/96613e138c984130b78daa9672da9427.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T3/1.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T3/2.png']),
        E(4,  '选择', 5,  '高数', '微分方程', '解微分方程',
          'https://oss.hzyankean.com/examMathQuestion/question/0e2a61c2b57c4dadb5d34b0a23331ed2.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T4/1.png']),
        E(6,  '选择', 5,  '高数', '一元积分', '反常积分',
          'https://oss.hzyankean.com/examMathQuestion/question/f388e611c8914f83a88d2499b38c3824.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T6/1.png']),
        E(8,  '选择', 5,  '线代', '矩阵', '伴随矩阵',
          'https://oss.hzyankean.com/examMathQuestion/question/f812fc913290473da2e4f7b8c457326a.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T8/1.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T8/2.png']),
        E(11, '填空', 5,  '高数', '极限', '无穷小比阶',
          'https://oss.hzyankean.com/examMathQuestion/question/55e6711d8eb64f32a9e049c21c9ea959.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T11/1.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T11/2.png']),
        E(12, '填空', 5,  '高数', '一元积分', '几何应用',
          'https://oss.hzyankean.com/examMathQuestion/question/a7de15682ad64194b7f110225dabbecf.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T12/1.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T12/2.png']),
        E(21, '解答', 12, '高数', '一元微分', '微分中值定理',
          'https://oss.hzyankean.com/examMathQuestion/question/4148bb170cbc4e218190cd35326945e0.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2023/T21/1.png']),
    ],
}

ex2024 = {
    'paper': {'name': '2024数二真题错题', 'date': '2024', 'group': '真题错题', 'taken': True,
              'sub': '真题错题 · 2024数学二 · 题面/解析源自研可岸真题网', 'answers': ''},
    'errors': [
        E(1,  '选择', 5,  '高数', '极限', '函数极限概念题',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T1/b2477ab2d1434e118e449ee0cdbcfaf1.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T1/c053a2da441d418283476e1089d2a8d3.png']),
        E(4,  '选择', 5,  '高数', '极限', '数列极限',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T4/25071aed631f43c0ac9d97304bcbdc2a.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T4/a2c98d979b784e95bf5df0901a58b8c5.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T4/7feb67f8a76c473787b1a2004bc4c955.png']),
        E(5,  '选择', 5,  '高数', '多元微分', '偏导数',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T5/588e9fd87c214374b0494374f12f61bf.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T5/4dbf9ad90c4b4e13ba0fb3a328934059.png']),
        E(7,  '选择', 5,  '高数', '一元积分', '反常积分',
          'https://oss.hzyankean.com/examMathQuestion/analysis-v2/eae0ffa6-2c0e-4448-8438-4157702b99b1.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T7/ab79988291764144888a502ea8afc45e.png']),
        E(9,  '选择', 5,  '线代', '矩阵', '伴随矩阵',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T9/fc8c4b1c7f67464da2aae9ea5bbf4e70.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T9/0488fbd4b8464b669b577fa50a23f9ad.png']),
        E(10, '选择', 5,  '线代', '特征值与特征向量', '相似对角化',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T10/29de936524634df4a4d30c2444f44fad.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T10/0e41d055bbe846f2b2b0900a7e78f3d4.png']),
        E(11, '填空', 5,  '高数', '一元微分', '曲率',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T11/48fe345744d84fe885becd974aef844b.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T11/17ab9775935a454cb66b2193d0687303.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T11/f514ec4f520347dab098aa03ea9812bb.png']),
        E(13, '填空', 5,  '高数', '微分方程', '解微分方程',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T13/ea0c9202eb2d443ea3e402ed31043e1a.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T13/cb4309035cd446bd918332b603c9751c.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T13/7ef5d74bbca448a8b9f40f4bdf9b4d0c.png']),
        E(14, '填空', 5,  '高数', '一元微分', '导数计算',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T14/ad1ab6639f5c4bf79207c9bf60b3aeec.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T14/58bc5d0316c04bfc89b7317a0f308441.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T14/63311057731d418b9b43fc84598305c1.png']),
        E(17, '解答', 10, '高数', '二重积分', '交换积分次序',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T17/67b6a13d3aa346289ddda8985dbfc33e.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T17/33b80ec05ced402abb9b6603ff308814.png',
           'https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T17/911405806cd84b7080b1f0f97edec2ba.png']),
        E(18, '解答', 12, '高数', '微分方程', '解微分方程',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T18/1674a2fe11014b2aae62587f4c9eab13.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T18/a26ff65a805648c48697cdb43ffde10e.png']),
        E(20, '解答', 12, '高数', '微分方程', '已知解反求微分方程（逆问题）',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T20/18ee067e1cb848248344e3871c2c0723.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T20/593611f0ac884e658683979e1ac19f15.png']),
        E(21, '解答', 12, '高数', '一元微分', '微分中值定理',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T21/6852294b22c547b09f98e3bf8d58b6be.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T21/2af122c8665e4afe907863181a0f9c38.png']),
        E(22, '解答', 12, '线代', '二次型', '标准型',
          'https://oss.hzyankean.com/examMathQuestion/question/math/math2/2024/T22/86a18e01daf44a93b5491144f1c78766.png',
          ['https://oss.hzyankean.com/examMathQuestion/analysis-v2/math/math2/2024/T22/22a4550343654c34b5ec41cb090019e0.png']),
    ],
}

set_year = None
for e_, y in ((ex2023, 2023), (ex2024, 2024)):
    for er in e_['errors']:
        er['ztYear'] = y

d2 = json.loads(json.dumps(d))
d2['exams'] = ex + [ex2023, ex2024]
before = sum(len(e.get('errors', [])) for e in d2['exams'])
assert len(d2['exams']) == len(ex) + 2
assert before - sum(len(e.get('errors', [])) for e in ex) == 21
for e_ in (ex2023, ex2024):
    for er in e_['errors']:
        assert er['ztYear'] in (2023, 2024)
        assert er['qimg'].startswith('https://oss.hzyankean.com/')
        assert all(a.startswith('https://oss.hzyankean.com/') for a in er['anaimgs'])

with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(d2, f, ensure_ascii=False, indent=1)
print('OK: exams', len(ex), '->', len(d2['exams']),
      '| errors', sum(len(e.get('errors', [])) for e in ex), '->', before,
      '| 2023:', len(ex2023['errors']), '2024:', len(ex2024['errors']))
