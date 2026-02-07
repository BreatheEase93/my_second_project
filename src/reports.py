import logging
from datetime import datetime
from typing import Any, Callable, Optional, TypeVar

import pandas as pd
from dateutil.relativedelta import relativedelta

# Type variable for generic function typing
F = TypeVar('F', bound=Callable[..., Any])


def report_writer(function: F, filename: Optional[str] = None) -> F:
    """Декоратор для функций-отчетов, который записывает результат функции в файл,
    если filename не задан, имя создается автоматически."""

    def inner(*args: Any, **kwargs: Any) -> Any:
        result = function(*args, **kwargs)
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            func_name = function.__name__
            output_filename = f"report_{func_name}_{timestamp}.txt"
        else:
            output_filename = filename
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(str(result))

        return result

    return inner  # type: ignore


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    logger.info(f"Запуск функции. Категория: {category}, дата: {date}")

    if date is None:
        end_date = datetime.now()
        logger.info(f"Используем текущую дату: {end_date}")
    else:
        end_date = datetime.strptime(date, '%Y-%m-%d')
        logger.info(f"Используем дату: {end_date}")

    start_date = end_date - relativedelta(months=3)
    logger.info(f"Начальная дата: {start_date}")

    df = transactions.copy()
    logger.info(f"Входных строк: {len(df)}")

    df['date'] = pd.to_datetime(df['date'])

    mask1 = df['date'] >= start_date
    mask2 = df['date'] <= end_date
    mask3 = df['category'] == category

    filtered_df = df[mask1 & mask2 & mask3]
    logger.info(f"Найдено транзакций: {len(filtered_df)}")

    result_df = filtered_df.sort_values('date')

    return result_df
