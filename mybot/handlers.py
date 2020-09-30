import ephem
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import operator
import random
import os

from utilis import  is_cat, key_board

citiles = ['адыгея', "амурск","брянс", "барнаул","владимир","вологда",'галич','геленджик', 'дубна','дно','ейцк',
 'емва','жигулёвск','жердевка',"зеленоград","зверево","иркутск", "иваново","казань", "краснодар",
 "люберцы", "лениногорск","магадан","москва","новгород","норильск","омск", "орел","пермь", 
 "павловск","реутов", "ростов","смоленск", "саратов","тула", "тверь","учта", "уфа","фатеж", 
 "фролово","хабаровск", "хилок","чита", "чехов","шахты", "шилка","щёлкино", "щёкино","электрогорск", 
 "энгельс","югорск", "юрьевец", "ядрин","якутск"]

operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '//': operator.floordiv,
        '%': operator.mod,
        '@': operator.matmul,
        '**': operator.pow
        }

def greet_user(update, context):
    text = 'Вызван /start'
    update.message.reply_text(text,
                              reply_markup = key_board()
                              )
    

# команда, которая выводит, в каком созвездии находиться сейчас планета#
def get_planet(update, context):
    text = update.message.text.split()
    planet = text[-1]
    time = str(datetime.datetime.now()).split()
    
    try:
      searched_planet = getattr(ephem, planet)
      constellation = ephem.constellation(searched_planet(time[0]))
      update.message.reply_text(f"Planet {planet} now in constellation {constellation[1]}")
    except AttributeError:
         text = 'Sorry, this is not a planet. Anyway the time is ' + ', '.join(time)
         update.message.reply_text(text)



#возвращает колличество слов в предложении
def word_count(update, context):
      print(type(update.message.text))
      text1 = update.message.text.split()
      update.message.reply_text(f'{len(text1[1:])} слов(а)')

# возвражает доту ближайшего полнолуния
def next_full_moon (update, context):
      text = update.message.text.split()
      time = text[-1]
      next_full_moon = ephem.next_full_moon(time)
      update.message.reply_text(f"Next fullmun will be at {next_full_moon}")

#простой калькулятор  
def calc (update, context):
    text = update.message.text.replace('/calc', '').replace(' ','')
    symbol = ''
    #находи мат. знаки
    for symbols in text:
        if symbols in operators:
            symbol += symbols
    #делим текст дна цифры
    operator_left, operator_right = text.split(symbol)
    
    #производим вычесления
    try:
        result = operators.get(symbol)(float(operator_left), float(operator_right))
        update.message.reply_text(f"{operator_left} {symbol} {operator_right} = {result}")
    except ZeroDivisionError:
        update.message.reply_text("If you divide by 0 the whole universe will be collapse! So, please dont do that")
    except ValueError:
        update.message.reply_text('Incorrect input, please use numbers')


def cities11(update, context):
    city = context.args[0]
    city = city.lower()
    cities1 = citiles.copy()
    
    last_letter = context.user_data.get('last_letter')
    if not last_letter:
        print(last_letter)
    
    if last_letter == None:
        cities1 = cities1.remove(city)
        context.user_data[city] = city
        my_city = ''
        
        my_city = random.choice([m_c for m_c in citiles if m_c.startswith(city[-1]) if m_c not in context.user_data])
       
        text = f'{city[-1]} - {str(my_city.capitalize())}, Ваш ход'
        update.message.reply_text(text)
        context.user_data['last_letter'] = my_city[-1]
        context.user_data[my_city] = my_city
    
    elif city not in cities1:
        text = 'Я не знаю такого города'
        update.message.reply_text(text)   

    
    elif (city not in context.user_data) and (city in cities1) and (context.user_data['last_letter'] == city[0]):
        cities1 = cities1.remove(city)
        context.user_data[city] = city
        my_city = ''
        
        my_city = random.choice([m_c for m_c in citiles if m_c.startswith(city[-1]) if m_c not in context.user_data])
       
        text = f'{city[-1]} - {str(my_city.capitalize())}, Ваш ход'
        update.message.reply_text(text)
        context.user_data['last_letter'] = my_city[-1]
        context.user_data[my_city] = my_city

    elif context.user_data['last_letter'] != city[0]:
        text = f'Надо написать город, который начинается с {context.user_data["last_letter"]}'
        update.message.reply_text(text)
        
    elif city in context.user_data[city]:
        text = 'Такой город Уже был, попробуй другой город'
        update.message.reply_text(text)
    
    else:
        text = 'Something wrong i can feel that'
        update.message.reply_text(text)
    
    

# повторяет сообщения за юзером
def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def user_coordinates(update, context):
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты: широта {coords['longitude']}, долгота {coords['latitude']}",
        reply_markup = key_board()
    )
    
def check_user_photo(update, context):
    update.message.reply_text("In process")
    os.makedirs('photos1', exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('photos1', f'{user_photo.file_id}.jpg')
    user_photo.download(file_name)
    if is_cat(file_name):
        update.message.reply_text("Cat is found")
        new_filename = os.path.join('photos', f'{user_photo.file_id}.jpg')
        os.rename(file_name, new_filename)
    else:
        update.message.reply_text("It's not a cat")
        os.remove(file_name)
