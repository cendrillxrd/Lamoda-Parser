"""
Одноразовое создание таблиц. Запуск из корня проекта:

    python db/create_tables.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.models import Base
from db.session import engine
from utils.log_helper import log_message


def create_tables():
    log_message('app', 'Создание таблиц в MySQL (если не существуют)', 'INFO')
    Base.metadata.create_all(bind=engine)
    log_message('app', 'Таблицы готовы', 'INFO')


if __name__ == '__main__':
    create_tables()
