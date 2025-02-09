import os
import requests
from dotenv import load_dotenv
load_dotenv()
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")
data_file_path_json = os.path.join(project_root, "data", "user_settings.json")

EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
ALPHAVANTAGE_API_KEY_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def convert_currency(user_settings):
    """Функция конвертации валюты и вывода текущего курса"""
    tot_res = []
    currencies = user_settings.get("user_currencies", [])

    for currency in currencies:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/{currency}"
        # try:
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
        # except KeyError:
        # print("Скорее всего закончились бесплатные запросы API")

    return tot_res



def result_ticker(user_settings):
    """Функция конвертации валюты и вывода текущего курса"""
    tot_res = []
    tickers = user_settings.get("user_stocks", [])

    for tick in tickers:
        try:
            # url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={tick}&apikey={API_KEY}"
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={tick}&apikey={ALPHAVANTAGE_API_KEY_API_KEY}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                res = round(float(data['Global Quote']['05. price']), 2)
                # res = data ['Information']
                tot_res.append({
                    "stock": tick,
                    "price": res
                })
            # else:
            #     print(f"Request failed with status code {response.status_code}")
        except KeyError:
            print("Скорее всего закончились бесплатные запросы API")

    return tot_res


if __name__ == "__main__":
    with open(data_file_path_json, 'r') as f:
        user_settings = json.load(f)

    results_cur = convert_currency(user_settings)
    print("Конвертация валют:", results_cur)

    results_tickers = result_ticker(user_settings)
    print("Котировки акций:", results_tickers)