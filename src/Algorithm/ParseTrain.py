import os
import sys
import yaml
import os
import sys
import yaml
import requests
from .config import API_KEY_TRN, city_name_to_code_train
from datetime import datetime
import json

def fetch_train_prices(origin, destination, departure_date):
    """
    Выполняет запрос к API Яндекс Расписания и возвращает данные о билетах на поезда.
    """
    origin_code = city_name_to_code_train.get(origin)
    destination_code = city_name_to_code_train.get(destination)

    if not origin_code or not destination_code:
        print(f"Не найден код для города: {origin} или {destination}")
        return {"data": [], "currency": "rub"}

    endpoint = "https://api.rasp.yandex.net/v3.0/search/"
    params = {
        "apikey": API_KEY_TRN,
        "format": "json",
        "from": origin_code,
        "to": destination_code,
        "date": departure_date.strftime("%Y-%m-%d"),
        "transport_types": "train",
        "et_marker": 'true',
        "limit": 10
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        trains = []
        for segment in data.get("segments", []):
            price_info = segment.get("price", {})
            train = {
                "origin": origin_code,
                "destination": destination_code,
                "departure_station": segment.get("from", {}).get("title", "N/A"),
                "arrival_station": segment.get("to", {}).get("title", "N/A"),
                "price": price_info.get("total") if price_info else None,
                "carrier": segment.get("thread", {}).get("carrier", {}).get("title", "N/A"),
                "train_number": segment.get("thread", {}).get("number", "N/A"),
                "departure_time": segment.get("departure", "N/A"),
                "arrival_time": segment.get("arrival", "N/A"),
                "transfers": 0,
                "duration": segment.get("duration", "N/A"),
                "link": f"https://rasp.yandex.ru/train/{segment.get('thread', {}).get('uid', 'N/A')}"
            }
            trains.append(train)

        return {"data": trains, "currency": "rub"}

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return {"data": [], "currency": "rub"}

def print_detailed_trains(result, base_url="https://rasp.yandex.ru"):
    """
    Выводит максимально подробный форматированный вывод данных о поездах.
    Для каждого найденного билета выводятся все поля, которые возвращает API.
    """
    if result and result.get("data"):
        print("Найденные билеты на поезда:")
        for index, train in enumerate(result["data"], start=1):
            print("=" * 50)
            print(f"Билет #{index}")
            print("=" * 50)
            print(f"Пункт отправления (код): {train.get('origin', 'N/A')}")
            print(f"Пункт назначения (код): {train.get('destination', 'N/A')}")
            print(f"Станция отправления: {train.get('departure_station', 'N/A')}")
            print(f"Станция прибытия: {train.get('arrival_station', 'N/A')}")
            print(f"Цена билета: {train.get('price', 'N/A')} {result.get('currency', '')}")
            print(f"Перевозчик: {train.get('carrier', 'N/A')}")
            print(f"Номер поезда: {train.get('train_number', 'N/A')}")
            print(f"Время отправления: {train.get('departure_time', 'N/A')}")
            print(f"Время прибытия: {train.get('arrival_time', 'N/A')}")
            print(f"Количество пересадок: {train.get('transfers', 'N/A')}")
            print(f"Длительность поездки (мин): {train.get('duration', 'N/A')}")
            print(f"Ссылка на билет: {train.get('link', 'N/A')}")
            print()
    else:
        print("По заданным параметрам билеты на поезда не найдены.")

if __name__ == "__main__":
    origin = "Москва"
    destination = "Санкт-Петербург"
    departure_date = datetime(2025, 3, 25)

    result = fetch_train_prices(origin, destination, departure_date)
    if result.get("data"):
        print("Сырой ответ API:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\nДетализированный форматированный вывод:\n")
        print_detailed_trains(result)
    else:
        print("Билеты на поезда не найдены.")