import requests
from .config import *
from googletrans import Translator


# Метод по извлечению билетов с авиаселса с учетом городов и даты.
# Вовзращает структуру вида:
# {1:[ПАРАМЕТРЫ БИЛЕТА],
# 2:[ПАРАМЕТРЫ БИЛЕТА],
# 3:[ПАРАМЕТРЫ БИЛЕТА]}
def getTicket(origin_city_name, destination_city_name, departure_date):
    response_air = requests.get(BASE_URL_AIRPORTS)
    print(city_code_to_name)
    if response_air.status_code == 200:
        airports = response_air.json()

        airport_dict = {airport['code']: airport for airport in airports}

        city_code_to_airports = {}
        for airport in airports:
            city_code = airport['city_code'].lower()
            if city_code not in city_code_to_airports:
                city_code_to_airports[city_code] = []
            city_code_to_airports[city_code].append(airport['code'])

        origin_city_code = None
        destination_city_code = None
        for code, name in city_code_to_name.items():
            if name.lower() == origin_city_name.lower():
                origin_city_code = code
            if name.lower() == destination_city_name.lower():
                destination_city_code = code

        if not origin_city_code:
            return f"Не найден код города для: {origin_city_name}"
        if not destination_city_code:
            return f"Не найден код города для: {destination_city_name}"

        origin_airports = city_code_to_airports.get(origin_city_code, [])
        destination_airports = city_code_to_airports.get(destination_city_code, [])

        if not origin_airports:
            return f"Не найдено аэропортов для города: {origin_city_name}"
        if not destination_airports:
            return f"Не найдено аэропортов для города: {destination_city_name}"

        params['origin'] = origin_city_code
        params['destination'] = destination_city_code

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            filtered_tickets = []
            for ticket in data['data']:
                # Фильтруем билеты по указанной дате
                if ticket['depart_date'] == departure_date:
                    filtered_tickets.append(ticket)
                    # Ограничиваем количество билетов до 10
                    if len(filtered_tickets) >= 1:
                        break

            tickets_list = []
            if filtered_tickets:
                for ticket in filtered_tickets:
                    origin_code = ticket['origin']
                    destination_code = ticket['destination']
                    departure_date = ticket['depart_date']
                    price = ticket['value']

                    origin_airport = airport_dict.get(origin_code, {'name': origin_code})
                    destination_airport = airport_dict.get(destination_code, {'name': destination_code})

                    ticket_info = [
                        f"Из города: {origin_city_name.capitalize()} (Аэропорт: {origin_airport['name']})",
                        f"В город: {destination_city_name.capitalize()} (Аэропорт: {destination_airport['name']})",
                        f"Дата вылета: {departure_date}",
                        f"Цена: {price} руб."
                    ]
                    tickets_list.append(ticket_info)

                return tickets_list
            else:
                return f"Нет доступных билетов из {origin_city_name.capitalize()} в {destination_city_name.capitalize()} на дату {departure_date}."
        else:
            return f'Ошибка при запросе данных: {response.status_code}'
    else:
        return f'Ошибка при запросе данных об аэропортах: {response_air.status_code}'