import os
import requests
from dotenv import load_dotenv
load_dotenv()
import json
# import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")
data_file_path_json = os.path.join(project_root, "data", "user_settings.json")
path_logs = os.path.join(project_root, "logs", "utils.log")

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# # print(f'{project_root}/logs/utils.log')
# file_handler = logging.FileHandler(path_logs)
# file_formatter = logging.Formatter(
#     "%(levelname)s: %(name)s: Request time: %(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S"
# )
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")
data_file_path_json = os.path.join(project_root, "data", "user_settings.json")


EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")

def convert_currency(user_settings):
    """Функция конвертации валюты и вывода текущего курса"""
    # logger.info("Запуск функции конвертации валюты и вывода текущего курса")
    tot_res = []
    currencies = user_settings.get("user_currencies", [])

    for currency in currencies:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/{currency}"
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/{currency}"
        # try:
        response = requests.get(url)
        if response.status_code == 200:
            # logger.info("Запрос на получение информации по валюте успешен")
            data = response.json()
            res = round(data["conversion_rates"]["RUB"], 2)
            tot_res.append({
                "currency_rates": currency,
                "rate": res
            })
        # else:
            # logger.error("Ошибка в получение ответа на запрос на получение информации по валюте"
            #             " скорее всего закончились бесплатные запросы API")
            # print(f"Request failed with status code {response.status_code}")
        # except KeyError:
        # print("Скорее всего закончились бесплатные запросы API")

    return tot_res



def result_ticker(user_settings):
    """Функция вывода стоимости  пяти тикеров"""
    # logger.info("Запуск функции вывода стоимости  пяти тикеров")
    tot_res = []
    tickers = user_settings.get("user_stocks", [])

    for tick in tickers:
        try:
            # url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={tick}&apikey={API_KEY}"
            # url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={tick}&apikey={ALPHAVANTAGE_API_KEY}'
            url = (f'https://api.twelvedata.com/time_series?apikey={TWELVEDATA_API_KEY}&interval=1day&symbol={tick}&type=stock&outputsize=1&format=JSON')
            response = requests.get(url)
            if response.status_code == 200:
                # logger.info("Запрос на получение информации по акциям успешен")
                data = response.json()
                # res = round(float(data['Global Quote']['05. price']), 2)
                res = round(float(data['values'][0]['close']), 2)
                # res = data ['Information']
                tot_res.append({
                    "stock": tick,
                    "price": res
                })
            else:
                print(f"Request failed with status code {response.status_code}")
        except KeyError:
            # logger.error("Ошибка в получение ответа на запрос на получение информации по акциям"
            #             " скорее всего закончились бесплатные запросы API")
            # print("Скорее всего закончились бесплатные запросы API")
            continue
    return tot_res


if __name__ == "__main__":
    with open(data_file_path_json, 'r') as f:
        user_settings = json.load(f)

    results_cur = convert_currency(user_settings)
    # logger.info("Вывод печати результата по валютам")
    print("Конвертация валют:", results_cur)

    results_tickers = result_ticker(user_settings)
    # logger.info("Вывод печати результата по акциям")
    print("Котировки акций:", results_tickers)