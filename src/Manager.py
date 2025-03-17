from Algorithm.FindCheapestWay import get_routes
import datetime
import json

# Исходные данные
cites = ["Москва", "Владивосток"]
start_city = cites[0],0
end_city = cites[1],0
departure_date = datetime.date(2025, 3, 20)

segments = [
    [("Челябинск", 5), ("Санкт-Петербург", 3)],
    [("Казань", 4), ("Екатеринбург", 2)],
    [("Сочи",3), ("Новосибирск", 2)]
]

# Вызов функции
routes = get_routes(start_city, end_city, departure_date, segments)

def save_routes_to_json(routes, filename):
    # Преобразуем маршруты в JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(routes, f, ensure_ascii=False, indent=4)

# Пример использования
save_routes_to_json(routes, 'Map/routes.json')
# Вывод найденных маршрутов
for i, route in enumerate(routes, 1):
    print(f"Маршрут {i}: {route['route']}")
    print(f"Общая цена: {route['total_price']} руб.")
    print(f"Общее расстояние: {route['total_distance']} км")
    print(f"Общее время в пути: {route['total_duration']} часов")
    print("Сегменты маршрута:")
    for segment in route["segments"]:
        print(f"  {segment['from']} -> {segment['to']} ({segment['transport']})")
        print(f"    Отправление: {segment['departure']}")
        print(f"    Прибытие: {segment['arrival']}")
        print(f"    Цена: {segment['price']} руб.")
        print(f"    Дистанция: {segment['distance']} км")
        print(f"    Время в пути: {segment['duration']} часов")
    print("-" * 40)
