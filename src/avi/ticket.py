import requests
from src.avi.config import *


# Метод по извлечению билетов с авиаселса с учетом городов и даты.
# Вовзращает структуру вида:
# {1:[ПАРАМЕТРЫ БИЛЕТА],
# 2:[ПАРАМЕТРЫ БИЛЕТА],
# 3:[ПАРАМЕТРЫ БИЛЕТА]}
def getTicket_Avi(origin_city_name, destination_city_name, departure_date):
    response_air = requests.get(BASE_URL_AIRPORTS)
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
        for code, name in city_code_to_name_avi.items():
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

        params_avi['origin'] = origin_city_code
        params_avi['destination'] = destination_city_code

        response = requests.get(BASE_URL, params=params_avi)

        if response.status_code == 200:
            data = response.json()

            filtered_tickets = []
            for ticket in data['data']:
                # Фильтруем билеты по указанной дате
                if ticket['depart_date'] == departure_date:
                    filtered_tickets.append(ticket)
                    # Ограничиваем количество билетов до 10
                    if len(filtered_tickets) >= 10:
                        break

            tickets_list = []
            count = 0
            if filtered_tickets:
                for ticket in filtered_tickets:
                    origin_code = ticket['origin']
                    destination_code = ticket['destination']
                    departure_date = ticket['depart_date']
                    price = ticket['value']
                    departure_time = ticket.get('departure_time', 'Не указано')  # Время вылета
                    arrival_time = ticket.get('arrival_time', 'Не указано')  # Время прилета

                    origin_airport = airport_dict.get(origin_code, {'name': origin_code})
                    destination_airport = airport_dict.get(destination_code, {'name': destination_code})
                    if count == 0:
                        ticket_info = {
                            "origin_city": origin_city_name.capitalize(),
                            "origin_airport": origin_airport['name'],
                            "destination_city": destination_city_name.capitalize(),
                            "destination_airport": destination_airport['name'],
                            "departure_date": departure_date,
                            "departure_time": departure_time,
                            "arrival_time": arrival_time,
                            "price": price  # Теперь цена — это число
                        }
                        tickets_list.append(ticket_info)
                        count += 1
                    else:
                        break

                return tickets_list
            else:
                return f"Нет доступных билетов из {origin_city_name.capitalize()} в {destination_city_name.capitalize()} на дату {departure_date}."
        else:
            return f'Ошибка при запросе данных: {response.status_code}'
    else:
        return f'Ошибка при запросе данных об аэропортах: {response_air.status_code}'

def getTicket_Train(origin_city_name, destination_city_name, departure_date):
    # Поиск кодов городов по названиям
    origin_city_code = None
    destination_city_code = None
    for code, name in city_code_to_name_train.items():
        if name.lower() == origin_city_name.lower():
            origin_city_code = code
        if name.lower() == destination_city_name.lower():
            destination_city_code = code

    # Проверка, найдены ли коды городов
    if not origin_city_code:
        return f"Не найден код города для: {origin_city_name}"
    if not destination_city_code:
        return f"Не найден код города для: {destination_city_name}"
    params_train['from'] = origin_city_code
    params_train['to'] = destination_city_code
    params_train['date'] = departure_date

    # Выполнение запроса
    response = requests.get(BASE_URL_TRAIN, params=params_train)
    #print(response.status_code)
    #print(response.text)
    # Обработка ответа
    if response.status_code == 200:
        schedule = response.json()

        # Проверка наличия данных
        if 'segments' not in schedule or not schedule['segments']:
            return f"Нет доступных поездов из {origin_city_name.capitalize()} в {destination_city_name.capitalize()} на дату {departure_date}."

        # Формирование списка билетов с ценами
        for segment in schedule['segments']:
            if 'tickets_info' in segment and segment['tickets_info']['places']:
                price = segment['tickets_info']['places'][0]['price']
            else:
                price = 'Не указана'  # Если цена не указана

            # Формируем информацию о билете в виде списка строк
            ticket_info = {
                "type": "train",
                "title": segment["thread"]["title"],  # Название поезда
                "departure": segment["departure"],  # Время отправления
                "arrival": segment["arrival"],  # Время прибытия
                "duration": segment["duration"],  # Продолжительность поездки
                "price": price  # Цена билета
            }

            return [ticket_info]  # Возвращаем первый найденный билет

        return ["Нет доступных билетов с указанной ценой."]
    else:
        return [f"Ошибка при запросе данных: {response.status_code}"]