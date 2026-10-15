# -*- coding: utf-8 -*-
# 2026-10-15: mock_errors.json 加选填专项 31 套目录（只录错题，errors 空）
# 来源：往年模拟卷选填精选（亚瑟爱数学做题本）94页，目录页码即 pdf_page
import json, io, sys

P = 'data/mock_errors.json'
d = json.load(io.open(P, encoding='utf-8'))
if any(s.get('id') == 'xuantian' for s in d.get('series', [])):
    print('already added'); sys.exit(0)

def vols(spec):
    # spec: [(name, pdf_page, done), ...]
    return [{'vol': i + 1, 'name': n, 'pdf_page': pg, 'done': bool(done), 'errors': []}
            for i, (n, pg, done) in enumerate(spec)]

def mk(name, pg0, k, done_vols=()):
    return vols([('卷%d' % (i + 1), pg0 + 3 * i, (i + 1) in done_vols) for i in range(k)])

series = [{
    'id': 'xuantian',
    'name': '选填专项',
    'source': '往年模拟卷选填精选 · 亚瑟爱数学做题本（PDF 94 页，本地微信文件 2026-10）',
    'groups': [
        {'id': 'yb24', 'name': '24 余炳森五套卷', 'vols': mk('余炳森', 2, 5, (1,))},
        {'id': 'll24', 'name': '24 李林四套卷',   'vols': mk('李林', 17, 4)},
        {'id': 'zy24', 'name': '24 张宇四套卷',   'vols': mk('张宇', 29, 4)},
        {'id': 'cy24', 'name': '24 超越十套卷',   'vols': mk('超越', 41, 10)},
        {'id': 'zy25', 'name': '25 张宇八套卷',   'vols': mk('张宇', 71, 8)},
    ],
}]

# 展平成页面用的 series[]：每组一套
flat = []
for g in series[0]['groups']:
    flat.append({'id': g['id'], 'name': g['name'], 'kind': '选填专项', 'vols': g['vols']})

d['series'] = flat
d['note'] = d.get('note', '') + ' | 2026-10-15 加选填专项31套目录（余炳森5/李林4/张宇4/超越10/张宇25年8），每套=选择1~10+填空11~16，只录错题；卷一已做待录。'

io.open(P, 'w', encoding='utf-8', newline='\n').write(
    json.dumps(d, ensure_ascii=False, indent=1) + '\n')

# 校验
d2 = json.load(io.open(P, encoding='utf-8'))
n = sum(len(v['errors']) for s in d2['series'] for v in s['vols'])
nv = sum(len(s['vols']) for s in d2['series'])
print('series:', len(d2['series']), 'vols:', nv, 'errors:', n)
print('exams kept:', len(d2['exams']))
v1 = [v for s in d2['series'] for v in s['vols'] if s['id'] == 'yb24'][0]
print('yb24 vol1:', v1)
