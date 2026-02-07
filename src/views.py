import json
from typing import Any, Dict, Hashable, List

from src.utils import (exchange_rates, hello, info_fo_card, information_on_transactions, period_of_time,
                       read_transactions_from_excel, share_price, top_5_transactions)


def main(date_string: str) -> str:
    """Функция принимающая строку с датой, и возвращающая в JSON-ответе:
    1 Приветствие.
    2 Информацию по картам
    3 Топ-5 транзакций по сумме платежа.
    4 Курс валют.
    5 Стоимость акций из S&P500.
    """
    data_from: str = period_of_time(date_string)
    transactions: list[dict[Hashable, Any]] = read_transactions_from_excel("../Data/operations.xlsx")
    sorted_transactions: List[Dict] = information_on_transactions(data_from, date_string, transactions)
    info_card: List[Dict] = info_fo_card(sorted_transactions)
    top_5: List[Dict] = top_5_transactions(sorted_transactions)

    data = {
        "greeting": hello(date_string),
        "cards": info_card,
        "top_transactions": top_5,
        "currency_rates": exchange_rates(),
        "stock_prices": share_price(),
    }

    json_string = json.dumps(data, ensure_ascii=False, indent=2)
    return json_string
