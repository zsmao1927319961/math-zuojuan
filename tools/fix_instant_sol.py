# -*- coding: utf-8 -*-
"""修复7道instant选择题速答残渣解析 + 3处题面碎片/叠字
(用户报"没有答案": 点字母后答案区只有字母+残渣)"""
import json, sys

path = r"D:/考研数学/组卷网站_static/data/questions.json"
qs = json.load(open(path, encoding="utf-8"))
Q = {q["id"]: q for q in qs}

def set_sol(qid, sol):
    Q[qid]["solution"] = sol

def edit_q(qid, old, new):
    cur = Q[qid].get("question_text") or ""
    if old not in cur:
        print(f"[MISS] {qid}: {old[:40]!r}"); sys.exit(1)
    Q[qid]["question_text"] = cur.replace(old, new, 1)

# ---- 题面碎片/叠字 ----
edit_q("tk299-52-01", "调频（上一行残缺文字）\n1、", "1、")
edit_q("tk299-113-02", "信息信息信号", "信息信号")
edit_q("tk299-63-05", "通信原理（页眉，部分被裁切）\n5、", "5、")

# ---- 7题解析重写 ----
set_sol("tk299-113-02",
    r"扩频码速率 $R_c=16R_b$：$s(t)=d(t)\,c(t)$ 的主瓣带宽由 chip 速率决定，$B_s\approx 2R_c=2\times16R_b=32R_b$；而 $d(t)$ 的主瓣带宽为 $R_b$ 量级，故 $s(t)$ 主瓣带宽是 $d(t)$ 的 32 倍，选 D。本质：扩频用 16 倍带宽换取处理增益。")
set_sol("tk299-52-01",
    r"先微分再调频：FM 的瞬时频偏 $\propto$ 输入，即 $\Delta f \propto \frac{dm(t)}{dt}$，积分回瞬时相位偏移 $\Delta\varphi \propto \int\frac{dm(t)}{dt}\,dt = m(t)$——相位偏移直接正比于 $m(t)$，这正是调相 PM 的定义，选 D。")
set_sol("tk299-41-03",
    r"卫星中继信道：视距传播、信道参数基本不随时间变化，属恒参信道；短波电离层反射信道：多径传播、衰减和时延随时间随机变化，是典型随参信道。选 A。")
set_sol("tk299-43-01",
    r"频带利用率 $=$ 信息速率 $/$ 带宽 $= C/B$。香农容量 $C=B\log_2\left(1+\frac{S}{N_0 B}\right)$（噪声功率 $N=N_0B$），两边除以 $B$ 得 $\eta=\log_2\left(1+\frac{S}{N_0B}\right)$ bit/(s·Hz)，选 B。注意 A 是容量不是利用率，多除了一个 $B$。")
set_sol("tk299-63-05",
    r"码元速率 $f_b$ 的无 ISI 传输，奈奎斯特最小带宽是 $\frac{f_b}{2}$（对应角频率 $\frac{\omega_b}{2}$）。选项 A 的理想矩形低通恰好截止在 $\frac{\omega_b}{2}$：既能实现无码间干扰，又达到频带利用率上限 $2$ Baud/Hz，是可实现的传输特性中最节省带宽的，选 A。")
set_sol("tk299-101-06",
    r"汉明码的最小码距 $d_{\min}=3$，纠错能力 $t=\left\lfloor\frac{d_{\min}-1}{2}\right\rfloor=1$，即只能纠 1 位错，选 D。(15,11) 满足 $n=2^m-1=15$、$k=n-m=11$，是标准汉明码。")
set_sol("tk299-102-01",
    r"全 1 码字合法意味着 $H\cdot\mathbf{1}^T=\mathbf{0}$，即校验矩阵每一行与全 1 向量的内积为 0——每行中 1 的个数（行重量）必须是偶数，选 D。")

json.dump(qs, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done: 3 题面修复 + 7 解析重写")
