from unittest.mock import Mock

import pytest


@pytest.fixture()
def valid_date_1() -> str:
    """Правильный форматы данных"""
    return "2024-03-11T05:26:18.671407"


@pytest.fixture()
def valid_date_2() -> str:
    """Правильный форматы данных"""
    return "2024-03-11T12:59:59"


@pytest.fixture()
def valid_date_3() -> str:
    """Правильный форматы данных"""
    return "2024-03-11T19:59:59"


@pytest.fixture()
def valid_date_4() -> str:
    """Правильный форматы данных"""
    return "2024-03-11T00:59:59"


@pytest.fixture()
def invalid_date_1() -> str:
    """Неправильный форматы данных"""
    return "2024-13-01"


@pytest.fixture()
def invalid_date_2() -> str:
    """Неправильный форматы данных"""
    return "2024-02-31"


@pytest.fixture()
def empty_string() -> str:
    """Пустая строка"""
    return ""


@pytest.fixture()
def empty_list() -> list:
    """Пустой список"""
    return []


@pytest.fixture()
def empty_number() -> None:
    """Полное отсутствие значения"""
    return None


@pytest.fixture()
def xlsx_file() -> str:
    """Путь файла transactions_excel.xlsx"""
    return "data/transactions_excel.xlsx"


@pytest.fixture()
def mock_xlsx_response():
    """Фикстура для мока ответа от xlsx файла"""
    mock_df = Mock()
    return mock_df


@pytest.fixture()
def sample_transactions():
    """Фикстура с примером транзакций"""
    return [
        {
            "Дата платежа": "2024-03-01T10:30:00",
            "Номер карты": "1234****5678",
            "Статус": "SUCCESS",
            "Сумма платежа": "1000.00",
            "Категория": "Продукты",
            "Описание": "Покупка в магазине",
        },
        {
            "Дата платежа": "2024-03-05T14:20:00",
            "Номер карты": "9876****5432",
            "Статус": "FAILED",
            "Сумма платежа": "2000.00",
            "Категория": "Рестораны",
            "Описание": "Обед в кафе",
        },
        {
            "Дата платежа": "2024-03-10T18:45:00",
            "Номер карты": "4567****8901",
            "Статус": "SUCCESS",
            "Сумма платежа": "1500.00",
            "Категория": "Транспорт",
            "Описание": "Такси",
        },
        {
            "Дата платежа": "2024-03-15T09:15:00",
            "Номер карты": "2345****6789",
            "Статус": "SUCCESS",
            "Сумма платежа": "3000.00",
            "Категория": "Развлечения",
            "Описание": "Кино",
        },
    ]


@pytest.fixture()
def transaction_missing_date():
    """Транзакция без даты платежа"""
    return {
        "Номер карты": "1111****2222",
        "Статус": "SUCCESS",
        "Сумма платежа": "500.00",
        "Категория": "Другое",
        "Описание": "Тестовая транзакция",
    }


@pytest.fixture()
def transaction_missing_card():
    """Транзакция без номера карты"""
    return {
        "Дата платежа": "2024-03-20T12:00:00",
        "Статус": "SUCCESS",
        "Сумма платежа": "750.00",
        "Категория": "Другое",
        "Описание": "Тестовая транзакция",
    }


@pytest.fixture
def basic_transactions():
    """Базовый набор транзакций"""
    return [
        {"last_digits": "1234****5678", "amount": "1000"},
        {"last_digits": "1234****5678", "amount": "500"},
        {"last_digits": "9999****0000", "amount": "2000"},
    ]


@pytest.fixture
def single_transaction():
    """Одна транзакция"""
    return [{"last_digits": "1234****5678", "amount": "100"}]


@pytest.fixture
def mixed_amounts_transactions():
    """Транзакции с разными суммами"""
    return [
        {"last_digits": "1234****5678", "amount": "-100"},
        {"last_digits": "1234****5678", "amount": "0"},
        {"last_digits": "1234****5678", "amount": "200"},
    ]


@pytest.fixture
def different_card_formats():
    """Транзакции с разными форматами номеров карт"""
    return [
        {"last_digits": "1234****5678", "amount": "100"},
        {"last_digits": "987654****3210", "amount": "200"},
        {"last_digits": "1111****9999", "amount": "300"},
    ]
