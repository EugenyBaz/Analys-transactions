import os
from typing import Any, Dict, List

import pytest

from src.reports import spending_by_category
from src.views import read_transactions_exl_all

trans_list = [
    {
        "Дата операции": "20.07.2019 15:27:06",
        "Дата платежа": "23.07.2019",
        "Номер карты": "*4556",
        "Статус": "OK",
        "Категория": "Супермаркет",
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
        "Дата операции": "12.12.2021",
        "Дата платежа": "12.12.2021",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Категория": "Аптеки",
        "Сумма операции": -6486.5,
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
        "Категория": "Супермаркет",
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
    "category, date, expected_result", [("Аптеки", "12.12.2021", {"category": "Аптеки", "total_spend": -6486.5})]
)
def test_spending_by_category(category: str, date: str, expected_result: List[Dict[str, Any]]) -> None:
    """Тестируем корректное фильтрование по дате и сумме."""

    result = spending_by_category(trans_list, category, date)
    assert result == expected_result


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl_all = os.path.join(project_root, "data", "operations.xlsx")

transactions = read_transactions_exl_all(data_file_path_exl_all)


@pytest.fixture
def category() -> str:
    return "Аптеки"


@pytest.fixture
def date_tr() -> str:
    return "12.12.2021"
