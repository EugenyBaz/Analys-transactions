import os
from src.views import read_transactions_exl
import re



current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")





def search_trans(transactions, search_tr):

    match_trans = []

    pattern = re.compile(r'\D+\D{1}\.{1}')
    for trans in transactions:
        if pattern.search(trans['Описание']):
            match_trans.append(trans)

    return match_trans


transactions = read_transactions_exl(data_file_path_exl)
search_tr = input('Введите адресата в формате  Имя Ф.' )
print(search_trans(transactions, search_tr))