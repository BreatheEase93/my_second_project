from unittest.mock import patch

import pytest

from src.views import hello, info_fo_card, information_on_transactions, period_of_time, read_transactions_from_excel


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


def test_information_on_transactions_valid_period(
    valid_date_1, valid_date_4, sample_transactions, transaction_missing_date
):
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
    assert cards_dict["0000"]["total_spent"] == 2000
    assert cards_dict["0000"]["cashback"] == 20.0

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
