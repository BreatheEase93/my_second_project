import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Hashable, List

import pandas as pd
import requests
from dateutil import parser
from dotenv import load_dotenv

# Самая простая настройка
logging.basicConfig(level=logging.INFO)


def period_of_time(date_string: str) -> str:
    """Функция, которая получает на вход дату и возвращает первый день месяца."""
    try:
        logging.info(f"Обрабатываем дату: {date_string}")

        date_object = parser.parse(date_string)
        date_object_new = datetime.strftime(date_object, "01.%m.%Y")
        result = str(date_object_new)

        logging.info(f"Успешно. Результат: {result}")
        return result

    except (ValueError, TypeError, OverflowError) as e:
        logging.error(f"Ошибка: {date_string} - {e}")
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


load_dotenv("../.env")


def exchange_rates() -> List[Dict]:
    """Функция, которая выводит курс валют, настройки в файле user_settings.json."""

    with open(r"..\user_settings.json", "r") as f:
        currencies = json.load(f).get("user_currencies", [])

    api_key = os.getenv("api_key")
    if not api_key:
        raise ValueError("API ключ не найден")

    pairs = [f"{c}RUB" for c in currencies if c != "RUB"]
    if not pairs:
        return []

    params = {'get': 'rates', 'pairs': ",".join(pairs), 'key': api_key}
    data = requests.get("https://currate.ru/api/", params=params, timeout=10).json()

    if data.get('status') != 200:
        raise Exception(f"API ошибка: {data.get('message', 'Unknown')}")

    return [
        {'currency': pair[:3], 'rate': float(rate)} for pair, rate in data.get('data', {}).items() if len(pair) >= 6
    ]


def share_price() -> list[Dict]:
    """Функция, которая выводит стоимость акций, настройки в файле user_settings.json."""
    pass
