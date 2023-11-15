import os
import re
import random
import tkinter as tk

from enum import Enum
from multiprocessing import Process, Lock


def remove_chars(text):
    return re.sub(r'^.*\. ', '', text)

class LearningMode(Enum):
    Sequence = 1
    Random = 2

class PlayMode(Enum):
    Manual = 1
    Auto = 2
    EnglishChinese = 3
    ChineseEnglish = 4
    ChinesePlay = 5

class PlayStatus(Enum):
    Start = 1
    End = 2


class Speaker():
    def __init__(self):
        self.lock = Lock()
        self.process = None

    def run(self, text, voice):
        with self.lock:
            voice_param = f'-v {voice}' if voice else ''
            say_command = f'say {voice_param} "{text}"'
            os.system(say_command)

    def stop(self):
        if self.process and self.process.is_alive():
            self.process.terminate()

    # Daniel Zoe Ava
    def say(self, text, voice='Ava'):
        self.process = Process(target=self.run, args=(text, voice))
        self.process.start()
        self.process.join()

    def say_chinese(self, text, voice='Tingting'):
        self.say(text, voice=voice)


class LearingEnglish():
    SPLIT_SYMBOL = '\n\n'

    def __init__(self, title='学习英语 - 快速背单词'):
        self.speaker = Speaker()
        self.play_mode = PlayMode.Manual
        self.play_status = PlayStatus.Start
        self.learning_mode = LearningMode.Sequence
        self.words = None
        self.current_word_index = -1
        self.is_show_chinese = True
        self.window = self.create_window(title)
        self.create_menu()
        self.bind_event()
        self.after_id = None


    def read_english_book(self, filename):
        with open(filename, 'r') as file:
            return eval(file.read())

    def all_words(self, units):
        all_words = []
        for _, word_list in units.items():
            all_words.extend(word_list)
        return all_words

    def set_words(self, words):
        self.words = words
        self.current_word_index = 0
        self.show_current_word()

    def set_play_mode(self, play_mode):
        self.play_mode = play_mode
        self.show_current_word()

    def get_current_word(self):
        return self.words[self.current_word_index]
    
    def set_text_widget(self, text):
        self.text_widget.config(state=tk.NORMAL)    # 设置为可编辑
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert(tk.END, text)
        self.text_widget.tag_configure("center", justify='center')  # 创建一个名为 "center" 的标签，设置其 justify 选项为 'center'
        self.text_widget.tag_add("center", '1.0', tk.END)           # 将 "center" 标签应用到所有的文本
        self.text_widget.config(state=tk.DISABLED)  # 设置为不可编辑

    def create_menu(self):
        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        self.wordbook_var = tk.StringVar()  # 创建一个 StringVar，用于存储当前选择的单词本
        for filename in os.listdir('wordbook'):
            filemenu.add_radiobutton(label=filename, variable=self.wordbook_var, 
                                     command=lambda: self.load_words(f'wordbook/{self.wordbook_var.get()}'))
        menubar.add_cascade(label="单词本", menu=filemenu)
        self.window.config(menu=menubar)
        
        # 模拟点击第一个菜单项，加载第一个单词本
        filemenu.invoke(0)

    def load_words(self, filename):
        self.Units = self.read_english_book(filename)
        self.words = self.all_words(self.Units)
        self.current_word_index = -1
        self.show_current_word()

    def create_window(self, title):
        window = tk.Tk()
        window.title(title)

        # 设置窗口大小
        window.geometry("1200x800")
        # window.state('zoomed')

        # 创建一个 Text，用于显示单词，禁用编辑功能。
        self.text_widget = tk.Text(window, 
                                   wrap=tk.WORD, 
                                   state=tk.DISABLED,
                                   font=("Arial", 72))

        # 控件布局
        # 将 english_label 放置在第 0 行
        self.text_widget.grid(row=0, sticky='nsew', pady=100)
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
        - 切换单词库：Unit1 - Unit14
          0 所有单词
          1 - 9 Unit1 - Unit9
          Ctrl/Control + [0-4] Unit10 - Unit14
        - 切换播放模式：F1 手动（默认），F2 自动，F3 英文-中文，F4 中文-英文，F5 中文播放（听写模式）
        - 切换学习模式：s 顺序（默认），r 随机
        - 全屏：z
        - 显示/隐藏中文：u
        - 上一个单词：左箭头，a，空格
        - 下一个单词：右箭头，d
        - 英文发音：p
        - 显示帮助：h
        - 退出：q
        """
        help_label = tk.Label(help_window, text=help_text, anchor='w', justify='left')
        help_label.pack()

    def show_config(self, event):
        pass

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
        english, chinese = self.get_current_word()

        if self.play_mode == PlayMode.Manual:
            word_text = english
            if self.is_show_chinese:
                word_text = f"{english}{self.SPLIT_SYMBOL}{chinese}"
            self.set_text_widget(word_text)
        elif self.play_mode == PlayMode.Auto:
            word_text = f"{english}{self.SPLIT_SYMBOL}{chinese}"
            self.set_text_widget(word_text)
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
                self.set_text_widget(english)
                self.play_status = PlayStatus.End
            elif self.play_status == PlayStatus.End:
                self.set_text_widget(chinese)
                self.play_status = PlayStatus.Start
        elif self.play_mode == PlayMode.ChineseEnglish:
            if self.play_status == PlayStatus.Start:
                self.set_text_widget(chinese)
                self.play_status = PlayStatus.End
            elif self.play_status == PlayStatus.End:
                self.set_text_widget(english)
                self.play_status = PlayStatus.Start
        elif self.play_mode == PlayMode.ChinesePlay:
            self.set_text_widget(chinese)
            # 等待播放两次英文、两次中文后结束
            self.after_id = self.window.after(500, lambda: (self.say(2), self.say_chinese(2), self.window.event_generate('<space>'))[2])
        
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
            # # 计算新的字体大小
            # new_font_size = min(int(event.width / 12), int(event.height / 8))
            # # 更新标签的字体大小
            # self.word_label.config(font=("Arial", new_font_size))

            # # 获取需要显示的文本
            # english, chinese = self.get_current_word()
            # # 计算新的字体大小
            # new_font_size = int(event.width*2 / max(len(english), len(chinese)))
            # # 更新标签的字体大小
            # self.text_widget.config(font=("Arial", new_font_size))

            pass

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
            '<F1>': lambda: self.set_play_mode(PlayMode.Manual),
            '<F2>': lambda: self.set_play_mode(PlayMode.Auto),
            '<F3>': lambda: self.set_play_mode(PlayMode.EnglishChinese),
            '<F4>': lambda: self.set_play_mode(PlayMode.ChineseEnglish),
            '<F5>': lambda: self.set_play_mode(PlayMode.ChinesePlay),
        }

        for key, _ in self.key_event_map.items():
            self.window.bind(key, self.on_key_press)
        self.window.bind('<Configure>', self.on_resize)
        self.window.bind('<Command-comma>', self.show_config)
        self.window.bind('<Key>', self.on_set_word)

    def on_set_word(self, event):
        """
        Unit number 快捷键
        0 : 所有单元
        n : 第 n 单元
        Ctrl + n : 第 1n 单元
        """

        if event.char and str.isdigit(event.char):
            single_digit = event.char
            tens_digit = '1' if event.state == 4 else '' # Control 的按键为 4
            digit = f'{tens_digit}{single_digit}'

            unit = self.Units.get(digit)
            if unit:
                self.set_words(unit)
            elif digit == '0':
                self.set_words(self.all_words())


    def run(self):
        self.window.after(200, self.next_word)
        # 运行窗口
        self.window.mainloop()

    def quit(self):
        self.window.destroy()

    def say(self, n=1):
        for _ in range(n):
            self.speaker.say(self.words[self.current_word_index][0])

    def say_chinese(self, n=1):
        for _ in range(n):
            chinese = self.words[self.current_word_index][1]
            self.speaker.say_chinese(remove_chars(chinese))

if __name__ == '__main__':
    learning_english = LearingEnglish()
    learning_english.run()
