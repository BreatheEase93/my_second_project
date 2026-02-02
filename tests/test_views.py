from src.views import period_of_time, hello


def test_period_of_time(valid_date_1, valid_date_2, invalid_date_1, invalid_date_2, empty_string):
    """Тест функции period_of_time"""
    assert period_of_time(valid_date_1) == "1.03.2024"
    assert period_of_time(valid_date_2) == "1.03.2024"
    assert period_of_time(invalid_date_1) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
    assert period_of_time(invalid_date_2) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
    assert period_of_time(empty_string) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"

def test_hello(valid_date_1, valid_date_2, valid_date_3, valid_date_4, invalid_date_1, invalid_date_2, empty_string):
    """Тест функции period_of_time"""
    assert period_of_time(valid_date_1) == "Доброе утро"
    assert period_of_time(valid_date_2) == "Добрый день"
    assert period_of_time(valid_date_3) == "Добрый вечер"
    assert period_of_time(valid_date_4) == "Доброй ночи"
    assert period_of_time(invalid_date_1) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
    assert period_of_time(invalid_date_2) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
    assert period_of_time(empty_string) == "Неверные данные. Пример: 2024-03-11T02:26:18.671407"
