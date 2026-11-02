# -*- coding: utf-8 -*-
"""2026-11-02: zhenti801.json 2016年选择填空缺空补录。

根因: 合订本精解里 2016 年有两个半角波浪分组标记 "**第16~18空**" / "**第21~22空**"，
当年 build 脚本只认全角 "～" 分组与单空 "第N空"，半角 "~" 组整组被跳过，且组内容
被顺序解析吞进了前一空(第15空/第20空)的 key 尾部。另精解源头本身缺第25/26空
(第11句纠错编码)，按备选项 g(低)/s(强) 与教材结论补录并标注。

补丁内容:
1. 第15空 key 剥离粘着的 "**第16~18空**" 段; 第20空 key 剥离 "**第21~22空**" 段。
2. 新增 7 个空块: 16(y余弦滚降)/17(f部分响应)/18(p理想低通)/21(n接收机模型)/
   22(w信号形式)/25(g低·补录)/26(s强·补录)。
3. subs 按 n 排序, 断言 ns==1..26 全覆盖。
"""
import json
import sys

PATH = r"D:\考研数学\组卷网站_static\data\zhenti801.json"

RAW = open(PATH, "r", encoding="utf-8", newline="").read()
CRLF = "\r\n" in RAW
data = json.loads(RAW)

y2016 = next(y for y in data["years"] if y["year"] == 2016)
q1 = next(q for q in y2016["qs"] if q["id"] == "y2016q1")
subs = q1["subs"]
assert len(subs) == 19, f"预期19个空块, 实际{len(subs)}"
ns0 = sorted(s["n"] for s in subs)
assert ns0 == [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,19,20,23,24], ns0

# ---- 1) 剥离第15空/第20空 key 里粘着的组内容 ----
s15 = next(s for s in subs if s["n"] == 15)
idx = s15["key"].find("\n\n**第16~18空**")
assert idx > 0, "第15空 key 未找到粘着的16~18组"
s15["key"] = s15["key"][:idx].rstrip()

s20 = next(s for s in subs if s["n"] == 20)
idx = s20["key"].find("\n\n**第21~22空**")
assert idx > 0, "第20空 key 未找到粘着的21~22组"
s20["key"] = s20["key"][:idx].rstrip()

assert "**第16~18空**" not in s15["key"]
assert "**第21~22空**" not in s20["key"]

# ---- 2) 新空块 ----
KP_TX = ("- 【知识点】三类常用无码间干扰传输特性对比\n"
         "- 【对应课件】第九讲、第十一讲《部分响应系统的分析》\n"
         "- 【要点】理想低通：频带利用率2 Baud/Hz最高，但物理不可实现、尾巴收敛慢；"
         "余弦滚降：物理可实现，带宽 $B=(1+\\alpha)R_B/2$，频带利用率 $2/(1+\\alpha)$ Baud/Hz；"
         "部分响应：有控制地引入码间干扰，实现2 Baud/Hz并使尾巴收敛，但相关电平数增多。")
KP_RX = ("- 【知识点】最佳接收理论的两条主线\n"
         "- 【对应课件】第二十讲《确知数字信号最佳接收相关分析与结论》、第二十一讲《匹配滤波接收相关分析与结论》\n"
         "- 【要点】一是给定信号形式下设计最佳接收机结构（相关接收机/匹配滤波器），使误码率最小；"
         "二是选择最佳信号形式（如 $\\rho=-1$ 的正反波形）进一步降低误码率。")
KP_BK = "- 【备注】合订本精解原缺本空，2026-11-02 按备选项与教材结论补录"

NEW = [
    dict(n=16, k="空", t="第16空", stem="",
         key="【答案】**y（余弦滚降）**\n" + KP_TX),
    dict(n=17, k="空", t="第17空", stem="",
         key="【答案】**f（部分响应）**\n" + KP_TX),
    dict(n=18, k="空", t="第18空", stem="",
         key="【答案】**p（理想低通）**\n" + KP_TX),
    dict(n=21, k="空", t="第21空", stem="",
         key="【答案】**n（接收机模型）**\n" + KP_RX),
    dict(n=22, k="空", t="第22空", stem="",
         key="【答案】**w（信号形式）**\n" + KP_RX),
    dict(n=25, k="空", t="第25空", stem="",
         key="【答案】**g（低）**\n- 【知识点】纠错编码：校验位越多，码率 $R=k/n$ 越低\n" + KP_BK),
    dict(n=26, k="空", t="第26空", stem="",
         key="【答案】**s（强）**\n- 【知识点】校验位/冗余越多，纠错能力越强\n" + KP_BK),
]

have = {s["n"] for s in subs}
for s in NEW:
    assert s["n"] not in have, f"空号 {s['n']} 已存在"
    subs.append(s)
subs.sort(key=lambda s: s["n"])

ns = [s["n"] for s in subs]
assert ns == list(range(1, 27)), f"补后空号应1..26全覆盖, 实际: {ns}"

# ---- 3) 写盘(CRLF 保持原格式) + round-trip 校验 ----
text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
if CRLF:
    text = text.replace("\n", "\r\n")
reloaded = json.loads(text)
q1v = next(q for q in next(y for y in reloaded["years"] if y["year"] == 2016)["qs"] if q["id"] == "y2016q1")
assert [s["n"] for s in q1v["subs"]] == list(range(1, 27))
assert q1v["subs"][15]["key"].startswith("【答案】**y（余弦滚降）**")

with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(text)

print("OK: 2016q1 subs 19→26 (补16/17/18/21/22/25/26), 第15/20空key已剥离粘组, CRLF保持")
