
import requests
from src.avi.config import *
from datetime import datetime

def getTicket_Train(origin_city_name, destination_city_name, departure_date):
    origin_city_code = None
    destination_city_code = None
    for code, name in city_code_to_name_train.items():
        if name.lower() == origin_city_name.lower():
            origin_city_code = code
        if name.lower() == destination_city_name.lower():
            destination_city_code = code

    if not origin_city_code:
        return f"Не найден код города для: {origin_city_name}"
    if not destination_city_code:
        return f"Не найден код города для: {destination_city_name}"

    params_train['from'] = origin_city_code
    params_train['to'] = destination_city_code
    params_train['date'] = departure_date

    response = requests.get(BASE_URL_TRAIN, params=params_train)

    if response.status_code == 200:
        schedule = response.json()

        if 'segments' not in schedule or not schedule['segments']:
            return f"Нет доступных поездов из {origin_city_name.capitalize()} в {destination_city_name.capitalize()} на дату {departure_date}."

        tickets = []
        for segment in schedule['segments']:
            if 'tickets_info' in segment and segment['tickets_info']['places']:
                price = segment['tickets_info']['places'][0]['price']
            else:
                price = 'Не указана'

            departure_datetime = datetime.fromisoformat(segment["departure"])
            arrival_datetime = datetime.fromisoformat(segment["arrival"])

            ticket_info = {
                "type": "train",
                "title": segment["thread"]["title"],  # Название поезда
                "departure_date": departure_datetime.strftime("%Y-%m-%d"),  # Дата отправления
                "departure_time": departure_datetime.strftime("%H:%M:%S"),  # Время отправления
                "arrival_date": arrival_datetime.strftime("%Y-%m-%d"),  # Дата прибытия
                "arrival_time": arrival_datetime.strftime("%H:%M:%S"),  # Время прибытия
                "duration": segment["duration"],  # Продолжительность поездки
                "price": price  # Цена билета
            }

            tickets.append(ticket_info)

        if tickets:
            return tickets[0]
        else:
            return "Нет доступных билетов."

    else:
        return f"Ошибка при запросе данных: {response.status_code}"