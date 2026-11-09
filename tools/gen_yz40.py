# -*- coding: utf-8 -*-
"""生成 data/yz40.json —— 《冲刺宝典》压轴40题入库。
源: 桌面\冲刺宝典\冲刺宝典题目收录.md（KaTeX+内联SVG 全量转录版）
  题目段: "冲刺压轴40题 · 题目（一）"(题1~17) + "分片E2"(题18~40, 题36-39 题干缺拍)
  解析段: "分片F1"(题1~20) + "分片F2"(题20续~40)
页码取自 <!-- p.N | 文件名 --> 标记。考点归类 YZ_MAP 手工核定（打印题干供过目）。"""
import json, re, io, sys, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
MD = r"C:\Users\19273\Desktop\冲刺宝典\冲刺宝典题目收录.md"
REPO = r"D:\考研数学\组卷网站_static"
TREE = json.load(open(REPO + r"\data\kp_tree.json", encoding="utf-8"))
KS = {c["n"]: c["ks"] for c in TREE["chapters"]}

# 考点归类：题号 → [章名, 考点名]（依题干逐题核定）
YZ_MAP = {
    1:  ["第3章 随机过程", "白噪声、低通白噪声、带通白噪声"],
    2:  ["第3章 随机过程", "平稳随机过程通过线性系统"],
    3:  ["第3章 随机过程", "平稳随机过程通过线性系统"],
    4:  ["第4章 信道", "条件熵、联合熵、互信息和离散信道容量求解"],
    5:  ["第4章 信道", "香农公式和连续信道容量求解"],
    6:  ["第5章 模拟调制系统", "频分复用和复合调制"],
    7:  ["第5章 模拟调制系统", "AM、SSB、DSB、FM抗噪声性能分析"],
    8:  ["第5章 模拟调制系统", "频分复用和复合调制"],
    9:  ["第5章 模拟调制系统", "求FM、PM信号的调制指数、带宽、最大频偏等"],
    10: ["第5章 模拟调制系统", "求FM、PM信号的调制指数、带宽、最大频偏等"],
    11: ["第5章 模拟调制系统", "求FM、PM信号的调制指数、带宽、最大频偏等"],
    12: ["第5章 模拟调制系统", "求FM、PM信号的调制指数、带宽、最大频偏等"],
    13: ["第6章 数字基带传输系统", "无码间干扰判断及相关问题"],
    14: ["第7章 数字频带传输系统", "二进制频带信号的可靠性和有效性比较"],
    15: ["第7章 数字频带传输系统", "多进制误码率与判决"],
    16: ["第7章 数字频带传输系统", "星座图"],
    17: ["第7章 数字频带传输系统", "星座图"],
    18: ["第7章 数字频带传输系统", "星座图"],
    19: ["第8章 数字信号最佳接收", "匹配滤波器的设计及误码率求解"],
    20: ["第8章 数字信号最佳接收", "匹配滤波器的设计及误码率求解"],
    21: ["第8章 数字信号最佳接收", "匹配滤波器的设计及误码率求解"],
    22: ["第6章 数字基带传输系统", "无码间干扰判断及相关问题"],
    23: ["第7章 数字频带传输系统", "多进制误码率与判决"],
    24: ["第7章 数字频带传输系统", "二进制频带信号的可靠性和有效性比较"],
    25: ["第9章 信源编码", "量化编码+时分复用+无码间传输综合题"],
    26: ["第7章 数字频带传输系统", "二进制频带调制解调及误码率求解"],
    27: ["第9章 信源编码", "时分复用"],
    28: ["第9章 信源编码", "抽样定理"],
    29: ["第9章 信源编码", "时分复用"],
    30: ["第9章 信源编码", "抽样定理"],
    31: ["第9章 信源编码", "均匀量化"],
    32: ["第9章 信源编码", "均匀量化"],
    33: ["第9章 信源编码", "均匀量化"],
    34: ["第9章 信源编码", "十三折线编码"],
    35: ["第9章 信源编码", "均匀量化"],
    36: ["第10章 信道编码", "线性分组码、循环码"],
    37: ["第10章 信道编码", "线性分组码、循环码"],
    38: ["第10章 信道编码", "卷积码"],
    39: ["第10章 信道编码", "卷积码"],
    40: ["第10章 信道编码", "卷积码"],
}

P_RE = re.compile(r"^<!--\s*p\.(\d+)\s*\|")
Q_ANCHOR = re.compile(r"^\*\*(\d+)\.\*\*")
BOLD_NUM = re.compile(r"\*\*(\d+)[.、]")

def locate(lines, keys):
    """返回各分片 (起,止) 行下标：起=锚点行，止=下一个 # 级标题或 ## 小结 前。"""
    pos = {}
    for i, ln in enumerate(lines):
        if ln.startswith("# ") :
            for k in keys:
                if k in ln and k not in pos:
                    pos[k] = i
    # 终点：锚点之后的下一个 "# " 标题
    order = sorted(pos.items(), key=lambda kv: kv[1])
    spans = {}
    for idx, (k, s) in enumerate(order):
        e = len(lines)
        for j in range(s + 1, len(lines)):
            if lines[j].startswith("# ") or lines[j].startswith("## 小结"):
                e = j
                break
        spans[k] = (s, e)
    return spans

def parse_questions(lines, lo, hi):
    blocks, cur, page = {}, None, None
    for i in range(lo, hi):
        ln = lines[i]
        mp = P_RE.match(ln)
        if mp:
            page = int(mp.group(1))
            continue
        mq = Q_ANCHOR.match(ln)
        if mq:
            n = int(mq.group(1))
            rest = ln[mq.end():].strip()
            cur = {"no": n, "page": page, "lines": [rest] if rest else []}
            blocks[n] = cur
        elif cur is not None:
            cur["lines"].append(ln)
    return blocks

def parse_solutions(lines, lo, hi):
    blocks, cur, page = {}, None, None
    for i in range(lo, hi):
        ln = lines[i]
        mp = P_RE.match(ln)
        if mp:
            page = int(mp.group(1))
            continue
        mb = BOLD_NUM.search(ln)
        if mb and mb.start() <= 12:
            n = int(mb.group(1))
            is_cont = ("续" in ln) or ("接p" in ln)
            if is_cont:
                cur = blocks.get(n)
                if cur is None:
                    cur = blocks[n] = {"no": n, "page": page, "lines": []}
                rest = BOLD_NUM.sub("", ln, count=1).strip()
                cur["lines"].append(rest if rest else "")
            else:
                rest = ln[mb.end():].strip()
                rest = re.sub(r"^解[:：]?\s*", "", rest)
                cur = blocks.get(n)
                if cur is None:
                    cur = blocks[n] = {"no": n, "page": page, "lines": []}
                    cur["lines"].append(rest) if rest else None
                else:
                    # 主块重复出现（跨分片重排）→ 追加
                    cur["lines"].append(ln)
            continue
        if cur is not None:
            cur["lines"].append(ln)
    return blocks

def tidy(lines):
    out, blank = [], 0
    for t in lines:
        s = t.rstrip()
        if s.lstrip().startswith(">"):
            continue  # 转录注记 blockquote（如题35尾部"衔接缺口"说明）不入题面
        if not s.strip():
            blank += 1
            if blank > 2:
                continue
        else:
            blank = 0
        out.append(s)
    return "\n".join(out).strip()

def main():
    raw = open(MD, encoding="utf-8").read()
    lines = raw.split("\n")
    spans = locate(lines, ["冲刺压轴40题 · 题目（一）", "冲刺压轴40题（分片E2", "冲刺宝典 分片F1", "冲刺压轴40题 · 习题解析（分片F2"])
    print("分片定位:", {k[:14]: v for k, v in spans.items()})
    qb = {}
    for k in ["冲刺压轴40题 · 题目（一）", "冲刺压轴40题（分片E2"]:
        lo, hi = spans[k]
        qb.update(parse_questions(lines, lo, hi))
    sb = {}
    for k in ["冲刺宝典 分片F1", "冲刺压轴40题 · 习题解析（分片F2"]:
        lo, hi = spans[k]
        for n, b in parse_solutions(lines, lo, hi).items():
            if n in sb:
                sb[n]["lines"] += b["lines"]
            else:
                sb[n] = b

    print(f"题干块 {len(qb)} 个: {sorted(qb)}")
    print(f"解析块 {len(sb)} 个: {sorted(sb)}")
    miss_stem = [n for n in range(1, 41) if n not in qb]
    miss_sol = [n for n in range(1, 41) if n not in sb]
    print("缺题干:", miss_stem, " 缺解析:", miss_sol)

    items = []
    for n in range(1, 41):
        ch, kp = YZ_MAP[n]
        assert ch in KS and kp in KS[ch], f"考点不存在: {n} → {ch}·{kp}"
        q = qb.get(n)
        if q:
            stem = tidy(q["lines"])
            page = q["page"]
        else:
            stem = ""
            page = None
        s = sb.get(n)
        sol = tidy(s["lines"]) if s else ""
        items.append({
            "id": f"yz40-{n}", "no": n,
            "ch": ch, "kp": kp,
            "page": page, "spage": s["page"] if s else None,
            "stem": stem, "sol": sol,
            "nsub": len(re.findall(r"（\d+）", stem)) if stem else 0,
        })
    # 树校验 + 题干过目输出
    for it in items:
        head = it["stem"].replace("\n", " ")[:52] if it["stem"] else "❗题干缺失(书p76-77缺拍)"
        print(f"[{it['no']}] {it['ch'][:3]}·{it['kp'][:12]} | p{it['page']}/解p{it['spage']} | {head}")
    empty_sol = [it["no"] for it in items if not it["sol"]]
    print("解析为空:", empty_sol)
    with open(REPO + r"\data\yz40.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump({"note": "冲刺宝典压轴40题; 题36-39题干书p76-77缺拍未录入,解析齐全", "items": items}, f, ensure_ascii=False, indent=1)
    print(f"yz40.json 写入 {len(items)} 题")

if __name__ == "__main__":
    main()
