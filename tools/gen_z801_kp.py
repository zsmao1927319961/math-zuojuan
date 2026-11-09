# -*- coding: utf-8 -*-
"""生成 data/z801_kp.json —— 801真题 722 追踪单元 → 统一考点树映射。
sid 方案与 zhenti801.html itemsOf() 完全一致：有subs块 sid=id#n(n=首空号)，无subs块 sid=id。
落位顺序: OVERRIDES(sid精确) > 【知识点】规则 > ZT_MAP(2014-2025大题) > 全文关键词规则 > 未落位清单。
评审清单写 tools/_z801_kp_review.txt 供逐条过目。"""
import json, re, io, sys, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = r"D:\考研数学\组卷网站_static"
TREE = json.load(open(REPO + r"\data\kp_tree.json", encoding="utf-8"))
CHN = {c["n"]: c["ks"] for c in TREE["chapters"]}
CHNAMES = list(CHN.keys())

def kp(chi, ki):
    return [CHNAMES[chi - 1], CHN[CHNAMES[chi - 1]][ki - 1]]

# 规则表（顺序敏感：先专后泛）。(正则, 章, 考点)
RULES = [
    # CH12 同步
    (r"同步|载波提取|科斯塔斯|平方环|平方变换|Costas|帧同步", *kp(12, 1)),
    # CH11 正交/扩频
    (r"扩频|伪随机|跳频", *kp(11, 3)),
    (r"m\s*序列|移存器|特征多项式|线性反馈", *kp(11, 2)),
    (r"正交编码|哈达玛|沃尔什|Hadamard|Walsh|阿达玛", *kp(11, 1)),
    # CH10 信道编码
    (r"卷积|维特比|网格图|格状", *kp(10, 3)),
    (r"码重|最小码距|汉明距|纠错能力|检错|纠错", *kp(10, 1)),
    (r"循环码|生成多项式|线性分组码|监督矩阵|一致校验|校验方程|系统码|汉明码|伴随式|译码", *kp(10, 2)),
    # CH9 信源编码
    (r"PCM\s*30|30/32|复帧|TS\s*16", *kp(9, 7)),
    (r"增量调制|ΔM|△M|\bDM\b", *kp(9, 4)),
    (r"十三折线|A\s*律|13\s*折线|折叠码|极性码|段落码|段内码", *kp(9, 3)),
    (r"抽样定理|抽样速率|抽样率|采样定理|奈奎斯特速率|混叠|带通采样|低通抽样|抽样.*频谱|采样.*频谱", *kp(9, 1)),
    (r"量化信噪比|量化噪声|量化间隔|量化电平|量化级|量化器|均匀量化|量化", *kp(9, 2)),
    (r"时分复用|TDM|时隙", *kp(9, 5)),
    # CH8 最佳接收
    (r"匹配滤波|最佳接收|相关接收", *kp(8, 1)),
    (r"最佳基带|理想信道|理想通信系统", *kp(8, 2)),
    # CH7 频带
    (r"星座|判决区域|欧氏距离|欧式距离|格雷", *kp(7, 5)),
    (r"MSK|最小频移", *kp(7, 6)),
    (r"OFDM|正交频分", *kp(7, 7)),
    (r"频带利用率|频谱利用率|有效性|可靠性|传码率.*带宽.*频带", *kp(7, 2)),
    (r"解调方式|相干.*非相干.*比较|包络检波.*相干", *kp(7, 3)),
    (r"频带.*(无码间|码间|滚降|奈奎斯特)", *kp(7, 4)),
    (r"多进制|M\s*进制|MASK|MPSK|4ASK|8PSK|4PSK|QPSK|8QAM|16QAM|MQAM|四电平|四进制", *kp(7, 8)),
    (r"2ASK|2FSK|2PSK|2DPSK|OOK|移频键控|相移键控|幅移键控|包络检波|相干解调|非相干|频带.*误码|调制.*误码", *kp(7, 1)),
    # CH6 基带
    (r"眼图", *kp(6, 7)),
    (r"时域均衡|均衡器|迫零|抽头", *kp(6, 6)),
    (r"部分响应|第\s*IV\s*类|第四类|相关电平", *kp(6, 4)),
    (r"HDB3|AMI|双相码|CMI|密勒|曼彻斯特|传号交替", *kp(6, 2)),
    (r"基带.*误码率|单极性|双极性.*误码|RZ|NRZ.*误码", *kp(6, 5)),
    (r"无码间|码间干扰|码间串扰|奈奎斯特带宽|奈氏带宽|升余弦|滚降|理想低通", *kp(6, 3)),
    (r"功率谱.*基带|基带.*功率谱|波形.*功率谱", *kp(6, 1)),
    # CH5 模拟调制
    (r"门限", *kp(5, 5)),
    (r"频分复用|FDM|副载波|复合调制|合路", *kp(5, 4)),
    (r"抗噪声|信噪比增益|解调器增益|制度增益|输出信噪比|输入信噪比|噪声性能", *kp(5, 3)),
    (r"调幅指数|调制效率|调幅度", *kp(5, 1)),
    (r"调频|调相|频偏|调角|卡森|贝塞尔|瞬时频率|鉴频|倍频", *kp(5, 2)),
    (r"SSB|DSB|VSB|\bAM\b|单边带|双边带|残留边带|包络", *kp(5, 1)),
    # CH4 信道
    (r"恒参|随参|视距|电离层|对流层|电缆|光纤", *kp(4, 1)),
    (r"多径|衰落|频率选择性|相关带宽|多普勒|快衰落|慢衰落", *kp(4, 2)),
    (r"香农|连续信道|带宽受限", *kp(4, 3)),
    (r"离散信道|对称信道|BSC|BEC|条件熵|联合熵|互信息|信道.*熵", *kp(4, 4)),
    # CH3 随机过程
    (r"白噪声|窄带高斯|高斯白噪声|窄带噪声|瑞利|莱斯", *kp(3, 3)),
    (r"通过.*系统|线性系统|输出.*平稳|系统.*输出", *kp(3, 4)),
    (r"各态历经|遍历|平稳性|广义平稳|严格平稳", *kp(3, 2)),
    (r"自相关|方差|期望|均值|协方差", *kp(3, 1)),
    # CH2 确知信号
    (r"频谱|能量谱|帕塞瓦尔|Parseval|傅里叶|自相关函数.*功率", *kp(2, 1)),
    # CH1 绪论
    (r"信息量|熵", *kp(1, 3)),
    (r"误码率|误比特率|误码", *kp(1, 4)),
    (r"传码率|传信率|码元速率|波特率|比特率|信息速率", *kp(1, 2)),
    (r"有效性|可靠性|信源编码|信道编码", *kp(1, 1)),
]

# 2014-2025 大题题型兜底（平界冲刺课分布，内容修正见分支）
ZT_CH = {
    "t1": lambda s: kp(3, 4),
    "t2": lambda s: kp(5, 3),
    "t3": lambda s: kp(5, 2),
    "t4": lambda s: kp(5, 4),
    "t5": lambda s: kp(6, 3),
    "t7": lambda s: kp(4, 4) if re.search(r"对称信道|四元|离散|互信息|条件熵", s) else kp(4, 3),
    "t8": lambda s: kp(7, 1),
    "t9": lambda s: kp(7, 5) if re.search(r"星座", s) else kp(7, 8),
    "t10": lambda s: kp(8, 1),
    "t11": lambda s: kp(7, 6) if re.search(r"MSK", s) else kp(7, 8),
    "t12": lambda s: kp(6, 6),
    "t13": lambda s: kp(9, 6),
    "t14": lambda s: kp(9, 3),
    "t15": lambda s: kp(9, 1) if re.search(r"抽样|采样|混叠", s) else kp(9, 2),
    "t16": lambda s: kp(10, 3) if re.search(r"卷积|维特比", s) else (kp(10, 1) if re.search(r"码重|最小码距|纠错能力", s) else kp(10, 2)),
}
ZT_MAP = {
    "2014": {4: "t7", 5: "t2", 6: "t5", 7: "t12", 8: "t8", 9: "t13", 10: "t10", 11: "t16"},
    "2015": {4: "t1", 5: "t7", 6: "t2", 7: "t5", 8: "t11", 9: "t8", 10: "t10", 11: "t16"},
    "2016": {4: "t1", 5: "t3", 6: "t12", 7: "t8", 8: "t11", 9: "t10", 10: "t15", 11: "t16"},
    "2017": {4: "t1", 5: "t4", 6: "t5", 7: "t8", 8: "t9", 9: "t10", 10: "t15", 11: "t16"},
    "2018": {4: "t1", 5: "t7", 6: "t2", 7: "t5", 8: "t8", 9: "t10", 10: "t16", 11: "t15"},
    "2019": {4: "t1", 5: "t7", 7: "t9", 8: "t9", 9: "t10", 10: "t16", 11: "t16"},
    "2020": {4: "t1", 5: "t7", 6: "t12", 7: "t9", 8: "t11", 9: "t10", 10: "t13", 11: "t16"},
    "2021": {4: "t7", 5: "t5", 6: "t8", 7: "t9", 8: "t10", 9: "t16", 10: "t13", 11: "t16"},
    "2022": {4: "t7", 5: "t2", 6: "t5", 7: "t15", 8: "t9", 9: "t16"},
    "2023": {4: "t3", 5: "t5", 6: "t8", 7: "t13", 8: "t10", 9: "t16", 10: "t14"},
    "2024": {4: "t1", 5: "t2", 6: "t12", 7: "t8", 8: "t16", 9: "t10", 10: "t13"},
    "2025": {4: "t1", 5: "t2", 6: "t5", 7: "t8", 8: "t14", 9: "t16", 10: "t10"},
}

# sid 精确覆盖（722 单元逐条过目后的人工修正，2026-11-09 全量评审）
OVERRIDES = {
    "y1998q1#2": kp(1, 2), "y1998q1#6": kp(4, 3), "y1998q2": kp(9, 1),
    "y1999q1#4": kp(1, 4), "y1999q1#5": kp(2, 1), "y1999q1#6": kp(2, 1),
    "y1999q3": kp(5, 4), "y1999q4": kp(5, 2), "y1999q5": kp(9, 5),
    "y1999q6": kp(6, 4), "y1999q9": kp(6, 4),
    "y2000q1#6": kp(3, 3), "y2000q4": kp(6, 3), "y2000q5": kp(6, 5),
    "y2000q7": kp(9, 2), "y2000q8": kp(8, 1),
    "y2001q1#1": kp(1, 3), "y2001q1#2": kp(1, 2), "y2001q1#3": kp(2, 1),
    "y2001q1#4": kp(7, 2), "y2001q1#6": kp(3, 1), "y2001q1#8": kp(6, 3),
    "y2001q1#9": kp(6, 3), "y2001q1#15": kp(8, 1),
    "y2002q4": kp(5, 1), "y2002q8": kp(8, 1),
    "y2003q1#4": kp(6, 1), "y2003q4": kp(3, 3), "y2003q7": kp(6, 3), "y2003q10": kp(9, 4),
    "y2004q1": kp(4, 2), "y2004q4": kp(2, 1), "y2004q7": kp(8, 1),
    "y2005q1#2": kp(6, 3), "y2005q1#3": kp(6, 3), "y2005q1#4": kp(6, 3),
    "y2005q2": kp(6, 3), "y2005q6": kp(9, 5),
    "y2006q1": kp(3, 2), "y2006q2": kp(5, 4), "y2006q4": kp(5, 1),
    "y2006q7": kp(6, 3), "y2006q8": kp(9, 2),
    "y2007q1#3": kp(3, 3), "y2007q1#6": kp(5, 1), "y2007q1#8": kp(6, 1),
    "y2007q1#11": kp(2, 1), "y2007q1#15": kp(6, 3),
    "y2008q1#5": kp(5, 5), "y2008q1#22": kp(5, 1), "y2008q1#24": kp(6, 3),
    "y2008q1#30": kp(9, 7), "y2008q2#5": kp(5, 1), "y2008q6": kp(8, 1),
    "y2009q1#1": kp(1, 1), "y2009q1#11": kp(5, 1), "y2009q1#12": kp(6, 2),
    "y2009q1#23": kp(9, 7), "y2009q2#4": kp(12, 1), "y2009q2#7": kp(6, 2),
    "y2009q3#1": kp(6, 3), "y2009q4": kp(3, 4),
    "y2010q1#3": kp(9, 2), "y2010q1#5": kp(7, 1), "y2010q1#6": kp(6, 3),
    "y2010q1#11": kp(4, 1), "y2010q1#16": kp(1, 1), "y2010q1#24": kp(5, 1),
    "y2010q1#26": kp(5, 1), "y2010q1#27": kp(9, 4),
    "y2010q2#5": kp(1, 1), "y2010q2#6": kp(6, 2), "y2010q2#9": kp(11, 3),
    "y2010q2#10": kp(4, 1),
    "y2010q3#1": kp(1, 1), "y2010q3#3": kp(6, 2), "y2010q3#4": kp(5, 1), "y2010q7": kp(8, 1),
    "y2011q1#1": kp(9, 2), "y2011q1#2": kp(1, 2), "y2011q1#20": kp(7, 1),
    "y2011q1#23": kp(9, 7), "y2011q1#26": kp(4, 1),
    "y2011q2#6": kp(6, 6), "y2011q3#1": kp(4, 4), "y2011q3#2": kp(5, 1),
    "y2011q4": kp(5, 1), "y2011q8": kp(10, 2),
    "y2012q1#2": kp(6, 3), "y2012q1#5": kp(3, 3), "y2012q1#20": kp(6, 1),
    "y2012q1#25": kp(9, 7), "y2012q1#28": kp(7, 5), "y2012q1#30": kp(4, 2),
    "y2012q2#4": kp(9, 5), "y2012q2#5": kp(9, 5), "y2012q2#7": kp(1, 1),
    "y2012q3#1": kp(4, 2), "y2012q3#2": kp(6, 3), "y2012q7": kp(10, 2),
    "y2013q1#2": kp(3, 3), "y2013q1#3": kp(3, 3), "y2013q1#4": kp(6, 2),
    "y2013q1#5": kp(7, 1), "y2013q1#7": kp(5, 2), "y2013q1#16": kp(1, 2),
    "y2013q1#20": kp(5, 1), "y2013q1#22": kp(6, 3), "y2013q1#26": kp(4, 1),
    "y2013q1#30": kp(4, 2),
    "y2013q2#2": kp(1, 1), "y2013q2#4": kp(5, 1), "y2013q2#6": kp(4, 2),
    "y2013q2#8": kp(4, 2), "y2013q2#9": kp(7, 6), "y2013q2#10": kp(7, 1),
    "y2013q3#1": kp(7, 7), "y2013q3#4": kp(10, 1), "y2013q4": kp(5, 3),
    "y2014q1#2": kp(4, 1), "y2014q1#5": kp(8, 1), "y2014q1#6": kp(7, 5),
    "y2014q2": kp(6, 2), "y2014q3#3": kp(7, 4), "y2014q5": kp(5, 3),
    "y2014q9": kp(9, 6), "y2014q10": kp(8, 1), "y2014q11": kp(10, 2),
    "y2015q1#2": kp(3, 1), "y2015q1#6": kp(9, 5), "y2015q3#1": kp(4, 3),
    "y2015q7": kp(6, 3), "y2015q8": kp(8, 1),
    "y2016q1#5": kp(3, 1), "y2016q1#9": kp(3, 3), "y2016q1#14": kp(5, 5),
    "y2016q1#23": kp(9, 7), "y2016q8": kp(7, 6), "y2016q9": kp(8, 1),
    "y2017q1": kp(4, 3), "y2017q3#1": kp(1, 1), "y2017q3#5": kp(10, 2),
    "y2017q8": kp(7, 5), "y2017q9": kp(8, 1),
    "y2018q1": kp(1, 1), "y2018q2#1": kp(1, 2), "y2018q3#1": kp(2, 1),
    "y2018q3#2": kp(5, 1), "y2018q6": kp(5, 1), "y2018q8": kp(8, 2), "y2018q9": kp(8, 1),
    "y2019q1": kp(1, 1), "y2019q2#2": kp(5, 4), "y2019q2#3": kp(5, 4),
    "y2019q2#4": kp(5, 4), "y2019q3#4": kp(5, 3), "y2019q6": kp(6, 1),
    "y2019q9": kp(8, 1), "y2019q10": kp(10, 2),
    "y2020q2#2": kp(9, 3), "y2020q3#1": kp(4, 2), "y2020q3#2": kp(7, 1),
    "y2020q3#3": kp(6, 4), "y2020q3#4": kp(5, 2), "y2020q3#5": kp(7, 8),
    "y2020q5": kp(4, 3), "y2020q6": kp(6, 6), "y2020q7": kp(7, 2),
    "y2020q10": kp(9, 5), "y2020q11": kp(10, 3),
    "y2021q2#2": kp(9, 2), "y2021q3#1": kp(1, 3), "y2021q3#2": kp(1, 1),
    "y2021q3#3": kp(5, 5), "y2021q3#4": kp(9, 2), "y2021q5": kp(6, 3),
    "y2021q6": kp(7, 1),
    "y2022q2#3": kp(10, 1), "y2022q3#1": kp(1, 3), "y2022q3#2": kp(1, 1),
    "y2022q3#3": kp(4, 1), "y2022q3#4": kp(7, 7),
    "y2022q5": kp(5, 1), "y2022q6": kp(6, 3), "y2022q9": kp(10, 3),
    "y2023q1#6": kp(9, 7), "y2023q2#2": kp(9, 7), "y2023q2#3": kp(11, 2),
    "y2023q2#4": kp(4, 3), "y2023q2#5": kp(7, 8),
    "y2023q10": kp(9, 3), "y2024q1#11": kp(6, 4), "y2024q2#6": kp(9, 3),
    "y2024q5": kp(5, 3), "y2024q6": kp(6, 3),
    "y2025q1#12": kp(9, 7), "y2025q2#1": kp(7, 8), "y2025q3#5": kp(4, 1),
    "y2025q5": kp(5, 1), "y2025q8": kp(9, 3), "y2025q9": kp(10, 2),
    "y2008q1#1": kp(1, 1),
}

TOPIC_RE = re.compile(r"【知识点】([^】]+)")
SAME_UP = re.compile(r"^\s*(同上|同前|同上题|同前题|同)\s*$")

def first_topic(*texts):
    for t in texts:
        if not t:
            continue
        m = TOPIC_RE.search(t)
        if m:
            v = m.group(1).strip()
            if not SAME_UP.match(v):
                return v
    return ""

def rule_hit(text):
    if not text:
        return None
    for pat, ch, k in RULES:
        if re.search(pat, text):
            return [ch, k, pat]
    return None

def items_of(q):
    """zhenti801.html itemsOf() 的 python 镜像——sid 方案必须一致。"""
    subs = q.get("subs")
    if subs and len(subs) >= 2:
        return [{"sid": f"{q['id']}#{s['n']}", "label": s.get("t") or "", "stem": s.get("stem") or "",
                 "key": s.get("key") or "", "sub": True} for s in subs]
    return [{"sid": q["id"], "label": "整题", "stem": "", "key": q.get("key") or "", "sub": False}]

def main():
    d = json.load(open(REPO + r"\data\zhenti801.json", encoding="utf-8"))
    out, review, unmatched = {}, [], []
    rulecnt = collections.Counter()
    for y in d["years"]:
        for q in y["qs"]:
            bt = first_topic(q.get("stem"), q.get("key"))
            btext = (q.get("no") or "") + "\n" + (q.get("stem") or "")
            zt = None
            m = re.match(r"^y(\d{4})q(\d+)$", q["id"])
            if m:
                zt = ZT_MAP.get(m.group(1), {}).get(int(m.group(2)))
            for it in items_of(q):
                sid = it["sid"]
                if sid in OVERRIDES:
                    res = [*OVERRIDES[sid], "OVERRIDE"]
                else:
                    st = first_topic(it["key"], it["stem"]) if it["sub"] else bt
                    hit = rule_hit(st)
                    if hit:
                        res = [hit[0], hit[1], "规则:" + hit[2]]
                    elif zt:
                        r2 = ZT_CH[zt](btext)
                        res = [r2[0], r2[1], "题型兜底"]
                    else:
                        hit3 = rule_hit(btext + "\n" + it["key"][:400])
                        if hit3:
                            res = [hit3[0], hit3[1], "全文规则:" + hit3[2]]
                        else:
                            res = None
                if res is None:
                    unmatched.append(sid)
                    continue
                out[sid] = [res[0], res[1]]
                rulecnt[res[2].split(":")[0] if ":" not in res[2] else res[2].split(":")[0]] += 1
                topic = (first_topic(it["key"], it["stem"]) or bt or "")[:30]
                review.append(f"{sid} | {res[0][:2]}·{res[1][:14]} | {res[2][:14]} | {topic}")
    print("落位", len(out), "未落位", len(unmatched), unmatched[:20])
    print("方式统计:", dict(rulecnt))
    open(REPO + r"\tools\_z801_kp_review.txt", "w", encoding="utf-8").write("\n".join(review))
    # 校验考点名合法
    for sid, (ch, k) in out.items():
        assert ch in CHN and k in CHN[ch], f"{sid} → {ch}·{k} 不在树中"
    with open(REPO + r"\data\z801_kp.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=0, sort_keys=False)
    print("z801_kp.json 写入", len(out), "条（评审清单 tools/_z801_kp_review.txt）")

if __name__ == "__main__":
    main()
