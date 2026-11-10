# -*- coding: utf-8 -*-
"""
2026-11-10 修复小题卡题面泄露答案：
2009-2011 年选择题在精解合订本里是"答案式排版"，只印题干+正确选项（如 "…（  ）。B）带宽变大"），
导致 txbs_data.js / data/z801_qstems.json / data/zhenti801.json 三处题面把正确答案直接写在卡面上。
修复=把题面第一行末尾的答案尾巴剪掉（答案仍保留在 ans/key/精解 字段里，信息零丢失）。
幂等：重跑时若无泄露则不写盘。
"""
import json, re, io, sys, os, shutil, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BK = r'C:\Users\19273\.zcode\workspace\535ea3dd-0465-49eb-aba2-34497bac154e\_stemfix_backup'
os.makedirs(BK, exist_ok=True)

TX_P = os.path.join(ROOT, 'txbs_data.js')
QS_P = os.path.join(ROOT, 'data', 'z801_qstems.json')
ZT_P = os.path.join(ROOT, 'data', 'zhenti801.json')

def dec(raw):
    """decode a JSON-escaped JS string body (without quotes)"""
    return json.loads('"' + raw + '"')

def enc(s):
    """encode to JSON string body matching file style (raw CJK, escaped backslash)"""
    return json.dumps(s, ensure_ascii=False)[1:-1]

# ---------- 1) collect leaks from txbs_data.js ----------
tx = open(TX_P, encoding='utf-8').read()
# id ... ans ... within one card object; stems captured raw
card_pat = re.compile(r'"id":"(zt(\d{4})-(选择|判断)(\d+))"(.{0,1500}?)"ans":"((?:[^"\\]|\\.)*?)"', re.S)
stem_pat = re.compile(r'"stem":"((?:[^"\\]|\\.)*)"')

fixes = {}   # cid -> dict(year,no,type,dans,newline_dec,raw_old,raw_new)
skips = []
for m in card_pat.finditer(tx):
    cid, year, typ, no, mid, ans_raw = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), m.group(5), m.group(6)
    sm = stem_pat.search(mid)
    if not sm:
        continue
    stem_dec = dec(sm.group(1))
    ans_dec = dec(ans_raw)
    if not ans_dec or len(ans_dec) < 2:
        continue
    nl = stem_dec.find('\n')
    line = stem_dec if nl < 0 else stem_dec[:nl]
    # 泄露判定：题面第一行以答案尾巴结尾，且整题面只含 ≤1 种选项字母（排除2008式全选项题面）
    marks = set(x[0] for x in re.findall(r'[A-D][）)、]', stem_dec))
    ends = line.endswith(ans_dec) or line.rstrip('。. ') == (line[:line.rfind(ans_dec)] if ans_dec in line else '').rstrip('。. ') + ans_dec.rstrip('。. ')
    if not line.rstrip('。. ').endswith(ans_dec.rstrip('。. ')):
        continue
    if len(marks) > 1:
        continue  # 完整选项题面，正常
    idx = line.rfind(ans_dec)
    if idx <= 5:
        skips.append((cid, 'cut point too early', line[:40]))
        continue
    newline = line[:idx].rstrip()
    new_dec = newline if nl < 0 else newline + stem_dec[nl:]
    fixes[cid] = dict(year=year, typ=typ, no=no, dans=ans_dec,
                      raw_old=sm.group(1), raw_new=enc(new_dec),
                      line_before=line[-46:], line_after=newline[-46:])

print('txbs 泄露卡:', len(fixes), '| skip:', len(skips))
for s in skips:
    print('  SKIP', s)
byyear = collections.Counter((f['year']) for f in fixes.values())
print('按年份:', dict(sorted(byyear.items())))

if not fixes:
    print('无泄露，幂等退出，不写盘')
    sys.exit(0)

# ---------- 2) patch txbs_data.js by absolute spans ----------
ops = []
for m in card_pat.finditer(tx):
    cid = m.group(1)
    if cid not in fixes:
        continue
    mid_span = m.span(5)
    seg = tx[m.start(5):m.end(5)]
    sm = stem_pat.search(seg)
    if not sm or sm.group(1) != fixes[cid]['raw_old']:
        skips.append((cid, 'txbs raw mismatch'))
        continue
    ops.append((m.start(5) + sm.start(1), m.start(5) + sm.end(1), fixes[cid]['raw_new'], cid))
ops.sort()
for a, b, _, _ in reversed(ops):  # sanity: non-overlapping
    pass
new_tx_parts, pos = [], 0
covered = 0
for a, b, repl, cid in ops:
    if a < covered:
        skips.append((cid, 'overlap'))
        continue
    new_tx_parts.append(tx[pos:a]); new_tx_parts.append(repl)
    pos = b; covered = b
new_tx_parts.append(tx[pos:])
tx_new = ''.join(new_tx_parts)
print('txbs 替换段:', len(ops))

shutil.copy(TX_P, os.path.join(BK, 'txbs_data.js.bak'))
open(TX_P, 'w', encoding='utf-8', newline='').write(tx_new)

# ---------- 3) patch data/z801_qstems.json ----------
qs = json.load(open(QS_P, encoding='utf-8'))
LETTER_TAIL = re.compile(r'[A-D][）)]')
qs_changed, qs_skip = 0, []
for cid, f in fixes.items():
    if f['typ'] != '选择':
        continue
    key = 'y%dq1#%d' % (f['year'], f['no'])
    if key not in qs:
        qs_skip.append((key, 'absent in qstems'))
        continue
    v = qs[key]
    s = v if isinstance(v, str) else (v.get('stem') or '')
    nl = s.find('\n')
    line = s if nl < 0 else s[:nl]
    if line.rstrip('。. ').endswith(f['dans'].rstrip('。. ')):
        idx = line.rfind(f['dans'])
    else:
        ms = list(LETTER_TAIL.finditer(line))
        if len(ms) == 1 and ms[0].start() > 5:
            idx = ms[0].start()
        else:
            qs_skip.append((key, 'no tail match', line[-40:]))
            continue
    newline = line[:idx].rstrip()
    new_s = newline if nl < 0 else newline + s[nl:]
    qs[key] = new_s if isinstance(v, str) else {**v, 'stem': new_s}
    qs_changed += 1
print('qstems 修改:', qs_changed, '| skip:', len(qs_skip))
for s in qs_skip[:12]:
    print('  QS SKIP', s)
shutil.copy(QS_P, os.path.join(BK, 'z801_qstems.json.bak'))
json.dump(qs, open(QS_P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- 4) patch data/zhenti801.json (root source) ----------
zt = json.load(open(ZT_P, encoding='utf-8'))
zt_changed, zt_skip = 0, []
for y in zt['years']:
    yy = y.get('year')
    if yy not in byyear:
        continue
    for blk in y.get('qs', []):
        for sub in blk.get('subs', []):
            n = sub.get('n')
            cid = 'zt%d-选择%d' % (yy, n) if n is not None else None
            if cid not in fixes:
                continue
            s = sub.get('stem') or ''
            nl = s.find('\n')
            line = s if nl < 0 else s[:nl]
            dans = fixes[cid]['dans']
            if line.rstrip('。. ').endswith(dans.rstrip('。. ')):
                idx = line.rfind(dans)
            else:
                ms = list(LETTER_TAIL.finditer(line))
                if len(ms) == 1 and ms[0].start() > 5:
                    idx = ms[0].start()
                else:
                    zt_skip.append((cid, line[-40:]))
                    continue
            newline = line[:idx].rstrip()
            sub['stem'] = newline if nl < 0 else newline + s[nl:]
            zt_changed += 1
print('zhenti801 修改:', zt_changed, '| skip:', len(zt_skip))
for s in zt_skip[:12]:
    print('  ZT SKIP', s)
shutil.copy(ZT_P, os.path.join(BK, 'zhenti801.json.bak'))
json.dump(zt, open(ZT_P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- 5) post checks ----------
leak2 = 0
for m in card_pat.finditer(tx_new):
    sm = stem_pat.search(m.group(5))
    if not sm:
        continue
    sd = dec(sm.group(1)); ad = dec(m.group(6))
    line = sd.split('\n')[0]
    marks = set(x[0] for x in re.findall(r'[A-D][）)、]', sd))
    if ad and len(ad) >= 2 and len(marks) <= 1 and line.rstrip('。. ').endswith(ad.rstrip('。. ')):
        leak2 += 1
print('复检 txbs 剩余泄露:', leak2)
assert leak2 == 0, 'txbs 仍有泄露'
qs2 = json.load(open(QS_P, encoding='utf-8'))
bad = [k for k, v in qs2.items()
       if isinstance(v, str) and len(re.findall(r'[A-D][）)]', v)) == 1 and re.search(r'[A-D][）)][^（]*$', v)]
print('qstems 单选项残留(宽松):', len(bad))
# txbs_data.js 可解析性校验
body = tx_new[tx_new.index('=') + 1:].rstrip().rstrip(';')
obj = json.loads(body)
print('txbs_data.js JSON 解析 OK, cards:', len(obj['cards']))

print('ALL DONE. 备份在', BK)
