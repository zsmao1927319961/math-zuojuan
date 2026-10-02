# -*- coding: utf-8 -*-
# 题库全量质检：qhzt 113题 + tk299 317题
import json, re, os, collections

BASE = r'D:/考研数学/组卷网站_static'
d = json.load(open(os.path.join(BASE, 'data/questions.json'), encoding='utf-8'))
qhzt = [x for x in d if x.get('source') == 'qhzt']
tk = [x for x in d if x.get('source') == 'tk299']

def latex_issues(t):
    issues = []
    if not t:
        return issues
    if t.count('$') % 2:
        issues.append('$奇数')
    if t.count('\\left') != t.count('\\right'):
        issues.append('\\left\\right不配对')
    for m in re.findall(r'\$([^$]+)\$', t):
        seg = m
        if seg.count('{') != seg.count('}'):
            issues.append('花括号不平衡:' + seg[:40])
    # 残留 OCR 病灶
    if re.search(r'[０-９]', t):
        issues.append('全角数字')
    if re.search(r'\\[a-zA-Z]+\s*[0-9]', t) and '\\pi ' not in t:
        pass
    for pat, name in [(r'\\d?frac\{\}', '\\frac空参'), (r'\^\{\}', '空上标'), (r'_\{\}', '空下标'),
                      (r'\\text\{[^}]*[\u4e00-\u9fff]', '\\text包中文'), (r'[<>]', '裸尖括号')]:
        if re.search(pat, t):
            issues.append(name)
    return issues

print('===== qhzt', len(qhzt), '题 =====')
for f in ['question_text', 'answer_text', 'solution', 'kp', 'kp_sub', 'chapter_name', 'type']:
    miss = [x['id'] for x in qhzt if not (x.get(f) or '').strip()]
    if miss:
        print('字段空', f, miss)
print('四段式检查: 既有answer_text又有solution的', sum(1 for x in qhzt if x.get('answer_text') and x.get('solution')))
figref = [x['id'] for x in qhzt if re.search(r'图|波形|频谱|星座|曲线|框图', x.get('question_text', '')) and not x.get('question_img')]
print('题面提图但无题图:', figref or '无')
noansimg = [x['id'] for x in qhzt if not x.get('answer_img')]
print('无answer_img:', len(noansimg), noansimg[:12])
# answer_img 文件在盘上吗
miss_img = []
for x in qhzt:
    for f in ('question_img', 'answer_img'):
        v = x.get(f)
        if v and not os.path.exists(os.path.join(BASE, v.lstrip('/').replace('/', os.sep))):
            miss_img.append((x['id'], f, v))
print('图片文件缺失:', miss_img or '无')
# LaTeX 质检
bad = 0
for x in qhzt:
    probs = []
    for f in ['question_text', 'answer_text', 'solution']:
        probs += [(f, i) for i in latex_issues(x.get(f) or '')]
    if probs:
        bad += 1
        if bad <= 25:
            print('LaTeX', x['id'], probs[:4])
print('qhzt LaTeX疑似问题题数:', bad)
# 选择题 options
print('type分布 qhzt:', dict(collections.Counter(x.get('type') for x in qhzt)))
noopt = [x['id'] for x in qhzt if x.get('type') in ('单选', '选择') and not x.get('options')]
print('选择题无options:', noopt or '无')
# answer 与 answer_text 关系
print('answer字段样例:', json.dumps({k: qhzt[0].get(k) for k in ('answer', 'answer_text')}, ensure_ascii=False)[:200])

print()
print('===== tk299', len(tk), '题 =====')
print('type分布:', dict(collections.Counter(x.get('type') for x in tk)))
print('status分布:', dict(collections.Counter(x.get('status') for x in tk)))
print('level分布:', dict(collections.Counter(x.get('level') for x in tk)))
print('chapter分布:', dict(collections.Counter(x.get('chapter_name') or x.get('chapter') for x in tk)))
for f in ['question_text', 'answer_text']:
    lens = [len(x.get(f) or '') for x in tk]
    short = [x['id'] for x in tk if len(x.get(f) or '') < 15]
    print(f, '均值', round(sum(lens) / len(lens)), '最短10:', sorted(lens)[:10], '<15字数', len(short), short[:10])
qimg = sum(1 for x in tk if x.get('question_img'))
aimg = sum(1 for x in tk if x.get('answer_img'))
print('带题图', qimg, '带答案图', aimg)
miss_img2 = []
for x in tk:
    for f in ('question_img', 'answer_img'):
        v = x.get(f)
        if v and not os.path.exists(os.path.join(BASE, v.lstrip('/').replace('/', os.sep))):
            miss_img2.append((x['id'], f, v))
print('tk299图片文件缺失:', len(miss_img2), miss_img2[:8])
bad2 = 0
for x in tk:
    probs = []
    for f in ['question_text', 'answer_text', 'solution']:
        probs += [(f, i) for i in latex_issues(x.get(f) or '')]
    if probs:
        bad2 += 1
        if bad2 <= 20:
            print('LaTeX', x['id'], probs[:4])
print('tk299 LaTeX疑似问题题数:', bad2)
# kp / kp_sub
print('kp空:', sum(1 for x in tk if not (x.get('kp') or '').strip()))
print('kp样例:', collections.Counter((x.get('kp') or '')[:12] for x in tk).most_common(8))
