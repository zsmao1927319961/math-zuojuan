# -*- coding: utf-8 -*-
"""把 2025/2026 两卷册的 OSS 图链本地化（1:1 保 OSS 子路径 → data/images/yka/，json 改 images/yka/ 相对路径）。
2026 题面图为中文路径（question/2026/数学二/...）：下载时 URL 百分号编码，本地文件名保留中文。幂等。"""
import json, os, sys, urllib.parse, urllib.request

DATA = 'data/mock_errors.json'
HOST = 'https://oss.hzyankean.com/'

with open(DATA, encoding='utf-8') as f:
    d = json.load(f)

targets = [e for e in d['exams'] if e['paper']['name'] in ('2025数二真题错题', '2026数二真题错题')]
if len(targets) != 2:
    print('找不到两卷册，退出')
    sys.exit(1)

downloaded, reused, failures = 0, 0, []
for e in targets:
    for er in e['errors']:
        urls = [er['qimg']] + list(er['anaimgs'])
        rels = []
        for u in urls:
            if not u.startswith(HOST):
                rels.append(u)
                continue
            rel = 'images/yka/' + u[len(HOST):]
            path = os.path.join('data', rel)
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                try:
                    quoted = urllib.parse.quote(u, safe=':/')
                    req = urllib.request.Request(quoted, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=30) as resp, open(path, 'wb') as f:
                        f.write(resp.read())
                    downloaded += 1
                except Exception as ex:
                    failures.append((u, str(ex)[:60]))
                    continue
            else:
                reused += 1
            rels.append(rel)
        er['qimg'] = rels[0]
        er['anaimgs'] = rels[1:]

if failures:
    print('下载失败:', failures)
    sys.exit(1)

for e in targets:
    for er in e['errors']:
        for p in [er['qimg']]+ list(er['anaimgs']):
            assert p.startswith('images/yka/'), p
            fp = os.path.join('data', p)
            assert os.path.exists(fp) and os.path.getsize(fp) > 0, fp

with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print(f'OK: 新下载 {downloaded}, 沿用 {reused}, 失败 0；两卷册全部本地化')
