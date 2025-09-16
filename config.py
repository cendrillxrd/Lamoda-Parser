import os

from dotenv import load_dotenv

load_dotenv()

BASE_URLS = {
    'live': 'https://api-b2b.lamoda.ru',
    'demo': 'https://api-demo-b2b.lamoda.ru',
}

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

LIMIT_NOMENCLATURE = 1000
LIMIT_STOCK = 1000
LIMIT_ORDER = 100
TIME_SLEEP_NOMENCLATURES = 10
TIME_SLEEP_STOCK = 10
TIME_SLEEP_ORDER = 10
