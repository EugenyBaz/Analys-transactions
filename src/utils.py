import json
import logging
import os
from datetime import date, datetime
from typing import Any, Dict, Hashable, List, Union

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")
data_file_path_json = os.path.join(project_root, "data", "user_settings.json")
path_logs = os.path.join(project_root, "logs", "utils.log")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# print(f'{project_root}/logs/utils.log')
file_handler = logging.FileHandler(path_logs)
file_formatter = logging.Formatter(
    "%(levelname)s: %(name)s: Request time: %(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
# data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")
# data_file_path_json = os.path.join(project_root, "data", "user_settings.json")


EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")
APILAYER_API_KEY = os.getenv("APILAYER_API_KEY")


def convert_currency(user_settings: Dict[str, Any]) -> List[Dict[str, float]]:
    """Функция конвертации валюты и вывода текущего курса"""
    logger.info("Запуск функции конвертации валюты и вывода текущего курса")
    tot_res = []
    currencies = user_settings.get("user_currencies", [])

    for currency in currencies:
        # url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/{currency}"
        url = f"https://api.apilayer.com/currency_data/convert?to=RUB&from={currency}&amount=1"
        headers = {"apikey": APILAYER_API_KEY}

        response = requests.request("GET", url, headers=headers)
        try:
            # response = requests.get(url)
            if response.status_code == 200:
                logger.info("Запрос на получение информации по валюте успешен")
                data = response.json()
                # res = round(data["conversion_rates"]["RUB"], 2)
                res = round(data["result"], 2)

                tot_res.append({"currency_rates": currency, "rate": res})
            else:
                logger.error(
                    "Ошибка в получение ответа на запрос на получение информации по валюте"
                    " скорее всего закончились бесплатные запросы API"
                )
                print(f"Request failed with status code {response.status_code}")
        except KeyError:
            print("Скорее всего закончились бесплатные запросы API")
    logger.info("Вывод результата по вылютам")
    return tot_res


def result_ticker(user_settings: Dict[str, Any]) -> List[Dict[str, float]]:
    """Функция вывода стоимости  пяти тикеров"""
    logger.info("Запуск функции вывода стоимости  пяти тикеров")
    tot_res = []
    tickers = user_settings.get("user_stocks", [])

    for tick in tickers:
        try:
            # url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={tick}&apikey={API_KEY}"
            # url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=
            # {tick}&apikey={ALPHAVANTAGE_API_KEY}'
            url = (
                f"https://api.twelvedata.com/time_series?apikey"
                f"={TWELVEDATA_API_KEY}&interval=1day&symbol={tick}&type=stock&outputsize=1&format=JSON"
            )
            response = requests.get(url)
            if response.status_code == 200:
                logger.info("Запрос на получение информации по акциям успешен")
                data = response.json()
                # res = round(float(data['Global Quote']['05. price']), 2)
                res = round(float(data["values"][0]["close"]), 2)
                # res = data ['Information']
                tot_res.append({"stock": tick, "price": res})
            else:
                print(f"Request failed with status code {response.status_code}")
        except KeyError:
            logger.error(
                "Ошибка в получение ответа на запрос на получение информации по акциям"
                " скорее всего закончились бесплатные запросы API"
            )
            print("Скорее всего закончились бесплатные запросы API")
            continue
    logger.info("Вывод результата по акциям")
    return tot_res


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


def card_info(transactions: List[Dict[Any, Any]],  start: Union[str, date], end: Union[str, date]) -> List[Dict[str, Any]]:
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
    transactions: List[Dict[Any, Any]], start: Union[str, date], end: Union[str, date], reverse_str: bool = True
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


if __name__ == "__main__":
    with open(data_file_path_json, "r") as f:
        user_settings = json.load(f)

    results_cur = convert_currency(user_settings)
    results_tickers = result_ticker(user_settings)
