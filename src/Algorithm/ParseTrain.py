import os

from src.Algorithm.config import API_KEY_TRN
from datetime import datetime

import json

import requests
from datetime import datetime


def fetch_train_prices(origin, destination, current_date):
    """
    Выполняет запрос к API Яндекс.Расписаний для получения данных о железнодорожных рейсах.
    """
    # URL API Яндекс.Расписаний
    endpoint = "https://api.rasp.yandex.net/v3.0/search/"
    # Получаем путь к директории, где находится текущий файл
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Формируем путь к файлу city_to_yandex_code.json
    file_path = os.path.join(script_dir, "city_to_yandex_code.json")

    # Открываем файл
    with open(file_path, "r", encoding="utf-8") as file:
        city_to_yandex_code = json.load(file)

    origin_code = city_to_yandex_code.get(origin)
    destination_code = city_to_yandex_code.get(destination)
    # Параметры запроса
    params = {
        "apikey": API_KEY_TRN,  # Ваш API-ключ от Яндекс.Расписаний
        "format": "json",
        "from": city_to_yandex_code.get(origin),  # Код станции отправления (например, Yandex код)
        "to": city_to_yandex_code.get(destination),  # Код станции назначения
        "lang": "ru_RU",
        "date": current_date.strftime("%Y-%m-%d"),  # Дата отправления
        "transport_types": "train",  # Тип транспорта: поезд
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Проверка на успешный статус запроса
        data = response.json()

        # Преобразуем данные в удобный формат
        trains = []
        for segment in data.get("segments", []):
            train_info = {
                "origin": segment["from"]["title"],
                "destination": segment["to"]["title"],
                "departure_at": segment["departure"],
                "arrival_at": segment["arrival"],
                "train_number": segment["thread"]["number"],
                "price": float(segment.get("price", {}).get("whole", 0)),  # Цена в рублях
                "duration": segment["duration"]/60,  # Длительность в минутах
                "booking_link": segment.get("tickets_info", {}).get("buy_ticket_url", "N/A")  # Ссылка на покупку
            }
            trains.append(train_info)

        return trains
    except requests.RequestException as e:
        print("Ошибка при выполнении запроса к API Яндекс.Расписаний:", e)
        return None

def print_detailed_trains(result, base_url="https://rasp.yandex.ru"):
    """
    Выводит максимально подробный форматированный вывод данных о поездах.
    Для каждого найденного билета выводятся все поля, которые возвращает API.
    """
    if result:
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
    if result:
        print("Сырой ответ API:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("\nДетализированный форматированный вывод:\n")
        print_detailed_trains(result)
    else:
        print("Билеты на поезда не найдены.")