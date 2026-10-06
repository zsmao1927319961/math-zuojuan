# -*- coding: utf-8 -*-
# 为 tk299 薄解析题（answer_text<40字 且无 solution）批量生成详细解析 → 写入 solution 字段
# 管线：GLM 文本对话（glm-5.3-flash, thinking low），缓存续跑，并发4
import json, os, re, urllib.request, concurrent.futures, threading

BASE = r'D:/考研数学/组卷网站_static'
CACHE = os.path.join(BASE, 'tools', 'sol_cache')
os.makedirs(CACHE, exist_ok=True)
KEY = os.environ.get('GLM_API_KEY', '')
assert KEY, 'GLM_API_KEY 未设置'

URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
lock = threading.Lock()
results = {'ok': 0, 'fail': []}

def call_glm(q):
    prompt = (
        '你是通信原理考研辅导老师。下面是一道题和它的标准答案。请写出这道题的详细解析，要求：\n'
        '1. 所有数学符号用 KaTeX 行内公式（$...$）书写，禁止 Unicode 上下标，分数用 $\\\\frac{}{}$ 上下结构\n'
        '2. 从题目条件出发分步骤推导，过程必须与给定的标准答案一致（不得更改答案数值）\n'
        '3. 点明所用公式/定理（考点：' + str(q.get('kp') or '') + '）\n'
        '4. 篇幅 100~300 字，直接输出解析正文：不要标题、不要复述题目、不要开场白\n\n'
        '题目：\n' + (q.get('question_text') or '') + '\n\n标准答案：\n' + (q.get('answer_text') or '')
    )
    body = json.dumps({
        'model': 'glm-5.3-flash',
        'messages': [{'role': 'user', 'content': prompt}],
        'thinking': {'type': 'enabled', 'level': 'low'},
        'max_tokens': 2048,
        'temperature': 0.3,
    }).encode('utf-8')
    req = urllib.request.Request(URL, data=body, headers={
        'Content-Type': 'application/json', 'Authorization': 'Bearer ' + KEY})
    for attempt, wait in enumerate([3, 10, 25, 50], 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                j = json.loads(r.read().decode('utf-8'))
            return (j['choices'][0]['message'].get('content') or '').strip()
        except Exception as e:
            if attempt == 4:
                raise
            print('   retry%d (%s) after %ss' % (attempt, str(e)[:50], wait))
            import time
            time.sleep(wait)

def work(q):
    cache_f = os.path.join(CACHE, q['id'] + '.txt')
    if os.path.exists(cache_f):
        with open(cache_f, encoding='utf-8') as f:
            sol = f.read().strip()
        if sol:
            return (q['id'], sol, True)
    try:
        sol = call_glm(q)
        if not sol:
            return (q['id'], '', False)
        with open(cache_f, 'w', encoding='utf-8') as f:
            f.write(sol)
        import time
        time.sleep(2)   # 限流节流
        return (q['id'], sol, True)
    except Exception as e:
        with lock:
            results['fail'].append((q['id'], str(e)[:80]))
        return (q['id'], '', False)

d = json.loads(open(os.path.join(BASE, 'data/questions.json'), encoding='utf-8', newline='').read())
targets = [x for x in d if x.get('source') == 'tk299'
           and len((x.get('answer_text') or '')) < 40
           and not (x.get('solution') or '').strip()]
print('待补详解:', len(targets), '题')

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
    for qid, sol, ok in ex.map(work, targets):
        if ok:
            q = next(x for x in d if x['id'] == qid)
            q['solution'] = sol
            results['ok'] += 1
            print('  ✓', qid, '|', sol[:50].replace('\n', ' '))

out = json.dumps(d, ensure_ascii=False, indent=1).replace('\n', '\r\n')
open(os.path.join(BASE, 'data/questions.json'), 'w', encoding='utf-8', newline='').write(out)
print('完成', results['ok'], '/', len(targets), '| 失败:', results['fail'][:8])
