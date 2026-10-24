# -*- coding: utf-8 -*-
"""
作文模板 v5 成品化 (2026-10-24, 用户纠正: 要一套/两套能直接用的模板, 不是背例子库):
- 批1-5 不动 (苦瓜第一段×4 + 双图表总起, 打卡保留)
- v4 的批6-17 句型库坍缩为成品:
  批6 = ★第二段成品四句(动/静通用): 过渡+经济原因+意识原因+虚拟语气警醒
  批7 = ★动态图第三段两句: 趋势持续+共同努力倒装
  批8 = ★静态图第三段三句: 总结+措施(政府/个人媒体)+畅想
  批9 = 备选升级句库(眼熟即可, 不进 recite_order)
- 两套成品: 动态版=批3-4+6+7 / 静态版=批1-2+6+8 / 双图表=批5+6+7或8
- plan.version 保持 3 (zuowen.html 硬校验)
幂等守卫: 只接受 v4(17批) 输入, 重复运行安全失败。
"""
import io, json

PATH = 'data/sentences.json'
d = json.load(io.open(PATH, encoding='utf-8'))
old = {day['day']: day for day in d['days']}
assert set(old) == set(range(1, 18)), 'v4 应为17批, 实际: %s' % sorted(old)

def sent(en, zh, meta=None):
    s = {'en': en, 'zh': zh}
    if meta:
        s['meta'] = meta
    return s

new_days = [json.loads(json.dumps(old[n])) for n in (1, 2, 3, 4, 5)]
new_days[4]['tag'] = '双图表总起+万能应急(第一段延伸)'

ASPECTS = '某方面备选(六大方面高频):personal growth 个人成长 / quality of life 生活质量 / physical and mental health 身心健康 / social progress 社会进步 / effective communication 有效沟通 / family bonding 家庭纽带 / expand one\'s horizons 开拓眼界'

# ---------- 批6 ★成品·第二段(动/静通用) ----------
new_days.append({
    'day': 6, 'tag': '★成品·第二段四句(动/静通用)', 'sents': [
        sent('<span class="tpl">Three key reasons, from my perspective, account for</span> '
             '<span class="blank">this phenomenon(静态图可换 this situation)</span>.',
             '在我看来，三个关键原因可以解释这一现象。',
             '本段=过渡+原因1(经济)+原因2(意识)+原因3(警醒),全篇只换【题目相关词】【某方面】两处空。'),
        sent('<span class="tpl">First and foremost,</span> '
             '<span class="tpl">the rapid economic growth and rising disposable incomes have laid a solid foundation for</span> '
             '<span class="blank">题目相关词</span>.',
             '首先，经济的快速发展和可支配收入的提高为题目相关词奠定了坚实基础。',
             '经济万能原因,适配消费/生活/行业类图表;科技类图表换:The rapid advancement of technology has made 题目相关词 increasingly accessible to the general public.'),
        sent('<span class="tpl">What\'s more, an increasing number of people are beginning to realize that</span> '
             '<span class="blank">题目相关词</span> <span class="tpl">plays a crucial role in</span> '
             '<span class="blank">某方面</span>.',
             '更重要的是，越来越多的人开始意识到，题目相关词在某方面起着至关重要的作用。',
             ASPECTS + '。注意谓语单复数:outdoor activities play / the popularity of X plays。'),
        sent('<span class="tpl">Last but not least, if we ignored the importance of</span> '
             '<span class="blank">题目相关词</span>'
             '<span class="tpl">, we would never become a better version of ourselves.</span>',
             '最后，如果我们忽视题目相关词的重要性，我们将永远无法成为更好的自己。',
             '段尾警醒(方案五);社会层面版:If everyone failed to do sth., our society would be confronted with an unpromising and fruitless future.'),
    ]})

# ---------- 批7 ★成品·动态图第三段 ----------
new_days.append({
    'day': 7, 'tag': '★成品·动态图第三段两句', 'sents': [
        sent('<span class="tpl">In conclusion, the phenomenon reflected in the chart is bound to continue, '
             'and it will keep exerting a positive influence on</span> '
             '<span class="blank">某方面</span>.',
             '总之，图表所反映的现象必将持续下去，并将继续给某方面带来积极影响。',
             '趋势持续句,任何动态图通用;负面趋势把 positive 换 negative。'),
        sent('<span class="tpl">Only through the joint efforts of</span> '
             '<span class="blank">主体三方(如 the government, enterprises and the public)</span> '
             '<span class="tpl">can we effectively promote</span> '
             '<span class="blank">主题词的健康发展(按题换)</span>.',
             '只有通过(主体三方)的共同努力，我们才能有效促进主题词的健康发展。',
             'Only倒装收尾;主体按题换:parents and schools / the whole society / the government and the public。'),
    ]})

# ---------- 批8 ★成品·静态图第三段 ----------
new_days.append({
    'day': 8, 'tag': '★成品·静态图第三段三句', 'sents': [
        sent('<span class="tpl">It is not difficult to draw the conclusion that enough attention must be paid to</span> '
             '<span class="blank">题目相关词</span> '
             '<span class="tpl">by ourselves and our community.</span>',
             '不难得出结论，我们个人和整个社会都必须对题目相关词给予足够的重视。',
             '静态总结句;想更具体可换:We should bear in mind that 题目相关词 is of great importance to 某方面。'),
        sent('<span class="tpl">For one thing, it is imperative for the authorities to</span> '
             '<span class="blank">政府动作</span><span class="tpl">. For another, we should spare no pains to</span> '
             '<span class="blank">个人动作</span><span class="tpl">, and new media platforms should appeal to the public to</span> '
             '<span class="blank">呼吁动作</span>.',
             '一方面，当局必须(政府动作)；另一方面，我们应该不遗余力地(个人动作)，新媒体平台也应呼吁公众(呼吁动作)。',
             '动作库:make strict laws / formulate policies / allocate more funds / improve public facilities ｜ raise public awareness of... / develop a habit of... / create more opportunities for sb. to... ｜ care for the elderly / live a healthy life / participate in outdoor activities。两点原因版:For one thing,...For another,...'),
        sent('<span class="tpl">In this way, hopefully, we may embrace a brighter and more promising future.</span>',
             '通过这种方式，希望我们能拥抱一个更光明、更有希望的未来。',
             '万能收尾,不用改任何词。'),
    ]})

# ---------- 批9 备选升级句库(眼熟即可) ----------
LIB = [
    ('<span class="tpl">Not only does</span> <span class="blank">主题词</span> <span class="tpl">improve</span> '
     '<span class="blank">某方面</span><span class="tpl">, but it also enables them to</span> <span class="blank">另一方面</span>.',
     '主题词不仅改善某方面，还使他们能够(另一方面)。', '倒装加分句;主语复数用 do...but they also...'),
    ('<span class="tpl">For instance, my roommate, Kevin, is passionate about</span> <span class="blank">主题相关行为</span>'
     '<span class="tpl">, which helps him cultivate</span> <span class="blank">具体好处</span>. '
     '<span class="tpl">During this period, he earns the respect of our entire class.</span>',
     '例如，我的室友凯文热衷于(主题相关行为)，这帮助他培养了(具体好处)。在此期间，他赢得了全班的尊敬。',
     '个人例证(活动/品质类图表加分,语言丰富);主语可换 my grandfather / my hometown。'),
    ('<span class="tpl">Compared with</span> <span class="blank">对比对象</span>, '
     '<span class="blank">主题词</span> <span class="tpl">can</span> <span class="blank">小方面</span>'
     '<span class="tpl">, so as to</span> <span class="blank">大方面</span>.',
     '与对比对象相比，主题词能够(小方面)，从而(大方面)。', '对比论证;没有对比就创造对比。'),
    ('<span class="blank">主题词</span> <span class="tpl">is the engine that propels personal growth and social progress.</span>',
     '主题词是推动个人成长与社会进步的引擎。', '比喻句;品德→foundation/思维→compass/心态→lighthouse/合作→bridge。写不出来别硬套。'),
    ('<span class="tpl">Never can we give up our efforts to</span> <span class="blank">某事(按题换)</span>.',
     '我们决不能放弃在做某事上的努力。',
     '否定倒装;开头可换 On no account should we / Under no circumstances can we / By no means should we。'),
    ('<span class="tpl">Taking into account all the factors discussed above, we may reasonably conclude that, '
     'with the passage of time and the advancement of society, the number of</span> '
     '<span class="blank">主体(按题换)</span> <span class="tpl">will continue to increase in the coming years.</span>',
     '综合考虑上述所有因素，我们可以合理地得出结论：未来几年(主体)的数量将持续增加。',
     '趋势预测细分版(动态图,减少换 decline);主体按题:people who.../parcels/the ownership of...'),
    ('<span class="tpl">We are faced with the undeniable fact that</span> <span class="blank">题目相关词</span> '
     '<span class="tpl">has become an integral part of our lives.</span>',
     '我们面临着一个不可否认的事实：题目相关词已成为我们生活中不可或缺的一部分。', '总结备选句。'),
]
new_days.append({
    'day': 9, 'tag': '备选升级句库(眼熟即可,不进检测)', 'sents': [sent(en, zh, m) for en, zh, m in LIB]})

# ---------- 校验 ----------
assert len(new_days) == 9
for i, day in enumerate(new_days, 1):
    day['day'] = i
PAIRS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
for new_no, old_no in PAIRS:
    a = [s['en'] for s in new_days[new_no - 1]['sents']]
    b = [s['en'] for s in old[old_no]['sents']]
    assert a == b, '批%d en 被改动!' % new_no

note = ('2026-10-24 v5(用户纠正:要成品模板,不背例子库):批1-5不动(打卡保留);v4批6-17坍缩——'
        '批6=★第二段成品四句(动/静通用:过渡+经济原因+意识原因+虚拟语气警醒),'
        '批7=★动态图第三段两句(趋势持续+Only倒装),批8=★静态图第三段三句(总结+措施+畅想),'
        '批9=备选升级句库(眼熟即可,不进检测)。'
        '两套成品:动态版=批3-4+6+7 / 静态版=批1-2+6+8 / 双图表=批5+6+7或8。'
        'plan recite_order=[5,6,7,8]。tpl蓝字=必背框架;blank红字=考场按题填(汉字占位不背英文)。')

plan = d['plan']
plan.update({
    'recite_order': [5, 6, 7, 8],
    'recite_days': 2,
    'assembly': [
        '默写检测:静态段+动态段+双图表总起(批1-5,不看任何资料),错词抄3遍',
        '默写检测:第二段四句+动态三段+静态三段(批6-8),两版各默一遍',
        '组装作文#1:2026英二·儿童户外活动(静态版:批2+批6+批8),40分钟不查资料',
        '批改昨天作文,错词进本;组装作文#2:2025英二·老人休闲(静态版:同套)',
        '批改#2;组装作文#3:2023英二·居民健康素养(动态版:批3-4+批6+批7)',
        '批改#3;组装作文#4:2019英二·毕业生去向(动态多方向,细节句三数据三动词)',
        '批改#4;升级练:把#3第二段用批9句1/句2换装重写,比较手感',
        '批改续;组装作文#5:2024英二·劳动实践课(静态版)',
        '批改#5;限时彩排:任选一套未写真题,大小作文90分钟连写(对齐考场节奏)',
        '组装期总检:抽2段默写+错词本过一遍',
        '定稿:动态版/静态版各抄一页纸=独有模板,明天起进限时套用',
    ],
    'retention': [
        '保温篇#1:2026英二再写一遍(目标:零错词)',
        '复习日:错词本+一页纸终版过一遍',
        '保温篇#2:2023英二(动态)25分钟',
        '复习日:两套模板各默写一遍(批6-8)',
        '保温篇#3:2026英一(双图表)',
        '复习日:批9备选库过一遍,挑1句升级进模板',
        '保温篇#4:盲题(静态,自选预测话题)',
        '复习日:错词本+静态/动态段默写',
        '保温篇#5:2025英二或2024英二(自选)',
        '复习日:批9句5否定倒装+句6趋势预测各套一句',
        '保温篇#6:盲题(动态)',
        '复习日:第二段四句抽新题套写(只换主题词+某方面)',
        '保温篇#7:2023英一或2020英一(图画应急,低优先)',
        '复习日:错词本终过一遍',
        '保温篇#8:自选一篇,全套闭卷',
        '复习日:只看一页纸+随机抽1批默写',
        '最后两套模板全套大默写,收工',
    ],
    'detect_note': '全套默写检测:①静态段②动态段③双图表④第二段四句⑤动态三段⑥静态三段逐项默写,错词进错词本',
    'buffer_note': '缓冲补漏:优先把没背完的批补完;都背完了就过一遍错词本和批9备选库。',
})
d['note'] = note
d['days'] = new_days

text = json.dumps(d, ensure_ascii=False, indent=1) + '\n'
io.open(PATH, 'w', encoding='utf-8').write(text)

chk = json.load(io.open(PATH, encoding='utf-8'))
print('OK: %d批, recite_order=%s' % (len(chk['days']), chk['plan']['recite_order']))
for day in chk['days']:
    print(' 批%2d: %s (%d句)' % (day['day'], day['tag'], len(day['sents'])))
