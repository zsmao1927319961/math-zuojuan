# -*- coding: utf-8 -*-
"""2026-10-21 考点7·3 解析纠错(用户报"答案给错了,应为CBCA"):
tk299-97-03(PCM30/32, 南邮2023一6) answer_text="CBCA" 本就正确(书答案条p357/印177: "3、CBCA"),
错在 solution: 误把全系统总速率 2048kbit/s 当每路话音(选A)、TS16 总速率 64kbit/s 当信令速率(选C),
结论写成"答案 A、C、C、A", 与答案键自相矛盾。
重写解析: (1)每路话音=8bit×8000=64kbit/s→C; (2)信令=复帧轮转每路4bit/2ms=2kbit/s→B;
(3)8000帧/s→C; (4)8000/16=500复帧/s→A。答案 CBCA。
总数430不变, round-trip 逐字节校验后才落盘。
"""
import json

P = 'data/questions.json'
raw = open(P, encoding='utf-8').read()
data = json.loads(raw)

rt = json.dumps(data, ensure_ascii=False, indent=1)
assert rt == raw.rstrip('\n'), 'round-trip mismatch — 格式漂移, 中止不写盘'
assert len(data) == 430

q = next(x for x in data if x['id'] == 'tk299-97-03')
assert q['answer_text'] == 'CBCA', '答案键与预期不符: %r' % q['answer_text']
assert '选 **A**' in q['solution'] and '答案 **A、C、C、A**' in q['solution'], '旧解析锚点缺失'

q['solution'] = (
    'PCM30/32 总速率 2048 kbit/s 是全系统 32 个时隙之和,别拿来当每路;每路话音独占 1 个时隙:'
    '$8\\ \\text{bit}\\times 8000$ 帧$/\\mathrm{s}=64\\ \\mathrm{kbit/s}$,(1) 选 **C**。'
    '信令走 TS16,按复帧轮转:16 帧为 1 个复帧($2\\ \\mathrm{ms}$),其中 F0 的 TS16 作复帧同步与告警,'
    'F1~F15 的 TS16 每帧放 2 路信令、每路 $4\\ \\text{bit}$——每路信令速率'
    '$=\\dfrac{4\\ \\text{bit}}{2\\ \\mathrm{ms}}=2\\ \\mathrm{kbit/s}$,(2) 选 **B**。'
    '抽样率 8 kHz 故每秒传 **8000** 帧,(3) 选 **C**;每秒复帧数 $=\\dfrac{8000}{16}=500$,(4) 选 **A**。'
    '答案 **C、B、C、A**（与书答案条 CBCA 一致）。'
)

assert 'C、B、C、A' in q['solution'] and 'A、C、C、A' not in q['solution']

out = json.dumps(data, ensure_ascii=False, indent=1) + ('\n' if raw.endswith('\n') else '')
open(P, 'w', encoding='utf-8', newline='\n').write(out)
json.load(open(P, encoding='utf-8'))
print('OK: answer_text 仍为', q['answer_text'], '| 解析尾:', q['solution'][-60:])
