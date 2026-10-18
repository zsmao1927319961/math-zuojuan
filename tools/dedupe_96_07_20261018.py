# -*- coding: utf-8 -*-
"""2026-10-18 考点6·7 去重(用户报"题干重复,删上面三个"):
tk299-96-07(北邮2024第三题, 书p82)题干把同一题录了两遍。书页取证:
- 印刷页82(照片p264)只印下面一版: 比特流/各路的数据速率/调制阶数尽量低/发端到收端;
- 上面一版(数码率/调制阶数及滚降系数α/发射到接收)是录题混入的真题原文 → 按用户指示删除;
- 删除后残留的重复句"然后将4路比特流时分复用为一路…试:"一并去掉, 题干"比特"→"比特流"对齐书页;
- 答案截断尾补全: 书答案页175-176(照片p355/p356)"可设计成滚降系数a=1/7的16QAM调制。";
- (3)书答案页为框图, 按卡内既有惯例(75-08"此为补充")以文字补充并显式标注。
总数430不变。json round-trip 逐字节校验后才落盘。
"""
import json

P = 'data/questions.json'
raw = open(P, encoding='utf-8').read()
data = json.loads(raw)

rt = json.dumps(data, ensure_ascii=False, indent=1)
assert rt == raw.rstrip('\n'), 'round-trip mismatch — 格式漂移, 中止不写盘'
assert len(data) == 430

q = next(x for x in data if x['id'] == 'tk299-96-07')
qt = q['question_text']

# 锚点自检: 两版俱在
assert '求出此系统的数码率' in qt and '求出各路的数据速率' in qt

# 1) 删上面一版的三问(含行尾粘连的书源句头"（北京邮电大学 2024 年第三题）"保留给下版结尾)
lines = qt.split('\n')
i1 = next(i for i, l in enumerate(lines) if '求出此系统的数码率' in l)
i3 = next(i for i, l in enumerate(lines) if '画出从发射到接收的完整系统框图' in l)
assert i3 == i1 + 2, '上版三问行序异常: %d..%d' % (i1, i3)
# (3)行末粘着下一版的重复句, 先拆开
glue = '（北京邮电大学 2024 年第三题）然后将 4 路比特流时分复用为一路，再通过一个带宽为 $24\\,\\mathrm{kHz}$ 的带通信道传输。试：'
assert lines[i3].endswith(glue), '粘连句锚点不匹配: %r' % lines[i3][-80:]
lines[i3] = '（北京邮电大学 2024 年第三题）'
del lines[i1:i3 + 1]

# 2) 剩余 = 题干 + 下版三问(下版首行以"(1)求出各路的数据速率"开头)
assert lines[i1].startswith('(1)求出各路的数据速率'), '下版(1)锚点异常: %r' % lines[i1][:40]
qt2 = '\n'.join(lines)

# 3) 题干"比特时分复用"→"比特流时分复用"(书页p264: "4路比特流时分复用为一路")
assert '然后将 4 路比特时分复用为一路' in qt2
qt2 = qt2.replace('然后将 4 路比特时分复用为一路', '然后将 4 路比特流时分复用为一路')
q['question_text'] = qt2

# 4) 答案截断尾补全(书答案页176/照片p356)
at = q['answer_text']
assert at.endswith('可设计成滚降系数 $a=\\dfrac{1}{7}$ 的'), '答案尾锚点不匹配: %r' % at[-40:]
assert '16QAM调制' not in at
q['answer_text'] = (at + '16QAM 调制。\n'
                    '(3) 调制/解调框图（书答案页为框图；文字补充：发送端=抽样→$k=7$bit 均匀量化编码'
                    '→TDM 复用→串并变换→根号升余弦频谱成形→16QAM 调制→带通信道，接收端相逆）。')

# 5) 兜底断言
assert '数码率' not in json.dumps(q, ensure_ascii=False)
assert q['question_text'].count('时分复用为一路') == 1
assert q['question_text'].endswith('（北京邮电大学 2024 年第三题）')
assert q['answer_text'].count('(3)') == 1

out = json.dumps(data, ensure_ascii=False, indent=1) + ('\n' if raw.endswith('\n') else '')
open(P, 'w', encoding='utf-8', newline='\n').write(out)
json.load(open(P, encoding='utf-8'))

print('=== 去重后 question_text ===')
print(q['question_text'])
print('=== answer_text 尾部 ===')
print(q['answer_text'][-150:])
