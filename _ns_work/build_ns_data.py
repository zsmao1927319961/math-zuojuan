# -*- coding: utf-8 -*-
"""27南山作文模板吃鸡计划 → data/zuowen_nanshan.json
来源: 27南山大作文+素材库(P60-100)/小作文(P5-44)/小作文素材库/大小作文第二段补充句/4.0学习计划
句子由 PDF 渲染图 OCR 转录, 已修正 OCR 小错(As aresult/sopport/daage/To.s up等)
页码映射: 小作文书页=PDF页+4, 大作文书页=PDF页+59 (与4.0计划表页码互验吻合)
"""
import json, re

def T(s):  # tpl 蓝色骨架
    return f'<span class="tpl">{s}</span>'
def B(s):  # blank 红色填槽
    return f'<span class="blank">{s}</span>'

S = []  # sentences

def add(id, cat, grp, slot, en, zh, meta=None, lvl=1, page=None):
    o = {"id": id, "cat": cat, "grp": grp, "slot": slot, "en": en, "zh": zh, "lvl": lvl}
    if meta: o["meta"] = meta
    if page: o["page"] = page
    S.append(o)

# ============================================================ 小作文 xz
XZ = "xz"
# —— 第一段·公务书信 (P17-18)
add("xz-p1-gw-1", XZ, "第一段 · 公务书信", "①自我介绍·经典版",
    f"{T('I am a/an')} {B('身份')} {T('from/at/in')} {B('单位')}{T('.')}",
    "我是……（单位）的一名……",
    "身份备选: undergraduate 本科生 / postgraduate student 研究生 / member of the Students' Union 学生会成员 / volunteer / regular user of the library 图书馆常客; 单位备选: at your university / in our community",
    1, "P17")
add("xz-p1-gw-2", XZ, "第一段 · 公务书信", "①自我介绍·上岸版",
    f"{T('As a/an')} {B('身份')}{T(', I')} {B('相关经历或背景')}{T('.')}",
    "作为……，我曾……（适合建议/投诉/申请）",
    "经历备选: have organized several charity sales / have used the library for several years / have recently experienced a problem with... / have relevant experience in...",
    1, "P17")
add("xz-p1-mu-1", XZ, "第一段 · 写作目的", "②写作目的·较正式",
    f"{T('The purpose of this letter is to')} {B('动词原形 + 目的')}{T('.')}",
    "本信旨在……",
    "按信型替换: 建议 offer several constructive suggestions on+话题 / 邀请 invite you to+活动 / 推荐 recommend+人或物 to you / 申请 apply for+职位 / 感谢道歉 express my heartfelt gratitude/apology to sb. for sth. / 祝贺 express my congratulations on+成就 / 投诉 make a complaint about+事 / 答复 share some relevant details about... / 辞职 inform you of my decision to resign from+职位",
    1, "P18")
add("xz-p1-mu-2", XZ, "第一段 · 写作目的", "②写作目的·较轻松",
    f"{T('I am writing this letter in order to')} {B('动词原形 + 目的')}{T('.')}",
    "我写此信意在……", "动词替换同上句", 2, "P18")
# —— 第一段·私人书信 (P20)
add("xz-p1-sr-1", XZ, "第一段 · 私人书信", "①寒暄·自然问候",
    f"{T('It has been a long time since we last met. How is it going?')}",
    "好长时间没见，你好吗？", None, 1, "P20")
add("xz-p1-sr-2", XZ, "第一段 · 私人书信", "①寒暄·客气礼貌",
    f"{T('I hope this letter finds you well.')}",
    "展展佳。", None, 1, "P20")
add("xz-p1-sr-3", XZ, "第一段 · 私人书信", "①寒暄·回应来信",
    f"{T('It was')} {B('great / wonderful / lovely')} {T('to hear from you.')}",
    "很高兴收到你的来信。得知……，我感到高兴！", None, 2, "P20")
add("xz-p1-sr-4", XZ, "第一段 · 私人书信", "①寒暄·感谢分享",
    f"{T('Thank you for sharing your')} {B('experience of...')} {T('with me.')}",
    "感谢你与我分享……的经历。", "另备: I'm glad to know that you are interested in... 很高兴得知你对…感兴趣 / I still remember the wonderful time we spent together. 我仍记得我们一起度过的美好时光", 2, "P20")
# —— 第二段·讲事情类 (P21-22)
add("xz-p2-js-1", XZ, "第二段 · 讲事情类", "①核心事项",
    f"{T('The activity will focus on')} {B('主题或核心内容')}{T('.')}",
    "本次活动将围绕……展开。",
    "activity 可替换 the event / the program / the lecture; focus on 可替换 center on / be devoted to / feature / be organized around",
    1, "P21")
add("xz-p2-js-2", XZ, "第二段 · 讲事情类", "②时间地点细节·版A",
    f"{T('Scheduled for')} {B('时间')} {T('at/in')} {B('地点')}{T(', it will include')} {B('具体内容')}{T('.')}",
    "本次活动定于……时间在……地点举行，具体包括……",
    "地点备选: at the school auditorium 学校礼堂 / in Room 201 / on the playground / at the student center; include 可替换 will feature / will consist of / will cover / will offer",
    1, "P21-22")
add("xz-p2-js-3", XZ, "第二段 · 讲事情类", "②时间地点细节·版B",
    f"{T('It is scheduled to take place on')} {B('日期')} {T('at')} {B('具体时间')} {T('in/at')} {B('地点')}{T(', and will consist of')} {B('具体内容')}{T('.')}",
    "活动定于……日……时间在……地点举办，由……环节组成。", "两版选一背", 2, "P22")
add("xz-p2-js-4", XZ, "第二段 · 讲事情类", "③安排收获意义·版A",
    f"{T('Participants will also have the opportunity to')} {B('具体活动或收获')}{T('.')}",
    "参加者还将有机会……",
    "收获备选: exchange ideas with 与…交流 / learn more about / gain a better understanding of / develop their skills in / broaden their horizons 拓宽视野 / enrich their practical experience / make friends with like-minded peers / acquire professional knowledge",
    1, "P22")
add("xz-p2-js-5", XZ, "第二段 · 讲事情类", "③安排收获意义·版B",
    f"{T('This experience will also enable all participants to')} {B('具体活动或收获')}{T('.')}",
    "这段经历也将使所有参与者能够……", None, 2, "P22")
# —— 第二段·讲事情补充(感谢信/祝贺信, 补充句PDF P23-25)
add("xz-p2-bc-1", XZ, "第二段 · 讲事情补充", "①感谢信·核心帮助",
    f"{T('Your support with')} {B('具体事项')} {T('was particularly valuable.')}",
    "您在……方面给予的支持尤其宝贵。",
    "事项备选: my studies / my application / organizing the event / solving the problem; support with 可替换 help with / assistance with",
    2, "补充P23")
add("xz-p2-bc-2", XZ, "第二段 · 讲事情补充", "①祝贺信·核心成绩",
    f"{T('Your success in')} {B('具体事项')} {T('was particularly impressive.')}",
    "您在……方面取得的成功尤其令人钦佩。",
    "事项备选: the competition / your academic studies / completing the project / receiving the scholarship / gaining admission to your ideal university",
    2, "补充P23")
add("xz-p2-bc-3", XZ, "第二段 · 讲事情补充", "②感谢信·补充细节",
    f"{T('This support included')} {B('帮助一')} {T('and')} {B('帮助二')}{T(', reflecting your')} {B('品质一')} {T('and')} {B('品质二')}{T('.')}",
    "这些帮助包括……和……，体现了您的……和……",
    "帮助备选: detailed guidance / useful advice / warm encouragement / thoughtful arrangements; 品质备选: kindness / patience / responsibility / generosity",
    3, "补充P24")
add("xz-p2-bc-4", XZ, "第二段 · 讲事情补充", "③收获+进一步影响",
    f"{T('It has also enabled')} {B('me/you')} {T('to')} {B('直接收获')} {T('and given')} {B('me/you')} {T('the')} {B('confidence/opportunity')} {T('to')} {B('进一步行动')}{T('.')}",
    "这也使我/您能够……，并给了我/您……的信心/机会去……（感谢信用 confidence，祝贺信用 opportunity）",
    "感谢信收获: complete the task successfully / solve the problem / adapt to the new environment; 祝贺信收获: gain greater confidence / receive wider recognition / make further progress",
    3, "补充P25")
# —— 第二段·观点类 (P24-26)
add("xz-p2-gd-1", XZ, "第二段 · 观点类", "④提出建议或推荐",
    f"{T('I strongly recommend')} {B('推荐对象')} {T('as')} {B('具体选择或用途')}{T('.')}",
    "我强烈推荐……作为/用于……",
    "strongly recommend 可替换 highly recommend / would recommend / suggest choosing; 选择备选 an ideal choice / a suitable option / your first destination / a valuable resource",
    1, "P24")
add("xz-p2-gd-2", XZ, "第二段 · 观点类", "⑤说明主要理由",
    f"{T('One major reason is that')} {B('理由')}{T('.')}",
    "一个主要原因是……",
    "one major reason 可替换 the primary reason / a key reason / what makes it particularly attractive; 万能理由: it offers an excellent opportunity to / it has rich historical and cultural value / it has great educational value / it offers considerable practical value",
    1, "P24-25")
add("xz-p2-gd-3", XZ, "第二段 · 观点类", "⑥补充好处·推荐人",
    f"{T('More importantly, these qualities will enable him/her to')} {B('工作结果')}{T('.')}",
    "更重要的是，这些品质将使他/她能够……",
    "工作结果备选: perform the duties effectively / cooperate effectively with others / deal with unexpected problems / adapt quickly to the new environment / make a valuable contribution to the team",
    1, "P25")
add("xz-p2-gd-4", XZ, "第二段 · 观点类", "⑥补充好处·推荐事物",
    f"{T('More importantly, this feature allows')} {B('visitors/readers')} {T('to')} {B('实际收获')}{T('.')}",
    "更重要的是，这一特点能够让游客/读者……",
    "this feature 可替换 this advantage / its rich content / its unique design; 收获备选: gain a deeper understanding of / broaden their horizons / enjoy a memorable cultural experience / apply the ideas to their daily lives",
    1, "P26")
# —— 第二段·解决问题类 (P28-29)
add("xz-p2-jj-1", XZ, "第二段 · 解决问题类", "⑦说明具体问题",
    f"{T('Unfortunately,')} {B('具体问题')}{T('.')}",
    "很遗憾，……",
    "Unfortunately 可替换 Regrettably / I am sorry to say that / I regret to inform you that; 问题备选: I will be unable to attend... / I cannot complete the task on time / the product failed to work properly / the service did not meet my expectations",
    1, "P28")
add("xz-p2-jj-2", XZ, "第二段 · 解决问题类", "⑧A解释原因",
    f"{T('This is mainly because')} {B('原因')}{T('.')}",
    "这主要是因为……",
    "可替换 is due to the fact that / results from +名词 / has been caused by; 原因备选: I have to attend an important examination / an unexpected emergency has arisen / I have fallen ill / there has been a change in my schedule",
    1, "P28")
add("xz-p2-jj-3", XZ, "第二段 · 解决问题类", "⑧B说明影响",
    f"{T('As a result,')} {B('问题造成的影响')}{T('.')}",
    "因此，……",
    "影响备选: I was unable to use the product / the problem caused considerable inconvenience / my work was seriously affected / additional time and money were wasted",
    2, "P29")
add("xz-p2-jj-4", XZ, "第二段 · 解决问题类", "⑨A道歉·提出补救",
    f"{T('To make up for')} {B('问题')}{T(', I will')} {B('补救办法')}{T('.')}",
    "为了弥补……，我将……",
    "To make up for 可替换 To compensate for; 补救备选: arrange another meeting / complete the task as soon as possible / ask a classmate to take notes",
    1, "P29")
add("xz-p2-jj-5", XZ, "第二段 · 解决问题类", "⑨B投诉·解决办法",
    f"{T('To resolve the matter, I would appreciate it if you could')} {B('解决办法')}{T('.')}",
    "为了解决此事，如果您能……，我将不胜感激。",
    "To resolve the matter 可替换 To address the problem / To deal with the issue; 办法备选: provide a replacement / offer a full refund / take appropriate measures / investigate the matter",
    1, "P29")
# —— 第三段 (P31-32)
add("xz-p3-1", XZ, "第三段 · 结尾", "①表达情感",
    f"{T('I')} {B('sincerely / truly / genuinely')} {T('hope that you will')} {B('动作')} {T('my')} {B('事项')}{T('.')}",
    "我真诚地希望您能……我的……",
    "动作×事项搭配: accept invitation/apology 接受邀请/道歉 / consider suggestions 考虑建议 / adopt suggestions 采纳建议 / approve application 批准申请 / understand decision 理解决定 / respect decision 尊重决定",
    1, "P31")
add("xz-p3-2", XZ, "第三段 · 结尾", "②期待回复·公务A",
    f"{T('A reply at your earliest convenience would be highly appreciated.')}",
    "如能在您方便时尽早回复，我将十分感谢。", None, 1, "P31")
add("xz-p3-3", XZ, "第三段 · 结尾", "②期待回复·公务B",
    f"{T('Please let me know your decision at your earliest convenience.')}",
    "请您方便时尽早告知我您的决定。", None, 2, "P31")
add("xz-p3-4", XZ, "第三段 · 结尾", "②期待回复·私人",
    f"{T('Please let me know')} {B('回复内容')} {T('when convenient.')}",
    "请在方便时告诉我……",
    "回复内容备选: your thoughts / your opinion / your plans / whether you can attend / whether the arrangement suits you; when convenient 可替换 when you have time / at your convenience / as soon as possible",
    1, "P32")
# —— 通知·第一段 (P36-37)
add("xz-tz-1-1", XZ, "通知 · 第一段", "发布信息·版A",
    f'{T("The Students\' Union is pleased to announce that")} {B("活动名称")} {T("will be held.")}',
    "学生会很高兴地宣布……将举办。",
    "活动名称备选: reading sharing session 读书分享会 / English speech contest / essay competition / campus cultural festival / art exhibition / campus food festival / volunteer recruitment",
    1, "P36")
add("xz-tz-1-2", XZ, "通知 · 第一段", "发布信息·版B",
    f'{T("It\'s a pleasure to inform everyone that a")} {B("活动名称")} {T("will be held in our university.")}',
    "很高兴地通知大家，我校将举办……活动。", None, 2, "P36")
add("xz-tz-1-3", XZ, "通知 · 第一段", "说明活动目的",
    f"{T('The purpose of the event is to')} {B('活动目的')}{T('.')}",
    "本次活动的目的是……",
    "目的备选: promote cultural exchange / enrich campus life / raise environmental awareness / improve practical skills / encourage communication / provide learning opportunities / help students learn more about...",
    1, "P36")
add("xz-tz-1-4", XZ, "通知 · 第一段", "通知目的·告知信息",
    f"{T('The purpose of this notice is to provide')} {B('对象')} {T('with details about')} {B('事项')}{T('.')}",
    "本通知旨在向……提供有关……的详细信息。",
    "with details about 可替换 with information regarding / with relevant information on",
    2, "P36")
# —— 通知·第二段 活动通知 (P38)
add("xz-tz-hd-1", XZ, "通知 · 活动通知第二段", "①时间地点",
    f"{T('The event will be held at/in')} {B('地点')} {T('at')} {B('时间')} {T('on')} {B('日期')}{T('.')}",
    "该活动将于……在……举行。",
    "搭配: at+具体时刻 at 2:00 p.m. / on+具体日期 on May 10 / in+室内场所 in the school auditorium / at+具体地点 at the school gate; event 可替换 activity / lecture / competition / workshop",
    1, "P38")
add("xz-tz-hd-2", XZ, "通知 · 活动通知第二段", "②参加对象",
    f"{T('All students interested in')} {B('主题')} {T('are welcome to attend.')}",
    "欢迎所有对……感兴趣的学生参加。",
    "are welcome to attend 可替换 are encouraged to participate / may attend / can participate",
    1, "P38")
add("xz-tz-hd-3", XZ, "通知 · 活动通知第二段", "③活动内容",
    f"{T('Highlights will include')} {B('活动1')}{T(',')} {B('活动2')} {T('and')} {B('活动3')}{T('.')}",
    "本次活动亮点包括……", None, 1, "P38")
# —— 通知·第二段 招募通知 (P40-41)
add("xz-tz-zm-1", XZ, "通知 · 招募通知第二段", "④申请条件·版A",
    f"{T('Ideal applicants should be')} {B('品质')} {T('and possess')} {B('能力')}{T('.')}",
    "理想的申请者应当……并具备……",
    "品质(形容词): responsible / patient / reliable / enthusiastic / hard-working / cooperative / energetic; 能力(名词短语): good communication skills / strong organizational skills / excellent teamwork skills / a good command of English",
    1, "P40")
add("xz-tz-zm-2", XZ, "通知 · 招募通知第二段", "④申请条件·版B",
    f"{T('We are looking for applicants who are')} {B('品质')} {T('and have')} {B('能力')}{T('.')}",
    "我们寻找的申请者需拥有……品质，掌握……能力。", None, 2, "P40")
add("xz-tz-zm-3", XZ, "通知 · 招募通知第二段", "⑤优先条件·版A",
    f"{T('Previous volunteer experience will be considered an advantage.')}",
    "具有志愿服务经验将被视为一项优势。",
    "volunteer experience 可替换 relevant experience / working experience / similar experience / social practice experience / event-organizing experience",
    1, "P41")
add("xz-tz-zm-4", XZ, "通知 · 招募通知第二段", "⑤优先条件·版B",
    f"{T('Candidates with good cross-cultural awareness will be preferred.')}",
    "具备良好跨文化意识的候选人将优先录用。",
    "cross-cultural awareness 可替换 strong organizational skills / effective teamwork spirit / time-management ability / problem-solving skills / fluent oral English / public speaking ability",
    2, "P41")
add("xz-tz-zm-5", XZ, "通知 · 招募通知第二段", "⑥工作职责",
    f"{T('The main duties involve')} {B('动名词1')}{T(',')} {B('动名词2')} {T('and')} {B('动名词3')}{T('.')}",
    "主要工作包括……",
    "职责备选: receiving guests / answering inquiries / offering directions / preparing materials / maintaining order / providing language assistance / taking photos / distributing leaflets",
    1, "P41")
# —— 通知·第三段 (P42-43)
add("xz-tz-3-1", XZ, "通知 · 第三段", "①参加/申请方式",
    f"{T('Those who are interested should')} {B('参加/申请方式')} {T('through/at')} {B('渠道')} {T('by')} {B('截止时间')}{T('.')}",
    "感兴趣的同学应于……前通过……参加或申请。",
    "方式备选: register for the event / sign up for the activity / submit an application / send a brief self-introduction; 渠道备选: through the school website / through the online system / at the Students' Union office",
    1, "P42")
add("xz-tz-3-2", XZ, "通知 · 第三段", "①申请方式·正式版",
    f"{T('Interested applicants are expected to submit')} {B('材料')} {T('via')} {B('渠道')} {T('before the deadline.')}",
    "有意申请者需在截止日期前通过指定平台提交申请材料。",
    "材料备选: a brief self-introduction / application form / resume / personal statement",
    2, "P42")
add("xz-tz-3-3", XZ, "通知 · 第三段", "②联系方式·版A",
    f"{T('For further information, please contact')} {B('联系人/组织')} {T('at/via')} {B('联系方式')}{T('.')}",
    "如需了解更多信息，请通过……联系……",
    "For further information 可替换 For more details / If you have any questions",
    1, "P43")
add("xz-tz-3-4", XZ, "通知 · 第三段", "②联系方式·版B",
    f"{T('Should you have any questions, feel free to reach out to')} {B('联系人/组织')} {T('via')} {B('联系方式')}{T('.')}",
    "如您有任何疑问，可通过……联系……", None, 2, "P43")

# ============================================================ 大作文 dz
DZ = "dz"
# —— 第一段·引入图表 (P78)
add("dz-p1-1", DZ, "第一段 · 引入图表", "总起句·版A",
    f"{T('The')} {B('图表类型')} {T('above clearly')} {B('shows / compares')} {B('主题内容')} {B('in 地点')} {B('时间')}{T('.')}",
    "上述……清楚地展示/对比了……",
    "图表类型: bar chart 柱状图 / pie chart 饼状图 / line graph 折线图 / table 表格; 动词: show the changes in... / show the percentage of... / show the differences between... / compare... in terms of...",
    1, "P78")
add("dz-p1-2", DZ, "第一段 · 引入图表", "总起句·版B",
    f"{T('What the')} {B('图表类型')} {T('provided is the')} {B('reasons / purpose / choices')} {T('of')} {B('主题')}{T('.')}",
    "……提供了……的调查结果。", None, 2, "P78")
add("dz-p1-3", DZ, "第一段 · 引入图表", "总起句·版C",
    f"{T('According to the above')} {B('图表类型')}{T(', the percentages of')} {B('对象')} {T('in')} {B('范围')} {T('underwent an enormous change')} {B('时间')}{T('.')}",
    "根据上面……所示，……的百分比在……年间发生了巨大的变化。", None, 2, "P78")
# —— 第一段·动态描述 (P79-80)
add("dz-p1-dd-1", DZ, "第一段 · 动态描述", "显著变化句",
    f"{T('There was a noticeable')} {B('rise / decline')} {T('in')} {B('对象词')} {T('from')} {B('A')} {T('to')} {B('B')} {B('时间')}{T('.')}",
    "在……时间内，……出现了显著的上升/下降（从A到B）。",
    "升降名词: increase/rise/growth/drop/decline/fall; 程度词: noticeable/remarkable/dramatic; 副词库见素材: dramatically/sharply/considerably/rapidly/steadily/gradually/slightly",
    1, "P79-80")
add("dz-p1-dd-2", DZ, "第一段 · 动态描述", "对象变化句",
    f"{B('对象词')} {T('rose / increased / dropped / fell / stood at')} {B('数字')} {B('时间')}{T('.')}",
    "……（对象）在……（时间）上升/增长/下降/跌至/达到……",
    "词组备选: continue its upward trend / on the rise / on the decline / remain stable 保持平稳 / fluctuate between...and... 波动",
    1, "P80")
add("dz-p1-dd-3", DZ, "第一段 · 动态描述", "双对象对比句",
    f"{T('During this period, the percentage of')} {B('对象A')} {T('has declined/increased sharply from')} {B('A')} {T('to')} {B('B')}{T(', whereas those')} {B('doing sth')} {T('declined/increased markedly from')} {B('A1')} {T('and')} {B('A2')} {T('to')} {B('B1')} {T('and')} {B('B2')} {T('respectively.')}",
    "在此期间，……的数量从A急剧下降/显著增长至B；而……则分别从A1、A2急剧下降/显著增长到B1、B2。", None, 1, "P80")
# —— 第一段·静态描述 (P81-82)
add("dz-p1-jt-1", DZ, "第一段 · 静态描述", "高低对比句",
    f"{T('The proportion of')} {B('A')} {T('is higher than / lower than')} {B('B')}{T(', while')} {B('补充对比')}{T('.')}",
    "A的占比高于/低于B，而……。",
    "is higher than 可替换 is the same as / is equal to 与…持平",
    1, "P82")
add("dz-p1-jt-2", DZ, "第一段 · 静态描述", "相比对照句",
    f"{T('The percentage of')} {B('A')}{T(', compared with')} {B('B')}{T(',')} {B('数据描述')}{T('.')}",
    "A的数据，相较于B的数据……。",
    "compared with 可替换 compared to / in contrast to",
    2, "P82")
add("dz-p1-jt-3", DZ, "第一段 · 静态描述", "相近持平句",
    f"{T('The figure of')} {B('A')} {T('is similar to / the same as')} {B('B')}{T('.')}",
    "A的数据和B组相近/持平。", None, 2, "P82")
add("dz-p1-jt-4", DZ, "第一段 · 静态描述", "差距句",
    f"{T('There was a huge gap between')} {B('A')} {T('and')} {B('B')}{T(':')} {B('数据')}{T('.')}",
    "A与B之间存在很大差异/巨大差距。",
    "a huge gap 可替换 a big difference / a huge change",
    2, "P82")
# —— 第一段·复合图表 (P83-84)
add("dz-p1-fh-1", DZ, "第一段 · 复合图表", "共同主题句",
    f"{T('The two charts above jointly present the results of a survey concerning')} {B('共同主题')}{T('.')}",
    "上述两幅图表共同呈现了一项关于……的调查结果。", None, 1, "P83")
add("dz-p1-fh-2", DZ, "第一段 · 复合图表", "分别概括句·版A",
    f"{T('The pie chart shows')} {B('饼图信息')}{T(', while the bar chart displays')} {B('柱图信息')}{T('.')}",
    "饼图显示了……，而柱状图展示了……。", None, 1, "P84")
add("dz-p1-fh-3", DZ, "第一段 · 复合图表", "分别概括句·版B",
    f"{T('As can be seen from the two charts, the pie graph illustrates')} {B('饼图信息')}{T(', with the bar graph revealing')} {B('柱图信息')}{T('.')}",
    "从两幅图表中可以看出，饼图说明了……，同时柱状图揭示了……。", None, 2, "P84")
add("dz-p1-fh-4", DZ, "第一段 · 复合图表", "揭示联系句",
    f"{T('The two sets of data are closely related, as')} {B('A')} {T('may be a major reason for')} {B('B')}{T('.')}",
    "两组数据紧密相关，因为……或许是造成……的主要原因。", None, 1, "P84")
add("dz-p1-fh-5", DZ, "第一段 · 复合图表", "揭示联系句·版B",
    f"{T('It is clear that')} {B('A')} {T('has a close connection with')} {B('B')} {T('reflected in the charts.')}",
    "显而易见，图表反映出……与……有着密切的联系。", None, 2, "P84")
# —— 第一段·材料作文 (P85)
add("dz-p1-cl-1", DZ, "第一段 · 材料作文", "概括材料观点",
    f"{T('In the passage, the author argues that')} {B('作者观点')}{T('.')}",
    "在文章中，作者认为……",
    "argues 可替换 claims / suggests / states / believes",
    1, "P85")
add("dz-p1-cl-2", DZ, "第一段 · 材料作文", "表明自己立场",
    f"{T('I fully agree with')} {B('this view')}{T('.')}",
    "我完全同意这个观点。",
    "完全同意: I fully agree with / support / share / subscribe to this view; 部分同意: I partly agree with the author; 不同意: I disagree with / oppose this opinion",
    1, "P85")
# —— 第二段·过渡句 (P86)
add("dz-p2-gd-1", DZ, "第二段 · 过渡句", "现象分析类·版A",
    f"{T('This phenomenon can be attributed to several factors.')}",
    "这种现象可以归因于几个因素。",
    "可替换 can be traced to / is caused by",
    1, "P86")
add("dz-p2-gd-2", DZ, "第二段 · 过渡句", "现象分析类·版B",
    f"{T('Several factors can account for this')} {B('phenomenon / trend')}{T('.')}",
    "有几个因素能解释这一现象/趋势。",
    "另备: The reasons behind this phenomenon are not difficult to identify. 这一现象背后的原因不难发现",
    1, "P86")
add("dz-p2-gd-3", DZ, "第二段 · 过渡句", "材料观点类·版A",
    f'{T("The differences in people\'s opinions can be explained by their diverse demands and concerns.")}',
    "人们观点的差异，可以通过他们不同的需求与关注点来解释。", None, 1, "P86-90")
add("dz-p2-gd-4", DZ, "第二段 · 过渡句", "材料观点类·版B",
    f"{T('Behind these survey results lie different considerations and expectations among different groups of people.')}",
    "这些调查结果的背后，是不同人群各异的考量与期待。", None, 2, "P90")
# —— 第二段·原因句变体 (10-31用户自组拍板: 同槽替换用, 不设整段卡)
add("dz-p2-yy-1b", DZ, "第二段 · 现象原因", "宏观原因句·流行版",
    f"{T('First, the growing popularity of')} {B('原因')} {T('has offered people more opportunities to')} {B('机会做的事')}{T(', enabling them to')} {B('行为')}{T('.')}",
    "首先，【原因】的日益流行给人们提供了更多机会去做【机会做的事】，使他们能够【行为】。",
    "10-31用户拍板为主选。原因槽=能流行的事物(online shopping网购/fitness apps健身App/short videos短视频)；机会做的事=动词短语，to后不接名词(buy whatever they like)；行为=照抄图注口径，与yy-2系行为槽错开。经济/政策类原因popularity装不下，换用yy-1(development of)。约22词。",
    1, "P89")
add("dz-p2-yy-2b", DZ, "第二段 · 现象原因", "个人观念原因句·全龄版",
    f"{T('Besides, with the growing awareness of')} {B('主题')}{T(', people from different age groups are more likely to')} {B('行为')}{T('.')}",
    "此外，随着对【主题】意识的增强，不同年龄段的人更有可能【行为】。",
    "yy-2的全龄版(10-31用户拍板为主选)。age groups只配全民类话题(健身/手机/消费)；学生/农村/老人类图换回yy-2(an increasing number of people)。行为槽与yy-1系错开。",
    1, "P89-90")
# —— 第二段·现象数据类原因 (P89-90)
add("dz-p2-yy-1", DZ, "第二段 · 现象原因", "宏观原因句",
    f"{T('First, the development of')} {B('宏观原因')} {T('has provided people with')} {B('条件')}{T(', making it easier for them to')} {B('行为')}{T('.')}",
    "首先，……的发展为人们提供了……，使他们更容易……",
    "development of 可替换 improvement of / continued growth of / widespread application of / growing popularity of / increasing availability of",
    1, "P89")
add("dz-p2-yy-2", DZ, "第二段 · 现象原因", "个人观念原因句",
    f"{T('Besides, with the growing awareness of / demand for')} {B('主题')}{T(', an increasing number of people are willing to')} {B('行为')}{T('.')}",
    "此外，随着人们对……的意识/需求不断增强，越来越多的人愿意……",
    "growing awareness of 可替换 increasing attention paid to / rising demand for / changing attitudes toward / people attaching greater importance to",
    1, "P89-90")
# 万能原因 (P90, lvl2)
add("dz-p2-yy-3", DZ, "第二段 · 万能原因", "经济发展",
    f"{T('Rising incomes have enabled more people to')} {B('行为')}{T('.')}",
    "收入的增长使更多人能够……", None, 2, "P90")
add("dz-p2-yy-4", DZ, "第二段 · 万能原因", "科技进步",
    f"{T('The rapid development of technology has made it easier for people to')} {B('行为')}{T('.')}",
    "科技的快速发展使人们更容易……", None, 2, "P90")
add("dz-p2-yy-5", DZ, "第二段 · 万能原因", "政策支持",
    f"{T('Supportive policies have created favorable conditions for')} {B('主题')}{T('.')}",
    "支持性政策为……创造了有利条件。", None, 2, "P90")
add("dz-p2-yy-6", DZ, "第二段 · 万能原因", "观念变化",
    f"{T('Changing attitudes toward')} {B('主题')} {T('have made people more willing to')} {B('行为')}{T('.')}",
    "对……的态度变化使人们更愿意……", None, 2, "P90")
add("dz-p2-yy-7", DZ, "第二段 · 万能原因", "负面·个人意识不足",
    f"{T('Many people lack sufficient awareness of the importance of')} {B('主题')}{T('.')}",
    "许多人没有充分意识到……的重要性。", None, 2, "P90")
add("dz-p2-yy-8", DZ, "第二段 · 万能原因", "负面·监管不足",
    f"{T('The lack of effective supervision has allowed the problem to become increasingly serious.')}",
    "有效监管的缺失使这一问题日益严重。", None, 2, "P90")
# —— 第二段·影响句 (大补充PDF)
add("dz-p2-xy-1", DZ, "第二段 · 影响句", "通用型·个人+社会",
    f"{T('As a result, this phenomenon can not only')} {B('个人影响')} {T('but also')} {B('社会影响')}{T('.')}",
    "因此，这一现象不仅能够……，还能够……（正负面都可以）",
    "例: weaken individuals' ability to think independently + increase society's dependence on technology; help individuals make better health decisions + reduce pressure on the healthcare system",
    1, "补充P90")
add("dz-p2-xy-2", DZ, "第二段 · 影响句", "积极影响",
    f"{T('This trend can improve')} {B('个人积极结果')} {T('and promote')} {B('社会积极结果')}{T('.')}",
    "这一趋势能够改善……，并促进……",
    "improve 可替换 enhance; promote 可替换 support",
    2, "补充P90")
add("dz-p2-xy-3", DZ, "第二段 · 影响句", "负面影响",
    f"{T('This problem may harm')} {B('个人受损对象')} {T('and increase')} {B('社会负担')}{T('.')}",
    "这一问题可能损害……，并增加……",
    "harm 可替换 damage; increase 可替换 add to",
    2, "补充P90")
# —— 第二段·材料观点类展开 (P90-91)
add("dz-p2-cl-1", DZ, "第二段 · 材料观点类", "第一种观点原因·版A",
    f"{T('Those who choose')} {B('A')} {T('mainly do so because they believe that')} {B('原因')}{T('.')}",
    "选择A的人主要是因为他们认为……", None, 1, "P90")
add("dz-p2-cl-2", DZ, "第二段 · 材料观点类", "第一种观点原因·版B",
    f"{T('One major reason why some people prefer')} {B('A')} {T('is that it enables them to')} {B('具体好处')}{T('.')}",
    "一些人偏向A的一个主要原因是，它能够使他们……", None, 2, "P91")
add("dz-p2-cl-3", DZ, "第二段 · 材料观点类", "第一种观点原因·版C",
    f"{T('From their perspective,')} {B('A')} {T('is a more practical choice, as it helps them')} {B('具体好处')}{T('.')}",
    "在他们看来，A是更加实际的选择，因为这有助于他们……", None, 2, "P91")
add("dz-p2-cl-4", DZ, "第二段 · 材料观点类", "另一种观点·版A",
    f"{T('By contrast, those who prefer')} {B('B')} {T('tend to attach greater importance to')} {B('重视内容')}{T('.')}",
    "相比之下，偏向B的人往往更加重视……",
    "attach greater importance to 可替换 value / place emphasis on / give priority to",
    1, "P91")
add("dz-p2-cl-5", DZ, "第二段 · 材料观点类", "另一种观点·版B",
    f"{T('Others, however, choose')} {B('B')} {T('because they believe it can introduce them to')} {B('好处')}{T('.')}",
    "然而，另一些人选择B，因为他们认为它能够……",
    "introduce them to 可替换 provide them with / give them access to",
    2, "P91")
add("dz-p2-cl-6", DZ, "第二段 · 材料观点类", "另一种观点·版C",
    f"{T('For another group,')} {B('B')} {T('is more attractive, since it provides them with')} {B('机会/资源/经验')}{T('.')}",
    "对另一群体而言，B更具吸引力，因为它为他们提供了……",
    "attractive 可替换 appealing / suitable / valuable",
    2, "P91")
# —— 第二段·总结句 (P92)
add("dz-p2-zj-1", DZ, "第二段 · 总结句", "积极趋势",
    f'{T("Overall, this change reflects social progress and people\'s pursuit of a better life.")}',
    "总体而言，这一变化反映了社会进步和人们对美好生活的追求。", None, 1, "P92")
add("dz-p2-zj-2", DZ, "第二段 · 总结句", "负面现象",
    f"{T('If left unaddressed, this problem may produce more serious consequences in the future.')}",
    "如果得不到解决，这一问题将来可能造成更加严重的后果。", None, 1, "P92")
add("dz-p2-zj-3", DZ, "第二段 · 总结句", "中性趋势",
    f"{T('Overall, this phenomenon is the result of both social development and changing individual needs.')}",
    "总体而言，这一现象是社会发展与个人需求变化共同作用的结果。", None, 1, "P92")
add("dz-p2-zj-4", DZ, "第二段 · 总结句", "材料观点·归纳",
    f'{T("In essence, these different choices reflect people\'s diverse needs, priorities and values.")}',
    "从本质上讲，这些不同选择反映了人们多样化的需求、优先考虑和价值观。",
    "另备: Taken together, these views reflect the diversity of public attitudes toward+主题. 综合来看，这些观点反映了公众对…态度的多样性",
    1, "P92")
add("dz-p2-zj-5", DZ, "第二段 · 总结句", "图表数据变化",
    f"{T('Therefore, the change shown in the chart is not accidental but the result of several interconnected factors.')}",
    "因此，图表所显示的变化并非偶然，而是多种相互关联因素共同作用的结果。", None, 2, "P92")
# —— 第三段·总体评价 (P95-96)
add("dz-p3-1", DZ, "第三段 · 总体评价", "正向·版A",
    f"{T('In conclusion,')} {B('主题词')} {T('is essential for both individuals and society.')}",
    "总之，……对个人和社会都是必不可少的。",
    "In conclusion 可替换 To sum up / In summary / Overall; is essential for 可替换 is of great importance to / plays a key role in / is vital for",
    1, "P95")
add("dz-p3-2", DZ, "第三段 · 总体评价", "正向·版B",
    f"{T('Overall,')} {B('主题词')} {T('plays a vital role in promoting personal growth and social progress.')}",
    "总体而言，……在促进个人成长和社会进步方面发挥着重要作用。",
    "promotes 可替换 encourages / facilitates / contributes to",
    1, "P95")
add("dz-p3-3", DZ, "第三段 · 总体评价", "负向·版A",
    f"{T('In conclusion, this issue deserves more attention from the public.')}",
    "总之，这个问题值得公众更多的关注。",
    "deserves more attention 可替换 calls for greater concern / requires immediate attention 亟待重视",
    1, "P95")
add("dz-p3-4", DZ, "第三段 · 总体评价", "负向·版B",
    f"{T('To sum up, effective measures should be taken to prevent this problem from becoming more serious.')}",
    "总之，应当采取有效措施，防止这一问题变得更加严重。",
    "effective measures 可替换 practical measures / concrete action / joint efforts; becoming more serious 可替换 growing worse / continuing to spread",
    1, "P95")
add("dz-p3-5", DZ, "第三段 · 总体评价", "中性·趋势预测A",
    f"{T('In conclusion, this trend is likely to continue in the coming years.')}",
    "总之，这一趋势很可能在未来几年继续下去。",
    "is likely to 可替换 is expected to / will probably / may well",
    1, "P96")
add("dz-p3-6", DZ, "第三段 · 总体评价", "中性·趋势预测B",
    f"{T('With the continued development of')} {B('相关因素')}{T(', an increasing number of people are likely to')} {B('行为')}{T('.')}",
    "随着……的持续发展，越来越多的人可能会……",
    "in the coming years 可替换 in the years ahead / in the near future / in the foreseeable future",
    1, "P96")
# —— 第三段·行动句 (P97-99)
add("dz-p3-xz-1", DZ, "第三段 · 行动句", "正向·基础版",
    f"{T('Therefore, we should develop')} {B('主题品质')} {T('in our daily lives. In this way, we can improve ourselves and achieve our goals.')}",
    "因此，我们应当在日常生活中培养……。这样，我们就能提升自我并实现目标。",
    "develop 可替换 cultivate 培养 / practice 践行; improve ourselves 可替换 make progress / develop our abilities; achieve our goals 可替换 realize our dreams / achieve success",
    1, "P97")
add("dz-p3-xz-2", DZ, "第三段 · 行动句", "正向·进阶版",
    f"{T('It is therefore necessary for us to translate our recognition of')} {B('主题')} {T('into concrete action. Only by integrating it into our daily practice can we achieve personal growth and contribute to social progress.')}",
    "因此，我们有必要将对……的认同转化为具体行动。只有将其融入日常实践，我们才能实现个人成长并推动社会进步。",
    "integrate it into 可替换 apply it to / incorporate it into",
    2, "P97")
add("dz-p3-xz-3", DZ, "第三段 · 行动句", "负向·基础版",
    f"{T('Therefore, we should take effective measures to address this problem. In this way, we can reduce its harmful effects and prevent it from worsening.')}",
    "因此，我们应当采取有效措施解决这一问题。这样，我们就能减少其危害，并防止问题进一步恶化。",
    "take effective measures 可替换 take action / adopt proper measures; address this problem 可替换 solve this problem / deal with this issue",
    1, "P97")
add("dz-p3-xz-4", DZ, "第三段 · 行动句", "负向·进阶版1",
    f"{T('To address this problem, individuals should')} {B('个人措施')}{T(', while')} {B('schools / the government')} {T('should')} {B('社会措施')}{T('. These efforts can help reduce its negative effects and create a healthier social environment.')}",
    "为了解决这一问题，个人应当……，而学校/政府应当……。这些努力有助于减少其负面影响，并营造更加健康的社会环境。",
    "个人措施: control their behavior / develop good habits / raise their awareness / exercise greater self-discipline; 社会措施: offer more support / strengthen public education / provide proper guidance / improve relevant regulations",
    1, "P98")
add("dz-p3-xz-5", DZ, "第三段 · 行动句", "负向·进阶版2",
    f"{T('Joint efforts should be made by individuals and relevant authorities to address the root causes of this problem. Only through coordinated action can we prevent it from causing further damage and bring about lasting improvement.')}",
    "个人和有关部门应当共同努力，从根源上解决这一问题。只有通过协调一致的行动，我们才能防止它造成进一步损害，并实现持久改善。",
    "relevant authorities 可替换 schools / communities / the government; address the root causes 可替换 tackle the problem at its source",
    2, "P98")
add("dz-p3-xz-6", DZ, "第三段 · 行动句", "中性·基础版1",
    f"{T('Therefore, we should view this phenomenon rationally and make proper use of it. In this way,')} {B('主题')} {T('can bring more benefits to')} {B('对象')} {T('while minimizing potential harm.')}",
    "因此，我们应当理性看待这一现象，并对其加以合理利用。这样，……就能为……带来更多益处，同时尽可能减少潜在危害。",
    "make proper use of it 可替换 use it wisely / deal with it properly; bring more benefits 可替换 play a positive role / create greater value",
    1, "P99")
add("dz-p3-xz-7", DZ, "第三段 · 行动句", "中性·基础版2",
    f"{T('Therefore, we should make full use of its advantages while keeping its possible risks under control. With proper guidance, it can develop in a healthier and more sustainable direction.')}",
    "因此，我们应当充分发挥其优势，同时控制可能存在的风险。通过合理引导，它能够朝着更加健康、可持续的方向发展。",
    "make full use of 可替换 take advantage of / bring...into full play; possible risks 可替换 potential problems / negative effects / limitations",
    2, "P99")
add("dz-p3-xz-8", DZ, "第三段 · 行动句", "中性·进阶版",
    f"{T('Rather than accepting or rejecting this trend blindly, we should evaluate it objectively and establish reasonable boundaries for its development. Only when its benefits are maximized and its risks minimized can it truly serve the long-term interests of individuals and society.')}",
    "我们不应盲目接受或排斥这一趋势，而应客观评价，并为其发展设定合理边界。只有充分发挥其优势并尽量降低风险，它才能真正服务于个人和社会的长远利益。",
    "evaluate it objectively 可替换 view it from a balanced perspective / assess it rationally",
    3, "P99")
# —— 第二段·品质哲理类(英一为主, 英二也能用) (P87-88, lvl3)
add("dz-p2-pz-1", DZ, "第二段 · 品质价值(拓展)", "正向价值1",
    f"{T('For one thing, it enables us to')} {B('正向价值1')}{T('.')}",
    "一方面，它使我们能够……",
    "enables 可替换 allows / makes it possible for; 品质×价值搭配: perseverance 坚持→overcome difficulties and keep moving forward / innovation 创新→break free from conventional thinking / responsibility 责任感→fulfill our duties and deal with problems actively",
    3, "P87")
add("dz-p2-pz-2", DZ, "第二段 · 品质价值(拓展)", "正向价值2",
    f"{T('For another, it helps us')} {B('正向价值2')}{T('.')}",
    "另一方面，它帮助我们……",
    "helps 可替换 encourages / motivates",
    3, "P87")

# ============================================================ 30天计划 (4.0学习计划原文)
PLAN = [
  {"day":1,"cat":"xz","title":"小作文格式+总框架(第一段目的、第二段任务、第三段收尾)","book":"P5-17",
   "learn":["xz-p1-gw-1","xz-p1-gw-2","xz-p1-mu-1","xz-p1-mu-2"],
   "practice":["2026英语二答复信,只分析结构"],
   "tip":"格式:称呼Dear+职务/名字+逗号 → 正文三段(段前空两格) → 结束语Yours sincerely,(正式)/Yours,(私人) → 署名Li Ming(右对齐)。三段思路:开头表明目的→中间展开→结尾期待收尾。"},
  {"day":2,"cat":"xz","title":"公务书信开头结尾+私人书信开头结尾","book":"P17-20, P31-33",
   "learn":["xz-p1-sr-1","xz-p1-sr-2","xz-p1-sr-3","xz-p1-sr-4","xz-p3-1","xz-p3-2","xz-p3-3","xz-p3-4"],
   "practice":["2011英语二祝贺信(私人)","2014英语二咨询信(公务):第一、三段真题练习"]},
  {"day":3,"cat":"xz","title":"讲事情类模板:活动主题、时间地点、具体安排","book":"P21-24",
   "learn":["xz-p2-js-1","xz-p2-js-2","xz-p2-js-3","xz-p2-js-4","xz-p2-js-5"],
   "practice":["2013英语二通知,第二段真题练习"]},
  {"day":4,"cat":"xz","title":"讲事情类模板:介绍、答复、感谢、祝贺的替换方法","book":"P24+补充句",
   "learn":["xz-p2-bc-1","xz-p2-bc-2","xz-p2-bc-3","xz-p2-bc-4"],
   "practice":["2010英语二邀请信","2017英语二答复信:第二段真题练习"]},
  {"day":5,"cat":"xz","title":"观点类模板:提出建议或推荐","book":"P24-27",
   "learn":["xz-p2-gd-1"],
   "practice":["2019英语二建议信,第二段真题练习"]},
  {"day":6,"cat":"xz","title":"观点类模板:说明理由和补充好处","book":"P24-27",
   "learn":["xz-p2-gd-2","xz-p2-gd-3","xz-p2-gd-4"],
   "practice":["2020英语二介绍+建议信,第二段真题练习"]},
  {"day":7,"cat":"xz","title":"解决问题类模板:说明问题、原因和影响","book":"P28-30",
   "learn":["xz-p2-jj-1","xz-p2-jj-2","xz-p2-jj-3"],
   "practice":["2012英语二投诉信,第二段真题练习"]},
  {"day":8,"cat":"xz","title":"解决问题类模板:提出补救措施或解决要求","book":"P28-30",
   "learn":["xz-p2-jj-4","xz-p2-jj-5"],
   "practice":["2018英语二道歉信,第二段真题练习"]},
  {"day":9,"cat":"xz","title":"通知告示类写作模板和写作思路","book":"P34-35",
   "learn":[],
   "practice":["2015英语二通知,只分析结构"],
   "tip":"通知格式:标题NOTICE居中 → 日期右对齐 → 正文三段(发布信息→展开信息→提出行动) → 署名右对齐(如The Students' Union)。两大类:活动通知(什么活动/何时何地/如何参加)和招募通知(招募什么/有何要求/如何申请)。"},
  {"day":10,"cat":"xz","title":"通知模板:活动通知","book":"P36-44",
   "learn":["xz-tz-1-1","xz-tz-1-2","xz-tz-1-3","xz-tz-1-4","xz-tz-hd-1","xz-tz-hd-2","xz-tz-hd-3"],
   "practice":["2015英语二通知+2010英语一通知,真题练习"]},
  {"day":11,"cat":"xz","title":"通知模板:招募通知","book":"P36-44",
   "learn":["xz-tz-zm-1","xz-tz-zm-2","xz-tz-zm-3","xz-tz-zm-4","xz-tz-zm-5","xz-tz-3-1","xz-tz-3-2","xz-tz-3-3","xz-tz-3-4"],
   "practice":["2015英语二通知(招募志愿者角度)重写一遍"]},
  {"day":12,"cat":"xz","title":"讲事情类综合训练","book":"复习",
   "learn":[],"review":"讲事情类(①②③+感谢祝贺补充)",
   "practice":["英语二2010/2014/2015/2017真题练习"]},
  {"day":13,"cat":"xz","title":"讲观点类综合训练","book":"复习",
   "learn":[],"review":"观点类(④⑤⑥)",
   "practice":["英语二2011/2016/2019真题练习"]},
  {"day":14,"cat":"xz","title":"解决问题类综合训练","book":"复习",
   "learn":[],"review":"解决问题类(⑦⑧⑨)",
   "practice":["英语二2012/2018真题练习"]},
  {"day":15,"cat":"dz","title":"大作文三段式总框架+图表第一段第一句模板","book":"P60-65, P77-78",
   "learn":["dz-p1-1","dz-p1-2","dz-p1-3"],
   "practice":["2014英语二真题,只分析结构"],
   "tip":"第一天先立三段骨架:第一段总起=引入图表句 → 第二段总起=过渡句(Several factors...) → 第三段总起=总体评价(In conclusion...)。三段句数:第一段2-4句/第二段4-5句/第三段2-3句。后面各天往骨架里填肉:第一段描述句→第二段原因/影响→第三段行动/展望。"},
  {"day":16,"cat":"dz","title":"图表第一段二三句·动态图表模板","book":"P79-80",
   "learn":["dz-p1-dd-1","dz-p1-dd-2","dz-p1-dd-3"],
   "practice":["2017英语二第一段真题练习"]},
  {"day":17,"cat":"dz","title":"动态第一段巩固练习","book":"P79-80",
   "learn":[],
   "practice":["2022英语二第一段真题练习"]},
  {"day":18,"cat":"dz","title":"图表第一段二三句·静态图表模板","book":"P81-82",
   "learn":["dz-p1-jt-1","dz-p1-jt-2","dz-p1-jt-3","dz-p1-jt-4"],
   "practice":["2015英语二第一段真题练习"]},
  {"day":19,"cat":"dz","title":"静态第一段巩固练习","book":"P81-82",
   "learn":[],
   "practice":["2018英语二第一段真题练习"]},
  {"day":20,"cat":"dz","title":"静态第一段巩固练习II","book":"P81-82",
   "learn":[],
   "practice":["2021英语二第一段真题练习"]},
  {"day":21,"cat":"dz","title":"图表第一段·复合图表模板","book":"P83-84",
   "learn":["dz-p1-fh-1","dz-p1-fh-2","dz-p1-fh-3","dz-p1-fh-4","dz-p1-fh-5"],
   "practice":["英语一2024或2026复合图表,迁移训练"]},
  {"day":22,"cat":"dz","title":"现象数据类第二段:宏观原因+个人需求","book":"P87-94",
   "learn":["dz-p2-gd-1","dz-p2-gd-2","dz-p2-yy-1","dz-p2-yy-2"],
   "practice":["2023英语二第二段真题练习"],
   "tip":"第二段槽位顺序=过渡句(gd-2)→宏观原因句(yy-1b流行版/yy-1发展版按题选)→个人需求句(yy-2b全龄版/yy-2按题选)→收尾(zj-1/2/3/5四选一,见次日备选区)。"},
  {"day":23,"cat":"dz","title":"现象数据类第二段:原因+影响+趋势判断","book":"P87-94+补充",
   "learn":["dz-p2-yy-3","dz-p2-yy-4","dz-p2-yy-5","dz-p2-yy-6","dz-p2-yy-7","dz-p2-yy-8","dz-p2-xy-1","dz-p2-xy-2","dz-p2-xy-3","dz-p2-zj-1","dz-p2-zj-2","dz-p2-zj-3"],
   "practice":["2024英语二第二段真题练习"]},
  {"day":24,"cat":"dz","title":"材料观点类第二段:不同选择背后的原因","book":"P90-91",
   "learn":["dz-p1-cl-1","dz-p1-cl-2","dz-p2-gd-3","dz-p2-gd-4","dz-p2-cl-1","dz-p2-cl-2","dz-p2-cl-3","dz-p2-cl-4","dz-p2-cl-5","dz-p2-cl-6","dz-p2-zj-4"],
   "practice":["2026英语二第二段真题练习"]},
  {"day":25,"cat":"dz","title":"正向话题第三段:价值+行动+积极结果","book":"P95-100",
   "learn":["dz-p3-1","dz-p3-2","dz-p3-xz-1","dz-p3-xz-2"],
   "practice":["2024英语二第三段真题练习"]},
  {"day":26,"cat":"dz","title":"负向/争议话题第三段","book":"P95-100",
   "learn":["dz-p3-3","dz-p3-4","dz-p3-xz-3","dz-p3-xz-4","dz-p3-xz-5"],
   "practice":["2018英语二第三段真题练习"]},
  {"day":27,"cat":"dz","title":"中性趋势第三段:理性评价+合理引导","book":"P95-100",
   "learn":["dz-p3-5","dz-p3-6","dz-p3-xz-6","dz-p3-xz-7","dz-p3-xz-8"],
   "practice":["2025英语二第三段真题练习"]},
  {"day":28,"cat":"dz","title":"图表类完整训练·动态图","book":"复习",
   "learn":[],
   "practice":["2010英语二整篇","2011英语二整篇","2014英语二整篇"]},
  {"day":29,"cat":"dz","title":"图表类完整训练·静态图","book":"复习",
   "learn":[],
   "practice":["2012英语二整篇","2013英语二整篇","2015英语二整篇"]},
  {"day":30,"cat":"dz","title":"英语二最终模拟","book":"冲刺",
   "learn":[],
   "practice":["选一套未练过的英语二图表真题,限时30分钟整篇","继续完整练习2010-2026历年完整真题"]},
]

# ============================================================ 精背/备选拆分(用户10-28指出:书的设计是每槽"选一两句",不全背)
# key=原天序(xz1-14,dz15-30); learn=精背主选(计入天完成), skim=备选眼熟(同槽替换,不强制)
LEARN_SKIM = {
  1:  (["xz-p1-gw-1","xz-p1-mu-1"], ["xz-p1-gw-2","xz-p1-mu-2"]),
  2:  (["xz-p1-sr-2","xz-p3-1","xz-p3-2","xz-p3-4"], ["xz-p1-sr-1","xz-p1-sr-3","xz-p1-sr-4","xz-p3-3"]),
  3:  (["xz-p2-js-1","xz-p2-js-2","xz-p2-js-4"], ["xz-p2-js-3","xz-p2-js-5"]),
  4:  (["xz-p2-bc-1","xz-p2-bc-2","xz-p2-bc-3","xz-p2-bc-4"], []),
  5:  (["xz-p2-gd-1"], []),
  6:  (["xz-p2-gd-2","xz-p2-gd-3","xz-p2-gd-4"], []),
  7:  (["xz-p2-jj-1","xz-p2-jj-2","xz-p2-jj-3"], []),
  8:  (["xz-p2-jj-4","xz-p2-jj-5"], []),
  9:  ([], []),
  10: (["xz-tz-1-1","xz-tz-1-3","xz-tz-hd-1","xz-tz-hd-2","xz-tz-hd-3"], ["xz-tz-1-2","xz-tz-1-4"]),
  11: (["xz-tz-zm-1","xz-tz-zm-3","xz-tz-zm-5","xz-tz-3-1","xz-tz-3-3"], ["xz-tz-zm-2","xz-tz-zm-4","xz-tz-3-2","xz-tz-3-4"]),
  12: ([], []), 13: ([], []), 14: ([], []),
  15: (["dz-p1-1","dz-p2-gd-2","dz-p3-1"], ["dz-p1-2","dz-p1-3"]),
  16: (["dz-p1-dd-1","dz-p1-dd-3"], ["dz-p1-dd-2"]),
  17: ([], []),
  18: (["dz-p1-jt-1"], ["dz-p1-jt-2","dz-p1-jt-3","dz-p1-jt-4"]),
  19: ([], []), 20: ([], []),
  21: (["dz-p1-fh-1","dz-p1-fh-2","dz-p1-fh-4"], ["dz-p1-fh-3","dz-p1-fh-5"]),
  22: (["dz-p2-yy-1b","dz-p2-yy-2b"], ["dz-p2-gd-1","dz-p2-yy-1","dz-p2-yy-2"]),
  23: (["dz-p2-xy-1"], ["dz-p2-yy-3","dz-p2-yy-4","dz-p2-yy-5","dz-p2-yy-6","dz-p2-yy-7","dz-p2-yy-8","dz-p2-xy-2","dz-p2-xy-3","dz-p2-zj-1","dz-p2-zj-2","dz-p2-zj-3","dz-p2-zj-5"]),
  24: (["dz-p1-cl-1","dz-p1-cl-2","dz-p2-gd-3","dz-p2-cl-1","dz-p2-cl-4","dz-p2-zj-4"], ["dz-p2-gd-4","dz-p2-cl-2","dz-p2-cl-3","dz-p2-cl-5","dz-p2-cl-6"]),
  25: (["dz-p3-xz-1"], ["dz-p3-2","dz-p3-xz-2"]),
  26: (["dz-p3-3","dz-p3-xz-3"], ["dz-p3-4","dz-p3-xz-4","dz-p3-xz-5"]),
  27: (["dz-p3-5","dz-p3-xz-6"], ["dz-p3-6","dz-p3-xz-7","dz-p3-xz-8"]),
  28: ([], []), 29: ([], []), 30: ([], []),
}
for _d in PLAN:
    _ln, _sk = LEARN_SKIM[_d["day"]]
    assert not (set(_ln) & set(_sk)), "day%d 精背/备选重复" % _d["day"]
    _d["learn"] = _ln
    _d["skim"] = _sk
# lvl 重排: 精背=1(★), 备选=2(◎), 原3级(○眼熟)保留
_learn_ids = {sid for ln, sk in LEARN_SKIM.values() for sid in ln}
_skim_ids = {sid for ln, sk in LEARN_SKIM.values() for sid in sk}
for _s in S:
    if _s["id"] in _learn_ids: _s["lvl"] = 1
    elif _s["id"] in _skim_ids and _s["lvl"] != 3: _s["lvl"] = 2

# ============================================================ 斜杠备选定死(用户10-28:选一个最好的,其余进meta)
SLASH_FIX = {
  "xz-p1-gw-1":  (T("from/at/in"), T("from")),
  "xz-p1-sr-3":  (B("great / wonderful / lovely"), B("wonderful")),
  "xz-p2-js-2":  (T("at/in"), T("in")),
  "xz-p3-1":     (B("sincerely / truly / genuinely"), B("sincerely")),
  "xz-p2-bc-4": ('<span class="blank">me/you</span>', '<span class="blank">me</span>'),
  "xz-p2-bc-4b": ('<span class="blank">confidence/opportunity</span>', '<span class="blank">confidence</span>'),
  "xz-p2-gd-4": ('<span class="blank">visitors/readers</span>', '<span class="blank">visitors</span>'),
  "xz-tz-hd-1": ("held at/in", "held in"),
  "xz-tz-3-1": (B("参加/申请方式"), B("报名方式")),
  "xz-tz-3-3": (B("联系人/组织"), B("联系人")),
  "dz-p1-1":     (B("shows / compares"), B("shows")),
  "dz-p1-2":     (B("reasons / purpose / choices"), B("purpose")),
  "dz-p1-dd-1":  (B("rise / decline"), B("increase")),
  "dz-p1-dd-2":  (T("rose / increased / dropped / fell / stood at"), T("increased")),
  "dz-p1-dd-3":  ("has declined/increased sharply", "has increased sharply"),
  "dz-p1-dd-3b": ("declined/increased markedly", "increased markedly"),
  "dz-p1-jt-1":  (T("is higher than / lower than"), T("is higher than")),
  "dz-p2-yy-2":  ("awareness of / demand for", "awareness of"),
  "dz-p2-gd-2":  (B("phenomenon / trend"), B("trend")),
}
for _s in S:
    if _s["id"] in SLASH_FIX:
        _old, _new = SLASH_FIX[_s["id"]]
        assert _old in _s["en"], "slash fix 不匹配: " + _s["id"]
        _s["en"] = _s["en"].replace(_old, _new)
    if _s["id"] == "dz-p1-dd-3b":  # 占位键: dd-3 的第二处
        pass
# dd-3 有两处斜杠, bc-4 有两处, 单独二次替换
for _s in S:
    if _s["id"] == "dz-p1-dd-3":
        _o2, _n2 = SLASH_FIX["dz-p1-dd-3b"]
        assert _o2 in _s["en"]
        _s["en"] = _s["en"].replace(_o2, _n2)
    if _s["id"] == "xz-p2-bc-4":
        _o2, _n2 = SLASH_FIX["xz-p2-bc-4b"]
        assert _o2 in _s["en"]
        _s["en"] = _s["en"].replace(_o2, _n2)
    if _s["id"] == "xz-tz-3-1":
        _o2, _n2 = '<span class="tpl">through/at</span>', '<span class="tpl">through</span>'
        assert _o2 in _s["en"]
        _s["en"] = _s["en"].replace(_o2, _n2)
    if _s["id"] == "xz-tz-3-3":
        _o2, _n2 = '<span class="tpl">at/via</span>', '<span class="tpl">at</span>'
        assert _o2 in _s["en"]
        _s["en"] = _s["en"].replace(_o2, _n2)
# meta 补充被定死的备选词
_META_APPEND = {
  "xz-p3-1": "sincerely 可替换 truly / genuinely",
  "dz-p1-1": "compares 用于多类对比(如饼图各因素)",
  "dz-p1-2": "purpose 可替换 reasons / choices / elements",
  "dz-p1-dd-1": "increase 可替换 rise / growth;下降用 decline / drop",
  "dz-p1-dd-3": "下降方向: has declined sharply / declined markedly",
  "dz-p1-jt-1": "下降用 is lower than;持平 is the same as",
  "dz-p2-gd-2": "trend 可替换 phenomenon",
  "xz-p2-bc-4": "祝贺信版: enabled you to + given you the opportunity to",
  "xz-p2-gd-4": "推荐书籍/电影/课程时 visitors 换 readers",
  "xz-tz-hd-1": "at 用于具体地点(at the school gate), in 用于室内场所",
}
for _s in S:
    if _s["id"] in _META_APPEND:
        _s["meta"] = (_s.get("meta", "") + ("；" if _s.get("meta") else "") + _META_APPEND[_s["id"]]) or _META_APPEND[_s["id"]]

# zh 同步定死(与英文选择一致)
ZH_FIX = {
  "dz-p2-gd-2": "有几个因素能解释这一趋势。",
  "dz-p1-1": "上述……清楚地展示了……。",
  "dz-p1-dd-1": "在……时间内，……出现了显著的增长（从A到B）。",
  "dz-p1-dd-2": "……（对象）在……（时间）增长到……。",
  "dz-p1-dd-3": "在此期间，……的数量从A急剧增长至B；而……分别从A1、A2显著增长到B1、B2。",
  "dz-p1-jt-1": "A的占比高于B，而……。",
  "dz-p1-jt-4": "A与B之间存在巨大差距。",
  "dz-p2-yy-2": "此外，随着人们对……的意识不断增强，越来越多的人愿意……。",
  "xz-p1-sr-3": "很高兴收到你的来信。",
  "xz-p2-bc-4": "这也使我能够……，并给了我……的信心去……。（感谢信版）",
  "xz-tz-3-1": "感兴趣的同学应于……前通过……报名。",
}
for _s in S:
    if _s["id"] in ZH_FIX:
        _s["zh"] = ZH_FIX[_s["id"]]

# ============================================================ 套用例句(用户10-28:模板没有例句没法背,照书【例】/真题示例补)
EXAMPLES = {
  "dz-p2-yy-1b": ("First, the growing popularity of national fitness has offered people more opportunities to exercise at any time, enabling them to take regular exercise.", "2021英语二健身：首先，全民健身的日益流行给人们提供了更多随时锻炼的机会，使他们能够定期锻炼。"),
  "dz-p2-yy-2b": ("Besides, with the growing awareness of health, people from different age groups are more likely to do sports in their daily lives.", "此外，随着健康意识的增强，不同年龄段的人更有可能在日常生活中运动。（接yy-1b后使用）"),
  "xz-p1-gw-1": ("I am a second-year student from the Department of Literature at your university.", "我是贵校文学系的一名大二学生。"),
  "xz-p1-gw-2": ("As a member of the Students' Union, I have organized several charity sales and volunteer activities on campus.", "作为学生会成员，我曾在校内组织过多次慈善义卖和志愿活动。"),
  "xz-p1-mu-1": ("The purpose of this letter is to invite you to serve as a judge for the upcoming English speech contest.", "本信旨在邀请您担任即将举行的英语演讲比赛的评委。"),
  "xz-p1-mu-2": ("I am writing to offer several suggestions in this regard.", "我写信是想就此提出几点建议。（2007英语一）"),
  "xz-p1-sr-2": ("I hope this letter finds you well. I am writing to recommend one of my favorite movies, The Pursuit of Happyness, to you.", "希望你一切安好。我写信是想向你推荐我最喜欢的电影之一《当幸福来敲门》。（2011英语一）"),
  "xz-p3-1": ("I sincerely hope that you will understand and respect my decision.", "我真诚地希望您能够理解并尊重我的决定。"),
  "xz-p3-4": ("Please let me know your thoughts when convenient.", "方便时请告诉我你的想法。（2011英语一）"),
  "xz-p2-js-1": ("The activity will focus on traditional Chinese culture.", "本次活动将围绕中国传统文化展开。"),
  "xz-p2-js-2": ("Scheduled for May 10 in the school auditorium, it will include a lecture, a group discussion and a cultural performance.", "本次活动定于5月10日在学校礼堂举行，包括讲座、小组讨论和文化表演。"),
  "xz-p2-js-3": ("It is scheduled to take place on October 15 at 14:00 in the lecture hall, and will consist of a keynote speech and an interactive Q&A session.", "活动定于10月15日14点在报告厅举办，由主题演讲和互动问答环节组成。"),
  "xz-p2-js-4": ("Participants will also have the opportunity to exchange ideas with students from different countries.", "参加者还将有机会与来自不同国家的学生交流观点。"),
  "xz-p2-js-5": ("This experience will also enable all participants to develop their practical skills in cross-cultural communication.", "这段经历也将使所有参与者培养跨文化交流的实践能力。"),
  "xz-p2-bc-1": ("Your support with my studies was particularly valuable.", "您在我学习方面给予的支持尤其宝贵。"),
  "xz-p2-bc-2": ("Your success in the competition was particularly impressive.", "你在这次比赛中取得的成功尤其令人钦佩。"),
  "xz-p2-bc-3": ("This support included detailed guidance and warm encouragement, reflecting your kindness and patience.", "这种支持包括详细的指导和热情的鼓励，体现了您的善良和耐心。"),
  "xz-p2-bc-4": ("It has also enabled me to complete the task successfully and given me the confidence to face similar challenges in the future.", "这也使我顺利完成了任务，并给了我面对未来类似挑战的信心。（感谢信版）"),
  "xz-p2-gd-1": ("I strongly recommend the Palace Museum as your first destination in Beijing.", "我强烈推荐你将故宫作为北京之行的第一站。"),
  "xz-p2-gd-2": ("One major reason is that it offers an excellent opportunity to learn about Chinese history and traditional architecture.", "一个主要原因是，它提供了了解中国历史和传统建筑的绝佳机会。"),
  "xz-p2-gd-3": ("More importantly, these qualities will enable him to perform the duties effectively.", "更重要的是，这些品质将使他能够高效履行职责。"),
  "xz-p2-gd-4": ("More importantly, its grand ancient walls and beautiful mountain views allow visitors to enjoy amazing scenery and learn interesting historical stories.", "更重要的是，宏伟的古墙和优美的山景让游客能够欣赏到壮丽的风景，并了解有趣的历史故事。（2020英语二）"),
  "xz-p2-jj-1": ("Unfortunately, I will be unable to attend the meeting as originally planned.", "很遗憾，我无法按原计划参加会议。"),
  "xz-p2-jj-2": ("This is mainly because I have to attend an important examination at the same time.", "这主要是因为我必须在同一时间参加一场重要考试。"),
  "xz-p2-jj-3": ("As a result, I was unable to complete my work and suffered considerable inconvenience.", "因此，我无法完成工作，并遭受了很大不便。"),
  "xz-p2-jj-4": ("To make up for my absence, I will ask a classmate to take notes and send me the relevant materials.", "为了弥补缺席，我会请一位同学做记录，并把相关材料发给我。"),
  "xz-p2-jj-5": ("To resolve the matter, I would appreciate it if you could provide a replacement or offer a full refund.", "为了解决此事，如果您能更换产品或全额退款，我将不胜感激。"),
  "xz-tz-1-1": ("The Students' Union is pleased to announce that a campus book fair will be held.", "学生会很高兴地宣布，将举办校园书展。"),
  "xz-tz-1-2": ("It's a pleasure to inform everyone that an English speech contest will be held in our university.", "很高兴地通知大家，我校将举办英语演讲比赛。"),
  "xz-tz-1-3": ("The purpose of the event is to encourage students to develop an interest in reading.", "本次活动旨在鼓励学生培养阅读兴趣。"),
  "xz-tz-1-4": ("The purpose of this notice is to provide all students with details about the upcoming book fair.", "本通知旨在向全体学生介绍即将举行的书展的具体信息。"),
  "xz-tz-hd-1": ("The event will be held in the school auditorium from 2:00 to 4:00 p.m. on May 10.", "该活动将于5月10日下午2点至4点在学校礼堂举行。"),
  "xz-tz-hd-2": ("All students interested in traditional Chinese culture are welcome to attend.", "欢迎所有喜爱中国传统文化的同学到场参与。"),
  "xz-tz-hd-3": ("Highlights will include a keynote speech, a group discussion and a question-and-answer session.", "本次活动亮点设有主旨演讲、小组讨论以及问答环节。"),
  "xz-tz-zm-1": ("Ideal applicants should be responsible and possess good communication skills.", "理想人选需有责任心，并且具备良好的沟通能力。"),
  "xz-tz-zm-2": ("We are looking for applicants who are patient and have good communication skills.", "我们寻找的申请者需富有耐心，并且掌握良好的沟通能力。"),
  "xz-tz-zm-5": ("The main duties involve receiving guests, offering directions and preparing conference materials.", "主要工作职责包括接待来宾、指引方向以及准备会议资料。"),
  "xz-tz-3-1": ("Those who are interested should register for the event through the school website by May 10.", "感兴趣的同学应于5月10日前通过学校网站报名参加本次活动。"),
  "xz-tz-3-3": ("For further information, please contact the Students' Union at studentsunion@university.edu.", "如需了解更多信息，请通过 studentsunion@university.edu 联系学生会。"),
  "dz-p1-1": ("The pie charts above clearly show the factors that students considered when choosing a university in China in two different years.", "上述饼状图清楚地展示了近两年中国学生选择大学时所考虑的因素。"),
  "dz-p1-2": ("What the pie chart provided is the purpose of mobile reading for students in a certain university.", "该饼状图提供了某高校学生手机阅读目的的调查结果。"),
  "dz-p1-3": ("According to the above bar chart, the percentages of graduates' choices after graduation in a certain university underwent an enormous change from 2013 to 2018.", "根据上面柱状图所示，某高校毕业生去向的百分比在2013至2018年间发生了巨大的变化。"),
  "dz-p1-dd-1": ("There was a remarkable increase in the health literacy level among Chinese residents, from 8.80% in 2012 to 25.40% in 2021.", "2012年至2021年，我国居民健康素养水平显著提高，从8.80%升至25.40%。（2023英语二真题数据）"),
  "dz-p1-dd-2": ("The volume of goods transported by rail increased to 40 million tons in 2002, and then it stood at this level in the rest of the period.", "铁路运输货物的数量2002年增加到了4000万吨，之后就一直保持这一水平。"),
  "dz-p1-dd-3": ("During this period, the percentage of students choosing further education has increased sharply from 26.3% to 34%, whereas those running their own business increased markedly from 1.3% to 2.6%.", "在此期间，选择升学的学生比例从26.3%急剧上升到34%，而自主创业的学生比例也从1.3%显著增长到2.6%。（2019英语二真题数据）"),
  "dz-p1-jt-1": ("The proportion of spending on New Year gifts is higher than that on dinners, transportation and other items, whereas the percentages of the latter three categories are equal to one another.", "新年礼物的花销占比高于聚餐、交通以及其他项目，而后三者的占比持平。（2015英语二）"),
  "dz-p1-jt-2": ("The percentage of males choosing computer science stands at 10%, compared with 4% of females.", "选择计算机专业的男生占10%，相比之下女生仅占4%。"),
  "dz-p1-jt-4": ("There was a huge gap between the proportions of males and females choosing medicine: about 4% for males and 15% for females.", "选择医学专业的男女比例存在巨大差距：男生约4%，女生约15%。"),
  "dz-p1-fh-1": ("The two charts above jointly present the results of a survey concerning consumers' acceptance of elderly-care robots and their primary concerns about such products.", "上述两幅图表共同呈现了一项关于消费者对养老机器人的接受度及对此类产品首要关注点的调查结果。"),
  "dz-p1-fh-2": ("The pie chart shows different levels of public acceptance of elderly-care robots, while the bar chart displays the three main factors that consumers care about most.", "饼图显示了公众对养老机器人不同程度的接受情况，而柱状图展示了消费者最关心的三大主要因素。"),
  "dz-p1-fh-3": ("As can be seen from the two charts, the pie graph illustrates different attitudes towards elderly-care robots, with the bar graph revealing that safety is the top concern.", "从两幅图表中可以看出，饼图说明了人们对养老机器人的不同态度，同时柱状图揭示出安全是首要的关注点。"),
  "dz-p1-fh-4": ("The two sets of data are closely related, as safety concerns may be a major reason for some people's unwillingness to accept elderly-care robots.", "两组数据紧密相关，因为安全顾虑或许是部分人不愿接受养老机器人的主要原因。"),
  "dz-p1-fh-5": ("It is clear that public acceptance of elderly-care robots has a close connection with their attention to product safety and price.", "显而易见，图表反映出公众对养老机器人的接受度与他们对产品安全和价格的关注度有着密切的联系。"),
  "dz-p1-cl-1": ("In the passage, the author argues that failure can be compensated by higher integrity.", "在这篇文章中，作者认为失败可以通过更高的诚信来弥补。"),
  "dz-p1-cl-2": ("In the passage, the author argues that failure can be compensated by higher integrity. I fully agree with this view.", "在这篇文章中，作者认为失败可以通过更高的诚信来弥补。我完全同意这一观点。"),
  "dz-p2-gd-2": ("Several factors can account for this trend. First, the development of the economy has provided local governments with more financial resources.", "有几个因素可以解释这一趋势。首先，经济发展为地方政府提供了更多资金。（英一2024城市公园真题套用）"),
  "dz-p2-yy-1": ("First, the rapid development of technology has provided people with more convenient services, making it easier for them to obtain information.", "首先，科技的快速发展为人们提供了更加便利的服务，使他们更容易获取信息。"),
  "dz-p2-yy-2": ("Besides, with the growing awareness of environmental protection, an increasing number of people are willing to adopt a greener lifestyle.", "此外，随着环保意识不断增强，越来越多的人愿意选择更加环保的生活方式。"),
  "dz-p2-xy-1": ("As a result, this phenomenon can not only weaken individuals' ability to think independently but also increase society's dependence on technology.", "因此，这一现象不仅可能削弱个人独立思考的能力，还可能加深社会对技术的依赖。"),
  "dz-p2-xy-2": ("This trend can improve individuals' quality of life and promote public health.", "这一趋势能够改善个人生活质量，并促进公共健康。"),
  "dz-p2-xy-3": ("This phenomenon may harm individuals' health and increase pressure on the healthcare system.", "这一现象可能损害个人健康，并增加医疗体系的压力。"),
  "dz-p2-cl-1": ("Those who choose not to attend the lecture mainly do so because they believe that a lecture unrelated to their major offers little practical value.", "选择不参加讲座的学生，主要是因为他们认为与专业无关的讲座没有多少实际价值。"),
  "dz-p2-cl-2": ("One major reason why some students focus only on professional courses is that this enables them to use their limited time more efficiently.", "一些学生只专注于专业课程的一个主要原因是，这能使他们更高效地利用有限的时间。"),
  "dz-p2-cl-3": ("From their perspective, skipping an unrelated lecture is a more practical choice, as it helps them concentrate on their professional studies.", "在他们看来，不参加与专业无关的讲座是更加实际的选择，因为这有助于他们专注于专业学习。"),
  "dz-p2-cl-4": ("By contrast, those who attend the lecture tend to attach greater importance to broadening their horizons and acquiring knowledge beyond their major.", "相比之下，参加讲座的学生往往更加重视开阔视野以及获取专业之外的知识。"),
  "dz-p2-cl-5": ("Others, however, choose to attend the lecture because they believe it can introduce them to new ideas and inspire creative thinking.", "然而，另一些学生选择参加讲座，因为他们认为讲座能够使他们接触新观点并激发创新思维。"),
  "dz-p2-cl-6": ("For another group of students, attending the lecture is more attractive, since it provides them with opportunities to explore different fields of knowledge.", "对另一部分学生而言，参加讲座更具吸引力，因为它为他们提供了探索不同知识领域的机会。"),
  "dz-p3-1": ("In conclusion, the awareness of environmental protection is essential for both individuals and society.", "总之，环保意识对个人和社会都至关重要。"),
  "dz-p3-2": ("Overall, perseverance plays a vital role in promoting personal growth and social progress.", "总体而言，坚持在促进个人成长和社会进步方面发挥着重要作用。"),
  "dz-p3-xz-1": ("Therefore, we should develop perseverance in our daily lives. In this way, we can better overcome difficulties and achieve our goals.", "因此，我们应当在日常生活中培养坚持的品质。这样，我们就能更好地克服困难、实现目标。"),
  "dz-p3-xz-6": ("Therefore, we should view this phenomenon rationally and make proper use of it. In this way, AI can bring more benefits to individuals while minimizing potential harm.", "因此，我们应当理性看待这一现象并加以合理利用。这样，人工智能就能为个人带来更多益处，同时尽可能减少潜在危害。"),
}
for _s in S:
    if _s["id"] in EXAMPLES:
        _s["ex"], _s["exz"] = EXAMPLES[_s["id"]]

# ============================================================ 换序(用户拍板2026-10-28:先大作文后小作文)
_dz = [d for d in PLAN if d["cat"] == "dz"]
_xz = [d for d in PLAN if d["cat"] == "xz"]
assert len(_dz) == 16 and len(_xz) == 14, "块数不对"
PLAN = _dz + _xz
for _i, d in enumerate(PLAN, 1):
    d["day"] = _i

# ============================================================ 校验+落盘
ids = [s["id"] for s in S]
assert len(ids) == len(set(ids)), "重复id"
idset = set(ids)
for d in PLAN:
    for sid in d.get("learn", []) + d.get("skim", []):
        assert sid in idset, f"计划引用了不存在的句子: {sid}"
    assert len(d["learn"]) or d.get("review") or d["practice"], f"day{d['day']} 空"

DATA = {
  "meta": {"version": 1, "updated": "2026-10-28", "exam": "2026-12-19",
           "source": "27南山作文模板吃鸡计划(大作文P60-100+小作文P5-44+素材库+补充句+4.0学习计划)",
           "note": "句子由PDF渲染图OCR转录并人工校对; 英二口径, 图画作文(英一)未收, 品质价值句作拓展"},
  "plan": PLAN,
  "sents": S,
}
out = r"D:\考研数学\组卷网站_static\data\zuowen_nanshan.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)
xz_n = sum(1 for s in S if s["cat"]=="xz"); dz_n = len(S)-xz_n
l1 = sum(1 for s in S if s["lvl"]==1)
print(f"OK {len(S)}句 (小作文{xz_n}+大作文{dz_n}), 必背{l1}, 计划{len(PLAN)}天")
print("learn句总数:", sum(len(d["learn"]) for d in PLAN))
