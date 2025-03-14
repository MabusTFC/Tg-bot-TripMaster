from itertools import permutations
from datetime import datetime, timedelta
from .GenerateFlights import generate_flights


# Заглушка для getTicket
def getTicket(departure_city, arrival_city, departure_date):
    """
    Симулирует получение информации о самом дешевом перелете.

    :param departure_city: Город отправления.
    :param arrival_city: Город прибытия.
    :param departure_date: Дата отправления (строка в формате 'YYYY-MM-DD').
    :return: Кортеж из 5 элементов: (дата и время отправления, дата и время прибытия,
                                     аэропорт отправления, аэропорт прибытия, цена).
    """
    # Фиктивные данные о перелетах
    flights = generate_flights("2023-11-01", "2023-11-15")

    # Проверяем, есть ли перелет между указанными городами
    key = (departure_city, arrival_city, departure_date)
    if key in flights:
        return flights[key]
    else:
        # Если рейса нет, возвращаем None
        return None


def get_cheapest_route(travel_plan, start_date):
    """
    Находит самый дешевый маршрут для посещения всех городов из списка.

    :param travel_plan: Список кортежей (название города, количество дней).
    :param start_date: Дата начала путешествия (строка в формате 'YYYY-MM-DD').
    :return: Самый дешевый маршрут (список словарей с деталями) и его общая стоимость.
    """

    def calculate_route_cost(route, current_date):
        """
        Вычисляет стоимость маршрута и формирует детальный маршрут.

        :param route: Список городов в порядке посещения.
        :param current_date: Текущая дата начала маршрута.
        :return: Общая стоимость маршрута и детальный маршрут.
        """
        total_cost = 0
        detailed_route = []

        for i in range(len(route) - 1):
            departure_city = route[i]
            arrival_city = route[i + 1]

            # Получаем информацию о самом дешевом перелете
            ticket_info = getTicket(departure_city, arrival_city, current_date)
            if not ticket_info:
                raise ValueError(f"Нет доступных билетов из {departure_city} в {arrival_city} на {current_date}")

            departure_datetime, arrival_datetime, departure_airport, arrival_airport, price = ticket_info

            # Обновляем общую стоимость
            total_cost += price

            # Формируем информацию о текущем перелете
            flight_details = {
                "departure_city": departure_city,
                "arrival_city": arrival_city,
                "departure_datetime": departure_datetime,
                "arrival_datetime": arrival_datetime,
                "departure_airport": departure_airport,
                "arrival_airport": arrival_airport,
                "price": price
            }
            detailed_route.append(flight_details)

            # Обновляем дату: добавляем время пребывания в текущем городе
            days_to_stay = next((days for city, days in travel_plan if city == arrival_city), 0)
            stay_details = {
                "city": arrival_city,
                "stay_duration": days_to_stay,
                "departure_date_after_stay": (datetime.strptime(arrival_datetime.split()[0], '%Y-%m-%d') + timedelta(
                    days=days_to_stay)).strftime('%Y-%m-%d')
            }
            detailed_route.append(stay_details)

            # Обновляем текущую дату для следующего перелета
            current_date = stay_details["departure_date_after_stay"]

        return total_cost, detailed_route

    # Разделяем города на начальный, конечный и промежуточные
    cities = [city for city, _ in travel_plan]
    start_city = cities[0]  # Город отправления
    end_city = cities[-1]  # Город прибытия
    intermediate_cities = cities[1:-1]  # Промежуточные города

    # Генерируем все возможные перестановки промежуточных городов
    all_permutations = permutations(intermediate_cities)

    # Инициализируем переменные для хранения самого дешевого маршрута
    cheapest_route = None
    min_cost = float('inf')

    # Перебираем все возможные маршруты
    for perm in all_permutations:
        route = [start_city] + list(perm) + [end_city]
        cost, detailed_route = calculate_route_cost(route, start_date)

        # Проверяем, является ли текущий маршрут самым дешевым
        if cost < min_cost:
            min_cost = cost
            cheapest_route = detailed_route

    return cheapest_route, min_cost