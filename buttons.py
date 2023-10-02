#Тут работа с кнопками
from telebot import types

#Функция отправки номера
def num_but():
    #Создаем пространство для кнопок
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #Создать кнопку
    num = types.KeyboardButton('Отправить номер', request_contact=True)
    #Добавить кнопку в пространство
    kb.add(num)
    return kb

#Функция отправки локации
def loc_button():
    # Создаем пространство для кнопок
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #Создаем кнопку
    loc = types.KeyboardButton('Отправить локацию', request_location=True)
    #Добавить кнопку в пространство
    kb.add(loc)
    return kb

