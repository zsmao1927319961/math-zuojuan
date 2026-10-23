# -*- coding: utf-8 -*-
# 2026-10-24 两件事:
# 1) 新增「2019数二真题错题」5题(选6/解18/19/21/22)与「2020数二真题错题」6题(选5/填12/解16/20/21/22),
#    题面/解析图热链研可岸 oss(题面图/解析图URL直取自 /api/question/subject/6, 2020年缺失解析图按
#    analysis-v2/math/math2/{year}/T{n}/1.png 规律探测补齐), 11题题面全部经视觉核验(题号/题型/考点相符),
#    kp/chapter 沿用已录87题的「研可岸考点→大观园节点」先例映射, 全部对照 cxy_categories_cache.json 校验。
# 2) 新增补刷卷⑥/⑦(耐刷王同型): 用户裁定补刷卷用耐刷王题。逐错题考点从 /api/question/subject/3969道
#    耐刷王题库(考点树 /api/knowledge-point/tree/26)按节点取T1(单中值取两道不同题), 题面+解析图热链
#    examNaishua oss, 4道抽查视觉核验(曲率/单中值构造/极大无关组含参/微分方程几何应用全匹配)。
# ⚠️ exams 键=数组下标(localStorage 错因/重做挂其上), 只追加不插队, 不动 exams[0..15] 的对象身份。
import json

BASE = r"D:\考研数学\组卷网站_static"
P = BASE + r"\data\mock_errors.json"
OSS = "https://oss.hzyankean.com/examMathQuestion/"
NS = "https://oss.hzyankean.com/examNaishua/"

# 1) 大观园分类树节点名校验集
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
assert len(exams) == 16, "应已有 16 卷(3模考+13真题系), 实际 %d" % len(exams)
assert exams[-1]["paper"]["name"] == "2018数二真题错题", exams[-1]["paper"]["name"]

def paper(name, date, group, taken, sub):
    return {"paper": {"name": name, "date": date, "group": group, "taken": taken,
                      "sub": sub, "answers": ""}, "errors": []}

# 2) 2019数二真题错题 5题(选6/解18/19/21/22)
Q2019 = [
    dict(no=6, type="选择", score=4, subject="高数", chapter="导数应用", kp="曲率",
         qimg=OSS + "question/13b5ee80efc44bcfa553b6b364975af0.png",
         ana=[OSS + "analysis-v2/math/math2/2019/T6/1.png"]),
    dict(no=18, type="解答", score=10, subject="高数", chapter="二重积分", kp="二重积分",
         qimg=OSS + "question/796c11d239d44d008b2c8ba77853d44f.png",
         ana=[OSS + "analysis-v2/math/math2/2019/T18/1.png",
              OSS + "analysis-v2/math/math2/2019/T18/2.png"]),
    dict(no=19, type="解答", score=10, subject="高数", chapter="一元积分", kp="几何应用",
         qimg=OSS + "question/0c5facde17b94598a28dc0b5ab5e0a40.png",
         ana=[OSS + "analysis-v2/math/math2/2019/T19/1.png"]),
    dict(no=21, type="解答", score=11, subject="高数", chapter="一元微分", kp="微分中值定理",
         qimg=OSS + "analysis-v2/f0c8ab30-c633-4177-8071-bef0da162fe1.png",
         ana=[OSS + "analysis-v2/24e80518-0b57-4f7e-a3ee-193105cfd242.png"]),
    dict(no=22, type="解答", score=11, subject="线代", chapter="向量", kp="极大无关组",
         qimg=OSS + "analysis-v2/e01d2a4c-64b5-4fbe-93ef-062caae73935.png",
         ana=[OSS + "analysis-v2/6ab68fef-7323-41b6-998a-b4de8188e376.png"]),
]

# 3) 2020数二真题错题 6题(选5/填12/解16/20/21/22)
#    2020年题面图/解析图 URL 含中文「题目.png」, 浏览器热链时自动编码, 照录 API 原始值。
Q2020 = [
    dict(no=5, type="选择", score=4, subject="高数", chapter="多元微分", kp="偏导数",
         qimg=OSS + "question/math/math2/2020/T5/题目.png",
         ana=[OSS + "analysis-v2/4358208f-4ac3-4c22-a3d5-b78310ba07c4.png"]),
    dict(no=12, type="填空", score=4, subject="高数", chapter="一元积分", kp="物理应用（数一二）",
         qimg=OSS + "question/math/math2/2020/T12/题目.png",
         ana=[OSS + "analysis-v2/math/math2/2020/T12/1.png"]),
    dict(no=16, type="解答", score=10, subject="高数", chapter="一元积分", kp="变限积分相关",
         qimg=OSS + "question/math/math2/2020/T16/题目.png",
         ana=[OSS + "analysis-v2/math/math2/2020/T16/1.png"]),
    dict(no=20, type="解答", score=11, subject="高数", chapter="一元微分", kp="微分中值定理",
         qimg=OSS + "question/math/math2/2020/T20/题目.png",
         ana=[OSS + "analysis-v2/math/math2/2020/T20/1.png"]),
    dict(no=21, type="解答", score=11, subject="高数", chapter="微分方程", kp="解微分方程",
         qimg=OSS + "question/math/math2/2020/T21/题目.png",
         ana=[OSS + "analysis-v2/9ef91d61-64d9-4e3c-9948-11d70eddb168.png"]),
    dict(no=22, type="解答", score=11, subject="线代", chapter="二次型", kp="标准型",
         qimg=OSS + "question/math/math2/2020/T22/题目.png",
         ana=[OSS + "analysis-v2/math/math2/2020/T22/1.png"]),
]

# 4) 补刷卷⑥·2019数二错题同型(耐刷王, 节点: 曲率与曲率圆/二重积分的计算/求平面图形的面积/单中值问题/向量组的秩与极大无关组)
N6 = [
    dict(no=1, type="解答", subject="高数", chapter="导数应用", kp="曲率", ztCol="耐刷王·曲率与曲率圆",
         qimg=NS + "question/第3章_导数与微分/T1_54190_be5969c7.png",
         ana=[NS + "analysis/第3章_导数与微分/T1_54190_7fce1a89.png"]),
    dict(no=2, type="解答", subject="高数", chapter="二重积分", kp="二重积分", ztCol="耐刷王·二重积分的计算",
         qimg=NS + "question/第6章_二重积分/T1_19434_ee12460b.png",
         ana=[NS + "analysis/第6章_二重积分/T1_19434_b7fb5327.png"]),
    dict(no=3, type="解答", subject="高数", chapter="一元积分", kp="几何应用", ztCol="耐刷王·求平面图形的面积",
         qimg=NS + "question/第4章_一元积分学/T1_54177_ea214867.png",
         ana=[NS + "analysis/第4章_一元积分学/T1_54177_c0dd6cf0.png"]),
    dict(no=4, type="解答", subject="高数", chapter="一元微分", kp="微分中值定理", ztCol="耐刷王·单中值问题",
         qimg=NS + "question/第3章_导数与微分/T1_32006_5c976ee3.png",
         ana=[NS + "analysis/第3章_导数与微分/T1_32006_0ba664e6.png"]),
    dict(no=5, type="解答", subject="线代", chapter="向量", kp="极大无关组", ztCol="耐刷王·向量组的秩与极大无关组",
         qimg=NS + "question/第3章_向量/T10_59302_eea78d29.png",
         ana=[NS + "analysis/第3章_向量/T10_59302_5f238511.png"]),
]

# 5) 补刷卷⑦·2020数二错题同型(耐刷王, 节点: 多元显函数偏导全微分/抽水做功/变限积分函数/单中值问题(第二道)/微分方程几何应用/化二次型为标准形)
N7 = [
    dict(no=1, type="解答", subject="高数", chapter="多元微分", kp="偏导数", ztCol="耐刷王·偏导数与全微分计算",
         qimg=NS + "question/第5章_多元函数微分学/T1_53509_d0163cf5.png",
         ana=[NS + "analysis/第5章_多元函数微分学/T1_53509_2666ec53.png"]),
    dict(no=2, type="解答", subject="高数", chapter="一元积分", kp="物理应用（数一二）", ztCol="耐刷王·抽水做功",
         qimg=NS + "question/第9章_一元微积分的应用_仅数一_数二_/T1_57952_74767432.png",
         ana=[NS + "analysis/第9章_一元微积分的应用_仅数一_数二_/T1_57952_8c7c1165.png"]),
    dict(no=3, type="解答", subject="高数", chapter="一元积分", kp="变限积分相关", ztCol="耐刷王·变限积分函数",
         qimg=NS + "question/第4章_一元积分学/T1_28251_0ec4a574.png",
         ana=[NS + "analysis/第4章_一元积分学/T1_28251_22a50183.png"]),
    dict(no=4, type="解答", subject="高数", chapter="一元微分", kp="微分中值定理", ztCol="耐刷王·单中值问题",
         qimg=NS + "question/第3章_导数与微分/T10_88283_ea56ec85.png",
         ana=[NS + "analysis/第3章_导数与微分/T10_88283_3673676b.png"]),
    dict(no=5, type="解答", subject="高数", chapter="微分方程", kp="解微分方程", ztCol="耐刷王·微分方程的几何应用",
         qimg=NS + "question/第7章_微分方程/T1_54561_83303e4c.png",
         ana=[NS + "analysis/第7章_微分方程/T1_54561_1b0aa3e6.png"]),
    dict(no=6, type="解答", subject="线代", chapter="二次型", kp="标准型", ztCol="耐刷王·化二次型为标准形",
         qimg=NS + "question/第6章_二次型/T1_58972_bb147941.png",
         ana=[NS + "analysis/第6章_二次型/T1_58972_9718ad34.png"]),
]

def zt_exam(year, qs):
    ex = paper("%d数二真题错题" % year, str(year), "真题错题", True,
               "真题错题 · %d数学二 · 题面/解析源自研可岸真题网" % year)
    for r in qs:
        e = {k: r[k] for k in ("no", "type")}
        if "score" in r:
            e["score"] = r["score"]
        e["subject"] = r["subject"]; e["chapter"] = r["chapter"]; e["kp"] = r["kp"]
        e["qimg"] = r["qimg"]
        e["ztYear"] = year
        e["ztCol"] = "真题"
        e["anaimgs"] = list(r["ana"])
        ex["errors"].append(e)
    ex["errors"].sort(key=lambda x: x["no"])
    return ex

def drill_exam(no_, year, wrong_nos, qs):
    ex = paper("补刷卷%s·%d数二错题同型" % (no_, year), "2026-10-24", "补刷卷", False,
               "耐刷王同型补刷 · 对应%d数二错题 %s · 题面/解析源自研可岸耐刷王" % (year, "/".join(str(x) for x in wrong_nos)))
    for r in qs:
        e = {"no": r["no"], "type": r["type"], "score": None,
             "subject": r["subject"], "chapter": r["chapter"], "kp": r["kp"],
             "qimg": r["qimg"], "ztYear": 0, "ztCol": r["ztCol"], "anaimgs": list(r["ana"])}
        ex["errors"].append(e)
    return ex

exams.append(zt_exam(2019, Q2019))
exams.append(zt_exam(2020, Q2020))
exams.append(drill_exam("⑥", 2019, [6, 18, 19, 21, 22], N6))
exams.append(drill_exam("⑦", 2020, [5, 12, 16, 20, 21, 22], N7))

# 6) 备注与校验(全部针对内存对象, 通过后才落盘)
d["note"] = d["note"] + " | 2026-10-24 新增2019数二真题错题5题(选6/解18/19/21/22)+2020数二真题错题6题(选5/填12/解16/20/21/22), 研可岸API直取题面/解析图热链, 11题题面视觉核验, kp照大观园分类; 新增补刷卷⑥⑦(用户裁定用耐刷王题): 逐错题考点按耐刷王节点取同型题11道(单中值两卷各一道不重复), 题面/解析热链examNaishua oss, exams只追加不插队。"

bad = []
for ex in exams[16:]:
    for e in ex["errors"]:
        if e["chapter"] not in names:
            bad.append((ex["paper"]["name"], e["no"], "ch", e["chapter"]))
        if e["kp"] not in names:
            bad.append((ex["paper"]["name"], e["no"], "kp", e["kp"]))
        if not e.get("qimg"):
            bad.append((ex["paper"]["name"], e["no"], "qimg空", ""))
        if not e.get("anaimgs"):
            bad.append((ex["paper"]["name"], e["no"], "解析图空", ""))
if bad:
    print("节点名校验失败:", bad)
    raise SystemExit(1)

assert len(exams) == 20, len(exams)
total = sum(len(ex["errors"]) for ex in exams)
assert total == 138 + 22, total  # 原138 + 真题11 + 耐刷王11

json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 7) 复读摘要
d2 = json.load(open(P, encoding="utf-8"))
for ex in d2["exams"][15:]:
    print(ex["paper"]["name"], len(ex["errors"]))
print("错题总数:", sum(len(ex["errors"]) for ex in d2["exams"]))
