from psycopg2 import sql
import json
from datetime import date, datetime  # Импортируем date и datetime
from src.Algorithm.BDCache.DBConnect import get_ticket_cache_db_connection
from src.Algorithm.ParseAvia import fetch_prices
from src.Algorithm.ParseTrain import fetch_train_prices


def fetch_cached_ticket(origin, destination, departure_date, transport_type):
    """
    Получает билеты из кеша или делает запрос к API, если данных в кеше нет.
    """
    # Преобразуем departure_date в datetime.datetime, если это необходимо
    if isinstance(departure_date, date) and not isinstance(departure_date, datetime):
        departure_date = datetime.combine(departure_date, datetime.min.time())

    # Подключение к базе данных

    #conn = get_ticket_cache_db_connection()
    #cursor = conn.cursor()

    try:
        # Попытка найти билеты в кеше
        '''query = sql.SQL("""
            SELECT response_data FROM ticket_cache
            WHERE origin = %s AND destination = %s AND departure_date = %s AND transport_type = %s
            ORDER BY created_at DESC LIMIT 1
        """)
        cursor.execute(query, (origin, destination, departure_date, transport_type))
        result = cursor.fetchone()

        if result:
            #print("Данные найдены в кеше.")
            return result[0]  # Возвращаем JSON из базы данных'''

        # Если данных в кеше нет, делаем запрос
        if transport_type == "avia":
            api_response = fetch_prices(origin, destination, departure_date)
        elif transport_type == "train":
            api_response = fetch_train_prices(origin, destination, departure_date)
        else:
            raise ValueError("Неподдерживаемый тип транспорта")

        if not api_response:
            return None

        # Сохраняем ответ в кеш
        '''insert_query = sql.SQL("""
            INSERT INTO ticket_cache (origin, destination, departure_date, transport_type, response_data)
            VALUES (%s, %s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (origin, destination, departure_date, transport_type, json.dumps(api_response)))
        conn.commit()'''

        print("Данные получены и сохранены в кеш.")
        return api_response

    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None

    '''finally:
        cursor.close()
        conn.close()'''
