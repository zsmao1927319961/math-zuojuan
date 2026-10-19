# -*- coding: utf-8 -*-
# 2026-10-19 两件事:
# 1) 把 exams[6]「真题网错题本 · 历年错题」49 题按 ztYear 拆成 2010~2017 八个年份卷册(07-09 同款形式),
#    耐刷王 3 题(ztYear 空)留在原卷并改名; 2) 新增「2018数二真题错题」7 题(选4/填9/解17/18/20/21/22),
#    题面/解析图热链研可岸 oss, 全部答案经官方解析图+sympy 双核验。
# ⚠️ exams 键=数组下标(localStorage 错因/重做挂其上), 本脚本只追加不插队, 不动 exams[0..6] 的对象身份。
import json
import copy

BASE = r"D:\考研数学\组卷网站_static"
P = BASE + r"\data\mock_errors.json"

# 1) 分类树节点名校验集
tree = json.load(open(BASE + r"\tools\cxy_categories_cache.json", encoding="utf-8"))
names = set()
def walk(n):
    if isinstance(n, list):
        for x in n:
            walk(x)
        return
    if isinstance(n, dict):
        nm = n.get("name") or n.get("title") or n.get("label")
        if nm:
            names.add(nm)
        for ch in (n.get("children") or n.get("sub") or n.get("items") or []):
            walk(ch)
walk(tree)

d = json.load(open(P, encoding="utf-8"))
exams = d["exams"]
assert len(exams) == 7, "应已有 3 模考 + 4 真题卷, 实际 %d" % len(exams)
ex6 = exams[6]
assert ex6["paper"]["name"] == "真题网错题本 · 历年错题", ex6["paper"]["name"]

# 2) 按 ztYear 分流(对象原样搬移, 不修任何字段 → 零转录风险)
by_year = {}
resid = []
for e in ex6["errors"]:
    y = e.get("ztYear")
    if y in (2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017):
        by_year.setdefault(y, []).append(e)
    else:
        resid.append(e)
got = {y: len(v) for y, v in sorted(by_year.items())}
assert got == {2010: 7, 2011: 6, 2012: 9, 2013: 6, 2014: 6, 2015: 4, 2016: 5, 2017: 3}, got
assert len(resid) == 3, len(resid)

def paper(name, year, sub):
    return {"paper": {"name": name, "date": str(year), "group": "真题错题", "taken": True,
                      "sub": sub, "answers": ""}, "errors": []}

# 3) 原卷改名留耐刷王 3 题(下标 6 不动, localStorage 键不变)
ex6["paper"]["name"] = "真题网错题本 · 耐刷王错题"
ex6["paper"]["sub"] = "真题错题 · 耐刷王 · 题面/解析源自研可岸真题网"
ex6["errors"] = resid

# 4) 追加 2010~2017 年份卷册(07-09 同款形式, 组内按题号升序)
for y in range(2010, 2018):
    ex = paper("%d数二真题错题" % y, y, "真题错题 · %d数学二 · 题面/解析源自研可岸真题网" % y)
    ex["errors"] = sorted(by_year[y], key=lambda x: x["no"])
    exams.append(ex)

# 5) 追加 2018 数二真题错题 7 题(研可岸 API 直取, 答案官方解析图+sympy 双核验)
OSS = "https://oss.hzyankean.com/examMathQuestion/"
Q2018 = [
    dict(no=4, type="选择", score=4, subject="高数", chapter="一元积分", kp="积分三大定理",
         qimg=OSS + "question/801d9628ffb54bbbb9554c8f4947a73f.png",
         ana=[OSS + "analysis-v2/math/math2/2018/T4/2.png", OSS + "analysis-v2/math/math2/2018/T4/3.png"]),
    dict(no=9, type="填空", score=4, subject="高数", chapter="极限", kp="极限计算",
         qimg=OSS + "question/5c3d12f7daf84a2490599a835f06dfb8.png",
         ana=[OSS + "analysis-v2/math/math2/2018/T9/2.png", OSS + "analysis-v2/math/math2/2018/T9/3.png"]),
    dict(no=17, type="解答", score=10, subject="高数", chapter="二重积分", kp="二重积分",
         qimg=OSS + "question/17ee2d8883b646be8c8a9b444f82b68d.png",
         ana=[OSS + "analysis-v2/math/math2/2018/T17/2.png", OSS + "analysis-v2/math/math2/2018/T17/3.png"]),
    dict(no=18, type="解答", score=10, subject="高数", chapter="导数应用", kp="不等式",
         qimg=OSS + "question/28ce2a07dc5740618c47c45798fa6242.png",
         ana=[OSS + "analysis-v2/math/math2/2018/T18/2.png"]),
    dict(no=20, type="解答", score=11, subject="高数", chapter="一元积分", kp="几何应用",
         qimg=OSS + "question/2e1253ca5d424482afb8e0ec5b81ac70.png",
         ana=[OSS + "analysis-v2/math/math2/2018/T20/2.png", OSS + "analysis-v2/math/math2/2018/T20/3.png"]),
    dict(no=21, type="解答", score=11, subject="高数", chapter="极限", kp="数列极限",
         qimg=OSS + "question/296ebc9e75b34560a795b3429762c099.png",
         ana=[OSS + "analysis-v2/e7f7698d-941d-4476-9841-4b5a5d4d1f6e.png"]),
    dict(no=22, type="解答", score=11, subject="线代", chapter="二次型", kp="标准型",
         qimg=OSS + "question/f1bdec7e040d49949f080f273c512f10.png",
         ana=[OSS + "analysis-v2/math/math2/2018/T22/2.png", OSS + "analysis-v2/math/math2/2018/T22/3.png"]),
]
ex18 = paper("2018数二真题错题", 2018, "真题错题 · 2018数学二 · 题面/解析源自研可岸真题网")
for r in Q2018:
    e = {k: r[k] for k in ("no", "type", "score", "subject", "chapter", "kp")}
    e["qimg"] = r["qimg"]
    e["ztYear"] = 2018
    e["ztCol"] = "真题"
    e["anaimgs"] = list(r["ana"])
    ex18["errors"].append(e)
ex18["errors"].sort(key=lambda x: x["no"])
exams.append(ex18)

# 6) 备注与校验(全部针对内存对象, 通过后才落盘)
d["note"] = d["note"] + " | 2026-10-19 历年错题49按年份拆卷(2010~2017各一卷共46题, 原卷改名耐刷王错题留3题), 新增2018数二真题错题7题(选4/填9/解17/18/20/21/22, 官方解析图+sympy双核验), exams只追加不插队。"

bad = []
for ex in exams[3:]:
    for e in ex["errors"]:
        if e["chapter"] not in names:
            bad.append((ex["paper"]["name"], e["no"], "ch", e["chapter"]))
        if e["kp"] not in names:
            bad.append((ex["paper"]["name"], e["no"], "kp", e["kp"]))
        if not e.get("qimg"):
            bad.append((ex["paper"]["name"], e["no"], "qimg空", ""))
if bad:
    print("节点名校验失败:", bad)
    raise SystemExit(1)

assert len(exams) == 16, len(exams)  # 3模考 + 2007/2008/2009 + 耐刷王残卷 + 8年份卷 + 2018卷
total = sum(len(ex["errors"]) for ex in exams)
assert total == 131 + 7, total  # exams[] 原 131(模考44+真题87; 51 是含 series 余炳森7题的全站数) + 7 新录 = 138

json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 7) 复读摘要
d2 = json.load(open(P, encoding="utf-8"))
for ex in d2["exams"]:
    print(ex["paper"]["name"], len(ex["errors"]))
print("错题总数:", sum(len(ex["errors"]) for ex in d2["exams"]))
