# -*- coding: utf-8 -*-
# 重建 tk299_dxy.json：以 questions.json 为唯一真源同步内容字段
# 保留：分类树(categories)、category_id/full_path、serial_number、question_type、options、answer 结构
# 同步：stem_md←question_text、explanation_md←solution(缺则answer_text)、reference_answer_md←answer_text、legacy全量
import json

BASE = r'D:/考研数学/组卷网站_static'
qj = json.load(open(BASE + '/data/questions.json', encoding='utf-8'))
Q = {x['id']: x for x in qj if x.get('source') == 'tk299'}
dpath = BASE + '/data/tk299_dxy.json'
dxy = json.load(open(dpath, encoding='utf-8'))

n_sync = 0
missing = []
for q in dxy['questions']:
    src = Q.get(q['question_id'])
    if not src:
        missing.append(q['question_id'])
        continue
    q['stem_md'] = src.get('question_text') or ''
    q['explanation_md'] = (src.get('solution') or '').strip() or (src.get('answer_text') or '')
    if 'answer' in q and isinstance(q['answer'], dict) and 'reference_answer_md' in q['answer']:
        q['answer']['reference_answer_md'] = src.get('answer_text') or ''
    leg = q.get('legacy') or {}
    leg['answer_text'] = src.get('answer_text') or ''
    leg['question_img'] = src.get('question_img') or ''
    leg['answer_img'] = src.get('answer_img') or ''
    leg['kp'] = src.get('kp') or ''
    q['legacy'] = leg
    if src.get('book_page'):
        q['book_page'] = src['book_page']
    if src.get('video_p'):
        q['video_p'] = src['video_p']
    else:
        q.pop('video_p', None)
    n_sync += 1

# 单选题的 reference_answer_md 情况检查（option_ids 型不动）
sc_bad = [q['question_id'] for q in dxy['questions']
          if q['question_type'] == 'single_choice' and (not q.get('options') or not (q.get('answer') or {}).get('option_ids'))]

json.dump(dxy, open(dpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('同步', n_sync, '题 | 未对齐:', missing or '无', '| single_choice结构异常:', sc_bad or '无')
# 抽查
qs = {q['question_id']: q for q in dxy['questions']}
print('61-05 题面:', qs['tk299-61-05']['stem_md'][:60].replace('\n', ' '))
print('61-05 解析:', qs['tk299-61-05']['explanation_md'][:60])
print('11-01 解析:', qs['tk299-11-01']['explanation_md'][:50])
