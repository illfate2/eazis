from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from pymorphy2 import MorphAnalyzer
from collections import OrderedDict
from nltk import word_tokenize
from kivy.uix.dropdown import DropDown
from collections import OrderedDict
from functools import partial
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.filechooser import FileChooserListView
import json


class TextMorhProcessor:
    def __init__(self):
        self.text = ""
        self.word_to_analysis = {}
        self.lexema_counter = OrderedDict()
        self.wordform_counter = OrderedDict()

    def set_text(self, text):
        self.text = text

    def set_word_analysis(self, word, analysis):
        self.word_to_analysis[word] = analysis

    def reset(self):
        self.lexema_counter = OrderedDict()
        self.wordform_counter = OrderedDict()

    def process(self):
        analyzer = MorphAnalyzer()
        for w in word_tokenize(self.text):
            parsed = analyzer.parse(w)
            if parsed[0].tag.POS == None:
                continue
            self.wordform_counter[w] = self.wordform_counter.get(w, 0)+1
            if w not in self.word_to_analysis:
                self.word_to_analysis[w] = parsed[0].tag.cyr_repr

            self.lexema_counter[parsed[0].normal_form] = self.lexema_counter.get(
                parsed[0].normal_form, 0)+1
        formatted_wordforms = ''
        for word, count in self.wordform_counter.items():
            formatted_wordforms += str(word)+", число повторений: "+str(count)+", анализ: " + \
                self.word_to_analysis[word]+"\n"
        formatted_lexems = ''
        for word, count in self.lexema_counter.items():
            formatted_lexems += str(word) + \
                ", число повторений: " + str(count)+"\n"
        return "лексемы:\n"+str(formatted_lexems)+"\nсловоформа:\n"+formatted_wordforms


class BaseDropdown:
    def __init__(self, name, dropdown_words):
        self.dropdown_words = dropdown_words
        self.drop_down = DropDown()
        for part in dropdown_words:
            btn = Button(text=part, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.drop_down.select(btn.text))
            self.drop_down.add_widget(btn)

        buttons_layout = BoxLayout(orientation='horizontal')
        self.mainbutton = Button(text=name, size_hint=(None, None))
        self.mainbutton.bind(on_release=self.drop_down.open)

        self.drop_down.bind(on_select=lambda instance,
                            x: setattr(self.mainbutton, 'text', x))

    def get(self):
        return self.mainbutton

    def string(self):
        return self.mainbutton.text


class AnimDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(self, "одушвленность", ["од", "неуд"])


class GenderDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(self, "род", ["жр", "мр", "ср", "мж"])


class NumberDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(self, "число", ["ед", "мн"])


class CaseDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(
            self, "падеж", ["им", "рд", "дт", "вн", "тв", "пр"])


class TrnsDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(self, "переходность", ["перех", "неперех"])


class AspcDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(self, "вид", ["сов", "несов"])


class PersDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(self, "лицо", ["1л", "2л", "3л"])


class TensDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(self, "время", ["наст", "прош", "буд"])


class MoodDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(self, "накл", ["изъяв", "повел"])


class VoicDropdown(BaseDropdown):
    def __init__(self):
        BaseDropdown.__init__(self, "залог", ["действ", "страд"])


class PartOfSpeechLayout:
    def __init__(self, dropdowns):
        self.layout = BoxLayout(orientation='horizontal')
        for dropdown in dropdowns:
            self.layout.add_widget(dropdown.get())
        self.dropdowns = dropdowns

    def get(self):
        return self.layout

    def string(self):
        str = ''
        for dropdown in self.dropdowns:
            str += dropdown.string()+', '
        return str


class NounLayout(PartOfSpeechLayout):
    def __init__(self):
        PartOfSpeechLayout.__init__(self, [
            AnimDropdown(), GenderDropdown(), NumberDropdown(), CaseDropdown(), PersDropdown()])


class AdjfLayout(PartOfSpeechLayout):
    def __init__(self):
        PartOfSpeechLayout.__init__(self, [
            GenderDropdown(), NumberDropdown(), CaseDropdown(), PersDropdown()])


class VerbLayout(PartOfSpeechLayout):
    def __init__(self):
        PartOfSpeechLayout.__init__(self, [
            GenderDropdown(), NumberDropdown(), PersDropdown(), TensDropdown(), MoodDropdown()])


class HelpPopup:
    def __init__(self):
        self.text = '''Необходимо ввести в верхней части текст, который надо обработать.
После нажания кнопки запуска процесса, в нижней текстовой области появится разбор текста.
Также есть возмость задать предустановленную и в свободной форме заданнуой форме характеристику'''
        self.label = Label(text=self.text)
        popup_box_layout = BoxLayout(orientation='vertical')
        popup_box_layout.add_widget(self.label)
        self.popup = Popup(content=popup_box_layout)

    def open(self, obj):
        self.popup.open()


class CustomCharPopup:
    def __init__(self, text_processor):
        self.text_processor = text_processor
        self.custom_word_input = TextInput(text='ворон')
        self.custom_word_char = TextInput(text='ворона')
        self.custom_popup_box_layout = BoxLayout(orientation='vertical')

        self.popup = Popup(content=self.custom_popup_box_layout)

        close_btn = Button(text='Close!')
        submit_btn = Button(text='Submit!')

        buttons_layout = BoxLayout(orientation='horizontal')
        self.custom_popup_box_layout.add_widget(self.custom_word_input)
        self.custom_popup_box_layout.add_widget(self.custom_word_char)
        self.custom_popup_box_layout.add_widget(buttons_layout)
        close_btn.bind(on_press=self.popup.dismiss)
        submit_btn.bind(on_press=self.popup.dismiss)
        submit_btn.bind(on_press=self.on_custom_submit)
        buttons_layout.add_widget(submit_btn)
        buttons_layout.add_widget(close_btn)

    def open(self, obj):
        self.popup.open()

    def on_custom_submit(self, obj):
        self.text_processor.set_word_analysis(
            self.custom_word_input.text, self.custom_word_char.text)


class DefinedCharPopup:
    def __init__(self, text_processor):
        self.text_processor = text_processor
        self.word_input = TextInput(text='Input your ')
        self.drop_down = DropDown()
        part_of_speech_btns = ["noun", "adjective", "verb"]
        for part in part_of_speech_btns:
            btn = Button(text=part, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.drop_down.select(btn.text))
            self.drop_down.bind(on_select=self.on_select)
            self.drop_down.add_widget(btn)

        box_layout = BoxLayout(orientation='vertical')
        close_btn = Button(text='Close!')
        submit_btn = Button(text='Submit!')
        box_layout.add_widget(self.word_input)
        buttons_layout = BoxLayout(orientation='horizontal')
        buttons_layout.add_widget(submit_btn)

        buttons_layout.add_widget(close_btn)

        mainbtn_layot = RelativeLayout()
        mainbutton = Button(text='speech part',
                            size_hint=(None, None), pos=(335, 35))
        mainbutton.bind(on_release=self.drop_down.open)

        self.part_of_speech_char_layout = BoxLayout(orientation='horizontal')
        mainbtn_layot.add_widget(mainbutton)
        box_layout.add_widget(mainbtn_layot)
        box_layout.add_widget(self.part_of_speech_char_layout)

        self.drop_down.bind(on_select=lambda instance,
                            x: setattr(mainbutton, 'text', x))
        box_layout.add_widget(buttons_layout)
        self.popup = Popup(content=box_layout)
        close_btn.bind(on_press=self.popup.dismiss)
        submit_btn.bind(on_press=self.on_sumbit)
        self.part_of_speech_layout = None
        self.speach_part_to_layout = {
            'noun': NounLayout(),
            'adjective': AdjfLayout(),
            'verb': VerbLayout()}

    def on_sumbit(self, obj):
        self.popup.dismiss()
        self.text_processor.set_word_analysis(
            self.word_input.text, self.part_of_speech_layout.string())

    def open(self, obj):
        self.popup.open()

    def on_select(self, obj, x):
        if self.part_of_speech_layout != None:
            self.part_of_speech_char_layout.remove_widget(
                self.part_of_speech_layout.get())
        self.part_of_speech_layout = self.speach_part_to_layout[x]
        self.part_of_speech_char_layout.add_widget(
            self.part_of_speech_layout.get())


class NLApp(App):
    def build(self):
        self.text_processor = TextMorhProcessor()
        self.custom_char_popup = CustomCharPopup(self.text_processor)
        self.defined_char_popup = DefinedCharPopup(self.text_processor)
        self.help_popup = HelpPopup()

        b = BoxLayout(orientation='vertical')
        textinput = TextInput(
            text='Ворон к ворону летит Ворон ворону кричит Ворон! Где б нам отобедать')
        self.textinput = textinput
        text_output = TextInput(text='', readonly=True)
        self.text_output = text_output
        options_layout = BoxLayout(orientation='horizontal')

        h = BoxLayout(orientation='horizontal')
        button = Button(text='Process')
        add_custom = Button(text='Add custom word analysis')
        add_custom.bind(on_press=self.on_add_custom_btn_click)

        add_concrete = Button(text='Add concrete word analysis')
        add_concrete.bind(on_press=self.on_add_concrete_btn_click)
        button.bind(on_press=self.on_process_click)

        help_btn = Button(text="Help")
        help_btn.bind(on_press=self.on_help_btn_click)

        save_btn = Button(text="Save dictinary")
        save_btn.bind(on_release=self.save_dict)

        load_btn = Button(text="Load dictinary")
        load_btn.bind(on_release=self.load_dict)

        h.add_widget(button)
        h.add_widget(add_custom)
        h.add_widget(add_concrete)
        options_layout.add_widget(help_btn)
        options_layout.add_widget(save_btn)
        options_layout.add_widget(load_btn)
        b.add_widget(textinput)
        b.add_widget(options_layout)
        b.add_widget(h)
        b.add_widget(text_output)

        return b

    def on_process_click(self, obj):
        self.text_processor.set_text(self.textinput.text)
        self.text_output.text = self.text_processor.process()
        self.text_processor.reset()

    def save_dict(self, obj):
        self.fileChooser.path
        self.fileChooser.selection

    def on_add_custom_btn_click(self, obj):
        self.custom_char_popup.open(obj)

    def on_add_concrete_btn_click(self, obj):
        self.defined_char_popup.open(obj)

    def on_help_btn_click(self, obj):
        self.help_popup.open(obj)

    def load_dict(self, obj):
        layout = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path='/home/')
        layout.add_widget(file_chooser)
        btn = Button(text="load")
        btn.bind(on_release=partial(self.on_load_btn, file_chooser))
        layout.add_widget(btn)

        popup = Popup(content=layout)
        btn.bind(on_release=popup.dismiss)

        popup.open()

    def on_load_btn(self, file_chooser, obj):
        f = open(file_chooser.selection[0], 'r')
        self.text_processor.word_to_analysis = json.loads(f.read())

    def save_dict(self, obj):
        layout = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path='/home/')
        file_chooser.dirselect = True
        layout.add_widget(file_chooser)
        btn = Button(text="save")

        textinput = TextInput()

        popup = Popup(content=layout)
        btn.bind(on_release=partial(self.on_save_btn, file_chooser, textinput))
        btn.bind(on_release=popup.dismiss)
        layout.add_widget(textinput)
        layout.add_widget(btn)

        popup.open()

    def on_save_btn(self, file_chooser, textinput, obj):
        f = open(file_chooser.selection[0] + "/" + textinput.text, 'w')
        f.write(json.dumps(self.text_processor.word_to_analysis))
        f.close()


NLApp().run()
