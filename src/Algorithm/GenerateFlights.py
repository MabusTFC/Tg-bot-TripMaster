from datetime import datetime, timedelta
import random

# Список городов
cities = ["Москва", "Санкт-Петербург", "Казань", "Екатеринбург", "Сочи", "Новосибирск"]

# Фиксированные аэропорты для каждого города
airports = {
    "Москва": "SVO",
    "Санкт-Петербург": "LED",
    "Казань": "KZN",
    "Екатеринбург": "SVX",
    "Сочи": "AER",
    "Новосибирск": "OVB"
}


# Генерация всех возможных рейсов
def generate_flights(start_date, end_date):
    """
    Генерирует фиктивные данные о перелетах между всеми парами городов на каждый день.

    :param start_date: Начальная дата (строка в формате 'YYYY-MM-DD').
    :param end_date: Конечная дата (строка в формате 'YYYY-MM-DD').
    :return: Словарь с информацией о рейсах.
    """
    flights = {}
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    while current_date <= end_date_obj:
        date_str = current_date.strftime('%Y-%m-%d')

        for i, departure_city in enumerate(cities):
            for j, arrival_city in enumerate(cities):
                if departure_city != arrival_city:  # Исключаем рейсы из города в себя
                    departure_airport = airports[departure_city]
                    arrival_airport = airports[arrival_city]

                    # Фиксированное время отправления и прибытия
                    departure_time = "10:00"
                    arrival_time = "12:00"

                    # Случайная цена
                    price = random.randint(3000, 10000)

                    # Формируем ключ и значение для словаря
                    key = (departure_city, arrival_city, date_str)
                    flights[key] = (
                        f"{date_str} {departure_time}",
                        f"{date_str} {arrival_time}",
                        departure_airport,
                        arrival_airport,
                        price
                    )

        # Переходим к следующему дню
        current_date += timedelta(days=1)

    return flights