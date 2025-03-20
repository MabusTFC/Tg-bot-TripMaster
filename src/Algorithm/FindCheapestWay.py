from itertools import product
from .MyParser import fetch_prices  # Импортируем функцию fetch_prices
from .ParseTrain import fetch_train_prices
from src.Algorithm.BDCache.fetch_cached_tickets import fetch_cached_ticket
import datetime
# Словарь для преобразования названий городов в IATA-коды

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

            # Старый код:
            #response_avia = fetch_prices(origin, destination, current_date)
            #response_train = fetch_train_prices(origin, destination, current_date)

            # Новый код:
            #response_avia = fetch_cached_ticket(origin, destination, current_date, "avia")
            response_train = fetch_cached_ticket(origin, destination, current_date, "train")

            # Преобразуем данные в список билетов
            all_tickets = []
            #if response_avia and "data" in response_avia:
                #all_tickets.extend(response_avia["data"])
            if response_train:
                all_tickets.extend(response_train)

            if not all_tickets:
                print(f"Нет билетов из {origin} в {destination} на {current_date.strftime('%Y-%m-%d')}")
                break  # Этот маршрут невозможен

            # Выбираем самый дешевый билет
            best_ticket = min(
                all_tickets,
                key=lambda t: float(t.get("price", float("inf")))
                if isinstance(t.get("price"), (int, float, str)) and t.get("price") != "Не указана"
                else float("inf")
            )

            # Обновляем маршрутную информацию
            departure_time = best_ticket.get("departure_at")
            duration = best_ticket.get("duration", 0)  # Длительность полета в часах

            # Вычисляем время прибытия
            if departure_time:
                try:
                    departure_datetime = datetime.datetime.fromisoformat(departure_time.replace("Z", "+00:00"))
                    arrival_datetime = departure_datetime + datetime.timedelta(minutes=duration)
                except ValueError:
                    print(f"Некорректный формат времени отправления: {departure_time}")
                    continue
            else:
                print(f"Отсутствует время отправления для рейса из {origin} в {destination}")
                break

            base_url = "https://www.aviasales.ru"
            flight_link = best_ticket.get("link", "")
            full_link = base_url + flight_link if flight_link else "N/A"

            segment_info = {
                "origin": origin,
                "destination": destination,
                "departure_datetime": best_ticket.get("departure_at"),
                "arrival_datetime": best_ticket.get("arrival_at"),
                "flight_number": best_ticket.get("flight_number", ""),  # Номер рейса (авиа)
                "train_number": best_ticket.get("train_number", ""),  # Номер поезда
                "price": float(best_ticket.get("price", 0)) if best_ticket.get("price") and best_ticket.get(
                    "price") != "Не указана" else 0,
                "duration_hours": best_ticket.get("duration", 0) / 60,  # Длительность перелета/поездки в часах
                "booking_link": best_ticket.get("booking_link", "N/A"),  # Полная ссылка на бронирование билета
                "transport_type": "avia" if "flight_number" in best_ticket else "train"  # Тип транспорта
            }
            route_info["full_path"].append(segment_info)
            route_info["full_path"].append(segment_info)

            route_info["total_price"] += segment_info["price"]
            route_info["total_duration"] += duration/60  # Добавляем длительность полета в общую продолжительность

            # Обновляем дату отправления для следующего сегмента
            current_date = arrival_datetime.date()  # Устанавливаем дату прибытия
            if stay_duration > 0:
                current_date += datetime.timedelta(days=stay_duration)  # Добавляем время пребывания в городе

            # Если это первый сегмент, сохраняем дату начала маршрута
            if route_info["start_date"] is None:
                route_info["start_date"] = departure_time

            # Обновляем дату окончания маршрута
            route_info["end_date"] = arrival_datetime.isoformat()

        else:
            # Если прошли весь маршрут, добавляем его в список
            all_routes.append(route_info)

    return all_routes

