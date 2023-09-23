import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader

from gtts import gTTS
import gtts.tokenizer.symbols

from decimal import Decimal
import time


gtts.tokenizer.symbols.SUB_PAIRS.append(('−', '引く'))
gtts.tokenizer.symbols.SUB_PAIRS.append(('+', '足す'))
gtts.tokenizer.symbols.SUB_PAIRS.append(('-', 'マイナス'))
gtts.tokenizer.symbols.SUB_PAIRS.append(('=', 'イコール'))


class Calculator(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.flag = False
        self.memory = 0

    def clear(self):
        self.ids.input_field.text = '0'
        self.speak('入力をクリアします')

    def clear_all(self):
        self.ids.input_field.text = '0'
        self.ids.calc_field.text = ''
        self.speak('今までの計算結果をすべて破棄しました')

    def input(self, number):
        if self.flag == True:
            self.ids.input_field.text = ''
            self.flag = False
        prior = self.ids.input_field.text
        if (prior == '0') or (prior == '-0') or (prior == ''):
            self.ids.input_field.text = number
        else:
            self.ids.input_field.text = prior + number
        self.speak(self.ids.input_field.text)

    def calculate(self, sign):
        self.flag = False
        prior = self.ids.calc_field.text
        if (prior == '') and (self.ids.input_field.text == ''):
            None
        elif prior == '':
            self.ids.calc_field.text = self.ids.input_field.text + sign
            self.speak(self.ids.calc_field.text)
        else:
            prior_number = Decimal(prior.strip('+−×÷'))
            if self.ids.input_field.text == '':
                total = prior_number
            else:
                new_number = Decimal(self.ids.input_field.text)
                if '+' in prior:
                    total = prior_number + new_number
                elif '−' in prior:
                    total = prior_number - new_number
                elif '×' in prior:
                    total = prior_number * new_number
                elif '÷' in prior:
                    total = prior_number / new_number
            self.ids.calc_field.text = f'{total}{sign}'
            self.speak(self.ids.calc_field.text)
        self.ids.input_field.text = ''

    def result(self):
        prior = self.ids.calc_field.text
        if prior == '':
            None
        else:
            prior_number = Decimal(prior.strip('+−×÷'))
            new_number = Decimal(self.ids.input_field.text)
            if '+' in prior:
                total = prior_number + new_number
            elif '−' in prior:
                total = prior_number - new_number
            elif '×' in prior:
                total = prior_number * new_number
            elif '÷' in prior:
                total = prior_number / new_number
            self.ids.calc_field.text = ''
            self.speak(prior + self.ids.input_field.text + '=' + str(total))
            self.ids.input_field.text = str(total)
            self.flag = True

    def delete(self):
        self.ids.input_field.text = self.ids.input_field.text[:-1]
        if self.ids.input_field.text == '':
            self.speak('入力はありません')
        else:
            self.speak(self.ids.input_field.text)

    def decimal(self):
        if '.' in self.ids.input_field.text:
            None
        else:
            if self.ids.input_field.text == '':
                self.ids.input_field.text = '0.'
            else:
                self.ids.input_field.text = self.ids.input_field.text + '.'
        self.speak(self.ids.input_field.text + 'てん')

    def add_zeros(self):
        if self.flag == True:
            self.ids.input_field.text = ''
            self.flag = False
        if (self.ids.input_field.text == '') or (self.ids.input_field.text == '0') or (self.ids.input_field.text == '-0'):
            None
        else:
            self.ids.input_field.text = self.ids.input_field.text + '00'
        self.speak(self.ids.input_field.text)

    def plus_minus(self):
        if '-' in self.ids.input_field.text:
            self.ids.input_field.text = self.ids.input_field.text.lstrip('-')
        else:
            self.ids.input_field.text = '-' + self.ids.input_field.text
        try:
            self.speak(self.ids.input_field.text)
        except:
            None

    def add_memory(self):
        self.memory = self.memory + Decimal(self.ids.input_field.text)
        self.speak(f'メモリーに{self.ids.input_field.text}が足されました')

    def subtract_memory(self):
        self.memory = self.memory - Decimal(self.ids.input_field.text)
        self.speak(f'メモリーから{self.ids.input_field.text}が引かれました')

    def clear_memory(self):
        self.memory = 0
        self.speak('メモリーを破棄しました')

    def memory_result(self):
        self.ids.input_field.text = str(self.memory)
        self.speak(f'メモリーの合計は{self.ids.input_field.text}です')

    def speak(self, text):
        tts = gTTS(text=text, lang='ja')
        tts.save('tmp.mp3')
        voice = SoundLoader.load('tmp.mp3')
        voice.play()

class CalculatorApp(App):
    def build(self):
        self.title = 'CalcSimple'
        return Calculator()

    def on_stop(self):
        Calculator.speak(self, 'アプリを終了します')
        time.sleep(3)
        exit()


if __name__ == '__main__':
    CalculatorApp().run()
