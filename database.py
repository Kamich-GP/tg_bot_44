#Тут работа с БД
import sqlite3

#Подключение к базе данных
connection = sqlite3.connect('delivery.db', check_same_thread=False)
#Связь SQL Python
sql = connection.cursor()

#Создание таблицы пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users'
            '(id INTEGER, name TEXT, number TEXT, loc TEXT);')
#Создание таблицы продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products'
            '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'pr_name TEXT, pr_des TEXT, pr_count INTEGER, pr_price REAL,'
            'pr_photo TEXT);')
#Создание таблицы корзины
sql.execute('CREATE TABLE IF NOT EXISTS cart'
            '(user_id INTEGER, user_product TEXT, product_quantity INTEGER,'
            'total REAL);')

##Методы для пользователя##
#Регистрация
def register(id, name, num, loc):
    sql.execute('INSERT INTO users VALUES(?,?,?,?);', (id, name, num, loc))
    #Фиксируем изменения
    connection.commit()

#Проверка на наличие юзера в БД
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False