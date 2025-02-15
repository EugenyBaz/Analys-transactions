import logging
import os
from datetime import date, datetime
from typing import Any, Dict, Hashable, List

import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")
data_file_path_json = os.path.join(project_root, "data", "user_settings.json")
data_file_path_result_main_screen = os.path.join(project_root, "data", "result_main_screen.json")
data_file_path_log = os.path.join(project_root, "logs", "views.log")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(data_file_path_log)
file_formatter = logging.Formatter(
    "%(levelname)s: %(name)s: Request time: %(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_transactions_exl(file_path: str) -> List[Dict[Hashable, Any]]:
    """Функция получения, чтения файла excel, преобразование в список словарей без нулевых значений по номеру карты"""
    logger.info(
        "Запуск функции получения, чтения файла excel, преобразование в список словарей"
        " без нулевых значений по номеру карты"
    )
    df = pd.read_excel(str(file_path))
    df_filtered = df.dropna(subset=["Номер карты"])
    list_transactions_exl = df_filtered.to_dict(orient="records")
    return list_transactions_exl


def read_transactions_exl_all(file_path: str) -> List[Dict[Hashable, Any]]:
    """Функция получения, чтения файла excel, преобразование в список словарей  без нулевых значений по дате"""
    logger.info(
        "Запуск функции получения, чтения файла excel,"
        " преобразование в список словарей  без нулевых значений по дате"
    )
    df = pd.read_excel(str(file_path))
    df_filtered = df.dropna(subset=["Дата платежа"])
    list_transactions_exl_all = df_filtered.to_dict(orient="records")
    return list_transactions_exl_all


def greeting(time_str: str) -> str:
    """Функция приветствия, в зависимости от указанного времени"""
    logger.info("Запуск функции приветствия, в зависимости от указанного времени ")
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    hour = dt.hour

    if 5 <= hour < 11:
        message = str(("Доброе утро!"))
    elif 11 <= hour < 18:
        message = str(("Добрый день!"))
    elif 18 <= hour < 23:
        message = "Добрый вечер!"
    else:
        message = "Доброй ночи!"

    logger.info(f"Сформированное приветствие: {message}")
    return message


def card_info(transactions: List[Dict[str, Any]], start: date, end: date) -> List[Dict[str, float]]:
    """Функция вывода информации по карте последние 4 цифры, траты, кэшбэк"""
    logger.info("Запуск функции вывода информации по карте последние 4 цифры, траты, кэшбэк ")
    result = []
    trans_list = {}

    if isinstance(start, str):
        start = datetime.strptime(start, "%d.%m.%Y").date()
    if isinstance(end, str):
        end = datetime.strptime(end, "%d.%m.%Y").date()

    for trans in transactions:
        transaction_date = datetime.strptime(trans["Дата платежа"], "%d.%m.%Y").date()
        if start <= transaction_date <= end:
            card_number_f = trans["Номер карты"]
            card_number = card_number_f[1:5].replace(card_number_f[:-4], card_number_f[-4:])
            amount = trans.get("Сумма операции", 0)

            if float(amount) < 0:

                if card_number not in trans_list:
                    trans_list[card_number] = 0

                trans_list[card_number] += int(float(amount))

    for key, value in trans_list.items():
        result.append(
            {"last_digits": key, "total_spent": -round(value, 2), "cashback": -round((round(value, 2) / 100), 2)}
        )
    logger.info("Вывод результата по картам")
    return result


def sort_by_amount(
    transactions: List[Dict[str, Any]], start: date, end: date, reverse_str: bool = True
) -> List[Dict[str, Any]]:
    """Функция сортировки по тратам по убыванию"""
    logger.info("Запуск функции сортировки по тратам по убыванию")
    result = []
    filtered_transactions = []

    if isinstance(start, str):
        start = datetime.strptime(start, "%d.%m.%Y").date()
    if isinstance(end, str):
        end = datetime.strptime(end, "%d.%m.%Y").date()

    # Фильтруем транзакции по дате
    for trans in transactions:
        transaction_date: date = datetime.strptime(trans["Дата платежа"], "%d.%m.%Y").date()
        if start <= transaction_date <= end:
            filtered_transactions.append(trans)

    # Сортируем отфильтрованные транзакции по сумме операции
    sorted_transactions = sorted(filtered_transactions, key=lambda x: float(x["Сумма операции"]), reverse=reverse_str)

    # Формируем результат, ограничивая до 5 записей
    for i in range(min(len(sorted_transactions), 5)):
        trans = sorted_transactions[i]
        result.append(
            {
                "date": trans["Дата платежа"],
                "amount": trans["Сумма операции"],
                "category": trans["Категория"],
                "description": trans["Описание"],
            }
        )
    logger.info("Возвращаем результат сортировки")
    return result
