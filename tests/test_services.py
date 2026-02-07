import pytest

from src.services import calculate_cashback_by_category, get_monthly_cashback_summary


def test_get_monthly_cashback_summary_valid_period(sample_transactions, transaction_missing_date):
    """Тест с корректным месяцем и годом"""
    result = get_monthly_cashback_summary(sample_transactions, "03", "2024")

    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]["category"] == "Супермаркеты"
    assert result[0]["cashback"] == 150.0
    assert result[1]["category"] == "Транспорт"
    assert result[1]["cashback"] == 50.0

    """Тест что транзакции без кэшбэка фильтруются"""
    transactions_with_missing = sample_transactions + [transaction_missing_date]
    result = get_monthly_cashback_summary(transactions_with_missing, "03", "2024")

    assert isinstance(result, list)
    assert len(result) == 3

    """Тест когда нет транзакций в указанном месяце"""
    result = get_monthly_cashback_summary(sample_transactions, "04", "2024")

    assert isinstance(result, list)
    assert len(result) == 0

    """Тест с невалидным месяцем"""
    result = get_monthly_cashback_summary(sample_transactions, "13", "2024")

    assert isinstance(result, list)
    assert len(result) == 0


def test_calculate_cashback_by_category_basic(
    basic_transactions, empty_list, different_card_formats, single_transaction, mixed_amounts_transactions
):
    """Основные тесты"""
    result = calculate_cashback_by_category(basic_transactions)

    assert len(result) == 2
    assert all(isinstance(r, dict) for r in result)
    assert all(len(r) == 1 for r in result)

    categories_dict = {}
    for item in result:
        categories_dict.update(item)

    assert categories_dict["Супермаркеты"] == 225
    assert categories_dict["Транспорт"] == 300

    """Граничные случаи"""
    assert calculate_cashback_by_category(empty_list) == []

    result = calculate_cashback_by_category(single_transaction)
    assert "Продукты" in result[0]
    assert result[0]["Продукты"] == 50

    result = calculate_cashback_by_category(mixed_amounts_transactions)
    assert "Продукты" in result[0]
    assert result[0]["Продукты"] == 175

    """Тест с разными категориями"""
    result = calculate_cashback_by_category(different_card_formats)
    all_categories = []
    for item in result:
        all_categories.extend(item.keys())

    assert set(all_categories) == {"Супермаркеты", "Транспорт", "Рестораны"}

    """Обработка некорректных данных"""
    with pytest.raises(KeyError):
        calculate_cashback_by_category([{"cashback": "100"}])

    result = calculate_cashback_by_category([{"category": "", "cashback": "100"}])
    assert len(result) == 1
    assert "" in result[0]
    assert result[0][""] == 100
