from datetime import datetime
from typing import List, Any, Hashable, Dict

import pandas as pd

from dateutil import parser


def period_of_time(date_string: str) -> str:
    """Функция, которая получает на вход дату и возвращает первый день месяца."""
    try:
        date_object = parser.parse(date_string)
        date_object_new = datetime.strftime(date_object, "")
        return str(date_object_new)
    except (ValueError, TypeError, OverflowError):
        return "Неверные данные. Пример: 2024-03-11T02:26:18.671407"


def hello(date_string: str) -> str:
    """Функция, которая получает на вход дату и возвращает приветствие."""
    try:
        date_object = parser.parse(date_string)
        date_object_new = datetime.strftime(date_object, "%H")
        hour: int = int(date_object_new)
        if 5 <= hour < 12:
            return "Доброе утро"
        elif 12 <= hour < 18:
            return "Добрый день"
        elif 18 <= hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"
    except (ValueError, TypeError, OverflowError):
        return "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
    pass



def read_transactions_from_excel(file_xlsx: str) -> list[dict[Hashable, Any]]:
    """Функция, которая принимает на вход путь до xlsx-файла и
    возвращает список словарей с данными о финансовых транзакциях."""
    try:
        df = pd.read_excel(file_xlsx)
        transactions = df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_xlsx}' не найден.")
    except Exception as e:
        raise Exception(f"Ошибка при обработке Excel-файла: {e}")


def information_on_transactions(data_for: str, data_to:str, list_transactions: List[dict[Hashable, Any]] )->List[Dict]:
    """Функция, которая получает на вход 2 даты и список, а возвращает список трат за период."""
    new_list_transactions: List[Dict] = []
    date_obj_1 = parser.parse(data_for).date()
    date_obj_3 = parser.parse(data_to).date()
    for transactions in list_transactions:
        if (not transactions["Дата платежа"] or pd.isna(transactions["Дата платежа"])
                        or not transactions["Номер карты"] or pd.isna(transactions["Номер карты"])):
            continue
        date_str: str = str(transactions["Дата платежа"])
        date_obj_2 = parser.parse(date_str).date()
        if date_obj_1 <= date_obj_2:
            if date_obj_2 <= date_obj_3:
                new_list_transactions.append({
                "date": transactions["Дата платежа"],
                "last_digits": transactions["Номер карты"],
                "amount": transactions["Сумма платежа"],
                "category": transactions["Категория"],
                "description": transactions["Описание"]})
    return new_list_transactions



def top_5_transactions():
    """Функция, которая получает на вход 2 даты и возвращает Топ-5 транзакций по сумме платежа."""
    pass


def exchange_rates():
    """Функция, которая выводит курс валют, настройки в файле user_settings.json."""
    pass


def share_price():
    """Функция, которая выводит стоимость акций, настройки в файле user_settings.json."""
    pass


my_list = read_transactions_from_excel(r"C:\Users\Dima\my_second_project\Data\operations.xlsx")
data = period_of_time("2021-03-11T02:26:18.671407")
print(data)
result = information_on_transactions(data, "2021-03-11T02:26:18.671407", my_list)
print(result)