# -*- coding: utf-8 -*-
"""430题二轮扩展体检 2026-10-08 (G系列, 补audit_430.py未覆盖的检查类)
新增: 答案字母有效性/选项序列/判断题答案/答案vs解析矛盾/多问编号越界/图片存在性/
dxy同步/book_page与video_p范围/全角字符/HTML残留/前缀残渣/近重复/无图引用"如图"/
超长数字残渣/LaTeX花括号配对/元数据空缺/答案区截断"""
import json, re, collections, os, difflib

REPO = r"D:\考研数学\组卷网站_static"
qs = json.load(open(REPO + r"\data\questions.json", encoding="utf-8"))
tx = [q for q in qs if q.get("subject") == "txyl"]
QMAP = {q["id"]: q for q in tx}

try:
    dxy = json.load(open(REPO + r"\data\tk299_dxy.json", encoding="utf-8"))
    DXY_Q = {x["question_id"]: x for x in dxy.get("questions", [])}
except Exception as e:
    DXY_Q = {}
    print("dxy读取失败:", e)

issues = collections.defaultdict(list)
def add(q, kind, detail):
    issues[kind].append((q["id"], detail))

def opt_letters(t):
    return re.findall(r"(?:^|\n|\s)([A-EＡ-Ｅ])[\.、．)）]", t or "")

for q in tx:
    qt, at, sol, t = q.get("question_text") or "", q.get("answer_text") or "", q.get("solution") or "", q.get("type") or ""
    letters = sorted(set(opt_letters(qt)))
    is_choice = ("选择" in t) or len(letters) >= 3

    # G1 选择题答案字母有效性
    if t == "选择":
        m = re.match(r"^[（(]?([A-EA-Ea-e]{1,6})[）).、．]?\s*$", at.strip())
        if not m:
            add(q, "G1_选择题答案格式异常", f"answer={at.strip()[:40]!r}")
        else:
            ls = m.group(1).upper()
            if ls != ''.join(sorted(set(ls))) and len(set(ls)) != len(ls):
                add(q, "G1b_答案字母重复", ls)
            if any(c in "Ee" for c in ls):
                add(q, "G1c_答案含E", ls)
    # G2 选项字母序列
    if letters:
        expect = [chr(ord('A') + i) for i in range(len(letters))]
        if letters != expect:
            add(q, "G2_选项字母序列异常", f"出现{letters}")
    # G3 判断题答案
    if t == "判断":
        a = at.strip()
        if not re.match(r"^(正确|错误|对|错|√|×|✓)$", a):
            add(q, "G3_判断题答案异常", repr(a[:30]))
    # G4 答案字母 vs 解析结论
    if t == "选择" and sol:
        concl = re.findall(r"(?:故选|故应选|答案为|答案应选|正确答案[是为应]|所以选|应选)\s*[（(]?([A-EA-E])[）)]?", sol)
        if concl:
            m = re.match(r"^[（(]?([A-EA-Ea-e]{1,6})[）).、．]?\s*$", at.strip())
            data_ls = set(m.group(1).upper()) if m else set()
            for c in concl:
                if data_ls and c not in data_ls:
                    add(q, "G4_答案与解析结论矛盾", f"答案={at.strip()!r} 解析结论={c}")
                    break
    # G5 多问编号: 答案最大问号 > 题面最大问号
    qn = [int(x) for x in re.findall(r"[（(]([1-9１-９])[)）]", qt) if x.isdigit()]
    an = [int(x) for x in re.findall(r"[（(]([1-9１-９])[)）]", at) if x.isdigit()]
    if qn and an and max(an) > max(qn):
        add(q, "G5_答案问数超题面", f"题面到{max(qn)}问 答案到{max(an)}问")
    # G6 图片存在性
    for f in ("question_img", "answer_img"):
        p = q.get(f)
        if p and not os.path.exists(os.path.join(REPO, "data", p)):
            add(q, "G6_图缺失", f"{f}={p}")
    # G8 book_page 范围(支持"3~6"范围串, 取首数)
    bp = q.get("book_page")
    if bp is not None:
        bpn = int(re.match(r"\d+", str(bp)).group())
        rng = (150, 325) if q["source"] == "tk299" else (1, 120)
        if not (rng[0] <= bpn <= rng[1]):
            add(q, "G8_页码越界", f"book_page={bp} 期望{rng}")
    # G9 video_p 范围
    vp = q.get("video_p")
    if vp is not None and not (1 <= int(vp) <= 115):
        add(q, "G9_视频P越界", f"video_p={vp}")
    # G10 全角数字/字母
    fw = re.findall(r"[０-９Ａ-Ｚａ-ｚ]+", qt + at)
    if fw:
        add(q, "G10_全角数字字母", f"{fw[:4]}")
    # G11 HTML残留
    for field, txt in (("题面", qt), ("答案", at), ("解析", sol)):
        if re.search(r"<(p|br|div|span|b|i|sub|sup)\b|&nbsp;|&lt;|&gt;|&amp;", txt):
            add(q, "G11_HTML残留", f"{field}: {re.findall(r'.{0,15}(?:<\\w+[^>]*>|&\\w+;).{0,10}', txt)[:2]}")
            break
    # G12 前缀残渣
    for field, txt in (("答案", at), ("解析", sol)):
        s = txt.strip()
        if re.match(r"^(【答案】|【解析】|答案[:：]|解析[:：]|解答[:：])", s):
            add(q, "G12_前缀残渣", f"{field}: {s[:20]!r}")
            break
    # G14 引用图但无题图
    if re.search(r"如图|下图|上图|图中", qt) and not q.get("question_img"):
        add(q, "G14_提图无题图", qt[:50])
    # G15 超长数字(QQ/电话残渣): 8位以上数字
    for field, txt in (("题面", qt), ("答案", at), ("解析", sol)):
        for m in re.findall(r"\d{8,}", txt):
            add(q, "G15_超长数字", f"{field}: {m}")
    # G16 LaTeX花括号配对(按字段)
    for field, txt in (("题面", qt), ("答案", at), ("解析", sol)):
        if txt.count("{") != txt.count("}"):
            add(q, "G16_花括号不配对", f"{field}: {{={txt.count('{')} }}={txt.count('}')}")
    # G19 答案/解析截断尾
    for field, txt in (("答案", at), ("解析", sol)):
        s = txt.rstrip()
        if s and s[-1] in "，、；：（(＋+=\\为则":
            add(q, "G19_答案区异常结尾", f"{field}: …{s[-22:]}")
    # G18 元数据
    if not (q.get("kp") or "").strip():
        add(q, "G18_kp为空", "")

# G7 dxy 同步一致性(同步链字段: book_page/video_p)
for qid, dq in DXY_Q.items():
    q = QMAP.get(qid)
    if not q:
        continue
    for f in ("book_page", "video_p"):
        dv, qv = dq.get(f), q.get(f)
        if (dv or None) != (qv or None):
            add(q, "G7_dxy不同步", f"{f}: 库={str(qv)[:30]!r} dxy={str(dv)[:30]!r}")
dxy_only = set(DXY_Q) - set(QMAP)
if dxy_only:
    print("dxy多余id:", sorted(dxy_only)[:10])
missing_in_dxy = [i for i in QMAP if i.startswith('tk299') and i not in DXY_Q]
if missing_in_dxy:
    print("tk299缺dxy条目:", missing_in_dxy[:10])

# G13 近重复题面(全等)
seen = collections.defaultdict(list)
for q in tx:
    key = re.sub(r"\s+", "", q.get("question_text") or "")
    if key:
        seen[key].append(q["id"])
for k, ids in seen.items():
    if len(ids) > 1:
        issues["G13_题面全重复"].append((ids[0], f"与{ids[1:]}相同"))

print(f"txyl: {len(tx)}  (tk299 {sum(1 for q in tx if q['source']=='tk299')}, qhzt {sum(1 for q in tx if q['source']=='qhzt')})")
print(f"dxy条目: {len(DXY_Q)}")
print("\n===== G系列汇总 =====")
for k in sorted(issues):
    print(f"\n## {k} ({len(issues[k])})")
    for qid, d in issues[k][:20]:
        print(f"  {qid}: {d}")
    if len(issues[k]) > 20:
        print(f"  ...共{len(issues[k])}")
