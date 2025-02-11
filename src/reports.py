from src.views import read_transactions_exl_all
from datetime import datetime, timedelta
import os
import pandas as pd
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("../logs/reports.log")
file_formatter = logging.Formatter(
    "%(levelname)s: %(name)s: Request time: %(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl_all= os.path.join(project_root, "data", "operations.xlsx")


def reports_cat(filename="reports_cat.json"):
    """ Декоратор вывода результата функции в отдельный json файл"""
    logger.info("Запуск функции декоратора для вывода функции в отдельный json файл")
    def my_decorator(func):
        def wrapper(*args,**kwargs):
            result = func(*args, **kwargs)
            if filename:
                report_cat = os.path.join(project_root, "data", filename)
                with open(report_cat, 'w', encoding='utf-8') as file:
                    json.dump(result, file,  ensure_ascii= False, indent = 4)
            else:
                print(f"{func.__name__}: {result}")

        return wrapper

    return my_decorator



@reports_cat(filename="reports_cat.json")
def spending_by_category(transactions, category, date) -> pd.DataFrame:
    """ Функция вывода трат по категории на указанную дату и три месяца ранее"""
    logger.info("Запуск функции трат по категории на указанную дату и три месяца ранее")

    start = datetime.strptime(date, '%d.%m.%Y').date()
    end = start + timedelta(days=-90)
    start_str = start.strftime('%Y%m%d')
    end_str = end.strftime('%Y%m%d')

    filtered_transactions_date = []
    fil_trans_cat = []
    total_amount = 0.0

    for trans in transactions:

        if trans["Категория"] == category:
            transaction_date = datetime.strptime(trans['Дата платежа'], '%d.%m.%Y').date()
            transaction_date_str = transaction_date.strftime('%Y%m%d')
            fil_trans_cat.append(transaction_date_str)

            if end_str <= transaction_date_str <= start_str:
                filtered_transactions_date.append(trans)


    for trans in filtered_transactions_date:
        amount = float(trans['Сумма операции'])
        if amount < 0:
            total_amount += amount

    result = {"category": category, "total_spend": round(total_amount,2)}
    print("Результат:", result)
    return result
if __name__ == "__main__":
    date = input("Введите текущую дату в формате DD.MM.YYYY\n")
    if date == "":
        date_request = datetime.now().strftime('%d.%m.%Y')
    else :
        date_request = date



    category = input("Введите  категорию").title()
    transactions = read_transactions_exl_all(data_file_path_exl_all)
    spending_by_category(transactions, category,date_request)




