import os
import time
import random
import tkinter as tk

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


def read_english_book(filename):
    with open(filename, 'r') as file:
        return eval(file.read())

Units = read_english_book('english/results/9.txt')

def all_words():
    all_words = []
    for _, word_list in Units.items():
        all_words.extend(word_list)
    return all_words


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

    def __init__(self, words, title='学习英语 - 快速背单词'):
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
        - 切换单词库：Unit1 - Unit14
          0 所有单词
          1 - 9 Unit1 - Unit9
          Ctrl/Control + [0-4] Unit10 - Unit14
        - 切换播放模式：F1 手动（默认），F2 自动，F3 英文-中文，F4 中文-英文
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
            '<F1>': lambda: self.set_play_mode(PlayMode.Manual),
            '<F2>': lambda: self.set_play_mode(PlayMode.Auto),
            '<F3>': lambda: self.set_play_mode(PlayMode.EnglishChinese),
            '<F4>': lambda: self.set_play_mode(PlayMode.ChineseEnglish),
        }

        for key, _ in self.key_event_map.items():
            self.window.bind(key, self.on_key_press)
        self.window.bind('<Configure>', self.on_resize)

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

            unit = Units.get(digit)
            if unit:
                self.set_words(unit)
            elif digit == '0':
                self.set_words(all_words())


    def run(self):
        self.window.after(200, self.next_word)
        # 运行窗口
        self.window.mainloop()

    def quit(self):
        self.window.destroy()

    def say(self):
        Speech.say(self.words[self.current_word_index][0])


if __name__ == '__main__':
    learning_english = LearingEnglish(all_words())
    learning_english.run()
