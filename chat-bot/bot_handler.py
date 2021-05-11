import random

import telebot
import os
import json
import text_analyze.dictionary
import text_analyze.similar_words
import text_analyze.check_films

HELPTEXT =  '''   
Для генерации той или иной словоформы по нужным для вас признакам 
используйте следующие условные обозначения(Теги):
https://pymorphy2.readthedocs.io/en/stable/user/grammemes.html
Введите ваше слово с нужными тегами.
Пример: машина, plur gent 
'''

MAINHELP = '''   
I can help you. 
I can help you find words or movies, or we can just chat.
'''

bot = telebot.TeleBot("")
bot_command_key = dict()
path = os.getcwd()

sorry_answer = 'I\'m sorry, I can\'t help you any more'


def get_dialogs():
    with open(path + '/dialog_handler/dialog.json', 'r', encoding='utf-8') as file:
        data = file.read().strip()

    return json.loads(data)


def get_patterns():
    with open(path + '/patterns/patterns.json', 'r', encoding='utf-8') as file:
        data = file.read().strip()

    pattern_name_to_items = dict()
    for pattern in json.loads(data):
        pattern_name_to_items[pattern['name']] = pattern['items']
    return pattern_name_to_items


patterns = get_patterns()


@bot.message_handler(commands=['start'])
def start_message_handler(message):
    bot.send_message(message.chat.id, 'Hello, can I help you?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message_handler(message):
    bot.send_message(message.chat.id, MAINHELP, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global bot_command_key
    key = False
    if 'form' in message.text.lower():
        bot_command_key[message.chat.id] = 'form'
        bot.send_message(message.chat.id, HELPTEXT)
    elif 'similar words' in message.text.lower():
        bot_command_key[message.chat.id] = 'word'
        bot.send_message(message.chat.id, "Enter a word")
    elif 'pattern' in message.text.lower() and 'get' in message.text.lower():
        bot_command_key[message.chat.id] = 'pattern'
        bot.send_message(message.chat.id, "What pattern do you want?")
    elif message.chat.id in bot_command_key and len(bot_command_key[message.chat.id]) > 0:
        if bot_command_key[message.chat.id] == 'form':
            answer = text_analyze.dictionary.generate_form(message.text)
            bot.send_message(message.chat.id, "Your word is " + answer)
        elif bot_command_key[message.chat.id] == 'word':
            bot.send_message(message.chat.id, text_analyze.similar_words.semantic_analysis(message.text))
        elif bot_command_key[message.chat.id] == 'pattern':
            bot.send_message(message.chat.id, "List of patterns:")
            separator = ', '
            bot.send_message(message.chat.id, separator.join(patterns[message.text.lower()]))
        bot_command_key[message.chat.id] = ''
    elif not key:
        dialogs = get_dialogs()
        answer_key = False
        for dialog in dialogs:
            if message.text.lower() in dialog['question'].lower():
                answer_key = True
                answers = list(dialog['answer'].split('|'))
                bot.send_message(message.chat.id, answers[random.randint(0, len(answers) - 1)])
                break
        if answer_key is False:
            bot.send_message(message.chat.id, sorry_answer)


keyboard = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyboard.row('Get a form of Russian word')
keyboard.row('Get a similar words')
keyboard.row('Get a microservice pattern')
