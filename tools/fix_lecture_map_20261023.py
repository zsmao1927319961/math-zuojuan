# -*- coding: utf-8 -*-
"""修正【对应课件】讲次错位:真实课件PDF标题从文件26起讲次=文件号-1
(文件26标题'第二十五讲-PCM', 文件29标题'第二十八讲-线性分组码', ... 文件37标题'第三十六讲-移动通信')。
当年精解按文件号标注,导致 PCM~移动通信 共12门课的标注全部+1。
修复目标:
  1) D:/考研数学/组卷网站_static/data/zhenti801.json (801真题错题模块)
  2) Downloads 的 真题精解合订本.md,并重跑 make_html.py 重新生成合订本.html
规则:按《标题关键词》定位,讲次token与真实讲次不符才替换;文件01-25的内容标注本就正确,不受影响。
"""
import json
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

# (标题关键词 → 真实讲次token)。顺序即匹配优先级。
TRUE_MAP = [
    ('PCM',                '第二十五讲'),
    ('语音压缩',            '第二十六讲'),
    ('变速率',              '第二十七讲'),
    ('时分复用',            '第二十七讲'),
    ('帧结构设计',          '第二十七讲'),
    ('线性分组码',          '第二十八讲'),
    ('循环码',              '第二十九讲'),
    ('代数表述',            '第三十讲'),
    ('几何表述',            '第三十一讲'),
    ('维特比',              '第三十二讲'),
    ('扩展频谱',            '第三十三讲'),
    ('扩频',               '第三十三讲'),
    ('载波同步',            '第三十四讲'),
    ('巴克码',              '第三十五讲'),
    ('移动通信',            '第三十六讲'),
]
CN = '第[一二三四五六七八九十]+讲'
HEBING = r'C:\Users\19273\Downloads\1998-2025年南邮通信原理真题及解析\南邮801通信原理历年真题答案精解_1998-2025合订本.md'
MAKE_HTML = r'D:\考研数学\组卷网站_static\make_html.py'


def fix_text(s):
    n = 0
    for kw, right in TRUE_MAP:
        # 第X讲《...kw...》:讲次与真实讲次不同→替换为真实讲次
        pat = re.compile(CN + r'(?=《[^》]*' + re.escape(kw) + ')')
        s2, k = pat.subn(right, s)
        n += k
        s = s2
    return s, n


# —— 1) 801真题错题模块数据 ——
p1 = r'D:\考研数学\组卷网站_static\data\zhenti801.json'
d = json.load(open(p1, encoding='utf-8'))
cnt1 = 0
for y in d['years']:
    for q in y['qs']:
        if q.get('key'):
            q['key'], k = fix_text(q['key'])
            cnt1 += k
        if q.get('stem'):
            q['stem'], k = fix_text(q['stem'])
            cnt1 += k
d['note'] += ' 2026-10-23 课件讲次修正:真实课件文件26起标题讲次=文件号-1(28讲=线性分组码), PCM~移动通信12门课的【对应课件】标注-1。'
json.dump(d, open(p1, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'zhenti801.json: 修正 {cnt1} 处讲次标注')

# —— 2) 合订本 md + 重新生成 html ——
md = open(HEBING, encoding='utf-8').read()
md2, cnt2 = fix_text(md)
open(HEBING, 'w', encoding='utf-8').write(md2)
print(f'合订本.md: 修正 {cnt2} 处讲次标注')
r = subprocess.run([sys.executable, MAKE_HTML], capture_output=True, text=True, encoding='utf-8')
print(r.stdout.strip()[-200:] if r.stdout else r.stderr.strip()[-200:])

# —— 自查:TDM题的对应课件 ——
d2 = json.load(open(p1, encoding='utf-8'))
for y in d2['years']:
    if y['year'] == 2014:
        for q in y['qs']:
            if 'TDM' in q['no']:
                line = [l for l in q['key'].split('\n') if '对应课件' in l]
                print('2014 TDM 题对应课件 →', line[0].strip() if line else '无')
