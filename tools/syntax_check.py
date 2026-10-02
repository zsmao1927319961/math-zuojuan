# -*- coding: utf-8 -*-
# 语法校验：独立 JS 直接 node --check；HTML 内联 script 逐块提取 node --check
import re, subprocess, sys, tempfile, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files_js = ['app.js', 'beisheng/app.js', 'sw.js']
files_html = ['index.html', 'math.html', 'zy.html', 'lianxi.html', 'ditu.html', 'dxy.html', 'beifen.html', 'beisheng/index.html']

def check(src, tag):
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(src)
        p = f.name
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True, shell=(os.name == 'nt'))
    os.unlink(p)
    ok = r.returncode == 0
    print(('PASS ' if ok else 'FAIL ') + tag)
    if not ok:
        print(r.stderr[:800])
    return ok

allok = True
for f in files_js:
    p = os.path.join(BASE, f.replace('/', os.sep))
    allok &= check(open(p, encoding='utf-8').read(), f)

html_re = re.compile(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', re.I)
for f in files_html:
    p = os.path.join(BASE, f.replace('/', os.sep))
    html = open(p, encoding='utf-8').read()
    for i, m in enumerate(html_re.findall(html)):
        if not m.strip():
            continue
        allok &= check(m, f + f' #inline{i+1}')

print('ALL PASS' if allok else 'HAS FAILURES')
sys.exit(0 if allok else 1)
