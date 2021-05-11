import os
import re
from nltk.corpus import wordnet


path = os.getcwd() + '/'


def letters_in_the_word(word):
    for i in list(word):
        if i == ' ':
            return False
    return True


def semantic_analysis(text):
    tree_text = re.sub('-', ',', text)
    if tree_text == '':
        return None
    if letters_in_the_word(tree_text):
        hyponyms = []
        # Кольцо синонимов или синсет - это группа элементов данных, которые считаются семантически эквивалентными
        # для целей поиска информации
        synsets = wordnet.synsets(tree_text)
        text = ''
        # Synset представляет группу лемм, имеющих одинаковый смысл, а лемма представляет собой отдельную словоформу.
        for lemma in synsets[0].lemmas():
            text += lemma.name() + ' '
            if lemma.antonyms():
                text += lemma.antonyms()[0].name() + ' '
        # Получение гиперонимов (более общих сущностей) и гипонимов (частных сущностей) заданного синсета
        for i in synsets[0].hyponyms():
            hyponyms.append(i.lemma_names()[0])
            text += i.lemma_names()[0] + ' '
        for j in synsets[0].hypernyms():
            text += j.lemma_names()[0] + ' '
        return text



