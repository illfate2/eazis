
from nltk.corpus import wordnet
import nltk

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from functools import partial

import time


def letters_in_the_word(word):
    for i in list(word):
        if i == ' ':
            return False
    return True


def semantic_word_analysis(word):
    start = time.time()
    if letters_in_the_word(word):
        hyponyms = []
        # Кольцо синонимов или синсет - это группа элементов данных, которые считаются семантически эквивалентными
        # для целей поиска информации
        synsets = wordnet.synsets(word)
        word = ''
        # Synset представляет группу лемм, имеющих одинаковый смысл, а лемма представляет собой отдельную словоформу.
        if synsets == []:
            return
        for lemma in synsets[0].lemmas():
            word += lemma.name() + ' '
            if lemma.antonyms():
                word += lemma.antonyms()[0].name() + ' '
        # Получение гиперонимов (более общих сущностей) и гипонимов (частных сущностей) заданного синсета
        for i in synsets[0].hyponyms():
            hyponyms.append(i.lemma_names()[0])
            word += i.lemma_names()[0] + ' '
        for j in synsets[0].hypernyms():
            word += j.lemma_names()[0] + ' '
        return word
    else:
        return ''


class SemanticAnalyzer:
    def __init__(self):
        self.text = ""

    def set_text(self, text):
        self.text = text

    def analyze(self):
        words = nltk.word_tokenize(self.text)
        analyze_res = ""
        for word in words:
            analyze_res += word+": "
            analysis = semantic_word_analysis(word)
            if type(analysis) == str:
                analyze_res += analysis
            analyze_res += "\n"
        return analyze_res


class HelpPopup:
    def __init__(self):
        self.text = '''Необходимо нажать кнопку открыть, затем выбрать файл для анализа.
После этого будет выведен результат'''
        self.label = Label(text=self.text)
        popup_box_layout = BoxLayout(orientation='vertical')
        popup_box_layout.add_widget(self.label)
        self.popup = Popup(content=popup_box_layout)

    def open(self, obj):
        self.popup.open()


class ParserApp(App):
    def build(self):
        self.analysis = SemanticAnalyzer()
        self.help_popup = HelpPopup()
        self.textinput = TextInput(readonly=True)
        vertical = BoxLayout(orientation='vertical')
        b = BoxLayout(orientation='horizontal')
        open_btn = Button(text="open")
        help_btn = Button(text="help")
        open_btn.bind(on_release=self.on_open)
        help_btn.bind(on_release=self.on_help_btn_click)

        b.add_widget(open_btn)
        b.add_widget(help_btn)
        vertical.add_widget(b)
        vertical.add_widget(self.textinput)
        return vertical

    def process(self, filechooser, obj):
        f = open(filechooser.selection[0], 'r')
        text = f.read()
        self.analysis.set_text(text)
        result = self.analysis.analyze()
        self.textinput.text = result

    def on_help_btn_click(self, obj):
        self.help_popup.open(obj)

    def on_open(self, obj):
        layout = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(
            path='/home/illfate/eazis/sentence-analysis')
        layout.add_widget(file_chooser)
        btn = Button(text="open")
        layout.add_widget(btn)

        popup = Popup(content=layout)
        btn.bind(on_release=popup.dismiss)
        btn.bind(on_press=partial(self.process, file_chooser))

        popup.open()


ParserApp().run()

# analyzer = SemanticAnalyzer()
# analyzer.set_text("is")
# analyzer.analysis()
