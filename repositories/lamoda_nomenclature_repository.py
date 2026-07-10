from dataclasses import asdict

from db.models import LamodaNomenclatureModel
from dto.columns_nomenclature_dto import ColumnsNomenclatureDTO
from repositories.base_repository import BaseRepository

_nomenclature_columns = asdict(ColumnsNomenclatureDTO())


class LamodaNomenclatureRepository(BaseRepository):
    model = LamodaNomenclatureModel
    unique_columns = ('supplier_sku', 'date')
    column_mapping = {russian: english for english, russian in _nomenclature_columns.items()}
