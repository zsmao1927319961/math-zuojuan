# -*- coding: utf-8 -*-
"""2026-10-18 考点5二合一拆分(用户报"一卡只能一题"):
1) tk299-75-01 回归北邮2017单题(选择题), school/year 归位 北京邮电大学/2017;
2) 北交大2022三3 题干从 75-01 归还 tk299-75-02(该书第2题的真题面), 撤"（题面照片缺失，据解析反推）",
   school/year 归位 北京交通大学/2022;
3) 顺修 75-02 答案 OCR 错 18a^3 -> 18a^2 (对照书答案页 p144, Es=(2a^2*4+10a^2*8+18a^2*4)/16=10a^2);
4) 题面图 q_tk299-75-02.jpg 原为书页页脚废条, 从 q_tk299-75-01.jpg(书p54整段照片)裁 y[220,336) 替换为第2题真题面。
总数 430 不变 -> 全站 317/430 计数零改动。json 经 round-trip 逐字节校验后才落盘。
"""
import json
from PIL import Image

P = 'data/questions.json'
raw = open(P, encoding='utf-8').read()
data = json.loads(raw)

# 0) 格式保真: 重序列化必须与原文件逐字节一致(仅允许文件尾换行差异), 否则中止
rt = json.dumps(data, ensure_ascii=False, indent=1)
assert rt == raw.rstrip('\n'), 'round-trip mismatch — 格式漂移, 中止不写盘'
assert len(data) == 430, '题数不是430: %d' % len(data)

q1 = next(q for q in data if q['id'] == 'tk299-75-01')
q2 = next(q for q in data if q['id'] == 'tk299-75-02')
assert '北京邮电大学 2017' in q1['question_text'] and '北京交通大学 2022' in q1['question_text']
assert q1['question_text'].index('2、16QAM') > q1['question_text'].index('A、6')

# 1) 拆题干: "2、..." 段整体移交给 75-02
lines = q1['question_text'].split('\n')
i2 = next(i for i, l in enumerate(lines) if l.startswith('2、16QAM'))
stem2 = '\n'.join(lines[i2:])
q1['question_text'] = '\n'.join(lines[:i2])
assert q1['question_text'].endswith('D、18'), '75-01 尾部意外: %r' % q1['question_text'][-20:]

old2 = q2['question_text']
q2['question_text'] = stem2

# 2) 元数据归位
q1['school'], q1['year'] = '北京邮电大学', '2017'
q2['school'], q2['year'] = '北京交通大学', '2022'

# 3) OCR 错修复
assert '18a^3 \\times 4' in q2['answer_text'], '75-02 答案锚点不在: %r' % q2['answer_text'][-60:]
q2['answer_text'] = q2['answer_text'].replace('18a^3 \\times 4', '18a^2 \\times 4')

# 4) 兜底断言
assert '北京交通大学' not in q1['question_text']
assert '题面照片缺失' not in json.dumps(q2, ensure_ascii=False)
assert '\\frac{2}{5}' in q2['answer_text']

out = json.dumps(data, ensure_ascii=False, indent=1) + ('\n' if raw.endswith('\n') else '')
open(P, 'w', encoding='utf-8', newline='\n').write(out)
json.load(open(P, encoding='utf-8'))  # 落盘后可解析

# 5) 题面图: 书p54照片裁出第2题段
im = Image.open('data/images/t299/q_tk299-75-01.jpg')
W, H = im.size
crop = im.crop((0, 220, W, 336))
crop.save('data/images/t299/q_tk299-75-02.jpg', quality=92)

print('OK 75-01 question_text:')
print(q1['question_text'])
print('OK 75-02 question_text:')
print(q2['question_text'])
print('OK 75-02 school/year:', q2['school'], q2['year'], '| 75-01:', q1['school'], q1['year'])
print('crop:', (W, H), '->', crop.size)
