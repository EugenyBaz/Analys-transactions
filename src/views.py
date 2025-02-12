import os
import pandas as pd
from typing import Any
from datetime import datetime, date
import json
from src.utils import convert_currency, result_ticker
# import logging
#
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("../logs/views.log")
# file_formatter = logging.Formatter(
#     "%(levelname)s: %(name)s: Request time: %(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S"
# )
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")
data_file_path_json = os.path.join(project_root, "data", "user_settings.json")
data_file_path_result_main_screen = os.path.join(project_root, "data", "result_main_screen.json")


def read_transactions_exl(file_path: Any) -> list[dict[Any, Any]]:
    """Функция получения, чтения файла excel, преобразование в список словарей без нулевых значений по номеру карты"""
    # logger.info("Запуск функции получения, чтения файла excel, преобразование в список словарей"
    #             " без нулевых значений по номеру карты")
    df = pd.read_excel(file_path)
    df_filtered = df.dropna(subset=['Номер карты'])
    list_transactions_exl = df_filtered.to_dict(orient="records")
    return list_transactions_exl

def read_transactions_exl_all(file_path: Any) -> list[dict[Any, Any]]:
    """Функция получения, чтения файла excel, преобразование в список словарей  без нулевых значений по дате"""
    # logger.info("Запуск функции получения, чтения файла excel,"
    #             " преобразование в список словарей  без нулевых значений по дате")
    df = pd.read_excel(file_path)
    df_filtered = df.dropna(subset=['Дата платежа'])
    list_transactions_exl_all = df_filtered.to_dict(orient="records")
    return list_transactions_exl_all



def greeting(time_str):
    """ Функция приветствия, в зависимости от указанного времени"""
    # logger.info("Запуск функции приветствия, в зависимости от указанного времени ")
    dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')

    hour = dt.hour

    if  5 <= hour < 11:
        return str(("Доброе утро!"))
    elif  11 <= hour < 18 :
        return str(("Добрый день!"))
    elif  18  <= hour < 23:
        return ("Добрый вечер!")
    else:
        return ("Доброй ночи!")


    # date_time = input(" Введите дату и время в формате YYYY-MM-DD HH:MM:SS")
date_time = '2021-12-31 12:30:45'

# print (greeting(date_time))


dt_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
start_of_month = dt_obj.replace(day=1)
start_date = start_of_month.strftime('%d.%m.%Y')
end_date = dt_obj.strftime('%d.%m.%Y')

def card_info(transactions,start,end):
    """ Функция вывода информации по карте последние 4 цифры, траты, кэшбэк"""
    # logger.info("Запуск функции вывода информации по карте последние 4 цифры, траты, кэшбэк ")
    result = []
    trans_list = {}

    if isinstance(start, str):
        start = datetime.strptime(start, '%d.%m.%Y').date()
    if isinstance(end, str):
        end = datetime.strptime(end, '%d.%m.%Y').date()


    for trans in transactions:
        transaction_date = datetime.strptime(trans['Дата платежа'], '%d.%m.%Y').date()
        if start <= transaction_date <= end:
            card_number_f= trans['Номер карты']
            card_number = card_number_f[1:5].replace(card_number_f[:-4], card_number_f[-4:])
            amount = trans.get('Сумма операции', 0)

            if float(amount) < 0:

                if card_number not in trans_list:
                    trans_list[card_number] = 0

                trans_list[card_number] += float(amount)

    for key,value in trans_list.items():
        result.append ({
        'last_digits': key,
        'total_spent': -round(value, 2),
        'cashback': -round((round(value, 2)/ 100), 2)
    })

    return result

transactions = read_transactions_exl(data_file_path_exl)
# print(card_info(transactions, start_date, end_date))



def sort_by_amount(transactions,start,end, reverse_str: bool = True):
    """Функция сортировки по тратам по убыванию"""
    # logger.info("Запуск функции сортировки по тратам по убыванию")
    result = []
    filtered_transactions = []  # Список для хранения транзакций в пределах указанного диапазона

    if isinstance(start, str):
        start = datetime.strptime(start, '%d.%m.%Y').date()
    if isinstance(end, str):
        end = datetime.strptime(end, '%d.%m.%Y').date()

    # Фильтруем транзакции по дате
    for trans in transactions:
        transaction_date: date = datetime.strptime(trans['Дата платежа'], '%d.%m.%Y').date()
        if start <= transaction_date <= end:
            filtered_transactions.append(trans)

    # Сортируем отфильтрованные транзакции по сумме операции
    sorted_transactions = sorted(filtered_transactions, key=lambda x: float(x["Сумма операции"]), reverse= reverse_str)

    # Формируем результат, ограничивая до 5 записей
    for i in range(min(len(sorted_transactions), 5)):
        trans = sorted_transactions[i]
        result.append({
            "date": trans['Дата платежа'],
            "amount": trans['Сумма операции'],
            "category": trans['Категория'],
            "description": trans['Описание']
        })

    return result
transactions_all = read_transactions_exl_all(data_file_path_exl)

# print(sort_by_amount(transactions_all, start_date,end_date))

with open(data_file_path_json, 'r') as f:
    user_settings = json.load(f)


# print(convert_currency(user_settings))
final_result = {"greeting": greeting(date_time), "cards" :[card_info(transactions, start_date,end_date )],
                "top_transactions": [sort_by_amount(transactions_all, start_date,end_date)],
                "currency_rates":[convert_currency(user_settings)], "stock_prices" : result_ticker(user_settings)}


if __name__ == "__main__":
    ff_result = json.dumps(final_result, indent=4, ensure_ascii= False)
    with open(data_file_path_result_main_screen, 'w', encoding= 'utf-8') as f:
        f.write(ff_result)
