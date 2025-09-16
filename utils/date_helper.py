from datetime import datetime, timedelta
import pytz


def get_daily_date_range() -> str:
    """
    Возвращает диапазон дат в формате: createdAt>=<start_timestamp,end_timestamp>
    где start_timestamp - вчера 23:00, end_timestamp - сегодня 23:00
    """
    # Устанавливаем временную зону (можно изменить на нужную)
    tz = pytz.timezone('Europe/Moscow')

    # Получаем текущее время в нужной временной зоне
    now = datetime.now(tz)

    # Сегодняшняя дата в 23:00
    today_23 = now.replace(hour=23, minute=0, second=0, microsecond=0)

    # Вчерашняя дата в 23:00
    yesterday_23 = today_23 - timedelta(days=1)

    # Форматируем в требуемый формат (YYYYMMDDHHMMSS)
    start_timestamp = yesterday_23.strftime('%Y%m%d%H%M%S')
    end_timestamp = today_23.strftime('%Y%m%d%H%M%S')

    return f"createdAt>=<{start_timestamp},{end_timestamp}"
