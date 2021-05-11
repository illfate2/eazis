from pymorphy2 import MorphAnalyzer
import re


def generate_form(text):
    global generated_form
    analyzer = MorphAnalyzer()
    lemma_text = re.match(r'\W*(\w[^,. !?"]*)', text).groups()[0]
    lemma_for_generate = analyzer.parse(lemma_text)[0]
    tags_text = re.sub(r'^\W*\w+\W*', ',', text)
    s = tags_text
    tags_for_generate = s.replace(',', '').split()
    if lemma_text or tags_text:
        started_temporary_generated_form = lemma_for_generate.inflect({tags_for_generate[0]})
        for i in range(len(tags_for_generate)):
            over_temporary_generated_form = started_temporary_generated_form.inflect({tags_for_generate[i]})
            generated_form = over_temporary_generated_form
    return generated_form.word
