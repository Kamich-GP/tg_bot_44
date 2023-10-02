#Тут основная работа с ботом
import telebot, buttons as bt, database as db
from geopy import Nominatim

#Создаем объект бота
bot = telebot.TeleBot('Ваш токен')
#Использование карт
geolocator = Nominatim(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
#Обработка команды старт
@bot.message_handler(commands=['start'])
def start_message(message):
    #Берем id пользователя
    user_id = message.from_user.id
    #Проверка на наличие юзера
    check_user = db.checker(user_id)
    #Если есть
    if check_user:
        bot.send_message(user_id, 'Добро пожаловать!')
    #Если нет
    else:
        bot.send_message(user_id, 'Добро пожаловать!\n'
                                'Давайте начнем регистрацию! Введите имя')
        #Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)

#Этап получения имени
def get_name(message):
    #Взяли имя пользователя
    user_name = message.text
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отлично! Теперь номер', reply_markup=bt.num_but())
    #Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)

#Этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id
    #Проверяем, отправлен ли номер по кнопке
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'Супер, теперь локацию!',
                         reply_markup=bt.loc_button())
        #Переход на этап получения локации
        bot.register_next_step_handler(message, get_loc, user_name, user_num)
    #Если отправил не через кнопку
    else:
        bot.send_message(user_id, 'Отправьте номер, используя кнопку!')
        bot.register_next_step_handler(message, get_num, user_name)

#Этап получения локации
def get_loc(message, user_name, user_num):
    user_id = message.from_user.id
    #Проверяем, отправил ли локацию по кнопке
    if message.location:
        user_loc = geolocator.reverse(f'{message.location.longitude},'
                                      f'{message.location.latitude}')
        #Регистрируем юзера
        db.register(user_id, user_name, user_num, user_loc)
        bot.send_message(user_id, 'Регистрация успешно завершена!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    #Если же отправил не по кнопке
    else:
        bot.send_message(user_id, 'Отправьте локацию, используя кнопку!')
        bot.register_next_step_handler(message, get_loc, user_name, user_num)

bot.polling(none_stop=True)

