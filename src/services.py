import logging
from datetime import datetime
from typing import Any, Dict, Hashable, List

import pandas as pd
from dateutil import parser


def get_monthly_cashback_summary(list_transactions: List[Dict[Hashable, Any]], month: str, year: str) -> List[Dict]:
    """Функция, которая получает на вход месяц и год, и список транзакций,
    а возвращает информацию о тратах за период."""
    new_list_transactions: List[Dict] = []

    try:
        date_from_obj = datetime.strptime(f"{str(year)}-{str(month)}", "%Y-%m").date()
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


# Настройка простейшего логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def calculate_cashback_by_category(list_transactions: List[Dict]) -> List[Dict]:
    """Функция, которая получает на вход список с информацией о транзакциях,
    а возвращает категорию и кэшбэк по ним."""

    logging.info(f"Начало расчета кэшбэка. Получено транзакций: {len(list_transactions)}")

    if list_transactions:
        logging.debug(f"Первая транзакция: {list_transactions[0]}")

    my_list: List[Dict] = []

    try:
        category = [transaction['category'] for transaction in list_transactions]
        unique_category = set(category)

        logging.info(f"Найдено уникальных категорий: {len(unique_category)}: {unique_category}")

        for category in unique_category:
            total_spent: int = 0
            for transaction in list_transactions:
                if transaction['category'] == category:
                    try:
                        cashback_value = int(transaction["cashback"])
                        total_spent += cashback_value
                    except (ValueError, KeyError) as e:
                        logging.warning(f"Ошибка обработки cashback в транзакции {transaction}: {e}")
                        continue

            my_list.append({category: total_spent})
            logging.info(f"Категория '{category}': общий кэшбэк = {total_spent}")

        logging.info(f"Расчет завершен. Результат: {my_list}")

    except Exception as e:
        logging.error(f"Ошибка при расчете кэшбэка: {e}")
        raise

    return my_list
