"""
Проверка подключения к MySQL. Запуск из корня проекта:

    python scripts/test_db_connection.py
"""
import sys
from pathlib import Path

from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.session import DATABASE_URL, DB_HOST, DB_NAME, DB_PORT, DB_USER, engine
from utils.log_helper import log_message


def test_connection() -> None:
    safe_url = DATABASE_URL.replace(DB_USER, '***', 1)
    log_message('app', f'Проверка подключения: host={DB_HOST}, port={DB_PORT}, db={DB_NAME}, url={safe_url}', 'INFO')

    try:
        with engine.connect() as conn:
            version = conn.execute(text('SELECT VERSION()')).scalar()
            db_name = conn.execute(text('SELECT DATABASE()')).scalar()
            tables = conn.execute(text('SHOW TABLES')).fetchall()

        log_message('app', f'Подключение успешно. Версия MySQL: {version}', 'INFO')
        log_message('app', f'Текущая база: {db_name}', 'INFO')

        if tables:
            table_names = [t[0] for t in tables]
            log_message('app', f'Таблицы в базе: {table_names}', 'INFO')
        else:
            log_message('app', 'В базе пока нет таблиц. Запусти python db/create_tables.py', 'WARNING')

    except Exception as err:
        log_message('app', f'Не удалось подключиться к БД: {err}', 'ERROR')
        raise


if __name__ == '__main__':
    test_connection()
