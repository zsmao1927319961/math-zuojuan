# -*- coding: utf-8 -*-
"""把 2023/2024 两卷册的 OSS 图链本地化：下载进 data/images/yka/（1:1 保留 OSS 子路径），
mock_errors.json 里 qimg/anaimgs 改为 images/yka/ 相对路径。幂等：已存在的文件跳过下载。
遵循 512fdc6 的本地化约定（OSS 浏览器侧加载劣化会裂图）。"""
import json, os, urllib.request, sys

DATA = 'data/mock_errors.json'
HOST = 'https://oss.hzyankean.com/'

with open(DATA, encoding='utf-8') as f:
    d = json.load(f)

targets = [e for e in d['exams'] if e['paper']['name'] in ('2023数二真题错题', '2024数二真题错题')]
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
                rels.append(u)          # 已是本地路径
                continue
            rel = 'images/yka/' + u[len(HOST):]
            path = os.path.join('data', rel)
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                try:
                    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
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

# 校验：所有本地文件存在且非空，路径格式统一
for e in targets:
    for er in e['errors']:
        for p in [er['qimg']] + er['anaimgs']:
            assert p.startswith('images/yka/'), p
            fp = os.path.join('data', p)
            assert os.path.exists(fp) and os.path.getsize(fp) > 0, fp

with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print(f'OK: 新下载 {downloaded}, 沿用 {reused}, 失败 0；两卷册全部本地化')
