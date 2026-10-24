# -*- coding: utf-8 -*-
# 2026-10-24 补刷卷交付方式纠正(用户裁定: '补刷卷不是加到网站里,而是生成pdf放到桌面上,
# 那个是补刷卷的错题才加里面'):
# 1) mock_errors.json 撤销尾部的「补刷卷⑥⑦」两个卷册(exams[18]/[19], 仅入库几小时且从未做过,
#    localStorage exam18/exam19 键无人使用, 尾部移除安全), 真题卷 2019/2020(exams[16]/[17])原样保留;
# 2) note 最后一段改写为 PDF 交付口径; 补刷卷⑥⑦ PDF 由 tools/gen_drill_pdf_20261024.py 生成到桌面;
# 3) 校验: 18 卷 / 149 错题(138+11)。
import json

BASE = r"D:\考研数学\组卷网站_static"
P = BASE + r"\data\mock_errors.json"

d = json.load(open(P, encoding="utf-8"))
exams = d["exams"]
assert len(exams) == 20, len(exams)
assert exams[18]["paper"]["name"] == "补刷卷⑥·2019数二错题同型", exams[18]["paper"]["name"]
assert exams[19]["paper"]["name"] == "补刷卷⑦·2020数二错题同型", exams[19]["paper"]["name"]
assert exams[16]["paper"]["name"] == "2019数二真题错题"
assert exams[17]["paper"]["name"] == "2020数二真题错题"

del exams[18:20]

OLD_TAIL = " | 2026-10-24 新增2019数二真题错题5题(选6/解18/19/21/22)+2020数二真题错题6题(选5/填12/解16/20/21/22), 研可岸API直取题面/解析图热链, 11题题面视觉核验, kp照大观园分类; 新增补刷卷⑥⑦(用户裁定用耐刷王题): 逐错题考点按耐刷王节点取同型题11道(单中值两卷各一道不重复), 题面/解析热链examNaishua oss, exams只追加不插队。"
NEW_TAIL = (" | 2026-10-24 新增2019数二真题错题5题(选6/解18/19/21/22)+2020数二真题错题6题(选5/填12/解16/20/21/22), "
            "研可岸API直取题面/解析图热链, 11题题面视觉核验, kp照大观园分类; "
            "补刷卷⑥⑦(耐刷王同型11道)改为PDF交付桌面(tools/gen_drill_pdf_20261024.py), 不入站——"
            "待用户做完报错题号后, 补刷卷错题再按补④先例入本(曾短暂入库已撤, 尾部下标无人用, 移除安全)。")
if d["note"].endswith(OLD_TAIL):
    d["note"] = d["note"][:-len(OLD_TAIL)] + NEW_TAIL
else:
    # 兜底: 按分隔符取最后一段整体替换
    parts = d["note"].split(" | ")
    d["note"] = " | ".join(parts[:-1]) + NEW_TAIL

assert len(exams) == 18, len(exams)
total = sum(len(ex["errors"]) for ex in exams)
assert total == 149, total  # 138 + 11(真题) ; 补刷卷11道不占错题口径

json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

d2 = json.load(open(P, encoding="utf-8"))
for ex in d2["exams"][-2:]:
    print(ex["paper"]["name"], len(ex["errors"]))
print("卷册数:", len(d2["exams"]), "错题总数:", sum(len(ex["errors"]) for ex in d2["exams"]))
print("note尾段:", d2["note"][-120:])
