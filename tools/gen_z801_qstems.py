# -*- coding: utf-8 -*-
"""给 801真题全部小题提取各自题面 → data/z801_qstems.json {sid: stem}。
来源优先级：
  A. 子项 key 里的【题目】段（2022q1/2022q2/2023q1/2023q3 等自带）
  B. 块题干完整时逐行拆（2016-2025 填空/选词/判断：行号（N）区间或 1:1 行）
  C. txbs_data.js 背诵卡题干（2007-2015 选择：按答案选项文本对账匹配；判断：数量相等时按位对齐）
落位失败的保持无题面（前端维持紧凑行）。输出覆盖报告供人工过目。"""
import json, re, io, sys, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = r"D:\考研数学\组卷网站_static"

def norm_ans(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    s = s.replace("**", "").replace("⚠", "").strip()
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"[（(].*?[)）]", "", s)  # 去掉括注
    return s[:24]

def main():
    z = json.load(open(REPO + r"\data\zhenti801.json", encoding="utf-8"))
    t = open(REPO + r"\txbs_data.js", encoding="utf-8").read()
    tx = json.loads(t.split("=", 1)[1].strip().rstrip(";").strip())["cards"]

    # txbs 索引：判断+选择 按年份；选择按 norm_ans 文本（仅当该年答案文本无碰撞=content 风格时启用，
    # 字母风格年（2007/2012/2013 等）答案文本全塌缩成单字母，文本匹配必错位，改走题号对齐）
    tx_by_year = collections.defaultdict(lambda: {"选择": [], "判断": []})
    tx_by_ans = collections.defaultdict(dict)
    tx_no = collections.defaultdict(dict)
    tx_style = {}
    seen = collections.defaultdict(collections.Counter)
    for c in tx:
        if c.get("src") != "zt" or not c.get("stem"):
            continue
        tx_by_year[c["year"]][c["type"]].append(c)
        if c["type"] == "选择":
            seen[c["year"]][norm_ans(c.get("ans"))] += 1
    for yr2, cnt in seen.items():
        tx_style[yr2] = "letter" if any(len(k) <= 2 for k in cnt) else "content"
    for c in tx:
        if c.get("src") == "zt" and c.get("stem"):
            if c["type"] == "选择":
                tx_no[c["year"]][c["no"]] = c
                if tx_style[c["year"]] == "content" and seen[c["year"]][norm_ans(c.get("ans"))] == 1:
                    tx_by_ans[c["year"]][norm_ans(c.get("ans"))] = c

    out, report, cov = {}, [], collections.Counter()
    for y in z["years"]:
        for q in y["qs"]:
            subs = q.get("subs")
            if not (subs and len(subs) >= 2):
                continue
            no = q.get("no") or ""
            stem = q.get("stem") or ""
            qid = q["id"]
            block_type = ("判断" if re.search(r"判断", no) else
                          ("选择" if re.search(r"选择", no) else
                           ("填空" if re.search(r"填空", no) else "其他")))
            if block_type == "其他" and yr >= 2007 and re.search(r"【答案】\s*\*?\*?[A-D]", subs[0].get("key") or ""):
                block_type = "选择"  # no 字段缺失题型时，按答案形态归为选择

            got = {}
            # A. 子项 key 自带【题目】
            for s in subs:
                m = re.search(r"【题目】([^【]+)", s.get("key") or "")
                if m:
                    txt = m.group(1).strip()
                    if len(txt) >= 8:
                        got[str(s["n"])] = txt
            # B. 块题干逐行拆（题干无明显截断：行数>=2 或 含（N）序号）；先剥掉引用注记行
            stem_body = "\n".join(ln for ln in stem.split("\n") if not ln.lstrip().startswith(">"))
            lines_ok = False
            if len(stem_body) > 120 or re.search(r"（\d{1,2}）", stem_body):
                lines = [ln for ln in stem_body.split("\n") if re.match(r"^\s*(\d{1,2}[、.．]|\*\*第\d{1,2}题\*\*)", ln)]
                if len(lines) >= 2:
                    numbered = any(re.search(r"（\d{1,2}）", ln) for ln in lines)
                    if numbered:
                        segs = []
                        for ln in lines:
                            nums = [int(x) for x in re.findall(r"[（(](\d{1,2})[)）]", ln)]
                            segs.append({"line": ln.strip(), "lo": min(nums) if nums else None, "hi": max(nums) if nums else None})
                        for s in subs:
                            n = s["n"]
                            hit = [g for g in segs if g["lo"] is not None and g["lo"] <= n <= g["hi"]]
                            if hit and str(s["n"]) not in got:
                                got[str(s["n"])] = hit[0]["line"]
                        lines_ok = True
                    elif len(lines) == len(subs):
                        for s, ln in zip(subs, lines):
                            if str(s["n"]) not in got:
                                got[str(s["n"])] = ln.strip()
                        lines_ok = True
                    elif block_type in ("填空", "其他"):
                        # 无编号空位：按每行空位数顺序分配
                        counts = [max(1, ln.count("（")) for ln in lines]
                        if sum(counts) == len(subs):
                            i = 0
                            for ln, c in zip(lines, counts):
                                for s in subs[i:i + c]:
                                    if str(s["n"]) not in got:
                                        got[str(s["n"])] = ln.strip()
                                i += c
                            lines_ok = True
            # C. txbs 匹配
            yr = y["year"]
            if block_type == "判断":
                tx_n = {c["no"]: c for c in tx_by_year[yr]["判断"]}
                for s in subs:
                    if str(s["n"]) in got:
                        continue
                    c = tx_n.get(s["n"]) or tx_n.get(int(re.sub(r"\D", "", s.get("t") or "0") or 0))
                    if c and c.get("stem"):
                        got[str(s["n"])] = c["stem"]
            elif block_type == "选择" or (block_type in ("填空", "其他") and yr >= 2007 and tx_style.get(yr) == "content"):
                tx_n = {c["no"]: c for c in tx_by_year[yr]["选择"]}
                for s in subs:
                    if str(s["n"]) in got:
                        continue
                    # 主策略：题号对齐（txbs no = 卷面题号）
                    c = tx_n.get(s["n"]) if tx_style.get(yr) == "letter" else None
                    if not c:
                        a = norm_ans(re.search(r"【答案】([^【\n]*)", s.get("key") or "").group(1) if re.search(r"【答案】", s.get("key") or "") else "")
                        c = tx_by_ans[yr].get(a)
                    if c and c.get("stem"):
                        got[str(s["n"])] = c["stem"]

            n_all, n_got = len(subs), len(got)
            cov[(block_type, "got" if n_got == n_all else ("part" if n_got else "none"))] += 1
            for s in subs:
                st = got.get(str(s["n"]))
                if st:
                    out[f"{qid}#{s['n']}"] = st
            if n_got < n_all:
                report.append(f"{qid} {block_type} {n_got}/{n_all} 缺:{[s['n'] for s in subs if str(s['n']) not in got][:8]}")

    # 自检：同一块内两道小题拿到同一题干 = 匹配错位，必须为零
    byblk = collections.defaultdict(dict)
    for sid, st in out.items():
        byblk[sid.rsplit("#", 1)[0]][re.sub(r"\s+", "", st)[:60]] = sid
    dup_err = [(m[k], sid, k[:30]) for blk, m in byblk.items() for k, sid in m.items() if list(m.values()).count(sid) > 1 and list(m.keys()).count(k) > 1]
    dup_report = []
    for blk, m in byblk.items():
        inv = collections.defaultdict(list)
        for k, sid in m.items():
            inv[k].append(sid)
        for k, sids in inv.items():
            if len(sids) > 1:
                dup_report.append(f"{blk}: {sids} → {k[:30]}")
    if dup_report:
        print("!! 同块重复题干:")
        for r in dup_report:
            print("  ", r)
    json.dump(out, open(REPO + r"\data\z801_qstems.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=0, sort_keys=True)
    print("题面覆盖:", len(out), "/", sum(len(q["subs"]) for y in z["years"] for q in y["qs"] if q.get("subs") and len(q["subs"]) >= 2))
    print("块覆盖分布:", dict(cov))
    print("缺题面块:")
    for r in report:
        print(" ", r)
    # 抽样过目
    print("\n抽样:")
    for sid in ["y2008q1#1", "y2008q1#15", "y2013q1#20", "y2008q2#3", "y2016q1#9", "y2024q1#1", "y2020q1#2"]:
        print(" ", sid, "→", (out.get(sid) or "(无)")[:60].replace("\n", " "))

if __name__ == "__main__":
    main()
