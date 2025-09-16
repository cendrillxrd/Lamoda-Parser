from dataclasses import asdict, dataclass

from config import LIMIT_ORDER


@dataclass
class OrderDTO:
    limit: int = LIMIT_ORDER
    page: int = 1
