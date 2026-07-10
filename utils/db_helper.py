from repositories.lamoda_nomenclature_repository import LamodaNomenclatureRepository
from repositories.lamoda_orders_repository import LamodaOrdersRepository
from utils.log_helper import log_message

TABLE_LAMODA_ORDERS = 'lamoda_orders'
TABLE_LAMODA_NOMENCLATURE = 'lamoda_nomenclature'

_orders_repo = LamodaOrdersRepository()
_nomenclature_repo = LamodaNomenclatureRepository()


def save_info(info: dict) -> None:
    """Сохраняет таблицы в MySQL (upsert по уникальному ключу вместо CSV)."""
    repos = {
        TABLE_LAMODA_ORDERS: _orders_repo,
        TABLE_LAMODA_NOMENCLATURE: _nomenclature_repo,
    }
    for key, df in info.items():
        repo = repos.get(key)
        if repo is None:
            log_message('app', f'Нет репозитория для ключа {key}, таблица не сохранена', 'WARNING')
            continue
        repo.upsert_dataframe(df)
        log_message('app', f'Таблица {key} сохранена в MySQL', 'INFO')
