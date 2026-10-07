# -*- coding: utf-8 -*-
"""430题(txyl: tk299+qhzt)全面文本体检 2026-10-07
检查: 截断/空题面/怪字符/LaTeX配对/选项缺失/填空答案数不匹配/重复片段/解析缺失"""
import json, re, collections, sys, unicodedata

REPO = r"D:\考研数学\组卷网站_static"
qs = json.load(open(REPO + r"\data\questions.json", encoding="utf-8"))
tx = [q for q in qs if q.get("subject") == "txyl"]
print(f"txyl total: {len(tx)}  (tk299 {sum(1 for q in tx if q['source']=='tk299')}, qhzt {sum(1 for q in tx if q['source']=='qhzt')})")

issues = collections.defaultdict(list)
def add(q, kind, detail):
    issues[kind].append((q["id"], detail))

# 原书页照片对照线索: 每题no字段与chapter
for q in tx:
    qt = q.get("question_text") or ""
    at = q.get("answer_text") or ""
    sol = q.get("solution") or ""
    t = q.get("type") or ""

    # 1. 空题面且无题图
    if not qt.strip() and not q.get("question_img"):
        add(q, "A1_空题面无图", f"type={t} answer={at[:30]}")
    # 2. 题面过短(非纯图题)
    if qt.strip() and len(qt.strip()) < 8 and not q.get("question_img"):
        add(q, "A2_题面过短", repr(qt))

    s = qt.strip()
    # 3. 异常结尾(截断嫌疑): 逗号/顿号/冒号/分号/加号/等号/左括号/反斜杠/且/或/为/的
    if s:
        bad_tail = "，、；：（(＋+=\\且或与及的和差的为则那么若当设求证计算下列"
        for ch in bad_tail:
            if s.endswith(ch):
                add(q, "B1_异常结尾", f"尾字符[{ch}] …{s[-25:]}")
                break
    # 4. $奇数个(未闭合公式)
    if qt.count("$") % 2 == 1:
        add(q, "B2_美元符奇数", f"${qt.count('$')}个")
    # 5. \left 无 \right (排除 \rightarrow/\leftarrow 前缀误报)
    n_l = len(re.findall(r"\\left(?![a-zA-Z])", qt))
    n_r = len(re.findall(r"\\right(?![a-zA-Z])", qt))
    if n_l != n_r:
        add(q, "B3_left_right不配对", f"left={n_l} right={n_r}")
    # 6. 怪字符
    weird = re.findall(r"[\ufffd\u25a1\u00a0\u3000\u2028\u2029]", qt + at + sol)
    if weird:
        add(q, "C1_替换符或异常空白", f"{collections.Counter(weird)}")
    # 常用汉字+ASCII+标点白名单外的稀有字符(启发式: 兼容区/私用区/生僻符号)
    for ch in qt + at:
        o = ord(ch)
        if 0xE000 <= o <= 0xF8FF or 0xFFF0 <= o <= 0xFFFF or unicodedata.category(ch) == "Cn" and ch not in "＿":
            add(q, "C2_私用或未定义字符", f"U+{o:04X} [{ch}] in {q['id']}")
            break

    # 7. 选择题缺选项
    if ("选择" in t or "单选" in t) and not re.search(r"[ABＡＢ][\.、．)）]", qt):
        # dxy里有question_type, 后续对照
        add(q, "D1_选择题无选项", f"type={t} 题面={s[:40]}")
    # 8. 填空题 空位数 vs 答案条目数
    blanks = len(re.findall(r"_{2,}|＿{2,}", qt))
    if blanks >= 1:
        # 答案侧按分隔符粗分
        parts = re.split(r"[;；,，、/／]|及(?![时论]|时)|和(?=[一二三四五六七八九十\d])", at)
        # 只对题面明确N空且答案很短的数值型填空报告极端不匹配
        if blanks >= 2 and len(parts) < blanks:
            add(q, "D2_空多答少", f"空{blanks}个 答案原文={at[:60]}")
    # 9. 连续重复汉字(OCR重影)
    for m in re.finditer(r"([\u4e00-\u9fff])\1", qt):
        w = m.group(0)
        # 数学/通信文本里合法叠词有限
        if w[0] not in "一一种种种种常常徐徐多多少少刚刚纷纷往往渐渐缓缓漫漫统统通通":
            ctx = qt[max(0, m.start()-10):m.end()+10]
            if w[0] not in "一一":  # 一一 之外的叠字报告
                add(q, "E1_叠字嫌疑", f"[{w}] …{ctx}…")
                break
    # 10. 解析
    if len(sol.strip()) < 10:
        add(q, "F1_solution缺失或过短", f"len={len(sol.strip())} {sol[:20]!r}")

# 11. tk299 no 与 chapter 一致性 + 深链兼容
ids = [q["id"] for q in tx]
dup = [i for i, n in collections.Counter(ids).items() if n > 1]
if dup: print("重复id:", dup)

print(f"\n===== 汇总 =====")
for k in sorted(issues):
    print(f"\n## {k} ({len(issues[k])})")
    for qid, d in issues[k][:25]:
        print(f"  {qid}: {d}")
    if len(issues[k]) > 25: print(f"  ...共{len(issues[k])}")
