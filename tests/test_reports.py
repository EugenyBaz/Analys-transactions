import pytest
from datetime import datetime, timedelta
from src.reports import spending_by_category


trans_list = [
             {'Дата операции': '20.07.2019 15:27:06',
             'Дата платежа': '23.07.2019',
             'Номер карты': '*4556',
             'Статус': 'OK',
              'Категория': 'Аптеки',
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
             'Категория': 'Аптеки',
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
             'Категория': 'Аптеки',
             'Сумма операции': -17000.0,
             'Валюта операции': 'RUB',
             'Сумма платежа': -17000.0,
             'Валюта платежа': 'RUB',
             'Описание': 'Перевод с карты',
             'Бонусы (включая кэшбэк)': 0,
             'Округление на инвесткопилку': 0,
             'Сумма операции с округлением': 17000.0}]


@pytest.mark.parametrize(
    "category, date, expected_result",[("Аптеки", "23.07.2019", {"category": "Аптеки", "total_spend": -22149.0})]
)
def test_correct_filtering_and_summing(category, date, expected_result):
    """Тестируем корректное фильтрование по дате и сумме."""

    result = spending_by_category(trans_list, category, date)
    assert result == expected_result