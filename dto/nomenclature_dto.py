from dataclasses import asdict, dataclass

from config import LIMIT_NOMENCLATURE


@dataclass
class NomenclatureDTO:
    limit: int = LIMIT_NOMENCLATURE
    page: int = 1
