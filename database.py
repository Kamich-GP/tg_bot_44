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


##Методы для продуктов##
#Добавление
def add_pr(name, des, count, price, photo):
    sql.execute('INSERT INTO products(pr_name, pr_des, pr_count, pr_price, pr_photo) '
                'VALUES(?, ?, ?, ?, ?);', (name, des, count, price, photo))
    #Фиксируем изменения
    connection.commit()
#Удаление
def del_pr(id):
    sql.execute('DELETE FROM products WHERE id=?;', (id,))
    #Фиксируем изменения
    connection.commit()
#Найти продукт по id
def check_pr(id):
    checker = sql.execute('SELECT id FROM products WHERE id=?;', (id,))
    if checker:
        return True
    else:
        return False

#Проверка на наличие продуктов в базе
def check_products():
    checker = sql.execute('SELECT * FROM products;')
    if checker:
        return True
    else:
        return False

