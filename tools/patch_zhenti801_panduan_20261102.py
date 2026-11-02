# -*- coding: utf-8 -*-
"""2026-11-02 二次补丁: zhenti801.json 判断题修复。

三件事:
1. y2022q3 / y2023q2 判断题当年整段精解误入 stem(答案裸奔、无子项、key为空)——
   题面从原卷PDF(Downloads\\1998-2025年南邮通信原理真题及解析\\)逐句转录补入,
   精解按 **第N题** 标记拆成 5 个子项(k='题'), 每题独立标记追踪。
2. 2016/2017/2018/2019 年判断题 stem 里的"逐条精解"分隔残留截除。
3. 断言: 拆分后 subs 全覆盖、精解条目数=5、原 stem 不再含【答案】。
"""
import json
import re

PATH = r"D:\考研数学\组卷网站_static\data\zhenti801.json"

RAW = open(PATH, "r", encoding="utf-8", newline="").read()
CRLF = "\r\n" in RAW
data = json.loads(RAW)

def get_q(yid):
    for y in data["years"]:
        for q in y["qs"]:
            if q["id"] == yid:
                return q
    raise SystemExit(f"未找到 {yid}")

# ---- 1) 2022/2023 判断题: 题面转录(源:原卷PDF第1/2页) + 精解拆子项 ----
STEMS = {
    "y2022q3": (
        "1、消息所含信息量与消息的重要性成反比。\n\n"
        "2、信源编码提高通信的可靠性，信道编码提高传输的有效性。\n\n"
        "3、一般认为移动通信信道属于恒参信道。\n\n"
        "4、OFDM 系统一般采用循环前缀(CP)提高频谱效率。\n\n"
        "5、数字通信系统中接收机通常不需要载波同步。"),
    "y2023q2": (
        "1、长距离无线传输采用频带传输的原因是频率越高信号衰减越慢。\n\n"
        "2、PCM30/32 系统中，帧同步码为巴克码。\n\n"
        "3、m 序列与其移位之后的序列近似正交。\n\n"
        "4、若信源信道速率大于信道容量，则不可能实现无差错传输。\n\n"
        "5、多进制频带传输，信道条件越好，越要选择低阶的调制方法。"),
}

for yid, new_stem in STEMS.items():
    q = get_q(yid)
    assert not q.get("subs") and q.get("key", "") == "" and "【答案】" in q["stem"], f"{yid} 形态与预期不符"
    parts = re.split(r"\*\*第(\d)题\*\*", q["stem"])
    # parts = [前导, '1', 内容1, '2', 内容2, ...]
    entries = {}
    for i in range(1, len(parts) - 1, 2):
        entries[int(parts[i])] = parts[i + 1].strip()
    assert sorted(entries) == [1, 2, 3, 4, 5], f"{yid} 精解条目数异常: {sorted(entries)}"
    for n in range(1, 6):
        assert "【答案】" in entries[n], f"{yid} 第{n}题精解无答案"
    q["subs"] = [dict(n=n, k="题", t=f"第{n}题", stem="",
                      key=entries[n]) for n in range(1, 6)]
    q["key"] = ""
    q["stem"] = new_stem

# ---- 2) 2016~2019 判断题 stem 截除"逐条精解"残留 ----
for yid in ["y2016q3", "y2017q3", "y2018q3", "y2019q3"]:
    q = get_q(yid)
    i = q["stem"].find("逐条精解")
    assert i > 0, f"{yid} 未找到逐条精解标记"
    q["stem"] = q["stem"][:i].rstrip()

# ---- 3) 终验 ----
for yid in ["y2022q3", "y2023q2"]:
    q = get_q(yid)
    assert len(q["subs"]) == 5 and "【答案】" not in q["stem"]
for yid in ["y2016q3", "y2017q3", "y2018q3", "y2019q3"]:
    q = get_q(yid)
    assert "逐条精解" not in q["stem"]

text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
if CRLF:
    text = text.replace("\n", "\r\n")
reloaded = json.loads(text)
for yid in STEMS:
    qq = next(q for y in reloaded["years"] for q in y["qs"] if q["id"] == yid)
    assert len(qq["subs"]) == 5

with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(text)

print("OK: 2022q3/2023q2 判断题已拆 5 子项(题面转录自原卷PDF), 2016~2019判断题stem残留已截除")
