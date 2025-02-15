import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Hashable, List
import pandas as pd

from src.views import read_transactions_exl_all

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl_all = os.path.join(project_root, "data", "operations.xlsx")
data_file_path_log = os.path.join(project_root, "logs", "reports.log")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(data_file_path_log)
file_formatter = logging.Formatter(
    "%(levelname)s: %(name)s: Request time: %(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def reports_cat(filename: str = "reports_cat.json") -> Callable:
    """Декоратор вывода результата функции в отдельный json файл"""
    logger.info("Запуск функции декоратора для вывода функции в отдельный json файл")

    def my_decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            if filename:
                report_cat = os.path.join(project_root, "data", filename)
                with open(report_cat, "w", encoding="utf-8") as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
            else:
                print(f"{func.__name__}: {result}")

            return result

        return wrapper

    return my_decorator


@reports_cat(filename="reports_cat.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: str) -> dict:
    """Функция вывода трат по категории на указанную дату и три месяца ранее"""
    logger.info("Запуск функции трат по категории на указанную дату и три месяца ранее")

    start = datetime.strptime(date, "%d.%m.%Y").date()
    end = start + timedelta(days=-90)
    start_str = start.strftime("%Y%m%d")
    end_str = end.strftime("%Y%m%d")


    # Фильтрация данных по дате и категории
    mask = (transactions["Категория"] == category) & \
           (end_str <= transactions["Дата платежа"]) & \
           (transactions["Дата платежа"] <= start_str)

    filtered_df = transactions[mask]

    # Суммирование расходов
    total_spend = filtered_df["Сумма операции"].sum() * -1

    result = {"category": category, "total_spend": float(round(total_spend, 2))}
    logger.info("Вывод  трат по категории на указанную дату и три месяца ранее")
    return result


