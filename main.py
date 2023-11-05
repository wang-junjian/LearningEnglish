import os
import time
import tkinter as tk
import random
# import playsound

from enum import Enum

class LearningMode(Enum):
    Sequence = 1
    Random = 2

class PlayMode(Enum):
    Manual = 1
    Auto = 2
    EnglishChinese = 3
    ChineseEnglish = 4

class PlayStatus(Enum):
    Start = 1
    End = 2


unit1 = [('textbook', 'n. 教科书；课本'), ('conversation', 'n. 交谈；谈话'), ('aloud', 'adv. 大声地；出声地'), ('pronunciation', 'n. 发音；读音'), ('sentence', 'n. 句子'), ('patient', 'adj. 有耐心的 n. 病人'), ('expression', 'n. 表达（方式）；表示'), ('discover', 'v. 发现；发觉'), ('secret', 'n. 秘密；adj. 秘密的；'), ('fall in love with', '爱上；与⋯⋯相爱'), ('grammar', 'n. 语法'), ('repeat', 'v. 重复；重做'), ('note', 'n. 笔记；记录 v. 注意；指出'), ('pal', 'n. 朋友；伙伴'), ('pattern', 'n. 模式；方式'), ('physics', 'n. 物理；物理学'), ('chemistry', 'n. 化学'), ('partner', 'n. 搭档；同伴'), ('pronounce', 'v. 发音'), ('increase', 'v. 增加；增长'), ('speed', 'n. 速度 v.加速'), ('ability', 'n. 能力；才能'), ('brain', 'n. 大脑'), ('active', 'adj. 活跃的；积极的'), ('attention', 'n. 注意；关注'), ('pay attention to', '注意；关注'), ('connect', 'v. （使）连接；与⋯⋯有联系'), ('connect … with', '把⋯⋯和⋯⋯连接或联系起来'), ('overnight', 'adv. 一夜之间；在夜间'), ('review', 'v. & n. 回顾；复习'), ('knowledge', 'n.知识；学问'), ('wisely', 'adv. 明智地；聪明地'), ('Annie', '安妮（女名）'), ('Alexander Graham Bell', '格雷厄姆 • 贝尔')]
unit2 = [('lantern', 'n. 灯笼'), ('stranger', 'n. 陌生人'), ('relative', 'n. 亲属；亲戚'), ('put on', '增加（体重）；发胖'), ('pound', 'n. 磅（重量单位）；英镑'), ('folk', 'adj. 民间的；民俗的'), ('goddess', 'n. 女神'), ('steal', 'v. (stole ; stolen) 偷；窃取'), ('lay', 'v. (laid; laid) 放置；安放；产（卵）；下（蛋）'), ('lay out', '摆开；布置'), ('dessert', 'n. （饭后）甜点；甜食'), ('garden', 'n. 花园；园子'), ('admire', 'v. 欣赏；仰慕'), ('tie', 'n. 领带 v. 捆；束'), ('haunted', 'a. 有鬼魂出没的；闹鬼的'), ('ghost', 'n. 鬼；鬼魂'), ('trick', 'n. 花招；把戏'), ('treat', 'n. 款待；招待v. 招待；请客'), ('spider', 'n. 蜘蛛'), ('Christmas', 'n. 圣诞节'), ('fool', 'n. 蠢人；傻瓜 v. 愚弄adj. 愚蠢的'), ('lie', 'v. (lay ;lain) 平躺；处于'), ('novel', 'n. （长篇）小说'), ('eve', 'n. （尤指宗教节假日的）前夕；前夜'), ('bookstore', 'n. 书店'), ('dead', 'adj. 死的；失去生命的'), ('business', 'n. 生意；商业'), ('punish', 'v. 处罚；惩罚'), ('warn', 'v. 警告；告诫'), ('present', 'n. 现在；礼物adj. 现在的'), ('nobody', 'pron. 没有人'), ('warmth', 'n. 温暖；暖和'), ('spread', 'v. 传播；展开 n. 蔓延；传播'), ('Macao', '澳门'), ('Chiang Mai', '清迈（泰城市）'), ('Halloween', '万圣节前夕'), ('St. Valentine’s Day', '情人节'), ('Clara', '克拉拉（女名）'), ('Santa Claus', '圣诞老人'), ('Charles Dickens', '查尔斯 • 狄更斯（英）'), ('Scrooge', '斯克鲁奇 n.（非正式）吝啬鬼'), ('Jacob Marley', '雅各布 • 马利')]
unit3 = [('restroom', 'n. （美）洗手间；公共厕所'), ('stamp', 'n. 邮票；印章'), ('postcard', 'n. 明信片'), ('pardon', 'interj. 请再说一遍；'), ('washroom', 'n. 洗手间；厕所'), ('bathroom', 'n. 浴室；洗手间'), ('quick', 'adj. 快的；迅速的'), ('rush', 'v.& n. 仓促；急促'), ('suggest', 'v. 建议；提议'), ('staff', 'n. 管理人员；职工'), ('grape', 'n. 葡萄'), ('central', 'adj. 中心的；中央的'), ('mail', 'v. 邮寄；发电子邮件n. 邮件'), ('east', 'adj. 东方的adv. 向东；n.东方'), ('fascinating', 'a. 迷人的；有吸引力的'), ('convenient', 'a. 便利的；方便的'), ('mall', 'n. 商场；购物中心'), ('clerk', 'n. 职员'), ('corner', 'n. 拐角；角落'), ('polite', 'adj. 有礼貌的；客气的'), ('politely', 'adv. 礼貌地；客气地'), ('speaker', 'n. 讲（某种语言）的人；发言者'), ('request', 'n. 要求；请求'), ('choice', 'n. 选择；挑选'), ('direction', 'n. 方向；方位'), ('correct', 'adj. 正确的；恰当的'), ('direct', 'adj. 直接的；直率的'), ('whom', 'pron. 谁；什么人'), ('address', 'n. 地址；通讯处'), ('faithfully', 'adv. 忠实地；忠诚地'), ('Italian', 'a. 意大利\\人的；n. 意大利人\\语'), ('Kevin', '凯文（男名）'), ('Tim', '蒂姆（男名）')]
unit4 = [('humorous', 'a. 有幽默感的；滑稽的'), ('silent', 'adj. 不说话的；沉默的'), ('helpful', 'adj. 有用的；有帮助的'), ('from time to time', '时常；有时'), ('score', 'n. & v. 得分；打分'), ('background', 'n. 背景'), ('interview', 'v. 采访；面试n.访谈'), ('Asian', 'a. 亚洲的；n. 亚洲人'), ('deal with', '对付 ; 应付'), ('dare', 'v. 敢于；胆敢'), ('private', 'adj. 私人的；私密的'), ('guard', 'n. 警卫；看守v. 守卫；保卫'), ('require', 'v. 需要；要求'), ('European', 'a. 欧洲\\人的'), ('British', 'adj.英国的；英国人的'), ('speech', 'n.讲话；发言'), ('ant', 'n. 蚂蚁'), ('insect', 'n. 昆虫'), ('influence', 'v. & n. 影响'), ('seldom', 'adv. 不常；很少'), ('proud', 'adj. 自豪的；骄傲的'), ('be proud of', '为 ⋯⋯骄傲；感到自豪'), ('absent', 'adj. 缺席；不在'), ('fail', 'v. 失败；未能（做到）'), ('examination', 'n. 考试；审查'), ('boarding school', '寄宿学校'), ('in person', '亲身；亲自'), ('exactly', 'adv. 确切地；精确地'), ('pride', 'n. 自豪；骄傲'), ('take pride in', '为 ⋯⋯感到自豪'), ('grandson', 'n. 孙子；外孙'), ('general', 'a. 普遍的；常规的；总的 n. 将军'), ('introduction', 'n. 介绍'), ('Paula', '葆拉 （女名）'), ('Alfred', '艾尔弗雷德（男名）'), ('Billy', '比利（男名）'), ('Candy', '坎迪（女名）'), ('Jerry', '杰里（男名）；杰丽（女名）'), ('Emily', '埃米莉（女名）')]
unit5 = [('material', 'n. 材料；原料'), ('chopsticks', 'n.筷子'), ('coin', 'n.硬币'), ('fork', 'n.餐叉，叉子'), ('blouse', 'n. （女士）短上衣；衬衫'), ('sliver', 'n.银，银器； adj.银色的'), ('glass', 'n. 玻璃'), ('cotton', 'n.棉；棉花'), ('steel', 'n. 钢；钢铁'), ('grass', 'n. 草；草地'), ('leaf', 'n. 叶，叶子'), ('produce', 'v. 生产；制造；出产'), ('widely', 'adv. 广泛地；普遍地'), ('process', 'v. 加工；处理'), ('France', '法国'), ('no matter', '不论 ;无论'), ('local', 'adj. 当地的；本地的'), ('even though', '虽然；即使'), ('brand', 'n. 品牌；牌子'), ('avoid', 'v. 避免；回避'), ('product', 'n. 产品；制品'), ('handbag', 'n. 小手提包'), ('mobile', 'a. 可移的；非固定的'), ('Germany', 'n. 德国'), ('surface', 'n. 表面；表层'), ('postman', 'n. 邮递员'), ('cap', 'n. （.尤指有帽舌的）帽子'), ('glove', 'n. （分手指的）手套'), ('international', 'adj. 国际的'), ('competitor', 'n. 参赛者；竞争者'), ('paint', 'v. 用颜料画；刷漆'), ('its', 'adj. 它的'), ('form', 'n. 形式；类型'), ('clay', 'n. 黏土；陶土'), ('balloon', 'n. 气球'), ('scissors', 'n. (pl.) 剪刀'), ('lively', 'a. 生气勃勃的;（色彩）鲜艳的'), ('fairy tale', 'n. 童话故事'), ('heat', 'n. 热；高温'), ('polish', 'v.磨光；修改；润色'), ('complete', 'v. 完成'), ('Korea', '朝鲜；韩国'), ('Switzerland', '瑞士'), ('San Francisco', '圣弗朗西斯科（旧金山，美国城市）'), ('Pam', '帕姆（女名）')]
unit6 = [('heel', 'n. 鞋跟；足跟'), ('electricity', 'n. 电；电能'), ('scoop', 'n. 勺; 铲子'), ('style', 'n. 样式; 款式'), ('project', 'n. 项目；工程'), ('pleasure', 'n. 高兴；愉快'), ('zipper', 'n. (= zip) 拉链；拉锁'), ('daily', 'adj. 每日的；日常的'), ('website', 'n. 网站'), ('pioneer', 'n.先锋；先驱'), ('list', 'v. 列表；列清单n. 名单；清单'), ('mention', 'v. 提到；说到'), ('by accident', '偶然；意外地'), ('nearly', 'adv. 几乎；差不多'), ('boil', 'v. 煮沸；烧开'), ('smell', 'n. 气味v. 发出气味；闻到'), ('saint', 'n. 圣人；圣徒'), ('take place', '发生；出现'), ('doubt', 'n. 疑惑；疑问 v. 怀疑'), ('without doubt', '毫无疑问；的确'), ('fridge', 'n.冰箱'), ('translate', 'v. 翻译'), ('lock', 'v. 锁上；锁住'), ('earthquake', 'n. 地震'), ('sudden', 'adj. 突然（的）'), ('all of a sudden', '突然 ; 猛地'), ('biscuit', 'n. 饼干'), ('cookie', 'n. 曲奇饼干'), ('instrument', 'n. 器械；仪器；工具'), ('crispy', 'adj. 脆的；酥脆的'), ('sour', 'adj. 酸的；有酸味的'), ('by mistake', '错误地；无意中'), ('customer', 'n. 顾客；客户'), ('Canadian', 'a. n. 加拿大; 人的'), ('divide', 'v. 分开；分散'), ('divide ... into', '把 ⋯⋯分开'), ('purpose', 'n. 目的；目标'), ('basket', 'n. 篮；筐'), ('the Olympics', '奥林匹克运动会'), ('look up to', '钦佩；仰慕'), ('hero', 'n.英雄；男主角'), ('Berlin', '柏林（德国城市）'), ('NBA', '(National Basketball Association)'), ('CBA', '(China Basketball Association)'), ('Chelsea Lanmon', '切尔西 • 兰曼'), ('Jayce Coziar', '杰斯 • 克里亚'), ('Jamie Ellsworth', '杰米 • 埃尔斯沃恩'), ('Julie Thompson', '朱莉 • 汤普森'), ('Whitcomb Judson', '惠特科姆 • 贾德森'), ('Thomas Watson', '托马斯 • 沃森'), ('George Crum', '乔治 • 克拉姆'), ('James n.ai smith', '詹姆斯 • 奈史密斯')]

words = unit1 + unit2 + unit3 + unit4 + unit5 + unit6


class Speech():
    @staticmethod
    def say(text, voice=None):
        voice_param = f'-v {voice}' if voice else ''
        say_command = f'say {voice_param} {text}'
        os.system(say_command)

    @staticmethod
    def say_zh(text, voice='Tingting'):
        Speech.say(text, voice=voice)

    @staticmethod
    def say_n_times(text, voice=None, n=1, interval=0.5):
        for i in range(n):
            Speech.say(text)
            time.sleep(interval)


class LearingEnglish():
    SPLIT_SYMBOL = '\n\n'

    def __init__(self, words, title='学习英语'):
        self.play_mode = PlayMode.Manual
        self.play_status = PlayStatus.Start
        self.learning_mode = LearningMode.Sequence
        self.words = words
        self.current_word_index = -1
        self.is_show_chinese = True
        self.window = self.create_window(title)
        self.bind_event()
        
        self.after_id = None

    def set_words(self, words):
        self.words = words
        self.current_word_index = 0
        self.show_current_word()

    def set_play_mode(self, play_mode):
        self.play_mode = play_mode
        self.show_current_word()

    def create_window(self, title):
        window = tk.Tk()
        window.title(title)

        # 设置窗口大小
        window.geometry("1200x800")
        # window.state('zoomed')

        # 创建一个标签，用于显示单词
        self.word_label = tk.Label(window, text="")

        # 控件布局
        # 将 english_label 放置在第 0 行
        self.word_label.grid(row=0, sticky='nsew')
        # 设置第 0 行权重为 1，这样它会分配整个窗口的空间
        window.grid_rowconfigure(0, weight=1)
        # 设置第 0 列的权重为 1，这样 label 会占满窗口的宽度
        window.grid_columnconfigure(0, weight=1)    
        
        return window

    def show_help(self):
        help_window = tk.Toplevel(self.window)
        help_window.title("帮助")

        help_text = """
        快捷键：
        - 切换单词库：Unit1-6
        - 切换播放模式：F1 手动，F2 自动，F3 英文中文，F4 中文英文
        - 全屏：z
        - 显示/隐藏中文：u
        - 上一个单词：左箭头，a，空格
        - 下一个单词：右箭头，d
        - 英文发音：p
        - 随机播放：r
        - 顺序播放：s（默认）
        - 显示帮助：h
        - 退出：q
        """
        help_label = tk.Label(help_window, text=help_text, anchor='w', justify='left')
        help_label.pack()

    def next_word(self, step=1):
        # 确保每次只有一个任务在执行，这可以防止任务堆积。
        if self.after_id:
            self.window.after_cancel(self.after_id)
            self.after_id = None

        if ((self.play_mode == PlayMode.EnglishChinese or 
            self.play_mode == PlayMode.ChineseEnglish) and 
            self.play_status == PlayStatus.End):
            pass
        else:
            if self.learning_mode == LearningMode.Sequence:
                self.current_word_index += step
            elif self.learning_mode == LearningMode.Random:
                self.current_word_index = random.randint(0, len(self.words) - 1)

            if self.current_word_index >= len(self.words):
                self.current_word_index = 0
            elif self.current_word_index < 0:
                self.current_word_index = len(self.words) - 1

        self.show_current_word()

    def show_current_word(self):
        english, chinese = self.words[self.current_word_index]

        if self.play_mode == PlayMode.Manual:
            word_text = english
            if self.is_show_chinese:
                word_text = f"{english}{self.SPLIT_SYMBOL}{chinese}"
            self.word_label['text'] = word_text
        elif self.play_mode == PlayMode.Auto:
            word_text = f"{english}{self.SPLIT_SYMBOL}{chinese}"
            self.word_label['text'] = word_text

            """
            在 Python 中，lambda 函数只能包含一个表达式，不能包含多条语句。但是，你可以通过将多个操作组合成一个表达式来绕过这个限制。
            以下是如何在 lambda 函数中同时调用 say 方法和生成一个空格键事件的代码：
            self.window.after(500, lambda: (self.say(), self.window.event_generate('<space>'))[1])
            在这个例子中，(self.say(), self.window.event_generate('<space>')) 是一个元组，
            它包含两个元素：self.say() 的返回值和 self.window.event_generate('<space>') 的返回值。
            [1] 选择了这个元组的第二个元素，也就是 self.window.event_generate('<space>') 的返回值。
            这样，lambda 函数就会先调用 self.say()，然后生成一个空格键事件，最后返回 self.window.event_generate('<space>') 的返回值。
            请注意，这种方法只适用于你不关心 self.say() 的返回值的情况。如果你需要 self.say() 的返回值，你应该使用一个正常的函数，而不是 lambda 函数。
            """
            self.after_id = self.window.after(500, lambda: (self.say(), self.window.event_generate('<space>'))[1])
        elif self.play_mode == PlayMode.EnglishChinese:
            if self.play_status == PlayStatus.Start:
                word_text = english
                self.word_label['text'] = word_text
                self.play_status = PlayStatus.End
            elif self.play_status == PlayStatus.End:
                word_text = chinese
                self.word_label['text'] = word_text
                self.play_status = PlayStatus.Start
        elif self.play_mode == PlayMode.ChineseEnglish:
            if self.play_status == PlayStatus.Start:
                word_text = chinese
                self.word_label['text'] = word_text
                self.play_status = PlayStatus.End
            elif self.play_status == PlayStatus.End:
                word_text = english
                self.word_label['text'] = word_text
                self.play_status = PlayStatus.Start
        
        self.window.update()

    def show_chinese(self):
        self.is_show_chinese = not self.is_show_chinese
        self.show_current_word()

    def on_key_press(self, event):
        try:
            self.key_event_map.get(event.char, lambda: None)()
            self.key_event_map.get(f'<{event.keysym}>', lambda: None)()
        finally:
            pass

    def on_resize(self, event):
        """
        在 Tkinter 中，当你调用 config 方法来改变一个组件的属性时，这可能会触发一个 <Configure> 事件。
        在你的代码中，每次你改变标签的字体大小时，都会触发一个新的 <Configure> 事件，这就导致了 on_resize 函数被不断地调用。
        """
        # 检查事件的类型
        if event.widget == self.window:
            # 计算新的字体大小
            new_font_size = min(int(event.width / 12), int(event.height / 8))
            # 更新标签的字体大小
            self.word_label.config(font=("Arial", new_font_size))

    def bind_event(self):
        self.key_event_map = {
            'h': self.show_help,
            'q': self.quit,
            'z': lambda: self.window.state('zoomed'),
            'u': self.show_chinese,
            'p': self.say,
            's': lambda: setattr(self, 'learning_mode', LearningMode.Sequence),
            'r': lambda: setattr(self, 'learning_mode', LearningMode.Random),
            'd': lambda: self.next_word(),
            '<Right>': lambda: self.next_word(),
            '<space>': lambda: self.next_word(),
            'a': lambda: self.next_word(-1),
            '<Left>': lambda: self.next_word(-1),
            '1': lambda: self.set_words(unit1),
            '2': lambda: self.set_words(unit2),
            '3': lambda: self.set_words(unit3),
            '4': lambda: self.set_words(unit4),
            '5': lambda: self.set_words(unit5),
            '6': lambda: self.set_words(unit6),
            '<F1>': lambda: self.set_play_mode(PlayMode.Manual),
            '<F2>': lambda: self.set_play_mode(PlayMode.Auto),
            '<F3>': lambda: self.set_play_mode(PlayMode.EnglishChinese),
            '<F4>': lambda: self.set_play_mode(PlayMode.ChineseEnglish),
        }

        for key, _ in self.key_event_map.items():
            self.window.bind(key, self.on_key_press)
        self.window.bind('<Configure>', self.on_resize)

    def run(self):
        self.window.after(200, self.next_word)
        # 运行窗口
        self.window.mainloop()

    def quit(self):
        self.window.destroy()

    def say(self):
        Speech.say(self.words[self.current_word_index][0])


if __name__ == '__main__':
    learning_english = LearingEnglish(words)
    learning_english.run()
