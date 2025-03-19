import os
import sys
import yaml
import requests
from .config import API_KEY_TRN, city_name_to_code_train

def fetch_train_prices(origin, destination, departure_date):
    """
    Выполняет запрос к API Яндекс Расписания и возвращает данные о билетах на поезда (или другой транспорт).
    """
    origin_code = city_name_to_code_train.get(origin)
    destination_code = city_name_to_code_train.get(destination)

    if not origin_code or not destination_code:
        print(f"Не найден код для города: {origin} или {destination}")
        return []

    endpoint = "https://api.rasp.yandex.net/v3.0/search/?"
    params = {
        "apikey": API_KEY_TRN,
        "from": origin_code,  # Код станции отправления
        "to": destination_code,
        #"format": "json",# Код станции назначения
        "date": departure_date.strftime("%Y-%m-%d"),  # Дата отправления
        "transport_types": "train",  # Тип транспорта (по умолчанию "train")
        "show_to_affiliates": "true",
        #"system": "yandex"# Система кодирования (используем коды Яндекс Расписаний)

    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Проверяем HTTP-статус ответа
        schedule_data = response.json()

        # Проверяем наличие данных в ответе
        if "segments" not in schedule_data or not schedule_data["segments"]:
            print(f"Нет рейсов из {origin} в {destination} на {departure_date.strftime('%Y-%m-%d')}")
            return []

        # Преобразуем данные в формат, аналогичный fetch_prices
        tickets = []
        for segment in schedule_data.get("segments", []):
            thread = segment.get("thread", {})
            tickets_info = segment.get("tickets_info", {})
            places = tickets_info.get("places", [])

            for price_info in places:
                price_obj = price_info.get("price", {})
                if isinstance(price_obj, dict) and "whole" in price_obj:
                    whole = price_obj.get("whole", 0)
                    cents = price_obj.get("cents", 0)
                    price = float(f"{whole}.{cents:02d}")
                else:
                    price = float(price_info.get("price", 0))

                ticket = {
                    "origin": segment.get("from", {}).get("code", "N/A"),
                    "destination": segment.get("to", {}).get("code", "N/A"),
                    "departure_at": segment.get("departure", ""),
                    "arrival_at": segment.get("arrival", ""),
                    "duration": segment.get("duration", 0),  # В секундах
                    "price": price,
                    "currency": price_info.get("currency", "RUB"),
                    "train_number": thread.get("number", ""),
                    "carrier": thread.get("carrier", {}).get("title", "N/A"),
                    "vehicle": thread.get("vehicle", "N/A"),
                    "link": thread.get("thread_method_link", "")
                }
                tickets.append(ticket)

        return tickets

    except requests.RequestException as e:
        print("Ошибка при выполнении запроса к API Яндекс Расписания:", e)
        return []
if __name__ == "__main__":
    from datetime import datetime

    origin = "Москва"
    destination = "Санкт-Петербург"
    departure_date = datetime(2025, 3, 25)

    tickets = fetch_train_prices(origin, destination, departure_date)
    print("123")
    if tickets:
        for ticket in tickets:
            print(ticket)
    else:
        print("Билеты не найдены.")