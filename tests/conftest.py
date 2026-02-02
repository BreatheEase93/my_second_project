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
