# -*- coding: utf-8 -*-
"""2026-11-09 考点审计：216 题全量过目后的改标清单（20 处）。
耐刷卷两条同 no=1，按题面关键字区分。幂等。"""
import json, io, sys, os, shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(R, "data", "mock_errors.json")

# (exam匹配名, no, q子串或None) -> (new_kp, new_chapter或None=不改)
FIX = [
    (("2027考研数学开学大模考（数学二）", 15, None), ("定积分定义求 $n$ 项和极限", "一元积分")),
    (("2027考研数学开学大模考（数学二）", 22, None), (None, "矩阵")),
    (("2007数二真题错题", 12, None), ("参数方程求导", "导数计算")),
    (("2007数二真题错题", 23, None), ("公共解", None)),
    (("2008数二真题错题", 16, None), ("参数方程求导", None)),
    (("2008数二真题错题", 21, None), ("条件极值", None)),
    (("真题网错题本 · 耐刷王错题", 1, "531084"), ("几何应用", None)),
    (("真题网错题本 · 耐刷王错题", 1, "51090"), ("反常积分", None)),
    (("2010数二真题错题", 2, None), ("微分方程解的性质与结构", None)),
    (("2010数二真题错题", 13, None), ("相关变化率", "相关变化率")),
    (("2014数二真题错题", 12, None), ("导数应用（切法线、曲率）", "导数应用")),
    (("2015数二真题错题", 2, None), ("函数极限概念题", None)),
    (("2017数二真题错题", 21, None), ("解微分方程", "微分方程")),
    (("2021数二真题错题", 5, None), ("泰勒多项式", "极限")),
    (("2021数二真题错题", 9, None), ("公共解", None)),
    (("2024数二真题错题", 14, None), ("高阶导数", None)),
    (("2026数二真题错题", 7, None), ("二重积分", "二重积分")),
    (("2026数二真题错题", 10, None), ("特征值与特征向量", "特征值与特征向量")),
    (("欧几里得9月模考（数学二）", 20, None), ("解微分方程", None)),
    (("欧几里得9月模考（数学二）", 7, None), ("微分概念", None)),
]

raw = open(DATA, encoding="utf-8").read()
me = json.loads(raw)
applied = []
for (ename, no, qsub), (nkp, nch) in FIX:
    hits = 0
    for ex in me["exams"]:
        if ex["paper"].get("name", "") != ename:
            continue
        for e in ex["errors"]:
            if e["no"] != no:
                continue
            if qsub and qsub not in (e.get("q") or ""):
                continue
            if nkp:
                e["kp"] = nkp
            if nch:
                e["chapter"] = nch
            hits += 1
            applied.append(f"{ename[:10]}-{no}{('/' + qsub) if qsub else ''}: kp={e['kp']}, ch={e['chapter']}")
    if hits == 0:
        applied.append(f"!! 未命中: {ename[:12]} no={no} qsub={qsub}")

shutil.copyfile(DATA, os.path.join(R, "tools", "_bak_mock_errors_20261109b.json"))
open(DATA, "w", encoding="utf-8").write(json.dumps(me, ensure_ascii=False, indent=2))
print(f"applied {len(applied)} / {len(FIX)}")
for a in applied:
    print(" ", a)
