# -*- coding: utf-8 -*-
"""背作文模块 v2:
1) 追加批次16-22(本次AI归来+图片书融合新增:双图表总起/方案一/方案三/方案五/第三段总结措施畅想)
2) 新增 plan 段:2026-10-23 → 2026-12-19 共58天的逐日计划(背诵25天含3缓冲→组装12天→限时套用20天→考试日)
原有批次1-15一字不动,句子打卡键为内容哈希,旧进度不受影响。
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\考研数学\组卷网站_static\data\sentences.json'

def tpl(s):
    return f'<span class="tpl">{s}</span>'

def bl(s):
    return f'<span class="blank">{s}</span>'

NEW_BATCHES = [
    {
        "day": 16,
        "tag": "双图表总起+万能应急(AI归来融合)",
        "sents": [
            {
                "zh": "左侧的图展示了左图主题，而右侧的图列出了右图主题。",
                "en": f'{tpl("The chart on the left shows")} {bl("左图主题")}, {tpl("while the chart on the right lists")} {bl("右图主题")}.',
                "meta": "双图表第一段总起句:左右两图的内容分别套第①静态段或②动态段填数据。",
            },
            {
                "zh": "上方图表提供了年份1至年份2间关于题目相关词的信息。",
                "en": f'{tpl("The chart above provides information about")} {bl("题目相关词")} {tpl("from")} {bl("年份1")} {tpl("to")} {bl("年份2")}.',
                "meta": "万能应急句:图表看不懂/时间紧时总起就用它;细节补一句 with the proportions ranging from 最低值 to 最高值。",
            },
        ],
    },
    {
        "day": 17,
        "tag": "第二段·方案一 举例论证·个人路线(AI归来融合)",
        "sents": [
            {
                "zh": "例如，我的室友凯文热衷于参加劳动实践课，这帮助他培养了实践技能和合作精神。",
                "en": f'{tpl("For instance, my roommate, Kevin, is passionate about")} {bl("主题相关行为")}, {tpl("which helps him cultivate")} {bl("带来的好处")}.',
                "meta": "主语可换 my grandfather / my hometown(一个宜居城市);好处从六大方面挑:cultivate practical skills / keep him well informed / improve his sleep quality。",
            },
            {
                "zh": "在此期间，(主语)有了另一个积极结果。",
                "en": f'{tpl("During this period,")} {bl("主语+换角度的积极结果(句)")}。',
                "meta": "结果示例:he earns the respect of our entire class / his parents have noticed his growing curiosity / citizen satisfaction has improved。",
            },
        ],
    },
    {
        "day": 18,
        "tag": "第二段·方案三 从句+六大方面(AI归来融合)",
        "sents": [
            {
                "zh": "此外，越来越多的人开始认识到，题目相关词在某方面起着至关重要的作用。",
                "en": f'{tpl("Furthermore, a rising number of individuals are coming to the realization that")} {bl("题目相关词")} {tpl("plays a crucial role in")} {bl("某方面")}.',
                "meta": "六大方面速查:personal growth 个人成长 / quality of life 生活质量 / physical and mental health 身心健康 / social progress 社会进步 / effective communication 有效沟通 / technological innovation 科技创新",
            },
            {
                "zh": "毫无疑问，题目相关词与某方面有着密不可分的联系。",
                "en": f'{tpl("There is no doubt that")} {bl("题目相关词")} {tpl("is inextricably linked to")} {bl("某方面")}.',
                "meta": "注意谓语单复数:outdoor activities play / the popularity of X plays。",
            },
        ],
    },
    {
        "day": 19,
        "tag": "第二段·方案五 虚拟语气恐吓法(AI归来融合)",
        "sents": [
            {
                "zh": "最后，如果我们忽视题目相关词的重要性，我们将永远无法成为更好的自己。",
                "en": f'{tpl("In the end, if we ignored the importance of")} {bl("题目相关词")}, {tpl("we would never become a better version of ourselves.")}',
                "meta": "个人层面,建议放原因三作段尾警醒。",
            },
            {
                "zh": "如果每个人都没能做某事，我们的社会将面临一个黯淡无望、一无所获的未来。",
                "en": f'{tpl("If everyone failed to")} {bl("do sth.")}, {tpl("our society would be confronted with an unpromising and fruitless future.")}',
                "meta": "社会层面;国家层面版:If we underestimated the importance of 题目相关词, our nation would permanently lag behind in the new era of rapid development.",
            },
        ],
    },
    {
        "day": 20,
        "tag": "第三段·总结全文(AI归来融合,与⑥⑦尾段二选一)",
        "sents": [
            {
                "zh": "不难得出结论，我们个人和整个社会都必须对题目相关词给予足够的重视。",
                "en": f'{tpl("It is not difficult to draw the conclusion that enough attention must be paid to")} {bl("题目相关词")} {tpl("by ourselves and our community.")}',
                "meta": "",
            },
            {
                "zh": "我们应当牢记，题目相关词对我们的个人发展/社会进步至关重要。",
                "en": f'{tpl("We should bear in mind that")} {bl("题目相关词")} {tpl("is of great importance to")} {bl("our personal development / social progress")}.',
                "meta": "想写得具体就用批20+21+22拼第三段;想快就用⑥⑦整段。",
            },
        ],
    },
    {
        "day": 21,
        "tag": "第三段·具体措施:政府+个人媒体(AI归来融合)",
        "sents": [
            {
                "zh": "一方面，当局必须制定严格法规来(确保主题动作)。",
                "en": f'{tpl("For one thing, it is imperative for the authorities to formulate strict regulations to")} {bl("具体动作")}.',
                "meta": "政府动作库:make strict laws 制定法律 / allocate more funds 拨付资金 / improve public facilities 完善公共设施 / launch public initiatives 发起公共倡议",
            },
            {
                "zh": "另一方面，我们应该不遗余力地做(具体动作1)，新媒体平台也应呼吁公众去(具体动作2)。",
                "en": f'{tpl("For another, we should spare no pains to")} {bl("具体动作1")}, {tpl("and new media platforms should appeal to the public to")} {bl("具体动作2")}.',
                "meta": "个人/媒体动作:raise public awareness of... 增强公众意识 / develop a habit of... 养成习惯 / care for the elderly 关爱老人",
            },
        ],
    },
    {
        "day": 22,
        "tag": "第三段·畅想未来(AI归来融合)",
        "sents": [
            {
                "zh": "只有通过政府、企业和公众的共同努力，我们才能有效促进主题词的健康发展。",
                "en": f'{tpl("Only through the joint efforts of the government, enterprises and the public can we effectively promote")} {bl("主题词的健康发展")}.',
                "meta": "倒装句(Only开头主谓倒装);主体按题换:parents and schools / the whole society。",
            },
            {
                "zh": "通过这种方式，希望我们能拥抱一个更光明、更有希望的未来。",
                "en": f'{tpl("In this way, hopefully, we may embrace a brighter and more promising future.")}',
                "meta": "万能收尾,不用改任何词。",
            },
        ],
    },
]

ASSEMBLY = [
    "默写检测:静态第一段(不看任何资料),错词抄3遍",
    "默写检测:动态第一段+双图表总起句",
    "默写检测:经济类第二段+个人成长类第二段",
    "默写检测:正面尾段+负面尾段",
    "功能句替换练:给静态段细节句换2种写法(查段落库里的功能句批)",
    "组装作文#1:2026英二·儿童户外活动(静态:①+⑤+⑥),40分钟,不查资料",
    "批改昨天的作文:对照原文档逐句核对,错词记进错词本",
    "组装作文#2:2025英二·老人日常休闲(静态:①+④+⑥)",
    "组装作文#3:2023英二·居民健康素养(动态:②+④+⑥)",
    "组装作文#4:2024英二·劳动实践课(静态:①+体育健康换词⑤+⑥)",
    "组装作文#5:2026英一·养老机器人(双图表:③+①右图数据+⑤+⑥)",
    "组装期总检:随机抽2段默写+错词本过一遍;明天起进入限时套用",
]

PRACTICE = [
    "限时套用#1:2026英二·儿童户外活动,25分钟写作+10分钟对照订正",
    "限时套用#2:2023英二·居民健康素养(动态)",
    "限时套用#3:2025英二·老人日常休闲(静态)",
    "限时套用#4:2024英二·劳动实践课(静态)",
    "限时套用#5:2026英一·养老机器人(双图表)",
    "限时套用#6:2024英一·公园建设(图画+图表)",
    "限时套用#7:2022英二·快递业务量(动态)",
    "限时套用#8:2019英二·毕业生去向(动态多方向)",
    "限时套用#9:2020英二·手机阅读(饼图)",
    "二刷:重写前8天里最不满意的一篇,重点修错词",
    "限时套用#10:2021英二真题图表(先自己判断动/静再动笔)",
    "限时套用#11:2023英一·龙舟与传统文化(单图画,练图画第一段)",
    "文字作文·大纲样题1(职场坦诚):文字改写+态度句+④+⑥",
    "文字作文·大纲样题2(孩子与屏幕):同上套路再来一篇",
    "限时套用#12:2020英一·习惯(双图画,练应急描述)",
    "盲题演练:自选一个预测话题(静态图),全程闭卷25分钟",
    "盲题演练:自选一个预测话题(动态图),全程闭卷",
    "全套段落大默写:必背7段+备用段一次过,标出还不熟的",
    "盲题演练:双图表,重点练③总起句+左右图数据分配",
    "轻复盘:只看错词本+一页纸终版,不写新作文,早睡",
]

PLAN = {
    "start": "2026-10-23",
    "exam": "2026-12-19",
    "total_days": 58,
    "buffers": [6, 13, 20],
    "recite": {},
    "assembly": ASSEMBLY,
    "practice": PRACTICE,
    "buffer_note": "缓冲日:不新背。把之前没背熟的句子和功能句再过一遍,勾齐了再休息。",
    "exam_note": "今天初试。早上只过一页纸终版;写作文先花3分钟定三段骨架再动笔。稳住,你背了58天。",
}

# 22个新背日铺进25个格子(3个缓冲日:第7/14/21天,即offset 6/13/20)
batch = 1
for off in range(25):
    if off in PLAN["buffers"]:
        continue
    PLAN["recite"][str(off)] = batch
    batch += 1
assert batch == 23, batch

with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

days = data['days']
have = {d['day'] for d in days}
added = 0
for nb in NEW_BATCHES:
    if nb['day'] not in have:
        days.append(nb)
        added += 1
days.sort(key=lambda d: d['day'])

data['plan'] = PLAN
data['note'] = (
    "2026-10-23 v2:新增批次16-22(AI归来+图片书融合:双图表总起/万能应急/方案一举例/方案三从句/"
    "方案五虚拟语气/第三段总结·措施·畅想),并新增 plan 段=2026-10-23→2026-12-19 共58天逐日计划"
    "(背诵25天含3缓冲→组装12天→限时套用20天→考试日);句子打卡键=内容哈希,1-15批旧进度不受影响。"
    "标记约定:tpl蓝字=必须背的框架;blank红字=考场按题填(汉字占位)。"
)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

total = sum(len(d['sents']) for d in data['days'])
print(f"新增批次 {added} 个;现有批次 {len(data['days'])} 个,总句数 {total};plan 天数 {PLAN['total_days']}")
print("recite 映射:", PLAN['recite'])
