from unittest.mock import patch

import pytest

from src.views import hello, period_of_time, read_transactions_from_excel


def test_period_of_time(valid_date_1, valid_date_2, invalid_date_1, invalid_date_2, empty_string):
    """Тест функции period_of_time"""
    assert period_of_time(valid_date_1) == "1.03.2024"
    assert period_of_time(valid_date_2) == "1.03.2024"
    assert period_of_time(invalid_date_1) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
    assert period_of_time(invalid_date_2) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
    assert period_of_time(empty_string) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"


def test_hello(valid_date_1, valid_date_2, valid_date_3, valid_date_4, invalid_date_1, invalid_date_2, empty_string):
    """Тест функции period_of_time"""
    assert hello(valid_date_1) == "Доброе утро"
    assert hello(valid_date_2) == "Добрый день"
    assert hello(valid_date_3) == "Добрый вечер"
    assert hello(valid_date_4) == "Доброй ночи"
    assert hello(invalid_date_1) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
    assert hello(invalid_date_2) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
    assert hello(empty_string) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"

def test_read_transactions_from_excel_success(xlsx_file: str, mock_xlsx_response):
    """Тест успешного чтения Excel файла"""
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


def test_read_transactions_from_excel_file_not_found(xlsx_file: str):
    """Тест обработки отсутствующего Excel файла"""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError) as exc_info:
            read_transactions_from_excel(xlsx_file)

        assert f"Файл '{xlsx_file}' не найден." in str(exc_info.value)


def test_read_transactions_from_excel_general_exception(xlsx_file: str):
    """Тест обработки общей ошибки при чтении Excel"""
    error_msg = "Произвольная ошибка Excel"

    with patch("pandas.read_excel", side_effect=Exception(error_msg)):
        with pytest.raises(Exception) as exc_info:
            read_transactions_from_excel(xlsx_file)

        assert f"Ошибка при обработке Excel-файла: {error_msg}" in str(exc_info.value)


def test_read_transactions_from_excel_empty_file(xlsx_file: str, mock_xlsx_response):
    """Тест чтения пустого Excel файла"""
    mock_df = mock_xlsx_response
    mock_df.to_dict.return_value = []

    with patch("pandas.read_excel", return_value=mock_df):
        result = read_transactions_from_excel(xlsx_file)

        assert isinstance(result, list)
        assert len(result) == 0