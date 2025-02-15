import os
from datetime import date
from typing import Any, Dict, Hashable, List

import pytest

from src.views import card_info, greeting, read_transactions_exl, read_transactions_exl_all, sort_by_amount

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")


def test_read_transactions_exl_valid_file() -> None:
    """Тест на корректность конвертации и формирования  файла без нулевых ячеек с номером карты"""
    transactions = read_transactions_exl(data_file_path_exl)
    assert isinstance(transactions, list)
    assert all(isinstance(t, dict) for t in transactions)
    assert len(transactions) > 0
    assert all("Номер карты" in t.keys() for t in transactions)


def test_read_transactions_exl_all_valid_file() -> None:
    """Тест на корректность конвертации и формирования  файла без нулевых ячеек с датой платежа"""
    transactions = read_transactions_exl_all(data_file_path_exl)
    assert isinstance(transactions, list)
    assert all(isinstance(t, dict) for t in transactions)
    assert len(transactions) > 0
    assert all("Дата платежа" in t.keys() for t in transactions)


@pytest.mark.parametrize(
    "time_str,expected_greeting",
    [
        ("2021-12-31 09:15:00", "Доброе утро!"),
        ("2021-12-31 13:30:00", "Добрый день!"),
        ("2021-12-31 19:45:00", "Добрый вечер!"),
        ("2021-12-31 22:59:59", "Добрый вечер!"),
        ("2021-12-31 00:00:00", "Доброй ночи!"),
        ("2021-12-31 04:59:59", "Доброй ночи!"),
    ],
)
def test_greeting(time_str: str, expected_greeting: List[Dict[Hashable, Any]]) -> None:
    """Тестирование корректного вывода приветствия в зависимости от времени"""
    result = greeting(time_str)
    assert result == expected_greeting


# transactions = read_transactions_exl(data_file_path_exl)
trans_list = [
    {
        "Дата операции": "20.07.2019 15:27:06",
        "Дата платежа": "23.07.2019",
        "Номер карты": "*4556",
        "Статус": "OK",
        "Категория": "Аптека",
        "Сумма операции": -5000.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -5000.0,
        "Валюта платежа": "RUB",
        "Описание": "Снятие в банкомате Сбербанк",
        "Бонусы (включая кэшбэк)": 0,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 5000.0,
    },
    {
        "Дата операции": "19.07.2019 22:02:30",
        "Дата платежа": "21.07.2019",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Категория": "Аптека",
        "Сумма операции": -149.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -149.0,
        "Валюта платежа": "RUB",
        "Описание": "Circle K",
        "Бонусы (включая кэшбэк)": 2,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 149.0,
    },
    {
        "Дата операции": "01.07.2019 17:44:36",
        "Дата платежа": "01.07.2019",
        "Номер карты": "*6002",
        "Статус": "FAILED",
        "Категория": "Аптека",
        "Сумма операции": -17000.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -17000.0,
        "Валюта платежа": "RUB",
        "Описание": "Перевод с карты",
        "Бонусы (включая кэшбэк)": 0,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 17000.0,
    },
]


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (
            "01.07.2019",
            "23.07.2019",
            [
                {"last_digits": "4556", "total_spent": 5000.0, "cashback": 50.0},
                {"last_digits": "7197", "total_spent": 149.0, "cashback": 1.49},
                {"last_digits": "6002", "total_spent": 17000.0, "cashback": 170.0},
            ],
        ),
        (
            "01.07.2019",
            "21.07.2019",
            [
                {"last_digits": "7197", "total_spent": 149.0, "cashback": 1.49},
                {"last_digits": "6002", "total_spent": 17000.0, "cashback": 170.0},
            ],
        ),
        ("01.07.2019", "01.07.2019", [{"last_digits": "6002", "total_spent": 17000.0, "cashback": 170.0}]),
    ],
)
def test_card_info(start: date, end: date, expected: List[Dict[Hashable, Any]]) -> None:
    """Тестирование корректного вывода результатов с номером карты, тратами и описанием"""
    result = card_info(trans_list, start, end)
    assert result == expected


transactions_all = read_transactions_exl_all(data_file_path_exl)


@pytest.mark.parametrize(
    "start, end, reverse_str, expected",
    [
        (
            "30.12.2021",
            "30.12.2021",
            True,
            [
                {
                    "date": "30.12.2021",
                    "amount": 174000.0,
                    "category": "Пополнения",
                    "description": "Пополнение через Газпромбанк",
                },
                {
                    "date": "30.12.2021",
                    "amount": 5046.0,
                    "category": "Пополнения",
                    "description": "Пополнение через Газпромбанк",
                },
                {"date": "30.12.2021", "amount": -349.0, "category": "Канцтовары", "description": "Mitrankov M.V."},
                {"date": "30.12.2021", "amount": -1411.4, "category": "Ж/д билеты", "description": "РЖД"},
                {"date": "30.12.2021", "amount": -1411.4, "category": "Ж/д билеты", "description": "РЖД"},
            ],
        ),
        (
            "23.12.2021",
            "23.12.2021",
            False,
            [
                {
                    "date": "23.12.2021",
                    "amount": -28001.94,
                    "category": "Переводы",
                    "description": "Перевод Кредитная карта. ТП 10.2 RUR",
                },
                {"date": "23.12.2021", "amount": -10000.0, "category": "Переводы", "description": "Светлана Т."},
                {"date": "23.12.2021", "amount": -2000.0, "category": "Переводы", "description": "Дмитрий Ш."},
                {"date": "23.12.2021", "amount": -250.0, "category": "Каршеринг", "description": "Ситидрайв"},
                {"date": "23.12.2021", "amount": -250.0, "category": "Каршеринг", "description": "Ситидрайв"},
            ],
        ),
    ],
)
def test_sort_by_amount(start: date, end: date, reverse_str: bool, expected: List[Dict[Hashable, Any]]) -> None:
    """Тест на сортировку по убыванию с выводом первых пяти транзакций"""
    transactions_for_test = [
        {str(key): value for key, value in transaction.items()} for transaction in transactions_all
    ]

    result = sort_by_amount(transactions_for_test, start, end, reverse_str)
    assert result == expected
