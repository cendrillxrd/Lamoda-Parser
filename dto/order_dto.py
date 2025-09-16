from dataclasses import asdict, dataclass

from config import LIMIT_ORDER
from utils.date_helper import get_daily_date_range


@dataclass
class OrderDTO:
    limit: int = LIMIT_ORDER
    page: int = 1
    filter: str = get_daily_date_range()
    sort: str = 'createdAt'
