import random
import os

path = os.getcwd() + '/patterns/'


def find_films(message):
    if message.find('detective') != -1 or message.find('detectives') != -1:
        genre = "detectives"
        DIR = path+'/'+genre
        return open(os.path.join(DIR, random.choice(os.listdir(DIR))), 'rb')
    elif message.find('cartoon') != -1 or message.find('cartoons') != -1:
        genre = "cartoons"
        DIR = path+'/'+genre
        return open(os.path.join(DIR, random.choice(os.listdir(DIR))), 'rb')
    elif message.find('comedy') != -1 or message.find('comedies') != -1:
        genre = "comedy"
        DIR = path+'/'+genre
        return open(os.path.join(DIR, random.choice(os.listdir(DIR))), 'rb')
    elif message.find('horror') != -1 or message.find('horrors') != -1:
        genre = "horrors"
        DIR = path+'/'+genre
        return open(os.path.join(DIR, random.choice(os.listdir(DIR))), 'rb')
    elif message.find('magic') != -1 or message.find('fantastic') != -1:
        genre = "magic"
        DIR = path+'/'+genre
        return open(os.path.join(DIR, random.choice(os.listdir(DIR))), 'rb')
    elif message.find('romans') != -1 or message.find('romantic') != -1:
        genre = "romans"
        DIR = path+'/'+genre
        return open(os.path.join(DIR, random.choice(os.listdir(DIR))), 'rb')
    elif message.find('trillers') != -1 or message.find('triller') != -1:
        genre = "triller"
        DIR = path+'/'+genre
        return open(os.path.join(DIR, random.choice(os.listdir(DIR))), 'rb')
    else:
        return open(path+'error.jpg', 'rb')



