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


def card_info(transactions):
    trans_list = {}
    for trans in transactions:

        card_number_f= trans['Номер карты']
        card_number = card_number_f[1:5].replace(card_number_f[:-4], card_number_f[-4:])
        amount = trans.get('Сумма операции', 0)

        if card_number is not None:
            round_amount = round(amount,2)

            if card_number in trans_list:

                total_sum = trans_list[card_number] + round_amount
                trans_list[card_number] = round(total_sum, 2)
            else:

                trans_list[card_number] = round_amount

    return trans_list

print(card_info(transactions))

final_result = {"greeting": greeting('2024-12-31 12:30:45'), "cards" :[card_info(transactions)]}

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

