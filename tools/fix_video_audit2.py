# -*- coding: utf-8 -*-
"""视频验证轮二批修复: 96-04出处尾、96-07题面补全、102-11题面补全(书p269)、93-05本地译码器"""
import json, sys

path = r"D:/考研数学/组卷网站_static/data/questions.json"
qs = json.load(open(path, encoding="utf-8"))
Q = {q["id"]: q for q in qs}

def edit(qid, field, old, new):
    cur = Q[qid].get(field) or ""
    if old not in cur:
        print(f"[MISS] {qid} {field}"); sys.exit(1)
    Q[qid][field] = cur.replace(old, new, 1)
    print(f"[OK] {qid} {field}")

# 96-04 出处尾部截断(视频P098: 十、= 第十题)
edit("tk299-96-04", "question_text", "（南京邮电大学 2020 年", "（南京邮电大学 2020 年第十题）")

# 96-07 题面截断补全(视频P100: 三问; 单位保留题库自洽的kHz)
edit("tk299-96-07", "question_text",
     "对每路信号分别按不发生频谱混叠的最低速率采样，对每个采样值按 $k$ 比特均匀量化（要求 $k$ 尽量小且量化信噪比不低于 $40\\,\\mathrm{dB}$），",
     "对每路信号分别按不发生频谱混叠的最低速率采样，对每个采样值按 $k$ 比特均匀量化（要求 $k$ 尽量小且量化信噪比不低于 $40\\,\\mathrm{dB}$），然后将 4 路比特时分复用为一路，再通过一个带宽为 $24\\,\\mathrm{kHz}$ 的带通信道传输。试：\n(1) 求出此系统的数码率；\n(2) 设计调制方式（调制阶数及滚降系数 $\\alpha$），给出码元速率，说明理由；\n(3) 画出从发射到接收的完整系统框图。（北京邮电大学 2024 年第三题）")

# 102-11 题面截断补全(书p269 原文)
edit("tk299-102-11", "question_text",
     "(1) 通过初等行变换将 $G_0$ 化为系统",
     "(1) 通过初等行变换将 $G_0$ 化为系统码形式的生成矩阵 $G$（约定系统位在左），并写出对应的校验矩阵 $H$；\n(2) 设 $c=(c_9c_8c_7c_6c_5c_4c_3c_2c_1c_0)$ 是该码的系统码码字，证明 $c_4c_3c_2c_1c_0 = c_9c_8c_7c_6c_5$；\n(3) 若接收端收到 $y=1100011001$，写出对应的伴随式 $s=Hy^T$、最可能的错误图样以及对应的译码结果。（北京邮电大学 2022 年第八题）")

# 93-05 本地编码器 -> 本地译码器(视频P092原文)
edit("tk299-93-05", "question_text", "求编码器本地编码器 $\\frac{7}{11}$ 变换输出码组；", "求编码器本地译码器 $\\frac{7}{11}$ 变换输出码组；")

json.dump(qs, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved")
