import logging
import os
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.reports import report_writer, spending_by_category


@pytest.mark.parametrize(
    "content,filename",
    [
        ("Текст отчета", None),  # Автоимя
        ("Другой отчет", "custom.txt"),  # Кастомное имя
        ("", None),  # Пустой отчет
        ("123", "numbers.txt"),  # Числа как строка
    ],
)
def test_report_writer_basic(content, filename):
    """Базовый тест с параметризацией"""

    # Создаем функцию с декоратором для каждого случая
    if filename is None:

        @report_writer
        def test_func():
            return content

        result = test_func()

        files = [f for f in os.listdir() if f.startswith("report_test_func_")]
        assert len(files) == 1
        file_to_check = files[0]
    else:

        def test_func():
            return content

        decorated_func = report_writer(test_func, filename)
        result = decorated_func()
        file_to_check = filename

    assert result == content
    assert os.path.exists(file_to_check)

    with open(file_to_check, 'r', encoding='utf-8') as f:
        assert f.read() == str(content)


def test_report_writer_args():
    """Тест с аргументами функции"""

    @report_writer
    def func_with_args(a, b, c=10):
        return f"Result: {a + b + c}"

    result = func_with_args(5, 3, c=2)
    assert result == "Result: 10"


def test_report_writer_unicode():
    """Тест с русскими символами и эмодзи"""

    @report_writer
    def russian_func():
        return "Русский текст 🌍 Привет!"

    result = russian_func()
    assert result == "Русский текст 🌍 Привет!"

    files = [f for f in os.listdir() if f.startswith("report_russian_func_")]
    assert len(files) == 1

    with open(files[0], 'r', encoding='utf-8') as f:
        assert f.read() == "Русский текст 🌍 Привет!"


def test_report_writer_mocked():
    """Тест с моком файловой системы"""

    @report_writer
    def mocked_func():
        return "моковый текст"

    with patch('builtins.open', mock_open()) as mock_file:
        result = mocked_func()

        assert result == "моковый текст"
        assert mock_file.called


def test_spending_logic():
    """Тест на правильную логику выборки по датам"""
    df = pd.DataFrame(
        {
            'date': [
                '2024-01-01',
                '2024-01-15',
                '2024-02-01',
                '2024-02-15',
                '2024-03-01',
                '2023-12-01',
                '2023-11-01',
            ],
            'category': ['Еда'] * 7,
            'amount': [100] * 7,
        }
    )

    result = spending_by_category(df, 'Еда', '2024-03-31')
    assert len(result) == 5

    result = spending_by_category(df, 'Еда', '2024-02-28')
    assert len(result) == 5
    assert all(result['date'] >= pd.Timestamp('2023-12-01'))
    assert all(result['date'] <= pd.Timestamp('2024-02-28'))


def test_with_date(basic_df):
    """Работает с указанной датой"""
    result = spending_by_category(basic_df, 'Еда', '2024-02-28')
    # За 3 месяца до 28 февраля: декабрь, январь, февраль
    # Попадают: 2023-12-20, 2024-01-15, 2024-02-10
    assert len(result) == 3


def test_empty_result(basic_df):
    """Нет трат по категории"""
    result = spending_by_category(basic_df, 'Несуществующая', '2024-12-31')
    assert len(result) == 0


def test_empty_df(empty_df):
    """Пустой вход"""
    result = spending_by_category(empty_df, 'Еда', '2024-12-31')
    assert len(result) == 0


def test_bad_date_format(basic_df):
    """Неправильный формат даты"""
    with pytest.raises(ValueError):
        spending_by_category(basic_df, 'Еда', '2024/02/28')


def test_null_date(basic_df):
    """Дата = None"""
    # Используем текущую дату, но проверяем только тип
    result = spending_by_category(basic_df, 'Еда', None)
    assert isinstance(result, pd.DataFrame)


def test_sorting(basic_df):
    """Проверка сортировки"""
    result = spending_by_category(basic_df, 'Еда', '2024-02-28')
    assert result['date'].is_monotonic_increasing


def test_boundary_date():
    """Граничная дата 31 марта"""
    df = pd.DataFrame({'date': ['2024-03-31', '2024-01-01'], 'category': ['Еда', 'Еда'], 'amount': [100, 200]})
    result = spending_by_category(df, 'Еда', '2024-03-31')
    assert len(result) == 2  # Оба попадают


def test_logging(basic_df, caplog):
    """Логи пишутся"""
    with caplog.at_level(logging.INFO):
        spending_by_category(basic_df, 'Еда', '2024-12-31')
    assert 'Запуск функции' in caplog.text
    assert 'Найдено транзакций' in caplog.text


def test_original_not_changed(basic_df):
    """Исходный DF не меняется"""
    original = basic_df.copy()
    spending_by_category(basic_df, 'Еда', '2024-12-31')
    pd.testing.assert_frame_equal(original, basic_df)
