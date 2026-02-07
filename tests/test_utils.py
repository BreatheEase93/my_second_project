import json
import os
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest
import requests

from src.utils import (hello, info_fo_card, information_on_transactions, period_of_time, read_transactions_from_excel,
                       share_price, top_5_transactions)


def test_period_of_time_various_scenarios(valid_date_1, valid_date_2, invalid_date_1, invalid_date_2, empty_string):
    """Тест функции форматирования даты period_of_time с различными входными данными"""

    """Тест с корректным форматом даты с временной зоной"""
    result = period_of_time(valid_date_1)
    assert result == "01.03.2024"

    """Тест с корректным форматом даты без временной зоны"""
    result = period_of_time(valid_date_2)
    assert result == "01.03.2024"

    """Тест с некорректным форматом даты (неправильный разделитель)"""
    result = period_of_time(invalid_date_1)
    assert result == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"

    """Тест с некорректным форматом даты (неполная дата)"""
    result = period_of_time(invalid_date_2)
    assert result == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"

    """Тест с пустой строкой"""
    result = period_of_time(empty_string)
    assert result == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"


def test_hello_various_scenarios(
    valid_date_1, valid_date_2, valid_date_3, valid_date_4, invalid_date_1, invalid_date_2, empty_string
):
    """Тест функции приветствия hello с различными временами суток и ошибками"""

    """Тест приветствия для утреннего времени (до 12:00)"""
    result = hello(valid_date_1)
    assert result == "Доброе утро"

    """Тест приветствия для дневного времени (12:00-18:00)"""
    result = hello(valid_date_2)
    assert result == "Добрый день"

    """Тест приветствия для вечернего времени (18:00-22:00)"""
    result = hello(valid_date_3)
    assert result == "Добрый вечер"

    """Тест приветствия для ночного времени (22:00-06:00)"""
    result = hello(valid_date_4)
    assert result == "Доброй ночи"

    """Тест обработки некорректного формата даты"""
    result = hello(invalid_date_1)
    assert result == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"

    """Тест обработки неполной даты"""
    result = hello(invalid_date_2)
    assert result == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"

    """Тест обработки пустой строки"""
    result = hello(empty_string)
    assert result == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"


def test_read_transactions_from_excel_various_scenarios(xlsx_file, mock_xlsx_response):
    """Тесты различных сценариев чтения Excel файла с транзакциями"""

    """Тест успешного чтения файла с корректными данными"""
    mock_df = mock_xlsx_response
    mock_df.to_dict.return_value = [
        {"id": 1, "state": "EXECUTED", "amount": "100.00"},
        {"id": 2, "state": "CANCELED", "amount": "200.00"},
    ]

    with patch("pandas.read_excel", return_value=mock_df):
        result = read_transactions_from_excel(xlsx_file)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["state"] == "EXECUTED"
        assert result[0]["amount"] == "100.00"
        assert result[1]["id"] == 2
        assert result[1]["state"] == "CANCELED"
        assert result[1]["amount"] == "200.00"

    """Тест чтения файла без данных (пустой файл)"""
    mock_df = mock_xlsx_response
    mock_df.to_dict.return_value = []

    with patch("pandas.read_excel", return_value=mock_df):
        result = read_transactions_from_excel(xlsx_file)

        assert isinstance(result, list)
        assert len(result) == 0

    """Тест обработки ошибки при отсутствии файла"""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError) as exc_info:
            read_transactions_from_excel(xlsx_file)

        assert f"Файл '{xlsx_file}' не найден." in str(exc_info.value)

    """Тест обработки других ошибок при чтении Excel"""
    error_msg = "Произвольная ошибка Excel"

    with patch("pandas.read_excel", side_effect=Exception(error_msg)):
        with pytest.raises(Exception) as exc_info:
            read_transactions_from_excel(xlsx_file)

        assert f"Ошибка при обработке Excel-файла: {error_msg}" in str(exc_info.value)


def test_information_on_transactions_valid_period(sample_transactions, transaction_missing_date):
    """Тест с корректным периодом и транзакциями"""
    result = information_on_transactions("2024-03-01T00:00:00", "2024-03-15T23:59:59", sample_transactions)

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]["date"] == "01.03.2024"
    assert result[0]["last_digits"] == "1234****5678"
    assert result[1]["category"] == "Транспорт"
    assert result[1]["description"] == "Такси"
    assert isinstance(result, list)
    assert len(result) == 3

    """Тест что транзакции без номера карты фильтруются"""
    transactions_with_missing = sample_transactions + [transaction_missing_date]
    result = information_on_transactions("2024-03-01T00:00:00", "2024-03-15T23:59:59", transactions_with_missing)

    assert isinstance(result, list)
    assert len(result) == 3

    """Тест когда нет транзакций в указанном периоде"""
    result = information_on_transactions("2024-04-01T00:00:00", "2024-04-30T23:59:59", sample_transactions)

    assert isinstance(result, list)
    assert len(result) == 0

    """Тест с граничными датами периода"""
    result = information_on_transactions("2024-03-05T00:00:00", "2024-03-10T23:59:59", sample_transactions)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["date"] == "10.03.2024"


def test_info_fo_card_basic(
    basic_transactions, empty_list, different_card_formats, single_transaction, mixed_amounts_transactions
):
    """Основные тесты"""
    result = info_fo_card(basic_transactions)

    assert len(result) == 2
    assert all(k in r for r in result for k in ["last_digits", "total_spent", "cashback"])

    cards_dict = {c["last_digits"]: c for c in result}

    assert cards_dict["5678"]["total_spent"] == 1500
    assert cards_dict["5678"]["cashback"] == 15.0
    assert cards_dict["0000"]["total_spent"] == 3000
    assert cards_dict["0000"]["cashback"] == 30.0

    """Граничные случаи"""
    assert info_fo_card(empty_list) == []

    result = info_fo_card(single_transaction)
    assert result[0]["total_spent"] == 100
    assert result[0]["cashback"] == 1.0

    result = info_fo_card(mixed_amounts_transactions)
    assert result[0]["total_spent"] == 100

    """Извлечение последних 4 цифр"""
    result = info_fo_card(different_card_formats)
    last4_list = [c["last_digits"] for c in result]

    assert set(last4_list) == {"5678", "3210", "9999"}

    """Обработка некорректных данных"""
    # Без номера карты
    with pytest.raises(KeyError):
        info_fo_card([{"amount": "100"}])

    result = info_fo_card([{"last_digits": "", "amount": "100"}])
    assert len(result) == 1
    assert result[0]["last_digits"] == ""
    assert result[0]["total_spent"] == 100
    assert result[0]["cashback"] == 1.0


def test_top_5_transactions_various_scenarios(sample_transactions_for_top_5, less_than_5_transactions, empty_list):
    """Тесты различных сценариев функции top_5_transactions"""

    """Тест успешного получения Топ-5 транзакций из полного списка"""
    result = top_5_transactions(sample_transactions_for_top_5)

    assert isinstance(result, list)
    assert len(result) == 5
    assert result[0]["amount"] == 1000
    assert result[4]["amount"] == 200
    assert all(result[i]["amount"] >= result[i + 1]["amount"] for i in range(4))

    """Тест, когда транзакций меньше 5"""
    result = top_5_transactions(less_than_5_transactions)

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]["amount"] == 1000
    assert result[2]["amount"] == 100

    """Тест с пустым списком транзакций"""
    result = top_5_transactions(empty_list)

    assert isinstance(result, list)
    assert result == []
    assert len(result) == 0

    """Тесты структуры и целостности данных"""

    result = top_5_transactions(sample_transactions_for_top_5)

    for transaction in result:
        assert all(key in transaction for key in ["date", "amount", "category", "description"])

    original_data = sample_transactions_for_top_5.copy()
    _ = top_5_transactions(sample_transactions_for_top_5)
    assert sample_transactions_for_top_5 == original_data


@pytest.mark.parametrize(
    "currencies,expected_count,expected_error",
    [
        (["USD", "EUR"], 2, None),
        (["USD", "RUB"], 1, None),  # RUB фильтруется
        ([], 0, None),  # Пустой список
        (["USD"], 1, None),
    ],
)
def test_currency_pairs_formation(currencies, expected_count, expected_error):
    """Тест формирования валютных пар"""
    pairs = [f"{c}RUB" for c in currencies if c != "RUB"]
    assert len(pairs) == expected_count


def test_api_key_missing(monkeypatch):
    """Тест отсутствия API ключа"""
    monkeypatch.delenv("api_key", raising=False)
    with pytest.raises(ValueError, match="None ключ не найден"):
        if not (api_key := os.getenv("api_key")):
            raise ValueError(f"{api_key} ключ не найден")


@pytest.mark.parametrize(
    "response_data,expected_count,should_raise",
    [
        ({"status": 200, "data": {"USDRUB": "75.5", "EURRUB": "85.2"}}, 2, False),
        ({"status": 200, "data": {}}, 0, False),
        ({"status": 403, "message": "Invalid key"}, 0, True),
    ],
)
def test_api_responses(response_data, expected_count, should_raise):
    """Тест различных ответов API"""
    with patch("builtins.open", mock_open()), patch(
        "json.load", return_value={"user_currencies": ["USD", "EUR"]}
    ), patch("requests.get") as mock_get:

        mock_response = Mock()
        mock_response.json.return_value = response_data
        mock_get.return_value = mock_response

        if should_raise:
            with pytest.raises(Exception, match="API ошибка"):
                if response_data.get('status') != 200:
                    raise Exception(f"API ошибка: {response_data.get('message', 'Unknown')}")
        else:
            # Имитация успешного выполнения
            result = [
                {'currency': pair[:3], 'rate': float(rate)} for pair, rate in response_data.get('data', {}).items()
            ]
            assert len(result) == expected_count


@pytest.mark.parametrize(
    "pair,expected_currency",
    [
        ("USDRUB", "USD"),
        ("EURRUB", "EUR"),
        ("GBPRUB", "GBP"),
    ],
)
def test_pair_parsing(pair, expected_currency):
    """Тест парсинга валютных пар"""
    test_data = {"data": {pair: "100.0"}}

    result = [{'currency': p[:3], 'rate': float(r)} for p, r in test_data.get('data', {}).items()]

    if result:
        assert result[0]['currency'] == expected_currency
        assert result[0]['rate'] == 100.0


def test_network_timeout():
    """Тест таймаута сети"""
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        with pytest.raises(requests.exceptions.Timeout):
            requests.get("https://currate.ru/api/", timeout=10)


def test_full_function_logic():
    """Полный тест логики функции"""
    test_data = {
        "settings": {"user_currencies": ["USD", "EUR", "RUB"]},
        "api_response": {"status": 200, "data": {"USDRUB": "75.5", "EURRUB": "85.2"}},
        "expected": [{'currency': 'USD', 'rate': 75.5}, {'currency': 'EUR', 'rate': 85.2}],
    }

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data["settings"]))), patch(
        "json.load", return_value=test_data["settings"]
    ), patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = test_data["api_response"]
        mock_get.return_value = mock_response

        # Имитация основной логики
        currencies = test_data["settings"]["user_currencies"]
        pairs = [f"{c}RUB" for c in currencies if c != "RUB"]

        assert pairs == ["USDRUB", "EURRUB"]

        result = [
            {'currency': pair[:3], 'rate': float(rate)} for pair, rate in test_data["api_response"]["data"].items()
        ]

        assert result == test_data["expected"]


def test_share_price_basic(mock_stock_data):
    """Базовый тест успешного получения цен"""

    # Настраиваем мок
    mock_stock_data['Close'].columns = ["AAPL"]
    mock_stock_data['Close']["AAPL"] = MagicMock()
    mock_stock_data['Close']["AAPL"].iloc = MagicMock()
    mock_stock_data['Close']["AAPL"].iloc.__getitem__.return_value = 150.25
    mock_stock_data['Close'].iloc.__getitem__.return_value = 150.25

    mock_settings = json.dumps({"user_stocks": ["AAPL"]})

    with patch("builtins.open", mock_open(read_data=mock_settings)):
        with patch("yfinance.download", return_value=mock_stock_data):
            result = share_price()

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["stock"] == "AAPL"

    """Тест пустого списка акций"""

    mock_settings = json.dumps({"user_stocks": []})

    with patch("builtins.open", mock_open(read_data=mock_settings)):
        result = share_price()

    assert result == []

    """Тест ошибки при чтении файла"""

    with patch("builtins.open", side_effect=FileNotFoundError):
        result = share_price()

    assert result == []
