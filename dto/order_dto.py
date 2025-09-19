from dataclasses import asdict, dataclass, field
from typing import Literal

from config import LIMIT_ORDER
from utils.date_helper import get_daily_date_range, get_formatted_date, get_today_date


@dataclass
class OrderDTO:
    limit: int = LIMIT_ORDER
    page: int = 1
    sort: str = 'createdAt'
    filter: str = field(init=False)

    def __post_init__(self):
        # Используем текущую дату по умолчанию
        self.filter = get_daily_date_range(get_formatted_date(get_today_date()), 'day')

    @classmethod
    def with_date(cls, date_str: str, period: Literal['day', 'month'] = None, **kwargs):
        """Альтернативный конструктор с указанием даты"""
        instance = cls(**kwargs)
        instance.filter = get_daily_date_range(get_formatted_date(date_str), period)
        return instance
