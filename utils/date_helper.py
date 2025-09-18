from datetime import datetime, timedelta
import pytz


def get_today_date() -> str:
    """Возвращает текущую дату в формате 'YYYY-MM-DD'."""
    return datetime.now().strftime('%Y-%m-%d')


def get_formatted_date(input_date_str):
    """
    Преобразует дату в формате 'YYYY-MM-DD' в datetime объект
    с временем 23:50:00 в московском часовом поясе.

    Parameters:
    input_date_str (str): Дата в формате '2025-09-16'

    Returns:
    datetime: Объект datetime с временем 23:50:00 в Europe/Moscow
    """
    tz = pytz.timezone('Europe/Moscow')

    # Парсим входную дату
    input_date = datetime.strptime(input_date_str, '%Y-%m-%d')

    # Устанавливаем время 23:50:00 и применяем временную зону
    result_date = input_date.replace(hour=23, minute=50, second=0, microsecond=0)
    result_date = tz.localize(result_date)

    return result_date


def get_daily_date_range(date) -> str:
    """
    Возвращает диапазон дат в формате: createdAt>=<start_timestamp,end_timestamp>
    где start_timestamp - вчера 23:50, end_timestamp - сегодня 23:50
    """
    today_23 = date

    # Вчерашняя дата в 23:55
    yesterday_23 = today_23 - timedelta(days=1)

    # Форматируем в требуемый формат (YYYYMMDDHHMMSS)
    start_timestamp = yesterday_23.strftime('%Y%m%d%H%M%S')
    end_timestamp = today_23.strftime('%Y%m%d%H%M%S')

    return f"createdAt>=<{start_timestamp},{end_timestamp}"
