# -*- coding: utf-8 -*-
"""补丁b: 清理三处尾巴(32-07/53-08重复段, 81-10右侧页碎片块)"""
import json, sys

path = r"D:/考研数学/组卷网站_static/data/questions.json"
qs = json.load(open(path, encoding="utf-8"))
Q = {q["id"]: q for q in qs}

def edit(qid, field, old, new, tag):
    cur = Q[qid].get(field) or ""
    if old not in cur:
        print(f"[MISS] {qid}: {old[:50]!r}"); sys.exit(1)
    Q[qid][field] = cur.replace(old, new, 1)
    print(f"[OK] {qid} {tag}")

edit("tk299-32-07", "question_text",
     "$Z(t)$ 是否各态历经？$X(t)$ 的任一样本函数，",
     "$Z(t)$ 是否各态历经？",
     "删重复尾巴")

edit("tk299-53-08", "question_text",
     "说明哪种更节省。常规 AM，求所需的",
     "说明哪种更节省。",
     "删重复尾巴")

# 81-10: 删"——右侧页…"起的整块碎片
cur = Q["tk299-81-10"]["question_text"]
i = cur.find("——右侧页")
if i < 0:
    print("[MISS] 81-10 右侧页 marker"); sys.exit(1)
Q["tk299-81-10"]["question_text"] = cur[:i].rstrip() + "\n"
print(f"[OK] tk299-81-10 删右侧页碎片块 ({len(cur)} -> {len(Q['tk299-81-10']['question_text'])})")

json.dump(qs, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved")
