import os
from src.views import read_transactions_exl_all
import re
import json
# import logging
#
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("../logs/services.log")
# file_formatter = logging.Formatter(
#     "%(levelname)s: %(name)s: Request time: %(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S"
# )
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl_all= os.path.join(project_root, "data", "operations.xlsx")



def search_trans(transactions):
    """ Функция вывода переводов физическим лицам"""
    # logger.info("Запуск функции вывода переводов физическим лицам")

    match_trans = []

    pattern = re.compile(r'\D+ \D{1}\.{1}')
    for trans in transactions:
        if trans['Категория'] == "Переводы" and pattern.search(trans['Описание']):
           match_trans.append(trans)


    return match_trans


if __name__ == "__main__":
    transactions = read_transactions_exl_all(data_file_path_exl_all)
    matched_transactions = search_trans(transactions)

    result = json.dumps(matched_transactions, indent=4, ensure_ascii=False)
    # logger.info("Вывод результатов")
    print(result)



