from datetime import datetime
from typing import Any, Dict, Hashable, List

import pandas as pd
from dateutil import parser


def get_monthly_cashback_summary(list_transactions: List[Dict[Hashable, Any]], month: str, year: str) -> List[Dict]:
    """Функция, которая получает на вход месяц и год, и список транзакций,
     а возвращает информацию о тратах за период."""
    new_list_transactions: List[Dict] = []

    try:
        date_from_obj = datetime.strptime(f"{year}-{month}", "%Y-%m").date()
    except ValueError:
        return []

    for transaction in list_transactions:
        if (
            "Дата платежа" not in transaction
            or "Кэшбэк" not in transaction
            or pd.isna(transaction["Дата платежа"])
            or transaction["Статус"] == "FAILED"
            or pd.isna(transaction["Кэшбэк"])
        ):
            continue

        try:
            trans_date_str = str(transaction["Дата платежа"])
            trans_date_obj = parser.parse(trans_date_str).date()
        except (ValueError, TypeError, AttributeError):
            continue

        if trans_date_obj.year == date_from_obj.year and trans_date_obj.month == date_from_obj.month:
            new_list_transactions.append(
                {
                    "category": transaction["Категория"],
                    "cashback": transaction["Кэшбэк"],
                }
            )

    return new_list_transactions


def calculate_cashback_by_category(list_transactions: List[Dict]) -> List[Dict]:
    """Функция, которая получает на вход список с информацией о транзакциях,
    а возвращает категорию и кэшбэк по ним."""

    my_list: List[Dict] = []

    category = [transaction['category'] for transaction in list_transactions]
    unique_category = set(category)

    for category in unique_category:
        total_spent: int = 0
        for transaction in list_transactions:
            if transaction['category'] == category:
                total_spent += int(transaction["cashback"])

        my_list.append({category: total_spent})

    return my_list
