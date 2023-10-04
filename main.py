#Тут основная работа с ботом
import telebot, buttons as bt, database as db
from geopy import Nominatim

#Создаем объект бота
bot = telebot.TeleBot('6407944506:AAEpMoGMxo4mxPnh0hFbdNxqmwnxKC9aEIU')
#Использование карт
geolocator = Nominatim(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
#Обработка команды старт
@bot.message_handler(commands=['start'])
def start_message(message):
    #Берем id пользователя
    user_id = message.from_user.id
    #Проверка на наличие юзера
    check_user = db.checker(user_id)
    #Берем продукты из БД
    products = db.get_pr_id()
    #Если есть
    if check_user:
        bot.send_message(user_id, 'Добро пожаловать!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню',
                         reply_markup=bt.main_menu(products))
    #Если нет
    else:
        bot.send_message(user_id, 'Добро пожаловать!\n'
                                'Давайте начнем регистрацию! Введите имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
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

#Вывод информации о продукте
@bot.callback_query_handler(lambda call: int(call.data) in db.get_pr_name_id())
def get_user_product(call):
    chat_id = call.message.chat.id
    prod = db.get_pr(int(call.data))
    bot.send_photo(chat_id, photo=prod[4], caption=f'Название товара: {prod[0]}\n\n'
                                                   f'Описание: {prod[1]}\n'
                                                   f'Кол-во: {prod[2]}\n'
                                                   f'Цена: {prod[3]}')

##Админ панель##
#Обработчик команды admin
@bot.message_handler(commands=['admin'])
def start_admin(message):
    admin_id = 791555605
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Добро пожаловать! Выберите действие',
                         reply_markup=bt.admin_menu())
        #Переход на этап выбора
        bot.register_next_step_handler(message, act)
    else:
        bot.send_message(message.from_user.id, 'Вы не админ!')
#Этап выбора
def act(message):
    admin_id = 791555605
    if message.text == 'Добавить продукт':
        bot.send_message(admin_id, 'Введите название товара',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        #Переход на этап получения названия
        bot.register_next_step_handler(message, get_pr_name)
    elif message.text == 'Удалить продукт':
        check = db.check_products()
        if check:
            bot.send_message(admin_id, 'Введите id товара',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
            # Переход на этап получения id
            bot.register_next_step_handler(message, get_pr_to_del)
        else:
            bot.send_message(admin_id, 'Товаров пока нет!')
            # Переход на этап выбора
            bot.register_next_step_handler(message, act)
def get_pr_name(message):
    admin_id = 791555605
    product_name = message.text
    bot.send_message(admin_id, 'А теперь напишите описание для продукта')
    #Переход на этап получения описания
    bot.register_next_step_handler(message, get_pr_des, product_name)
def get_pr_des(message, product_name):
    admin_id = 791555605
    product_des = message.text
    bot.send_message(admin_id, 'Какое количество товара есть?')
    #Переход на этап получения кол-ва
    bot.register_next_step_handler(message, get_pr_count, product_name, product_des)
def get_pr_count(message, product_name, product_des):
    admin_id = 791555605
    product_count = int(message.text)
    bot.send_message(admin_id, 'Сколько стоит товар?')
    #Переход на этап получения цены
    bot.register_next_step_handler(message, get_pr_price, product_name, product_des,
                                   product_count)
def get_pr_price(message, product_name, product_des, product_count):
    admin_id = 791555605
    product_price = float(message.text)
    bot.send_message(admin_id, 'А теперь перейдите на сайт https://postimages.org/ru/,'
                               ' загрузите фотографию и отправьте ссылку на фото!')
    #Переход на этап получения ссылки
    bot.register_next_step_handler(message, get_pr_photo, product_name,
                                   product_des, product_count, product_price)
def get_pr_photo(message, product_name, product_des, product_count, product_price):
    admin_id = 791555605
    product_photo = message.text
    db.add_pr(product_name, product_des, product_count, product_price, product_photo)
    bot.send_message(admin_id, 'Всё готово! Что-то еще?',
                     reply_markup=bt.admin_menu())
    #Переход на этап выбора
    bot.register_next_step_handler(message, act)
def get_pr_to_del(message):
    admin_id = 791555605
    id = int(message.text)
    check = db.check_pr(id)
    if check:
        db.del_pr(id)
        bot.send_message(admin_id, 'Всё готово! Что-то еще?',
                         reply_markup=bt.admin_menu())
        #Переход на этап выбора
        bot.register_next_step_handler(message, act)
    else:
        bot.send_message(admin_id, 'Такого продукта нет!')
        #Переход на этап получения id
        bot.register_next_step_handler(message, get_pr_to_del)

bot.polling(none_stop=True)

