# -*- coding: utf-8 -*-
"""给 mock_errors.json 的 2009-2026 数二真题错题批量回填 B 站视频讲解链接。
来源：郭伟老师《数二09-26年考研真题逐题精讲》上 BV1y84y127Cq(2009-2016全+2017前9题) /
下 BV1b8411k7Xt(2018-2026)，每分P一题，分P名=年份-题号。
映射表 tools/_zt_pmap.json 由分P名生成；幂等：重复运行结果一致。
"""
import json, io, sys, re, shutil, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(R, "data", "mock_errors.json")
PMAP = os.path.join(R, "tools", "_zt_pmap.json")

pmap = json.load(open(PMAP, encoding="utf-8"))
raw = open(DATA, encoding="utf-8").read()
me = json.loads(raw)

n_set = 0
n_skip = []
for ex in me["exams"]:
    name = ex["paper"].get("name", "")
    m = re.match(r"^(20\d{2})数二真题错题$", name)
    if not m:
        continue
    year = m.group(1)
    for e in ex["errors"]:
        key = f"{year}-{e['no']}"
        hit = pmap.get(key)
        if not hit:
            n_skip.append(key)
            continue
        e["video"] = f"https://www.bilibili.com/video/{hit['bv']}?p={hit['p']}"
        e["videoName"] = f"郭伟逐题精讲 {year}年第{e['no']}题"
        n_set += 1

shutil.copyfile(DATA, os.path.join(R, "tools", "_bak_mock_errors_20261109.json"))
with_ind = raw.lstrip().startswith("{\n")
out = json.dumps(me, ensure_ascii=False, indent=2) if with_ind else json.dumps(me, ensure_ascii=False, separators=(",", ":"))
open(DATA, "w", encoding="utf-8").write(out)
print(f"video stamped: {n_set} | skipped(no P): {len(n_skip)} -> {n_skip[:12]}...")
print("backup: tools/_bak_mock_errors_20261109.json")
