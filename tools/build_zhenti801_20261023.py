# -*- coding: utf-8 -*-
"""生成 data/zhenti801.json:南邮801通信原理历年真题(1998-2025)逐题卷册数据。
来源:另一工作区的逐题精解 markdown(draft-fbde2268/精解/YYYY.md,28年全)。
每题拆成 stem(题面,可见) + key(精解,默认隐藏),无分割标记的简答题整块并入题面。
"""
import glob
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
SRC_DIR = r'C:\Users\19273\.zcode\workspace\draft-fbde2268-b5a5-402c-83e5-17c48ed7b0b5\精解'
OUT = r'D:\考研数学\组卷网站_static\data\zhenti801.json'

# 精解起点标记(取最早命中处切一刀)
SPLIT = ['**逐空精解**', '**逐项精解**', '**逐问精解**', '**精解**', '【答案】',
         '【切入点】', '【解题过程】', '**第1空', '**第1问', '**答案**', '**解析**']
SKIP_HEAD = re.compile(r'自查')
STEM_LABEL = re.compile(r'^(\s*(?:-\s*)?(?:\*\*)?【?题目】?(?:\*\*)?[：:]?\s*)')

years_out = []
tot_q = 0
no_split = 0
for fp in sorted(glob.glob(SRC_DIR + r'\19*.md') + glob.glob(SRC_DIR + r'\20*.md')):
    ym = re.search(r'(19|20)\d{2}', fp.rsplit('/', 1)[-1].rsplit('\\', 1)[-1])
    year = int(ym.group(0))
    md = open(fp, encoding='utf-8').read()
    title_m = re.search(r'^# (.+)$', md, re.M)
    title = title_m.group(1).strip() if title_m else f'{year}年真题精解'
    brief_m = re.search(r'^> (.+)$', md, re.M)
    brief = brief_m.group(1).strip() if brief_m else ''
    secs = re.split(r'\n## ', md)[1:]
    qs = []
    for i, sec in enumerate(secs, 1):
        head, _, body = sec.partition('\n')
        head = head.strip()
        if SKIP_HEAD.search(head):
            continue
        # 找最早的精解起点
        cut = len(body)
        for mk in SPLIT:
            p = body.find(mk)
            if p != -1 and p < cut:
                cut = p
        stem = body[:cut].strip()
        key = body[cut:].strip() if cut < len(body) else ''
        stem = STEM_LABEL.sub('', stem).strip()
        if len(stem) < 15:  # 判断题等题干写在解析里的节:整块并入题面
            stem = body.strip()
            key = ''
        if not key:
            no_split += 1
        qs.append({'id': f'y{year}q{i}', 'no': head, 'stem': stem, 'key': key})
    tot_q += len(qs)
    years_out.append({'year': year, 'title': title, 'brief': brief, 'qs': qs})

years_out.sort(key=lambda x: x['year'])
out = {
    'note': ('2026-10-23 由 tools/build_zhenti801_20261023.py 从 28 年逐题精解 md 生成:'
             '每题 stem=题面(默认可见) key=精解(默认隐藏,页面点看);'
             '无分割标记的简答题整块并入题面精解为空;已剔除各年"本年自查"节。'
             '做题状态存 localStorage z801_state_v1(会/半/错+错因+重做打卡)。'),
    'years': years_out,
}
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f'年份 {len(years_out)} 个,总题 {tot_q} 道,无独立精解块 {no_split} 道')
for y in years_out[:3] + years_out[-2:]:
    print(f"  {y['year']}: {len(y['qs'])} 题 | {y['brief'][:36]}")
empty_stem = [q['id'] for y in years_out for q in y['qs'] if len(q['stem']) < 10]
print('题面过短(需人工看):', empty_stem if empty_stem else '无')
