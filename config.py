import os

from dotenv import load_dotenv

load_dotenv()

BASE_URLS = {
    'live': 'https://api-b2b.lamoda.ru',
    'demo': 'https://api-demo-b2b.lamoda.ru',
}

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
