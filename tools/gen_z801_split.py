# -*- coding: utf-8 -*-
"""把 zhenti801.json 里 5 个无 subs 的小题块逐题/逐行拆分：
  data/z801_split.json = {qid: {parts:[{n, stem, key}], opts}}
考点落位并入 data/z801_kp.json（删除整块条目、加入分题条目）。
拆分块: y2014q2 / y2015q2（填空, **第N题**型） + y2017q1 / y2018q1 / y2019q1（选词填空, 逐行+第N~M空组）。"""
import json, re, io, sys, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = r"D:\考研数学\组卷网站_static"
TREE = json.load(open(REPO + r"\data\kp_tree.json", encoding="utf-8"))
CHN = {c["n"]: c["ks"] for c in TREE["chapters"]}
CHNAMES = list(CHN.keys())

def kp(chi, ki):
    return [CHNAMES[chi - 1], CHN[CHNAMES[chi - 1]][ki - 1]]

# 分题考点（按题干/精解逐条核定）
PART_KP = {
    "y2014q2#1": kp(6, 2),   # HDB3+CMI 编码译码
    "y2014q2#2": kp(9, 3),   # A律13折线编码
    "y2015q2#1": kp(1, 3),   # 信源熵/信息速率/最大熵
    "y2015q2#2": kp(9, 1),   # 低通/带通抽样定理
    "y2017q1#1": kp(4, 3),   # 信道容量定义
    "y2017q1#2": kp(5, 1),   # 调制的作用
    "y2017q1#3": kp(5, 3),   # 抗噪声性能观察指标
    "y2017q1#4": kp(6, 6),   # 频域/时域均衡
    "y2017q1#5": kp(7, 6),   # MSK特点
    "y2017q1#6": kp(8, 1),   # 匹配滤波器设计目标
    "y2017q1#7": kp(9, 2),   # 均匀/非均匀量化
    "y2017q1#8": kp(10, 2),  # 循环码循环性/生成多项式
    "y2018q1#1": kp(1, 1),   # 传输对象/信宿/信号载体
    "y2018q1#2": kp(3, 2),   # 随机过程平稳性/各态历经
    "y2018q1#3": kp(3, 1),   # 高斯噪声方差
    "y2018q1#4": kp(4, 3),   # 连续信道容量三要素
    "y2018q1#5": kp(5, 3),   # VSB与SSB抗噪声性能
    "y2018q1#6": kp(6, 7),   # 眼图
    "y2018q1#7": kp(9, 4),   # 信源编码/ADPCM
    "y2018q1#8": kp(7, 7),   # OFDM/多进制/多路复用
    "y2019q1#1": kp(1, 1),   # 信源编码/信道编码组成
    "y2019q1#2": kp(4, 1),   # 恒参/随参信道与失真
    "y2019q1#3": kp(5, 2),   # 线性调制/角度调制分类
    "y2019q1#4": kp(7, 8),   # 多进制目的与代价
    "y2019q1#5": kp(8, 1),   # 最佳接收准则
    "y2019q1#6": kp(9, 1),   # 模拟信号数字化
}
WHOLE_REMOVE = ["y2014q2", "y2015q2", "y2017q1", "y2018q1", "y2019q1"]

TOPIC_RE = re.compile(r"【知识点】([^】]+)")
def topic(t):
    m = TOPIC_RE.search(t or "")
    return m.group(1).strip()[:36] if m else ""

def split_dati(stem, key):
    """**第N题** 型：题干/精解都按第N题标记切；精解首段（无标记）属第1题。"""
    def parts(text):
        ms = list(re.finditer(r"\*\*第(\d+)题\*\*", text))
        if not ms:
            return {"1": text.strip()}
        out = {}
        head = text[:ms[0].start()].strip()
        if head:
            out["1"] = head
        for i, m in enumerate(ms):
            end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
            out[m.group(1)] = text[m.end():end].strip()
        return out
    sp, kp_ = parts(stem), parts(key)
    ns = sorted(set(sp) | set(kp_), key=int)
    return [{"n": n, "stem": sp.get(n, ""), "key": kp_.get(n, "")} for n in ns]

def split_xuan(stem, key):
    """选词填空型：题干按 1. 2. 3. 行切（备选项段落共享），精解按 **第N~M空** 组切并按空号对齐。"""
    lines = stem.split("\n")
    opts_i = next((i for i, ln in enumerate(lines) if ln.strip().startswith("备选项")), None)
    body = lines[:opts_i] if opts_i is not None else lines
    opts = "\n".join(lines[opts_i:]).strip() if opts_i is not None else ""
    rows = []
    for ln in body:
        m = re.match(r"^\s*(\d{1,2})[.、．]\s*(.*)$", ln)
        if m:
            rows.append({"n": m.group(1), "stem": m.group(2).strip(),
                         "rng": [int(x) for x in re.findall(r"[（(](\d{1,2})[)）]", ln)]})
    if not rows:
        return []
    # 精解组：**第1~4空 主题** / **第N空 ...**
    secs, cur, lo_hi = [], None, None
    for ln in key.split("\n"):
        mg = re.match(r"^\s*\*\*第(\d+)(?:[~～](\d+))?空?\*\*\s*(.*)$", ln)
        if mg:
            cur = [mg.group(3)]
            lo_hi = (int(mg.group(1)), int(mg.group(2) or mg.group(1)))
            secs.append({"rng": lo_hi, "lines": cur})
        elif cur is not None:
            cur.append(ln)
    def key_for(idx, rng):
        if len(rows) == len(secs):
            return "\n".join(secs[idx]["lines"]).strip()
        if not rng:
            return ""
        hits = [s for s in secs if s["rng"][0] >= rng[0] and s["rng"][0] <= rng[-1]] or \
               [s for s in secs if s["rng"][0] <= rng[0] <= s["rng"][1]]
        if not hits:
            return ""
        return "\n".join(hits[0]["lines"]).strip()
    out = []
    for i, r in enumerate(rows):
        st = r["stem"] + (("\n\n" + opts) if opts else "")
        out.append({"n": r["n"], "stem": st, "key": key_for(i, r["rng"])})
    return out

SPECS = {
    "y2014q2": ("dati", "第{n}题"),
    "y2015q2": ("dati", "第{n}题"),
    "y2017q1": ("xuan", "第{n}题"),
    "y2018q1": ("xuan", "第{n}题"),
    "y2019q1": ("xuan", "第{n}题"),
}

def main():
    d = json.load(open(REPO + r"\data\zhenti801.json", encoding="utf-8"))
    zkp = json.load(open(REPO + r"\data\z801_kp.json", encoding="utf-8"))
    out = {}
    report = []
    for y in d["years"]:
        for q in y["qs"]:
            if q["id"] not in SPECS:
                continue
            mode, labfmt = SPECS[q["id"]]
            parts = split_dati(q.get("stem") or "", q.get("key") or "") if mode == "dati" \
                else split_xuan(q.get("stem") or "", q.get("key") or "")
            for p in parts:
                sid = f"{q['id']}#{p['n']}"
                assert sid in PART_KP, f"缺考点指派: {sid}"
                zkp[sid] = PART_KP[sid]
                report.append(f"{sid} | {PART_KP[sid][0][:2]}·{PART_KP[sid][1][:14]} | {topic(p['key'])} | {p['stem'][:40].replace(chr(10),' ')}")
            out[q["id"]] = {"parts": parts, "opts": ""}
    # 移除整块条目
    for w in WHOLE_REMOVE:
        zkp.pop(w, None)
    json.dump(out, open(REPO + r"\data\z801_split.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    json.dump(zkp, open(REPO + r"\data\z801_kp.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=0)
    for r in report:
        print(r)
    n = sum(len(v["parts"]) for v in out.values())
    print(f"\nz801_split.json: {len(out)} 块 {n} 分题; z801_kp.json: {len(zkp)} 条（-5 整块 +{n} 分题）")

if __name__ == "__main__":
    main()
