from datetime import datetime

from dateutil import parser


def period_of_time(date_string: str) -> str:
    """Функция, которая получает на вход дату и возвращает первый день месяца."""
    try:
        date_object = parser.parse(date_string)
        date_object_new = datetime.strftime(date_object, "1.%m.%Y")
        return str(date_object_new)
    except (ValueError, TypeError, OverflowError):
        return "Неверные данные. Пример: 2024-03-11T02:26:18.671407"


def hello() -> str:
    """Функция, которая получает на вход дату и возвращает приветствие."""
    pass


def information_on_cards():
    """Функция, которая получает на вход 2 даты и возвращает список трат по каждой карте и кэшбэк."""
    pass


def top_5_transactions():
    """Функция, которая получает на вход 2 даты и возвращает Топ-5 транзакций по сумме платежа."""
    pass


def exchange_rates():
    """Функция, которая выводит курс валют, настройки в файле user_settings.json."""
    pass


def share_price():
    """Функция, которая выводит стоимость акций, настройки в файле user_settings.json."""
    pass
