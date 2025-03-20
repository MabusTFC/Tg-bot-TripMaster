import psycopg2
from src.Algorithm.BDCache.config import TICKET_CACHE_DB_CONFIG  # Импортируем конфигурацию базы данных

def get_ticket_cache_db_connection():
    try:
        # Подключение к базе данных кеширования билетов
        return psycopg2.connect(**TICKET_CACHE_DB_CONFIG)
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        raise