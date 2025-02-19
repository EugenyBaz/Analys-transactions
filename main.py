from src.views import main_page
from src.services import search_trans
from src.utils import read_transactions_exl_all
from src.reports import spending_by_category
import os
import json
from datetime import datetime
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir))
data_file_path_exl = os.path.join(project_root, "data", "operations.xlsx")
data_file_path_json = os.path.join(project_root, "data", "user_settings.json")
data_file_path_result_main_screen = os.path.join(project_root, "data", "result_main_screen.json")
data_file_path_result_services = os.path.join(project_root, "data", "result_services.json")

if __name__ == "__main__":

    # Результат по views (main_page)
    # date_time = '2021-12-31 12:30:45'
    date_time = input(" Введите дату и время в формате YYYY-MM-DD HH:MM:SS")
    print(main_page(date_time))

    # Результат по блоку services
    transactions = read_transactions_exl_all(data_file_path_exl)
    matched_transactions = search_trans(transactions)
    result = json.dumps(matched_transactions, indent=4, ensure_ascii=False)
    with open(data_file_path_result_services, 'w', encoding='utf-8') as f:
        f.write(result)

    # Результат по блоку reports
    date = input("Введите текущую дату в формате DD.MM.YYYY\n")
    category = input("Введите  категорию").title()

    if date == "":
        date_request = datetime.now().strftime("%d.%m.%Y")
    else:
        date_request = date
    transactions = read_transactions_exl_all(data_file_path_exl)
    data_frame_file = pd.DataFrame(transactions)
    data_frame_file["Дата платежа"] = pd.to_datetime(data_frame_file["Дата платежа"], format="%d.%m.%Y")

    result = spending_by_category(data_frame_file, category, date_request)
    print(result)
