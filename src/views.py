import os
import pandas as pd
from typing import Any
from datetime import datetime
import math
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")

def read_transactions_exl(file_path: Any) -> list[dict[Any, Any]]:
    """Функция получения, чтения файла excel, преобразование в список словарей транзакций"""
    df = pd.read_excel(file_path)
    df_filtered = df.dropna(subset=['Номер карты'])
    list_transactions_exl = df_filtered.to_dict(orient="records")
    return list_transactions_exl
# print (read_transactions_exl(data_file_path_exl))

date_string = '2021-12-15'
current_date = datetime.strptime(date_string,'%Y-%m-%d' )
start_of_month = current_date.replace(day=1)
start_date = start_of_month.strftime('%Y-%m-%d'),
end_date = current_date.strftime('%Y-%m-%d')



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


print (greeting('2024-12-31 12:30:45'))

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


date_string = '15.12.2021'
current_date = datetime.strptime(date_string,'%d.%m.%Y')
start_of_month = current_date.replace(day=1)
start_date = start_of_month.strftime('%d.%m.%Y')
end_date = current_date.strftime('%d.%m.%Y')

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

            if card_number not in trans_list:
                trans_list[card_number] = 0

            trans_list[card_number] += float(amount)

    for key,value in trans_list.items():
        result.append ({
        'last_digits': key,
        'total_spent': round(value, 2),
        'cashback': round((round(value, 2)/ 100), 2)
    })

    return result

print(card_info(transactions, start_date,end_date ))

final_result = {"greeting": greeting('2024-12-31 12:30:45'), "cards" :[card_info(transactions, start_date,end_date )]}

ff_result = json.dumps(final_result, indent=4, ensure_ascii= False)
with open('proba.json', 'w', encoding= 'utf-8') as f:
    f.write(ff_result)






# def sort_by_date(
#     list_dict: List[Dict[str, Union[str, int]]], reverse_str: bool = True
# ) -> List[Dict[str, Union[str, int]]]:
#     """Функция сортировки по дате по убыванию"""
#     for i in list_dict:
#         if "date" not in i or i["date"] == "":
#             raise ValueError("Отсутствует дата")
#
#     sorted_list = sorted(list_dict, key=lambda x: x["date"], reverse=reverse_str)
#
#     return sorted_list

