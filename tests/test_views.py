import pytest
import os
import pandas as pd
from src.views import read_transactions_exl, read_transactions_exl_all, greeting, sort_by_amount
from src.views import card_info

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")



def test_read_transactions_exl_valid_file():
    transactions = read_transactions_exl(data_file_path_exl)
    assert isinstance(transactions, list)
    assert all(isinstance(t, dict) for t in transactions)
    assert len(transactions) > 0
    assert all('Номер карты' in t.keys() for t in transactions)


def test_read_transactions_exl_all_valid_file():
    transactions = read_transactions_exl_all(data_file_path_exl)
    assert isinstance(transactions, list)
    assert all(isinstance(t, dict) for t in transactions)
    assert len(transactions) > 0
    assert all('Номер карты' in t.keys() for t in transactions)



@pytest.mark.parametrize('time_str,expected_greeting', [("2021-12-31 09:15:00", "Доброе утро!"),
    ("2021-12-31 13:30:00", "Добрый день!"),
    ("2021-12-31 19:45:00", "Добрый вечер!"),
    ("2021-12-31 22:59:59", "Добрый вечер!"),
    ("2021-12-31 00:00:00", "Доброй ночи!"),
    ("2021-12-31 04:59:59", "Доброй ночи!")])
def test_greeting(time_str, expected_greeting):
    result = greeting(time_str)
    assert result == expected_greeting



# transactions = read_transactions_exl(data_file_path_exl)
trans_list = [
             {'Дата операции': '20.07.2019 15:27:06',
             'Дата платежа': '23.07.2019',
             'Номер карты': '*4556',
             'Статус': 'OK',
              'Категория': 'Аптека',
              'Сумма операции': -5000.0,
             'Валюта операции': 'RUB',
             'Сумма платежа': -5000.0,
             'Валюта платежа': 'RUB',
             'Описание': 'Снятие в банкомате Сбербанк',
             'Бонусы (включая кэшбэк)': 0,
             'Округление на инвесткопилку': 0,
             'Сумма операции с округлением': 5000.0},
            {'Дата операции': '19.07.2019 22:02:30',
             'Дата платежа': '21.07.2019',
             'Номер карты': '*7197',
             'Статус': 'OK',
             'Категория': 'Аптека',
             'Сумма операции': -149.0,
             'Валюта операции': 'RUB',
             'Сумма платежа': -149.0,
             'Валюта платежа': 'RUB',
             'Описание': 'Circle K',
             'Бонусы (включая кэшбэк)': 2,
             'Округление на инвесткопилку': 0,
             'Сумма операции с округлением': 149.0},
            {'Дата операции': '01.07.2019 17:44:36',
             'Дата платежа': '01.07.2019',
             'Номер карты': '*6002',
             'Статус': 'FAILED',
             'Категория': 'Аптека',
             'Сумма операции': -17000.0,
             'Валюта операции': 'RUB',
             'Сумма платежа': -17000.0,
             'Валюта платежа': 'RUB',
             'Описание': 'Перевод с карты',
             'Бонусы (включая кэшбэк)': 0,
             'Округление на инвесткопилку': 0,
             'Сумма операции с округлением': 17000.0}

            ]
@pytest.mark.parametrize("start, end, expected", [
    ("01.07.2019", "23.07.2019", [{"last_digits": "4556", "total_spent": 5000.0,
                                   "cashback": 50.0}, {"last_digits": "7197", "total_spent": 149.0, "cashback": 1.49},
                                  {"last_digits": "6002", "total_spent": 17000.0, "cashback": 170.0}]),
    ("01.07.2019", "21.07.2019", [{"last_digits": "7197",
                                   "total_spent": 149.0, "cashback": 1.49},
                                  {"last_digits": "6002", "total_spent": 17000.0, "cashback": 170.0}]),
    ("01.07.2019", "01.07.2019", [{"last_digits": "6002",
                                   "total_spent": 17000.0, "cashback": 170.0}]),

])
def test_card_info(start, end, expected):
    result = card_info(trans_list, start, end)
    assert result == expected



transactions_all = read_transactions_exl_all(data_file_path_exl)
@pytest.mark.parametrize("start, end, reverse_str, expected", [
    ("01.03.2023", "31.03.2023", True, [({
        "amount": "-2500.0",
        "category": "Переводы",
        "date": "28.02.2023",
        "description": "Константин Ф."})]),
    ("01.03.2023", "31.03.2023", False, [({
        "amount": "-1500.0",
        "category": "Переводы",
        "date": "31.03.2023",
        "description": "На кудыкину гору"})])])

def test_sort_by_amount(start, end, reverse_str, expected):
    result = sort_by_amount(transactions_all, start, end, reverse_str)
    assert result == expected
