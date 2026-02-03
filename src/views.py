from datetime import datetime
from typing import Any, Dict, Hashable, List

import pandas as pd
from dateutil import parser


def period_of_time(date_string: str) -> str:
    """Функция, которая получает на вход дату и возвращает первый день месяца."""
    try:
        date_object = parser.parse(date_string)
        date_object_new = datetime.strftime(date_object, "01.%m.%Y")
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


def information_on_transactions(
    data_from: str, data_to: str, list_transactions: List[Dict[Hashable, Any]]
) -> List[Dict]:
    """Функция, которая получает на вход 2 даты и список, а возвращает информацию о тратах за период."""
    new_list_transactions: List[Dict] = []

    try:
        date_from_obj = parser.parse(data_from).date()
        date_to_obj = parser.parse(data_to).date()
    except (ValueError, TypeError):
        return []

    for transaction in list_transactions:
        if (
            "Дата платежа" not in transaction
            or "Номер карты" not in transaction
            or pd.isna(transaction["Дата платежа"])
            or transaction["Статус"] == "FAILED"
            or pd.isna(transaction["Номер карты"])
        ):
            continue

        try:
            trans_date_str = str(transaction["Дата платежа"])
            trans_date_obj = parser.parse(trans_date_str).date()
        except (ValueError, TypeError, AttributeError):
            continue

        if date_from_obj <= trans_date_obj <= date_to_obj:
            new_list_transactions.append(
                {
                    "date": trans_date_obj.strftime("%d.%m.%Y"),
                    "last_digits": transaction["Номер карты"],
                    "amount": transaction["Сумма платежа"],
                    "category": transaction["Категория"],
                    "description": transaction["Описание"],
                }
            )

    return new_list_transactions


def info_fo_card(list_transactions: List[Dict]) -> List[Dict]:
    """Функция, которая получает на вход список с информацией о транзакциях,
    а возвращает общую сумму расходов и кэшбэк по картам."""

    my_list: List[Dict] = []

    card_numbers = [transaction['last_digits'] for transaction in list_transactions]
    unique_cards = set(card_numbers)

    for card in unique_cards:
        total_spent: int = 0
        for transaction in list_transactions:
            if transaction['last_digits'] == card:
                total_spent += int(transaction["amount"])

        my_list.append({"last_digits": card[-4:], "total_spent": total_spent, "cashback": total_spent / 100})

    return my_list


def top_5_transactions(list_transactions: list[dict]) -> list[dict]:
    """Функция, которая получает на вход список с информацией о транзакциях,
    а возвращает Топ-5 транзакций по сумме платежа."""
    sorted_by_amount: list[dict] = sorted(list_transactions, key=lambda x: x["amount"], reverse=True)
    top_5 = sorted_by_amount[0:5]
    my_list: list[dict] = []
    for transactions in top_5:
        my_list.append(
            {
                "date": transactions["date"],
                "amount": transactions["amount"],
                "category": transactions["category"],
                "description": transactions["description"],
            }
        )
    return my_list


def exchange_rates():
    """Функция, которая выводит курс валют, настройки в файле user_settings.json."""
    pass


def share_price():
    """Функция, которая выводит стоимость акций, настройки в файле user_settings.json."""
    pass


# my_list = read_transactions_from_excel(r"..\Data\operations.xlsx")
# data = period_of_time("2021-03-01T02:26:18.671407")
# result = information_on_transactions("2021-03-01T02:26:18.671407", "2021-03-15T02:26:18.671407", my_list)
# print(result)
