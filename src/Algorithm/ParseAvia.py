import os
import requests
import json
from .config import *


def fetch_prices(origin, destination, current_date):
    """
    Выполняет запрос к API Aviasales для получения самых дешёвых билетов за указанные даты.
    """
    origin_iata = city_to_iata.get(origin)
    destination_iata = city_to_iata.get(destination)

    if not origin_iata or not destination_iata:
        print(f"Не найден IATA-код для города: {origin} или {destination}")
        return

    params = {
        "origin": origin_iata,  # IATA-код города отправления
        "destination": destination_iata,  # IATA-код города назначения
        "departure_at": current_date.strftime("%Y-%m-%d"),  # Дата отправления (строка)
        "direct": "false",  # Разрешаем рейсы с пересадками
        "sorting": "price",  # Сортировка по цене
        "currency": "rub",  # Валюта
        "limit": 30,  # Количество записей в ответе
        "page": 1,  # Номер страницы для пагинации
        "one_way": "true"  # Флаг для получения билета в одну сторону
    }

    endpoint = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    params['token'] = API_KEY_AVI # Добавляем API-ключ в параметры запроса
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Проверка на успешный статус запроса
        return response.json()
    except requests.RequestException as e:
        print("Ошибка при выполнении запроса к API:", e)
        return None

def print_detailed_flights(result, base_url="https://www.aviasales.ru"):
    """
    Выводит максимально подробный форматированный вывод данных о рейсах.
    Для каждого найденного билета выводятся все поля, которые возвращает API.
    """
    if result and result.get("data"):
        print("Найденные билеты:")
        for index, flight in enumerate(result["data"], start=1):
            print("=" * 50)
            print(f"Билет #{index}")
            print("=" * 50)
            print(f"Пункт отправления (код): {flight.get('origin', 'N/A')}")
            print(f"Пункт назначения (код): {flight.get('destination', 'N/A')}")
            print(f"Аэропорт отправления: {flight.get('origin_airport', 'N/A')}")
            print(f"Аэропорт прибытия: {flight.get('destination_airport', 'N/A')}")
            print(f"Цена билета: {flight.get('price', 'N/A')} {result.get('currency', '')}")
            print(f"Авиакомпания (IATA): {flight.get('airline', 'N/A')}")
            print(f"Номер рейса: {flight.get('flight_number', 'N/A')}")
            print(f"Дата и время вылета: {flight.get('departure_at', 'N/A')}")
            print(f"Дата и время возвращения: {flight.get('return_at', 'N/A')}")
            print(f"Количество пересадок (туда): {flight.get('transfers', 'N/A')}")
            print(f"Количество пересадок (обратно): {flight.get('return_transfers', 'N/A')}")
            print(f"Общая длительность перелёта (мин): {flight.get('duration', 'N/A')}")
            print(f"Длительность перелёта туда (мин): {flight.get('duration_to', 'N/A')}")
            print(f"Длительность перелёта обратно (мин): {flight.get('duration_back', 'N/A')}")
            # Формируем полную ссылку для перехода на страницу поиска
            flight_link = flight.get("link", "")
            full_link = base_url + flight_link if flight_link else "N/A"
            print(f"Ссылка на билет: {full_link}")
            print()  # пустая строка для разделения
    else:
        print("По заданным параметрам билеты не найдены.")

def main():
    # Определяем путь к файлу config.yaml, если он находится в папке config относительно текущего файла
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #config_file = os.path.join(script_dir, "..", "config", "config.yaml")

    # Задаем параметры запроса.
    # Пример для получения самых дешёвых билетов (аналог /v1/prices/cheap)
    params = {
        "origin": "cek",  # IATA-код города или аэропорта отправления
        "destination": "kzn",  # IATA-код города или аэропорта назначения
        "departure_at": "2025-05-02",  # Месяц или полная дата вылета (YYYY-MM или YYYY-MM-DD)
        "direct": "false",  # Разрешаем рейсы с пересадками
        "sorting": "price",  # Сортировка по цене
        "currency": "rub",  # Валюта
        "limit": 30,  # Количество записей в ответе
        "page": 1,  # Номер страницы для пагинации
        "one_way": "true"  # Флаг для получения билета в одну сторону
    }

    # Выполняем запрос к API
    result = fetch_prices(params)

    # Выводим сырой ответ в формате JSON
    if result:
        print("Сырой ответ API:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\nДетализированный форматированный вывод:\n")
        print_detailed_flights(result)
    else:
        print("Не удалось получить данные от API.")

if __name__ == "__main__":
    main()