import os
from typing import Any, Hashable

from dotenv import load_dotenv

from src.reports import load_transactions_to_dataframe, spending_by_category
from src.services import calculate_cashback_by_category, get_monthly_cashback_summary
from src.utils import read_transactions_from_excel
from src.views import main_views

load_dotenv()


def main() -> None:
    """Основная функция программы"""
    print("Веб-страницы: страница «Главная»")
    data: str = str(input("Введите дату для проверок или оставьте поле пустым:"))
    print(main_views(data))

    print("Сервисы: выгодные категории повышенного кешбэка")
    data_year: str = input("Введите год для проверок:")
    data_month: str = input("Введите месяц для проверок:")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "Data", "operations.xlsx")

    transactions: list[dict[Hashable, Any]] = read_transactions_from_excel(file_path)
    cashback_summary: list[dict[str, Any]] = get_monthly_cashback_summary(transactions, data_month, data_year)
    print(calculate_cashback_by_category(cashback_summary))

    print("Отчеты: траты по категории")
    data_new: str = input("Введите дату для проверок:")
    category: str = input("Введите категорию для проверок:")

    transactions_df = load_transactions_to_dataframe(file_path)
    print(spending_by_category(transactions_df, category, data_new))


if __name__ == "__main__":
    main()
