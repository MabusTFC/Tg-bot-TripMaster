from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env
load_dotenv()

# Настройки базы данных
TICKET_CACHE_DB_CONFIG = {
    "dbname": os.getenv("TICKET_CACHE_DB_NAME"),
    "user": os.getenv("TICKET_CACHE_DB_USER"),
    "password": os.getenv("TICKET_CACHE_DB_PASSWORD"),
    "host": os.getenv("TICKET_CACHE_DB_HOST"),
    "port": os.getenv("TICKET_CACHE_DB_PORT")
}