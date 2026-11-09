# -*- coding: utf-8 -*-
"""审计用：把全部错题题面拼成带标注的对照表（每张12题）。文本题另存 txt。"""
import json, os, sys, io
from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(R, "data")
OUT = os.path.join(R, "tools", "_audit_sheets")
os.makedirs(OUT, exist_ok=True)

me = json.load(open(os.path.join(D, "mock_errors.json"), encoding="utf-8"))

def short(name):
    reps = [("2027考研数学开学大模考（数学二）", "开学"), ("欧几里得9月模考（数学二）", "欧9"),
            ("欧几里得10月模考（数学二）", "欧10"), ("真题网错题本 · 耐刷王错题", "耐刷"),
            ("张宇八套卷2027 卷一（数学二）", "张8-1"), ("张宇八套卷2027 卷二（数学二）", "张8-2")]
    for a, b in reps:
        if name == a:
            return b
    import re
    m = re.match(r"^(\d{4})数二真题错题$", name)
    if m:
        return m.group(1) + "真题"
    return name[:10]

items = []
for ex in me["exams"]:
    for e in ex["errors"]:
        items.append({"src": short(ex["paper"].get("name", "")), "no": e["no"], "kp": e.get("kp", ""),
                      "ch": e.get("chapter", ""), "q": e.get("q"), "qimg": e.get("qimg")})
for sr in me.get("series", []):
    for v in sr.get("vols", []):
        for e in v.get("errors", []):
            items.append({"src": short(sr.get("name", "")) + "-" + v.get("name", "")[:8], "no": e["no"],
                          "kp": e.get("kp", ""), "ch": e.get("chapter", ""), "q": e.get("q"), "qimg": e.get("qimg")})

texts = [it for it in items if it["q"] and not it["qimg"]]
imgs = [it for it in items if it["qimg"]]
print("items:", len(items), "texts:", len(texts), "imgs:", len(imgs))

# 文本题
with open(os.path.join(OUT, "texts.txt"), "w", encoding="utf-8") as f:
    for k, it in enumerate(texts):
        f.write(f"[T{k:02d}] {it['src']} 题{it['no']} 【{it['kp']}/{it['ch']}】\n{it['q'][:400]}\n\n")

# 图片题拼图
try:
    font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 22)
except Exception:
    font = ImageFont.load_default()

CW, CH, LBL = 460, 380, 34
COLS = 3
PER = 12
sheets = 0
for s in range(0, len(imgs), PER):
    batch = imgs[s:s + PER]
    rows = (len(batch) + COLS - 1) // COLS
    W, H = COLS * CW, rows * (CH + LBL)
    sheet = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(sheet)
    for k, it in enumerate(batch):
        cx, cy = (k % COLS) * CW, (k // COLS) * (CH + LBL)
        dr.rectangle([cx, cy, cx + CW - 2, cy + LBL - 2], fill=(250, 240, 225))
        dr.text((cx + 8, cy + 5), f"[{s+k:03d}] {it['src']}-{it['no']} 【{it['kp']}|{it['ch']}】",
                fill=(140, 60, 20), font=font)
        p = it["qimg"]
        fp = p if os.path.isabs(p) else os.path.join(D, p)
        if os.path.exists(fp):
            im = Image.open(fp).convert("RGB")
            im.thumbnail((CW - 12, CH - 12))
            sheet.paste(im, (cx + 6, cy + LBL))
        else:
            dr.text((cx + 8, cy + LBL + 10), "MISSING: " + p, fill=(200, 0, 0), font=font)
    sheets += 1
    sheet.save(os.path.join(OUT, f"sheet_{sheets:02d}.png"))
print("sheets:", sheets, "->", OUT)
