import sqlite3
import os
import db_interaction as database

PATH = os.path.dirname(__file__) + os.sep

con = sqlite3.connect(PATH + 'electronic_shop.db')
cursor = con.cursor()

instructions = """
1 - Створити таблицю
2 - Додати новий продукт
3 - Додати нового клієнта
4 - Додати нове замовлення
5 - Сумарний обсяг продажів
6 - Кількість замовлених продуктів кожного клієнта
7 - Середній чек 1 замовлення
8 - Найбільш популярна категорія
9 - Збільшити ціни в категорії "Technology" на 10%
10 - Додати зміни до датабази
"""

print(instructions)

while True:
    feedback = input("Введіть ваш запит: ")
    if not feedback:
        break
    elif feedback == '1':
        database.create_tables(cursor)
    elif feedback == '2':
        name = input("Введіть назву продукта: ")
        category = input("Введіть категорію продукта: ")
        price = float(input("Введіть ціну продукту: "))
        id = database.add_product(cursor, name, category, price)
        print(f'ID продукту: {id}')
    elif feedback == '3':
        first_name, last_name = input("Введіть ім'я та прізвище через пробіл: ").split(" ")
        email = input("Введіть e-mail: ")
        id = database.add_customer(cursor, first_name, last_name, email)
        print(f'ID клієнту: {id}')
    elif feedback == '4':
        customer_id = int(input("Введіть ID клієнта: "))
        product_id = int(input("Введіть ID продукту: "))
        quantity = int(input("Введіть кількість продукту: "))
        date = input("Введіть дату в форматі YYYY-MM-DD: ")
        id = database.place_an_order(cursor, customer_id, product_id, quantity, date)
        print(f'ID продукту: {id}')
    elif feedback == '5':
        print(database.get_sum_of_orders(cursor))
    elif feedback == '6':
        order_numbers = database.get_order_number_by_client(cursor)
        for client in order_numbers:
            print(f'{client[0]} {client[1]} - {client[2]}')
    elif feedback == '7':
        print(database.get_average_order(cursor))
    elif feedback == '8':
        print(database.get_most_popular_category(cursor))
    elif feedback == '9':
        database.make_technology_more_expensive(cursor)
    elif feedback == '10':
        con.commit()
    elif feedback == 'help':
        print(instructions)
    else:
        print('Команди не розпізнано. Введіть "help" (без лапок) щоб отримати інструкцію.')