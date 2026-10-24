# -*- coding: utf-8 -*-
"""
作文模板 v4 分段混搭重建 (2026-10-24, 用户拍板):
- 苦瓜只留静态+动态第一段(批1-4, 内容不动 => 打卡保留)
- 苦瓜批5-15(经济二段/尾段/备用段/功能句)按用户决定移除(git历史可找回)
- 原AI归来批16-22 内容原样保留, 重排为 批5/7/8/9/13/15/16 (en不动 => 打卡保留)
- 新增批6/10/11/12/14/17 (出自 AI归来《27考研英语大作文模板》PDF)
- plan: version 保持 3(zuowen.html 硬校验), recite_order/assembly/practice/retention 全部重写
幂等: 重复运行结果一致。
"""
import io, json, sys

PATH = 'data/sentences.json'
src = io.open(PATH, encoding='utf-8').read()
d = json.loads(src)
old_days = {day['day']: day for day in d['days']}
assert set(old_days) == set(range(1, 23)), 'v3 应为22批, 实际: %s' % sorted(old_days)

TPL = '<span class="tpl">'
BLK = '<span class="blank">'
END = '</span>'

def sent(en, zh, meta=None):
    s = {'en': en, 'zh': zh}
    if meta:
        s['meta'] = meta
    return s

def keep(n, tag=None):
    """原批内容原样保留(en/zh/meta 逐字节不动 => 打卡哈希不变), 只允许改 tag。"""
    day = json.loads(json.dumps(old_days[n]))  # deep copy
    if tag:
        day['tag'] = tag
    return day

# ---------- 批1-4 苦瓜第一段: 原样 ----------
new_days = [keep(1), keep(2), keep(3), keep(4)]

# ---------- 批5 = 原16 双图表 (内容不动) ----------
new_days.append(keep(16, tag='双图表总起+万能应急(第一段延伸)'))

# ---------- 批6 新增: 二段·过渡句+连接词 ----------
new_days.append({
    'day': 6, 'tag': '第二段·过渡句+连接词(方案骨架起点)', 'sents': [
        sent('<span class="tpl">Three key reasons, from my perspective, account for</span> '
             '<span class="blank">this phenomenon(按题换:tendency/issue)</span>.',
             '在我看来，三个关键原因可以解释这一现象。',
             '备选过渡句:A variety of reasons can be cited to account for this phenomenon. / '
             'A combination of factors has contributed to the tendency reflected in this chart.(图表专用,点题加分) / '
             'Several factors contribute to this phenomenon.。英语二写2~3点原因。'),
        sent('<span class="tpl">From my perspective, the causes of</span> '
             '<span class="blank">主题词(按题换)</span> '
             '<span class="tpl">can be summarized as three main aspects.</span>',
             '在我看来，主题词的成因可以归结为三个主要方面。'),
        sent('<span class="tpl">To begin with, ... What\'s more, ... Last but not least, ...</span>',
             '首先……；更重要的是……；最后但同样重要的是……。',
             '原因123连接词骨架,任记一组:For one thing, ... For another, ...(两点原因用) / '
             'Firstly, ... Secondly, ... Thirdly / First and foremost, ... Furthermore, ... Last but not least, ...'),
    ]})

# ---------- 批7 = 原17 方案一 (内容不动) ----------
new_days.append(keep(17, tag='第二段·方案一 举例论证·个人路线'))

# ---------- 批8 = 原18 方案三 (内容不动) ----------
new_days.append(keep(18, tag='第二段·方案三 从句+六大方面'))

# ---------- 批9 = 原19 方案五 (内容不动) ----------
new_days.append(keep(19, tag='第二段·方案五 虚拟语气恐吓法'))

# ---------- 批10 新增: 二段·方案四倒装+方案六对比(备选) ----------
new_days.append({
    'day': 10, 'tag': '第二段·方案四倒装+方案六对比(备选·七选五任选)', 'sents': [
        sent('<span class="tpl">Not only does</span> <span class="blank">主题词(动名词/事物,按题换)</span> '
             '<span class="tpl">improve</span> <span class="blank">某方面</span>'
             '<span class="tpl">, but it also enables them to</span> <span class="blank">另一方面</span>.',
             '主题词不仅改善某方面，还使他们能够(另一方面)。',
             '主语复数用do:Not only do outdoor activities improve..., but they also cultivate...。'
             'improve 可换 increase/promote/boost/cultivate;enable 可换 help/allow/encourage/relieve。'),
        sent('<span class="tpl">Compared with</span> <span class="blank">对比对象(没有对比就创造对比)</span>, '
             '<span class="blank">主题词</span> <span class="tpl">can</span> <span class="blank">小方面</span>'
             '<span class="tpl">, so as to</span> <span class="blank">大方面</span>.',
             '与对比对象相比，主题词能够(小方面)，从而(大方面)。',
             'so as to 可换 thereby promoting... / which makes it easier for sb. to...;大方面从批12词组库挑。'),
        sent('<span class="tpl">In contrast to</span> <span class="blank">对比对象</span>, '
             '<span class="tpl">the advantage of</span> <span class="blank">主题词</span> '
             '<span class="tpl">lies in</span> <span class="blank">某方面</span>.',
             '与对比对象相比，主题词的优势在于(某方面)。',
             '七选五:方案一/三/五(批7/8/9)必须,方案四/六/七任选二;主力没背熟先不碰本批。'),
    ]})

# ---------- 批11 新增: 二段·方案七 比喻句 ----------
new_days.append({
    'day': 11, 'tag': '第二段·方案七 比喻句(备选·画龙点睛)', 'sents': [
        sent('<span class="blank">主题词(按题换)</span> '
             '<span class="tpl">is the engine that propels personal growth and social progress.</span>',
             '主题词是推动个人成长与社会进步的引擎。',
             '适配:意志品质/行动实践类→engine;品德修养→foundation;思维认知→compass;心态→lighthouse;人际合作→bridge。'
             '可加插入语拉长:..., needless to say, ...。写不出来别硬套。'),
        sent('<span class="blank">主题词(按题换)</span> <span class="tpl">is the bridge between</span> '
             '<span class="blank">A</span> <span class="tpl">and</span> <span class="blank">B</span>.',
             '主题词是连接A与B之间的桥梁。',
             '例:Outdoor activities are the bridge between children and the natural world. / '
             'Parks and public spaces are the bridge between urban residents and a healthy lifestyle.'),
    ]})

# ---------- 批12 新增: 六大方面·高频词组库 ----------
PHRASES = [
    ('rapid economic growth', '快速经济增长'),
    ('bring convenience to people\'s daily lives', '给人们的日常生活带来便利'),
    ('social harmony', '社会和谐'),
    ('social progress', '社会进步'),
    ('personal growth', '个人成长'),
    ('all-round development', '全面发展'),
    ('physical and mental health', '身心健康'),
    ('quality of life', '生活质量'),
    ('expand one\'s horizons', '开拓眼界'),
    ('relieve the burden on families', '减轻家庭负担'),
    ('family bonding / parent-child interaction', '家庭纽带/亲子互动'),
    ('effective communication', '有效沟通'),
    ('technological innovation', '科技创新'),
    ('harmony between humanity and nature', '人与自然和谐共生'),
]
new_days.append({
    'day': 12, 'tag': '六大方面·高频词组库(方案一/三填空用,眼熟即可)', 'sents': [
        sent(en, zh) for en, zh in PHRASES
    ]})

# ---------- 批13 = 原20 总结全文 (内容不动, 仅修 tag/meta 去苦瓜引用) ----------
b13 = keep(20, tag='第三段·总结全文(方案一从句)')
if not b13['sents'][0].get('meta'):
    b13['sents'][0]['meta'] = '句首可加 All in all / To sum up / In general / Generally speaking / On the whole。'
b13['sents'][1]['meta'] = '第三段=总结(本批)+批15措施+批16畅想 三件拼装;字数不够就总结+畅想两句收尾。'
new_days.append(b13)

# ---------- 批14 新增: 三段·否定倒装+万能应急 ----------
new_days.append({
    'day': 14, 'tag': '第三段·否定倒装+万能应急', 'sents': [
        sent('<span class="tpl">By no means should we give up our efforts to</span> '
             '<span class="blank">某事(按题换)</span>.',
             '我们决不能放弃在做某事上的努力。',
             '组合公式:Never can we / On no account should we / Under no circumstances can we / '
             'By no means should we ✖ give up our efforts to... / underestimate the profound impact of... / '
             'cease our pursuit of... / doubt the importance of...。例:...protect the environment.'),
        sent('<span class="tpl">There is no denying that further attention must be paid to '
             'the scene/phenomenon/situation/tendency mentioned above.</span>',
             '不可否认，对上述场景/现象/趋势必须给予进一步的关注。',
             '万能且无需修改任何内容,应急使用;另一句:Given the above analysis, it is not difficult to '
             'understand why this phenomenon has aroused widespread concern.'),
    ]})

# ---------- 批15 = 原21 具体措施 (内容不动) ----------
new_days.append(keep(21, tag='第三段·具体措施:政府+个人/媒体'))

# ---------- 批16 = 原22 畅想未来 (内容不动) ----------
new_days.append(keep(22, tag='第三段·畅想未来'))

# ---------- 批17 新增: 三段·趋势预测(英二图表应急) ----------
new_days.append({
    'day': 17, 'tag': '第三段·趋势预测(英二图表应急)', 'sents': [
        sent('<span class="tpl">Taking into account all the factors discussed above, we may reasonably '
             'conclude that, with the passage of time and the advancement of society, the number of people who</span> '
             '<span class="blank">做某事(按题换)</span> '
             '<span class="tpl">will continue to increase in the coming years.</span>',
             '综合考虑上述所有因素，我们可以合理地得出结论：随着时代变迁和社会进步，未来几年做某事的人数将持续增加。',
             '动态图用,减少换 decline;深度不及建议措施,仅应急(时间紧/字数不够)。'),
        sent('<span class="tpl">In a word, as society keeps moving forward,</span> '
             '<span class="blank">主题词(按题换)</span> '
             '<span class="tpl">is likely to gain even greater significance in the days to come.</span>',
             '总之，随着社会不断前进，主题词在未来很可能变得更加重要。',
             '静态图用;静态另一版:In conclusion, the phenomenon reflected in the chart is bound to continue, '
             'and it will keep exerting a positive influence on 某方面。'),
    ]})

# ---------- 校验 ----------
assert len(new_days) == 17
for i, day in enumerate(new_days, 1):
    day['day'] = i  # 按新位置重编批号(旧day随拷贝带入,统一覆盖)
# 内容哈希保真: 保留批的 en 逐句与原文件一致
PAIRS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 16), (7, 17), (8, 18), (9, 19), (13, 20), (15, 21), (16, 22)]
for new_no, old_no in PAIRS:
    a = [s['en'] for s in new_days[new_no - 1]['sents']]
    b = [s['en'] for s in old_days[old_no]['sents']]
    assert a == b, '批%d(原批%d) en 内容被改动!' % (new_no, old_no)

note = ('2026-10-24 v4(分段混搭,用户拍板):苦瓜只留静态+动态第一段(批1-4,打卡保留);'
        '苦瓜二段/尾段/备用段/功能句(原批5-15)按决定移除(git历史可找回);'
        '原AI归来批16-22重排为批5/7/8/9/13/15/16(内容未动,打卡保留);'
        '新增批6过渡句/10方案四六/11比喻/12六大方面词组/14否定倒装/17趋势预测(均出自AI归来27版大作文PDF)。'
        '共17批,批1-5已有底子,剩余按plan补背≤2批/天,10/31默写检测不变。'
        'tpl蓝字=必背框架;blank红字=考场按题填(汉字占位不背英文)。')

plan = {
    'version': 3,  # zuowen.html 硬校验 ===3, 不得改
    'start': '2026-10-23',
    'exam': '2026-12-19',
    'total_days': 58,
    'recite_order': [5, 6, 7, 8, 9, 13, 14, 15, 16, 10, 11, 12, 17],
    'recite_quota': 2,
    'recite_days': 7,
    'detect_day': 8,
    'buffer_day': 9,
    'phase_bounds': {'recite': [0, 9], 'asm': [10, 20], 'pra': [21, 38], 'ret': [39, 55]},
    'light_day': 56,
    'assembly': [
        '默写检测:静态段+动态段+双图表总起(批1-5,不看任何资料),错词抄3遍',
        '默写检测:过渡句+方案一举例+方案三从句(批6-8)',
        '默写检测:方案五虚拟语气+总结全文+具体措施+畅想未来(批9+13+15+16)',
        '组装作文#1:2026英二·儿童户外活动(静态图:批2+批6+批7+批8+批13-16),40分钟不查资料',
        '批改昨天作文,错词进本;组装作文#2:2025英二·老人休闲(静态:同骨架,细节句换批1)',
        '批改#2;组装作文#3:2023英二·居民健康素养(动态:批3-4细节句+全套二三段)',
        '批改#3;组装作文#4:2019英二·毕业生去向(动态多方向,批7方案一换主语练对比)',
        '批改#4;备选方案替换练:把昨天第二段用批10(倒装/对比)重写一遍,体会七选五',
        '批改续;组装作文#5:2024英二·劳动实践课(静态,可试批11比喻句)',
        '批改#5;限时彩排:任选一套未写真题,大小作文90分钟连写(对齐考场节奏)',
        '组装期总检:随机抽3段默写+错词本过一遍;常用句型抄成一页纸独有模板,明天起进限时套用',
    ],
    'practice': [
        '限时#1:2026英二·儿童户外活动,25分钟写作+10分钟对照订正',
        '限时#2:2023英二·居民健康素养(动态)',
        '限时#3:2025英二·老人日常休闲(静态)',
        '限时#4:2024英二·劳动实践课(静态)',
        '限时#5:2026英一·养老机器人(双图表,批5总起)',
        '限时#6:2024英一·公园建设(图画+图表,图画半边借思路,重点练图表)',
        '限时#7:2022英二·快递业务量(动态)',
        '限时#8:2019英二·毕业生去向(动态多方向)',
        '限时#9:2020英二·手机阅读(饼图)',
        '二刷:把前8天最不满意的一篇重写,重点消灭错词',
        '限时#10:2021英二真题图表(先自己判断动/静再动笔)',
        '限时#11:2023英一·龙舟与传统文化(单图画,英二考生低优先)',
        '文字作文·大纲样题1(职场坦诚):文字改写+态度句+二三段照常拼',
        '文字作文·大纲样题2(孩子与屏幕):同上套路再来一篇',
        '限时#12:2020英一·习惯(双图画,应急)',
        '盲题演练:自选一个预测话题(静态图),全程闭卷25分钟',
        '盲题演练:自选一个预测话题(动态图)+二三段全模块默写一遍',
        '精通验收:随机抽一年真题,25分钟闭卷成文;结构完整/句式用上模板/150-180词/错词≤3,四项达标=精通达成🎯',
    ],
    'retention': [
        '保温篇#1:2026英二再写一遍(目标:零错词)',
        '复习日:错词本+一页纸终版过一遍',
        '保温篇#2:2023英二(动态)25分钟',
        '复习日:方案一/三/五各默写一段(抽新题套)',
        '保温篇#3:2026英一(双图表)',
        '复习日:六大方面词组库(批12)快速过一遍',
        '保温篇#4:盲题(静态,自选预测话题)',
        '复习日:错词本+静态/动态段默写',
        '保温篇#5:2025英二或2024英二(自选)',
        '复习日:批14否定倒装+批17趋势预测各套一句',
        '保温篇#6:盲题(动态)',
        '复习日:方案四/六/七备选批(10/11)抽背',
        '保温篇#7:2023英一或2020英一(图画应急,低优先)',
        '复习日:错词本终过一遍',
        '保温篇#8:自选一篇,全套闭卷',
        '复习日:只看一页纸+随机抽2批默写',
        '最后全套大默写(静态/动态段+过渡+三方案+三段件),收工',
    ],
    'detect_note': '全套默写检测:①静态段②动态段③双图表④过渡句⑤方案一⑥方案三⑦方案五逐项默写,错词进错词本',
    'buffer_note': '缓冲补漏:优先把没背完的批补完;都背完了就过一遍错词本和批12词组库。',
    'light_note': '轻复盘:只看错词本和一页纸终版,不写新东西,早睡。',
    'exam_note': '今天初试。早上只过一页纸终版;写作文先花3分钟定三段骨架再动笔。稳住,你背了58天。',
}

out = {'note': note, 'days': new_days, 'plan': plan}
text = json.dumps(out, ensure_ascii=False, indent=1) + '\n'
io.open(PATH, 'w', encoding='utf-8').write(text)

# 复读校验
chk = json.load(io.open(PATH, encoding='utf-8'))
print('OK: %d批, plan.version=%s, recite_order=%d项' % (
    len(chk['days']), chk['plan']['version'], len(chk['plan']['recite_order'])))
for day in chk['days']:
    print(' 批%2d: %s (%d句)' % (day['day'], day['tag'], len(day['sents'])))
