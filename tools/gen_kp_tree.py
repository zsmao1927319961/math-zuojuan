# -*- coding: utf-8 -*-
"""生成 data/kp_tree.json —— 统一考点树（12章，照《299题》章节）+ qhzt专题→考点映射。
章/考点名以 tk299 chapter_name 解析为权威（第N章 章名 · 考点M 考点名）；extras 手工补充；
qhzt 26 专题映射手工核定（kp_sub 佐证）。所有 gen/前端共用这一份树。"""
import json, re, io, sys, collections

REPO = r"D:\考研数学\组卷网站_static"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

Q = json.load(open(REPO + r"\data\questions.json", encoding="utf-8"))
CH_RE = re.compile(r"^第(\d+)章 (.+?) · 考点(\d+) (.+)$")

# extras：tk299 没有但题库里确实存在的考点（挂在章尾）
EXTRA_KPS = {
    7: ["多进制误码率与判决"],
}

# qhzt 26 专题（chapter_name 原文为键）→ [章号, 考点名]
QHZT_MAP = {
    "专题一 带宽求解":            [2, "功率、能量和带宽求解"],
    "专题二 功率求解":            [2, "功率、能量和带宽求解"],
    "专题三 平稳随机过程通过线性系统": [3, "平稳随机过程通过线性系统"],
    "专题四 随机过程的性质":        [3, "平稳随机过程、各态历经性的判断"],
    "专题五 信道容量求解":          [4, "香农公式和连续信道容量求解"],
    "专题六 模拟通信抗噪声性能":    [5, "AM、SSB、DSB、FM抗噪声性能分析"],
    "专题七 调频调相波参数":        [5, "求FM、PM信号的调制指数、带宽、最大频偏等"],
    "专题八 频分复用与复合调制":    [5, "频分复用和复合调制"],
    "专题九 无码间干扰":            [6, "无码间干扰判断及相关问题"],
    "专题十 时域均衡":              [6, "时域均衡"],
    "专题十一 二进制频带接收方式":  [7, "二进制频带调制解调及误码率求解"],
    "专题十二 二进制频带误码率":    [7, "二进制频带调制解调及误码率求解"],
    "专题十四 多进制误码率与判决":  [7, "多进制误码率与判决"],
    "专题十五 信号矢量空间与星座图": [7, "星座图"],
    "专题十六 匹配滤波器设计与简化": [8, "匹配滤波器的设计及误码率求解"],
    "专题十七 基带/频带系统设计":   [6, "无码间干扰判断及相关问题"],
    "专题十八 最佳基带传输系统":    [8, "最佳基带传输系统"],
    "专题十九 时分复用":            [9, "时分复用"],
    "专题二十 PCM/TDM/无ISI综合":   [9, "量化编码+时分复用+无码间传输综合题"],
    "专题二十一 MSK 信号相位":      [7, "MSK信号"],
    "专题二十二 抽样信号的量化":    [9, "均匀量化"],
    "专题二十三 循环码":            [10, "线性分组码、循环码"],
    "专题二十四 卷积码":            [10, "卷积码"],
    "专题二十五 维特比译码":        [10, "卷积码"],
    "专题二十六 m 序列":            [11, "m序列"],
    "专题二十七 载波同步及位同步":  [12, "同步原理"],
}

# kp_sub 级覆盖（跨章题归位）：键 = "专题名|kp_sub"，优先于专题级映射
QHZT_SUB_MAP = {
    "专题一 带宽求解|模拟调制带宽（AM/DSB/SSB/FM）":      [5, "求FM、PM信号的调制指数、带宽、最大频偏等"],
    "专题一 带宽求解|带通信号与希尔伯特变换（DSB/SSB 判别）": [2, "功率、能量和带宽求解"],
    "专题一 带宽求解|传码率与主瓣带宽频带利用率":          [1, "传信率、传码率及之间的关系"],
    "专题一 带宽求解|最小带宽与滚降带宽":                  [6, "无码间干扰判断及相关问题"],
    "专题一 带宽求解|PCM-TDM 传码率与带宽（同步时隙）":    [9, "时分复用"],
    "专题一 带宽求解|无码间干扰最高传输速率":              [6, "无码间干扰判断及相关问题"],
    "专题一 带宽求解|第一零点带宽（占空比）":              [6, "数字基带信号功率谱以及带宽"],
    "专题一 带宽求解|PCM-TDM 带宽（Sa 脉冲）":             [9, "时分复用"],
    "专题一 带宽求解|PCM-TDM 带宽（三种成形脉冲）":        [9, "时分复用"],
    "专题二 功率求解|窄带噪声正交分解功率":                [3, "白噪声、低通白噪声、带通白噪声"],
    "专题二 功率求解|白噪声过滤波器（Parseval）":          [3, "平稳随机过程通过线性系统"],
    "专题二 功率求解|采样信号分量与噪声分量统计":          [9, "抽样定理"],
    "专题二 功率求解|均匀量化功率":                        [9, "均匀量化"],
    "专题二 功率求解|数字调制信号功率与峰均比":            [7, "二进制频带调制解调及误码率求解"],
    "专题三 平稳随机过程通过线性系统|匹配滤波器结构与冲激响应": [8, "匹配滤波器的设计及误码率求解"],
    "专题四 随机过程的性质|R(τ) 三件套（均值方差功率）":   [3, "期望、方差、自相关函数求解"],
    "专题四 随机过程的性质|随机幅度乘载波的自相关":        [3, "期望、方差、自相关函数求解"],
    "专题五 信道容量求解|BSC 容量（源分布无关）":          [4, "条件熵、联合熵、互信息和离散信道容量求解"],
    "专题五 信道容量求解|M 进制对称信道容量":              [4, "条件熵、联合熵、互信息和离散信道容量求解"],
    "专题五 信道容量求解|BEC 容量":                        [4, "条件熵、联合熵、互信息和离散信道容量求解"],
    "专题五 信道容量求解|非对称信道互信息":                [4, "条件熵、联合熵、互信息和离散信道容量求解"],
    "专题十一 二进制频带接收方式|OOK 最佳接收：门限与错误概率": [8, "匹配滤波器的设计及误码率求解"],
    "专题十一 二进制频带接收方式|2PSK 最佳接收：判决量分布与误码率": [8, "匹配滤波器的设计及误码率求解"],
    "专题十七 基带/频带系统设计|卷积码+16QAM 系统设计":    [7, "多进制误码率与判决"],
    "专题十七 基带/频带系统设计|带通信道传 32Mbps 系统设计": [7, "数字频带信号无码间干扰"],
    "专题十七 基带/频带系统设计|4 路 TDM+MPAM 基带设计":   [9, "时分复用"],
}

def main():
    chs = collections.OrderedDict()
    for q in Q:
        if q["source"] != "tk299":
            continue
        m = CH_RE.match(q["chapter_name"])
        if not m:
            raise SystemExit("chapter_name 解析失败: " + q["chapter_name"])
        cn, kn = int(m.group(1)), int(m.group(3))
        chs.setdefault(cn, {"name": m.group(2), "kps": {}})
        chs[cn]["kps"][m.group(4)] = kn

    # qhzt probe + 校验
    qhz = collections.OrderedDict()
    for q in Q:
        if q["source"] != "qhzt":
            continue
        qhz.setdefault(q["chapter_name"], collections.Counter())[q.get("kp_sub") or "?"] += 1

    print("=== qhzt 专题 → kp_sub（供映射核定） ===")
    for cn, subs in qhz.items():
        if cn in QHZT_MAP:
            tgt = "→ %d·%s" % tuple(QHZT_MAP[cn])
        else:
            tgt = "→ !! 无映射"
        print(f"[{cn}] {tgt}  ({sum(subs.values())}题)")
        for s, c in subs.most_common():
            print(f"    {c}x {s}")

    missing = [k for k in qhz if k not in QHZT_MAP]
    if missing:
        raise SystemExit("缺映射: " + " | ".join(missing))

    # kp_sub 级覆盖键核对（防手打错字）
    real_keys = set()
    for q in Q:
        if q["source"] == "qhzt" and q.get("kp_sub"):
            real_keys.add(q["chapter_name"] + "|" + q["kp_sub"])
    bad = [k for k in QHZT_SUB_MAP if k not in real_keys]
    if bad:
        raise SystemExit("覆盖键没命中任何题: " + " | ".join(bad))

    chapters = []
    for cn in sorted(chs):
        ks = [k for k, _ in sorted(chs[cn]["kps"].items(), key=lambda kv: kv[1])]
        ks += [k for k in EXTRA_KPS.get(cn, []) if k not in ks]
        chapters.append({"n": f"第{cn}章 {chs[cn]['name']}", "ks": ks})

    out = {"chapters": chapters, "qhzt": QHZT_MAP, "qhzt_sub": QHZT_SUB_MAP}
    with open(REPO + r"\data\kp_tree.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"\nkp_tree.json 写入: {len(chapters)} 章, 考点总数 {sum(len(c['ks']) for c in chapters)}")

if __name__ == "__main__":
    main()
