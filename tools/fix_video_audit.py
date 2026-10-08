# -*- coding: utf-8 -*-
"""视频验证轮发现的碎片/截断修复(13处) + 41-02答案整理"""
import json, sys

path = r"D:/考研数学/组卷网站_static/data/questions.json"
qs = json.load(open(path, encoding="utf-8"))
Q = {q["id"]: q for q in qs}

def edit(qid, field, old, new):
    cur = Q[qid].get(field) or ""
    if old not in cur:
        print(f"[MISS] {qid} {field}: {old[:40]!r}"); sys.exit(1)
    Q[qid][field] = cur.replace(old, new, 1)
    print(f"[OK] {qid} {field}")

def head_drop(qid, field, junk):
    cur = Q[qid].get(field) or ""
    if not cur.startswith(junk):
        print(f"[MISS-head] {qid}: {junk[:30]!r}"); sys.exit(1)
    Q[qid][field] = cur[len(junk):].lstrip("\n")
    print(f"[OK] {qid} {field} 头部去碎片")

# ---- question_text ----
edit("tk299-13-06", "question_text", "平择出品，必是精品\n", "")
edit("tk299-32-08", "question_text", "（河北大学 2016 年第四题）\n$t_0$、$\\theta_0$ 为任意实数，$Z(t)$ 是否各态历经？", "（河北大学 2016 年第四题）")
edit("tk299-65-03", "question_text",
     "（河北大学 2020 年三、3）\n（右侧页面边缘可见的部分文字：）\n考点 6：\n平界小\n本考\n真计算\n1、在\n消除或\nA. 时",
     "（河北大学 2020 年三、3）")
head_drop("tk299-75-05", "question_text", "半并出晶，必是精晶")
edit("tk299-75-05", "question_text", "（南京邮电大学 2022 年第八题）\n平界\n8、其\n星座\n$s_4$", "（南京邮电大学 2022 年第八题）")
edit("tk299-75-11", "question_text",
     "试求：\n【图】\n（右页边缘残缺文字）\n12、\n$s_2 = $ …\n概出\n其中\n试\n(1)\n(2)\n(3)\n其中\n(1)星座点",
     "试求：\n【图】\n(1)星座点")

# ---- answer_text 头部碎片 ----
head_drop("tk299-31-01", "answer_text", "…相关函数求解")
head_drop("tk299-32-04", "answer_text", "$\\omega_0\\tau+\\theta)$")
head_drop("tk299-32-07", "answer_text", "18696")
head_drop("tk299-34-09", "answer_text", "$2B$\n$$\\frac{2}{2}B$$")
edit("tk299-44-04", "answer_text", "（1）\n8696\n", "（1）\n")
head_drop("tk299-52-07", "answer_text", "3696")
head_drop("tk299-71-01", "answer_text", "考点")
head_drop("tk299-102-05", "answer_text", "的最高次项均低于4。")
head_drop("tk299-102-12", "answer_text", "单界出错，必是精确")

# ---- 41-02 答案整理(书答案首行被裁切) ----
Q["tk299-41-02"]["answer_text"] = (
    "2、恒参信道：幅频特性；相频特性。随参信道：信号幅度的影响随时间而变（衰减），"
    "时延随时间变化，多径传播。（原书答案首行被扫描裁切，按可见内容整理）")
print("[OK] tk299-41-02 answer_text 重写")

json.dump(qs, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved")
