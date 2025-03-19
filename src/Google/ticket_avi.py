import re
import requests
from src.avi.config import *

def fetch_airports_data():
    """Получает данные об аэропортах."""
    response = requests.get(BASE_URL_AIRPORTS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Ошибка при запросе данных об аэропортах: {response.status_code}')

def get_city_code(city_name, city_code_mapping):
    """Возвращает код города по его названию."""
    for code, name in city_code_mapping.items():
        if name.lower() == city_name.lower():
            return code
    return None

def get_airports_for_city(city_code, city_code_to_airports):
    """Возвращает список аэропортов для города."""
    return city_code_to_airports.get(city_code, [])

def format_ticket_info(ticket, origin_city_name, destination_city_name, airport_dict):
    """Форматирует информацию о билете."""
    origin_code = ticket['origin']
    destination_code = ticket['destination']
    departure_date = ticket['depart_date']
    price = ticket['value']
    departure_time = ticket['depart_date'][11:]
    arrival_time = ticket['found_at'][11:]

    origin_airport = airport_dict.get(origin_code, {'name': origin_code})
    destination_airport = airport_dict.get(destination_code, {'name': destination_code})

    return {
        "origin_city": origin_city_name.capitalize(),
        "origin_airport": origin_airport['name'],
        "destination_city": destination_city_name.capitalize(),
        "destination_airport": destination_airport['name'],
        "departure_date": departure_date,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "price": price
    }

def getTicket_Avi(origin_city_name, destination_city_name, departure_date):
    """Основная функция для поиска билетов."""
    try:
        airports = fetch_airports_data()
        airport_dict = {airport['code']: airport for airport in airports}

        city_code_to_airports = {}
        for airport in airports:
            city_code = airport['city_code'].lower()
            if city_code not in city_code_to_airports:
                city_code_to_airports[city_code] = []
            city_code_to_airports[city_code].append(airport['code'])

        origin_city_code = get_city_code(origin_city_name, city_code_to_name_avi)
        destination_city_code = get_city_code(destination_city_name, city_code_to_name_avi)

        if not origin_city_code:
            return f"Не найден код города для: {origin_city_name}"
        if not destination_city_code:
            return f"Не найден код города для: {destination_city_name}"

        origin_airports = get_airports_for_city(origin_city_code, city_code_to_airports)
        destination_airports = get_airports_for_city(destination_city_code, city_code_to_airports)

        if not origin_airports:
            return f"Не найдено аэропортов для города: {origin_city_name}"
        if not destination_airports:
            return f"Не найдено аэропортов для города: {destination_city_name}"

        params_avi['origin'] = origin_city_code
        params_avi['destination'] = destination_city_code
        params_avi['departure_at'] = departure_date
        response = requests.get(BASE_URL, params=params_avi)

        if response.status_code == 200:
            data = response.json()

            filtered_tickets = [ticket for ticket in data['data'] if ticket['depart_date'] == departure_date]

            if not filtered_tickets:
                return f"Нет доступных билетов из {origin_city_name.capitalize()} в {destination_city_name.capitalize()} на дату {departure_date}."

            cheapest_ticket = min(filtered_tickets, key=lambda x: x['value'])
            tickets_dist = format_ticket_info(cheapest_ticket, origin_city_name, destination_city_name, airport_dict)
            return tickets_dist

        else:
            return f'Ошибка при запросе данных: {response.status_code}'
    except Exception as e:
        return f'Произошла ошибка: {str(e)}'