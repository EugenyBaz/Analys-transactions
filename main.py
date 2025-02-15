from src.views import read_transactions_exl_all, read_transactions_exl, greeting, card_info, sort_by_amount
from src.services import search_trans
from src.utils import convert_currency, result_ticker
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


with open(data_file_path_json, 'r') as f:
    user_settings = json.load(f)

if __name__ == "__main__":
    date_time = '2021-12-31 12:30:45'
    # date_time = input(" Введите дату и время в формате YYYY-MM-DD HH:MM:SS")

    dt_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    start_of_month = dt_obj.replace(day=1)
    start_date = start_of_month.strftime('%d.%m.%Y')
    end_date = dt_obj.strftime('%d.%m.%Y')

    transactions = read_transactions_exl(data_file_path_exl)
    transactions_all = read_transactions_exl_all(data_file_path_exl)

    final_result = {"greeting": greeting(date_time), "cards": [card_info(transactions, start_date, end_date)],
                    "top_transactions": [sort_by_amount(transactions_all, start_date, end_date)],
                    "currency_rates": [convert_currency(user_settings)], "stock_prices": result_ticker(user_settings)}

    ff_result = json.dumps(final_result, indent=4, ensure_ascii=False)
    with open(data_file_path_result_main_screen, 'w', encoding='utf-8') as f:
        f.write(ff_result)

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
