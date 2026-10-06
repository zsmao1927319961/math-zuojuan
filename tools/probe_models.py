# -*- coding: utf-8 -*-
# 探测哪些 GLM 模型在当前账户下可用（余额不足时的免费/低价备选）
import json, os, urllib.request, urllib.error

KEY = os.environ.get('GLM_API_KEY', '')
MODELS = ['glm-4.5-flash', 'glm-4-flash-250414', 'glm-4-flash', 'glm-4.5-air', 'glm-4-air', 'glm-5.3-flash']

for m in MODELS:
    body = json.dumps({'model': m, 'messages': [{'role': 'user', 'content': '回复两个字：收到'}], 'max_tokens': 16}).encode('utf-8')
    req = urllib.request.Request('https://open.bigmodel.cn/api/paas/v4/chat/completions', data=body,
                                 headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + KEY})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            j = json.loads(r.read().decode('utf-8'))
            print('OK  ', m, '->', (j['choices'][0]['message'].get('content') or '').strip()[:20])
    except urllib.error.HTTPError as e:
        msg = e.read().decode('utf-8')[:120]
        print('FAIL', m, e.code, msg)
    except Exception as e:
        print('FAIL', m, str(e)[:80])
