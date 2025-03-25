from itertools import product
from src.Algorithm.BDCache.fetch_cached_tickets import fetch_cached_ticket  # Предполагается, что это ваше кэширование
import datetime
from concurrent.futures import ThreadPoolExecutor

def process_segment(route_info, origin, destination, current_date, stay_duration):
    """Обработка одного сегмента маршрута."""
    # Получаем билеты из кэша или базы данных
    response_avia = fetch_cached_ticket(origin, destination, current_date, "avia")
    response_train = fetch_cached_ticket(origin, destination, current_date, "train")

    all_tickets = []
    if response_avia and "data" in response_avia:
        all_tickets.extend(response_avia["data"])
    if response_train:
        all_tickets.extend(response_train)

    if not all_tickets:
        print(f"Нет билетов из {origin} в {destination} на {current_date.strftime('%Y-%m-%d')}")
        return None  # Этот маршрут невозможен

    # Выбираем самый дешевый билет
    best_ticket = min(
        all_tickets,
        key=lambda t: float("inf") if not t.get("price") or t.get("price") == "Не указана" else float(t["price"])
    )

    # Обрабатываем время отправления и прибытия
    departure_time = best_ticket.get("departure_at")
    duration = best_ticket.get("duration", 0)  # Длительность в минутах

    if not departure_time:
        print(f"Отсутствует время отправления для рейса из {origin} в {destination}")
        return None

    try:
        departure_datetime = datetime.datetime.fromisoformat(departure_time.replace("Z", "+00:00"))
        arrival_datetime = departure_datetime + datetime.timedelta(minutes=duration)
    except ValueError:
        print(f"Некорректный формат времени отправления: {departure_time}")
        return None

    # Формируем информацию о сегменте
    base_url = "https://www.aviasales.ru"
    flight_link = best_ticket.get("link", "")
    full_link = base_url + flight_link if flight_link else "N/A"

    segment_info = {
        "origin": origin,
        "destination": destination,
        "departure_datetime": departure_time,
        "arrival_datetime": arrival_datetime.isoformat(),
        "flight_number": best_ticket.get("flight_number", ""),
        "train_number": best_ticket.get("train_number", ""),
        "price": float(best_ticket.get("price", 0)) if best_ticket.get("price") and best_ticket["price"] != "Не указана" else 0,
        "duration_hours": duration / 60,
        "booking_link": full_link,
        "transport_type": "avia" if "flight_number" in best_ticket else "train"
    }

    # Обновляем маршрутную информацию
    route_info["full_path"].append(segment_info)
    route_info["total_price"] += segment_info["price"]
    route_info["total_duration"] += segment_info["duration_hours"]

    # Обновляем дату отправления для следующего сегмента
    current_date = arrival_datetime.date()
    if stay_duration > 0:
        current_date += datetime.timedelta(days=stay_duration)

    return current_date

def get_routes(start_city, end_city, departure_date, segments):
    all_routes = []

    for mid_cities in product(*segments):
        route = [start_city] + list(mid_cities) + [end_city]
        route_info = {
            "route": [city[0] for city in route],
            "total_price": 0,
            "total_duration": 0,
            "full_path": [],
            "start_date": None,
            "end_date": None
        }

        current_date = departure_date
        valid_route = True

        # Параллельная обработка сегментов
        with ThreadPoolExecutor() as executor:
            futures = []
            for i in range(len(route) - 1):
                origin, destination = route[i][0], route[i + 1][0]
                stay_duration = route[i + 1][1]
                futures.append(executor.submit(process_segment, route_info, origin, destination, current_date, stay_duration))

            for future in futures:
                result = future.result()
                if result is None:
                    valid_route = False
                    break
                current_date = result

        if valid_route:
            # Если маршрут успешен, сохраняем его
            all_routes.append(route_info)

    return all_routes