from datetime import datetime, timedelta
from typing import Literal, Union

import pytz


def get_today_date() -> str:
    """Возвращает текущую дату в формате 'YYYY-MM-DD'."""
    return datetime.now().strftime('%Y-%m-%d')


def get_formatted_date(input_date_str: str):
    """
    Преобразует дату в формате 'YYYY-MM-DD' в datetime объект
    с текущим временем (без микросекунд) в московском часовом поясе.
    """
    tz = pytz.timezone('Europe/Moscow')

    # Получаем текущее время
    now = datetime.now(tz)

    # Парсим входную дату
    input_date = datetime.strptime(input_date_str, '%Y-%m-%d')

    # Устанавливаем текущее время (без микросекунд)
    result_date = input_date.replace(
        hour=now.hour,
        minute=now.minute,
        second=now.second,
        microsecond=0  # убираем микросекунды
    )
    result_date = tz.localize(result_date)

    return result_date


def get_daily_date_range(date, period: Literal['day', 'month'] = None) -> Union[str, None]:
    """
    Возвращает диапазон дат в формате: createdAt>=<start_timestamp,end_timestamp>
    где start_timestamp - вчера 23:30, end_timestamp - сегодня 23:30
    """
    if period == 'day':
        today = date

        # Вчерашняя дата в 23:30
        yesterday_23 = today - timedelta(days=1)

        # Форматируем в требуемый формат (YYYYMMDDHHMMSS)
        start_timestamp = yesterday_23.strftime('%Y%m%d%H%M%S')
        end_timestamp = today.strftime('%Y%m%d%H%M%S')
        return f"createdAt>=<{start_timestamp},{end_timestamp}"
    elif period == 'month':
        today_23 = date

        # дата в 23:30 месяц назад
        month_ago_23 = today_23 - timedelta(days=21)

        # Форматируем в требуемый формат (YYYYMMDDHHMMSS)
        start_timestamp = month_ago_23.strftime('%Y%m%d%H%M%S')
        end_timestamp = today_23.strftime('%Y%m%d%H%M%S')
        return f"createdAt>=<{start_timestamp},{end_timestamp}"
    return None
