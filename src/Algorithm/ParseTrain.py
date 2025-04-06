import os

from src.Algorithm.config import API_KEY_TRN
from datetime import datetime

import json

import requests
from datetime import datetime


def calculate_distance(segment, average_speed_km_per_hour):
    """
    Расчет расстояния по времени и средней скорости.

    :param segment: Сегмент поезда с информацией о времени.
    :param average_speed_km_per_hour: Средняя скорость поезда в км/ч.
    :return: Расстояние в километрах.
    """
    duration_in_seconds = segment.get("duration", 0)
    duration_in_hours = duration_in_seconds / 3600
    distance_km = duration_in_hours * average_speed_km_per_hour
    return distance_km

def fetch_train_prices(origin, destination, current_date):
    """
    Выполняет запрос к API Яндекс.Расписаний и вычисляет примерную цену билета,
    учитывая расстояние из API.
    """
    endpoint = "https://api.rasp.yandex.net/v3.0/search/"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "city_to_yandex_code.json")

    with open(file_path, "r", encoding="utf-8") as file:
        city_to_yandex_code = json.load(file)

    origin_code = city_to_yandex_code.get(origin)
    destination_code = city_to_yandex_code.get(destination)

    params = {
        "apikey": API_KEY_TRN,
        "format": "json",
        "from": origin_code,
        "to": destination_code,
        "lang": "ru_RU",
        "date": current_date.strftime("%Y-%m-%d"),
        "transport_types": "train",
        "limit": 10,
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        trains = []
        for segment in data.get("segments", []):
            average_speed = 80  # км/ч
            distance_km = calculate_distance(segment, average_speed)

            if "tickets_info" in segment and segment["tickets_info"].get("places"):
                price = segment["tickets_info"]["places"][0].get("price", {}).get("whole", 0)
            else:
                base_price_per_km = 1.8


                train_type = segment["thread"]["transport_type"]
                if train_type == "express":
                    train_coeff = 1.6
                else:
                    train_coeff = 1.0

                # Коэффициент типа вагона
                carriage_type = segment.get("thread", {}).get("carrier", {}).get("title", "")
                if "купе" in carriage_type.lower():
                    carriage_coeff = 1.8
                elif "плацкарт" in carriage_type.lower():
                    carriage_coeff = 1.2
                elif "СВ" in carriage_type.lower() or "люкс" in carriage_type.lower():
                    carriage_coeff = 2.5
                else:
                    carriage_coeff = 1.0

                days_until_departure = (current_date - datetime.now()).days
                if days_until_departure < 3:
                    dynamic_coeff = 1.5
                elif days_until_departure < 7:
                    dynamic_coeff = 1.3
                elif days_until_departure < 14:
                    dynamic_coeff = 1.1
                else:
                    dynamic_coeff = 1.0

                price = distance_km * base_price_per_km * train_coeff * carriage_coeff * dynamic_coeff
                price = round(price, -2)

            departure_datetime = datetime.fromisoformat(segment["departure"].replace("Z", "+00:00"))
            arrival_datetime = datetime.fromisoformat(segment["arrival"].replace("Z", "+00:00"))

            train_info = {
                "origin": segment["from"]["title"],
                "destination": segment["to"]["title"],
                "departure_at": segment["departure"],
                "arrival_at": segment["arrival"],
                "train_number": segment["thread"]["number"],
                "price": int(price),
                "duration": round(segment["duration"] / 3600, 1),  # Часы с округлением
                "distance_km": int(distance_km),
                "carrier": segment["thread"]["carrier"]["title"],
                "carriage_type": segment.get("thread", {}).get("carrier", {}).get("title", "N/A"),
                "link": f"https://rasp.yandex.ru/train/{segment['thread']['uid']}",
            }
            trains.append(train_info)

        return trains
    except requests.RequestException as e:
        print("Ошибка при выполнении запроса к API Яндекс.Расписаний:", e)
        return None
def print_detailed_trains(trains, currency="RUB"):
    """
    Выводит максимально подробный форматированный вывод данных о поездах.
    """
    if trains:
        print("Найденные билеты на поезда:")
        for index, train in enumerate(trains, start=1):
            print("=" * 50)
            print(f"Билет #{index}")
            print("=" * 50)
            print(f"Пункт отправления: {train.get('origin', 'N/A')}")
            print(f"Пункт назначения: {train.get('destination', 'N/A')}")
            print(f"Цена билета: {train.get('price', 'N/A')} {currency}")
            print(f"Перевозчик: {train.get('carrier', 'N/A')}")
            print(f"Номер поезда: {train.get('train_number', 'N/A')}")
            print(f"Время отправления: {train.get('departure_at', 'N/A')}")
            print(f"Время прибытия: {train.get('arrival_at', 'N/A')}")
            print(f"Длительность поездки (часы): {train.get('duration', 'N/A')}")
            #print(f"Ссылка на билет: {train.get('link', 'N/A')}")
            print()
    else:
        print("По заданным параметрам билеты на поезда не найдены.")

if __name__ == "__main__":
    origin = "Москва"
    destination = "Санкт-Петербург"
    departure_date = datetime(2025, 7, 29)

    result = fetch_train_prices(origin, destination, departure_date)
    if result:
        print("Сырой ответ API:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\nДетализированный форматированный вывод:\n")
        print_detailed_trains(result)
    else:
        print("Билеты на поезда не найдены.")