import nltk
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from functools import partial

GRAMMAR_RULES = r"""
        P: {<IN>}
        V: {<V.*>}
        N: {<S.*>}
        NP:{<PR>*<A.*|A-PRO><CONJ>*<A.*|A-PRO>*<N|NP>}   
        NP:{<A.*|A-PRO>*<S.*>+<A.*|A-PRO>*} 
        VP: {<V.*>+<NP|N>}
        VP: {<V.*>}
             
        """


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


class TextTreeParser:
    def __init__(self):
        self.text = ""

    def set_text(self, text):
        self.text = text

    def parse(self):
        doc = nltk.word_tokenize(self.text)
        doc = nltk.pos_tag(doc, lang='rus')
        new_doc = []
        for item in doc:
            if item[1] != 'NONLEX':
                new_doc.append(item)
        cp = nltk.RegexpParser(GRAMMAR_RULES)
        return cp.parse(new_doc)


class ParserApp(App):
    def build(self):
        self.parser = TextTreeParser()
        self.help_popup = HelpPopup()
        b = BoxLayout(orientation='horizontal')
        open_btn = Button(text="open")
        help_btn = Button(text="help")
        open_btn.bind(on_release=self.on_open)
        help_btn.bind(on_release=self.on_help_btn_click)

        b.add_widget(open_btn)
        b.add_widget(help_btn)
        return b

    def process(self, filechooser, obj):
        f = open(filechooser.selection[0], 'r')
        text = f.read()
        self.parser.set_text(text)
        self.parser.parse().draw()

    def on_help_btn_click(self, obj):
        self.help_popup.open(obj)

    def on_open(self, obj):
        layout = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(
            path='/home/illfate/eazis/parse-tree')
        layout.add_widget(file_chooser)
        btn = Button(text="open")
        layout.add_widget(btn)

        popup = Popup(content=layout)
        btn.bind(on_release=popup.dismiss)
        btn.bind(on_press=partial(self.process, file_chooser))

        popup.open()


ParserApp().run()
