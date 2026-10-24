# -*- coding: utf-8 -*-
# 2026-10-24 补刷卷⑥⑦ PDF 生成(用户裁定: 补刷卷做成PDF放桌面, 不入站; 做完报错题号后再录错题本):
# 题源=研可岸耐刷王同型题(选题过程见 tools/add_2019_2020_20261024.py 提交记录), 题面/解析图
# 已下载在 %TEMP%/ky_imgs。每卷结构: 封面 → 逐题题面(带题号+耐刷王节点+对应真题题号) →
# 分隔页(答案与解析·做完再看) → 逐题解析。输出到桌面两份PDF。
from PIL import Image, ImageDraw, ImageFont
import os

IMGDIR = os.path.join(os.environ["LOCALAPPDATA"], "Temp", "ky_imgs")
DESKTOP = os.path.join(os.environ["USERPROFILE"], "Desktop")
F_BOLD = os.path.join("C:", os.sep, "Windows", "Fonts", "msyhbd.ttc")
F_REG = os.path.join("C:", os.sep, "Windows", "Fonts", "msyh.ttc")

W = 1500                 # 页宽
HEADER_H = 130           # 题头带高
COVER_W, COVER_H = 1500, 1000
SCALE_W = 1400           # 图片缩放目标宽

PAPERS = [
    dict(out="补刷卷⑥·2019数二错题同型.pdf", year=2019, wrong="6 / 18 / 19 / 21 / 22",
         items=[(1, "曲率与曲率圆", "2019年第6题", "6-1_8850"),
                (2, "二重积分的计算", "2019年第18题", "6-2_10045"),
                (3, "求平面图形的面积", "2019年第19题", "6-3_9481"),
                (4, "单中值问题", "2019年第21题", "6-4_8937"),
                (5, "向量组的秩与极大无关组", "2019年第22题", "6-5_7304")]),
    dict(out="补刷卷⑦·2020数二错题同型.pdf", year=2020, wrong="5 / 12 / 16 / 20 / 21 / 22",
         items=[(1, "偏导数与全微分计算", "2020年第5题", "7-1_9679"),
                (2, "抽水做功", "2020年第12题", "7-2_10505"),
                (3, "变限积分函数", "2020年第16题", "7-3_9341"),
                (4, "单中值问题", "2020年第20题", "7-4_8946"),
                (5, "微分方程的几何应用", "2020年第21题", "7-5_10345"),
                (6, "化二次型为标准形", "2020年第22题", "7-6_7673")]),
]

f_title = ImageFont.truetype(F_BOLD, 64)
f_sub = ImageFont.truetype(F_REG, 36)
f_head = ImageFont.truetype(F_BOLD, 44)
f_head2 = ImageFont.truetype(F_REG, 34)
f_big = ImageFont.truetype(F_BOLD, 52)

def load_img(name):
    p = os.path.join(IMGDIR, name)
    if not os.path.exists(p) or os.path.getsize(p) < 2000:
        raise SystemExit("图片缺失或损坏: " + p)
    return Image.open(p).convert("RGB")

def page_with_image(header1, header2, img):
    """一页: 顶部题头带 + 图片(等比缩放至 SCALE_W)"""
    if img.width > SCALE_W:
        nh = round(img.height * SCALE_W / img.width)
        img = img.resize((SCALE_W, nh), Image.LANCZOS)
    margin = (W - img.width) // 2
    H = HEADER_H + img.height + 60
    page = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(page)
    d.rectangle([0, 0, W, HEADER_H - 20], fill=(24, 40, 72))
    d.text((50, 18), header1, font=f_head, fill="white")
    d.text((50, 72), header2, font=f_head2, fill=(200, 210, 230))
    page.paste(img, (margin, HEADER_H))
    return page

def text_page(lines, big=False):
    page = Image.new("RGB", (COVER_W, COVER_H), "white")
    d = ImageDraw.Draw(page)
    d.rectangle([0, 0, COVER_W, 14], fill=(24, 40, 72))
    y = 90
    for text, font, gap in lines:
        d.text((80, y), text, font=font, fill=(25, 30, 40))
        y += gap
    return page

for paper in PAPERS:
    pages = []
    # 封面
    pages.append(text_page([
        ("补刷卷%s" % ("⑥" if paper["year"] == 2019 else "⑦"), f_title, 130),
        ("· %d 数二错题同型 ·" % paper["year"], f_sub, 90),
        ("对应 %d 年数二真题错题: 第 %s 题" % (paper["year"], paper["wrong"]), f_sub, 70),
        ("共 %d 题 · 题源: 研可岸耐刷王(同考点节点选型)" % len(paper["items"]), f_sub, 70),
        ("生成日期: 2026-10-24", f_sub, 70),
        ("", f_sub, 40),
        ("用法: 打印或在屏作答, 全部做完再看答案区;", f_sub, 60),
        ("之后把做错的题号发我, 录入组题网错题本。", f_sub, 60),
    ]))
    # 题目区
    for no, node, src, stem in paper["items"]:
        img = load_img(stem + "_q.png")
        pages.append(page_with_image("第 %d 题" % no,
                                     "耐刷王·%s ｜ 对应%s ｜ 作答区见下" % (node, src), img))
    # 分隔页
    pages.append(text_page([
        ("", f_big, 60),
        ("── 答案与解析 ──", f_big, 120),
        ("做完再看!", f_sub, 80),
    ]))
    # 解析区
    for no, node, src, stem in paper["items"]:
        img = load_img(stem + "_a.png")
        pages.append(page_with_image("第 %d 题 · 解析" % no, "耐刷王·%s ｜ 对应%s" % (node, src), img))
    out = os.path.join(DESKTOP, paper["out"])
    pages[0].save(out, save_all=True, append_images=pages[1:], resolution=150)
    print("生成:", out, "共%d页" % len(pages), "%.1fMB" % (os.path.getsize(out) / 1048576))
print("done")
