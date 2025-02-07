import os
import pandas as pd
from typing import Any
from datetime import datetime, date
import math
import json
import requests
from dotenv import load_dotenv

load_dotenv()


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")
data_file_path_json = os.path.join(project_root, "data", "user_settings.json")

def read_transactions_exl(file_path: Any) -> list[dict[Any, Any]]:
    """Функция получения, чтения файла excel, преобразование в список словарей без нулевых значений по номеру карты"""
    df = pd.read_excel(file_path)
    df_filtered = df.dropna(subset=['Номер карты'])
    list_transactions_exl = df_filtered.to_dict(orient="records")
    return list_transactions_exl

def read_transactions_exl_all(file_path: Any) -> list[dict[Any, Any]]:
    """Функция получения, чтения файла excel, преобразование в список словарей  без нулевых значений по дате"""
    df = pd.read_excel(file_path)
    df_filtered = df.dropna(subset=['Дата платежа'])
    list_transactions_exl_all = df_filtered.to_dict(orient="records")
    return list_transactions_exl_all



def greeting(time_str):
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

print (greeting(date_time))

def card_number(transactions):
    result = []
    for trans in transactions:
        if 'Номер карты' in trans and trans['Номер карты']:
            value = trans['Номер карты']
            if isinstance(value, (int, float)) and not math.isnan(value):
                value = str(int(value))  # Преобразуем число в строку, отбрасывая дробную часть
            elif isinstance(value, str):
                pass  # Строковый тип уже подходит для среза
            else:
                continue  # Пропускаем значения, которые не являются ни строковыми, ни числовыми
            result.append(f"{value[-4:]}")  # Берем последние 4 символа
    return set(result)
transactions =  read_transactions_exl(data_file_path_exl)
print (card_number(transactions))

dt_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
start_of_month = dt_obj.replace(day=1)
start_date = start_of_month.strftime('%d.%m.%Y')
end_date = dt_obj.strftime('%d.%m.%Y')

def card_info(transactions,start,end):
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

print(card_info(transactions, start_date,end_date))



def sort_by_amount(transactions,start,end, reverse_str: bool = True):
    """Функция сортировки по сумме операций по убыванию"""
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

print(sort_by_amount(transactions_all, start_date,end_date))






API_KEY = os.getenv("EXCHANGERATE_API_KEY")


def convert_currency(user_settings):
    """Функция конвертации валюты и вывода текущего курса"""
    tot_res = []
    currencies = user_settings.get("user_currencies", [])

    for currency in currencies:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            res = round(data["conversion_rates"]["RUB"], 2)
            tot_res.append({
                "currency_rates": currency,
                "rate": res
            })
        else:
            print(f"Request failed with status code {response.status_code}")

    return tot_res

with open(data_file_path_json, 'r') as f:
    user_settings = json.load(f)

results = convert_currency(user_settings)

print(results)

final_result = {"greeting": greeting(date_time), "cards" :[card_info(transactions, start_date,end_date )],
                "top_transactions": [sort_by_amount(transactions_all, start_date,end_date)],
                "currency_rates":[convert_currency(user_settings)]}

ff_result = json.dumps(final_result, indent=4, ensure_ascii= False)
with open('proba.json', 'w', encoding= 'utf-8') as f:
    f.write(ff_result)


API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def result_ticker(user_settings):
    """Функция конвертации валюты и вывода текущего курса"""
    tot_res = []
    tickers = user_settings.get("user_stocks", [])

    for tick in tickers:
        # url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={tick}&apikey={API_KEY}"
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={tick}&apikey={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # res = round(data['price']['Global Quote']['05. price'], 2)
            res = data ['Information']
            tot_res.append({
                "stock": tick,
                "price": res
            })
        else:
            print(f"Request failed with status code {response.status_code}")

    return tot_res

with open(data_file_path_json, 'r') as f:
    user_settings = json.load(f)

results = result_ticker(user_settings)

print(results)

final_result = {"greeting": greeting(date_time), "cards" :[card_info(transactions, start_date,end_date )],
                "top_transactions": [sort_by_amount(transactions_all, start_date,end_date)],
                "currency_rates":[convert_currency(user_settings)], "stock_prices" : result_ticker(user_settings) }

ff_result = json.dumps(final_result, indent=4, ensure_ascii= False)
with open('proba.json', 'w', encoding= 'utf-8') as f:
    f.write(ff_result)