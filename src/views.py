import json
import logging
import os
from datetime import date, datetime
from typing import Dict


from src.utils import (card_info, convert_currency, greeting, read_transactions_exl, read_transactions_exl_all,
                       result_ticker, sort_by_amount)

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


def main_page(date_time: str) -> str:
    logger.info("Запуск функции главной страницы ")
    with open(data_file_path_json, "r") as f:
        user_settings = json.load(f)

    dt_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    start_of_month = dt_obj.replace(day=1)
    start_date = start_of_month.strftime("%d.%m.%Y")
    end_date = dt_obj.strftime("%d.%m.%Y")

    transactions = read_transactions_exl(data_file_path_exl)
    transactions_all = read_transactions_exl_all(data_file_path_exl)

    final_result = {
        "greeting": greeting(date_time),
        "cards": [card_info(transactions, start_date, end_date)],
        "top_transactions": [sort_by_amount(transactions_all, start_date, end_date)],
        "currency_rates": [convert_currency(user_settings)],
        "stock_prices": result_ticker(user_settings),
    }
    logger.info("Печать результата по главной странице")

    ff_result = json.dumps(final_result, indent=4, ensure_ascii=False)
    with open(data_file_path_result_main_screen, "w", encoding="utf-8") as f:
        f.write(ff_result)
    return ff_result
