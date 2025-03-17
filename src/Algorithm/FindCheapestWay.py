from itertools import product
from src.avi.ticket import getTicket_Avi, getTicket_Train
import datetime


def get_routes(start_city, end_city, departure_date, segments):
    all_routes = []

    # Генерация всех возможных маршрутов
    for mid_cities in product(*segments):
        route = [start_city] + list(mid_cities) + [end_city]
        route_info = {
            "route": [city[0] for city in route],  # Только названия городов
            "total_price": 0,
            "total_duration": 0,  # В часах
            "full_path": [],  # Полный путь с деталями
            "start_date": None,  # Дата начала маршрута
            "end_date": None  # Дата окончания маршрута
        }

        current_date = departure_date
        for i in range(len(route) - 1):
            origin, destination = route[i][0], route[i + 1][0]
            stay_duration = route[i + 1][1]  # Время пребывания в следующем городе

            # Получаем билеты
            avi_tickets = getTicket_Avi(origin, destination, current_date)
            train_tickets = getTicket_Train(origin, destination, current_date)

            all_tickets = []
            if isinstance(avi_tickets, list) and all(isinstance(t, dict) for t in avi_tickets):
                all_tickets.extend(avi_tickets)
            if isinstance(train_tickets, list) and all(isinstance(t, dict) for t in train_tickets):
                all_tickets.extend(train_tickets)

            if not all_tickets:
                print(f"Нет билетов из {origin} в {destination} на {current_date.strftime('%Y-%m-%d')}")
                break  # Этот маршрут невозможен

            # Выбираем самый дешевый билет (учитываем, что цена может отсутствовать)
            best_ticket = min(
                all_tickets,
                key=lambda t: float(t.get("price", float("inf")))
                if isinstance(t.get("price"), (int, float, str)) and t.get("price") != "Не указана"
                else float("inf")
            )

            # Обновляем маршрутную информацию
            segment_info = {
                "origin": origin,
                "destination": destination,
                "departure_datetime": best_ticket.get("departure"),
                "arrival_datetime": best_ticket.get("arrival"),
                "flight_number": best_ticket.get("flight_number", ""),  # Номер рейса
                "price": float(best_ticket.get("price", 0)) if best_ticket.get("price") and best_ticket.get("price") != "Не указана" else 0
            }
            route_info["full_path"].append(segment_info)

            route_info["total_price"] += segment_info["price"]

            # Обновляем дату отправления (добавляем время перелёта + пребывание в городе)
            arrival_time = best_ticket.get("arrival")
            if arrival_time:
                try:
                    arrival_date = datetime.datetime.fromisoformat(arrival_time)
                    if route_info["start_date"] is None:
                        route_info["start_date"] = best_ticket.get("departure")  # Сохраняем дату начала маршрута
                    route_info["end_date"] = arrival_time  # Обновляем дату окончания маршрута

                    # Добавляем время перелёта к общей продолжительности
                    duration = best_ticket.get("duration", 0)
                    route_info["total_duration"] += duration

                    # Обновляем текущую дату для следующего сегмента
                    current_date = arrival_date.date() + datetime.timedelta(days=stay_duration)
                except ValueError:
                    print(f"Некорректный формат времени прибытия: {arrival_time}")
                    continue
        else:
            # Если прошли весь маршрут, добавляем его в список
            all_routes.append(route_info)

    return all_routes