from Algorithm.FindCheapestWay import get_routes
import datetime
import json

# Исходные данные
cites = ["Москва", "Владивосток"]
start_city = cites[0],0
end_city = cites[1],0
departure_date = datetime.date(2025, 3, 25)

segments = [
    [("Челябинск", 5), ("Санкт-Петербург", 3)],
    [("Казань", 4), ("Екатеринбург", 2)],
    [("Сочи",3), ("Новосибирск", 2)]
]

# Вызов функции
routes = get_routes(start_city, end_city, departure_date, segments)

def save_routes_to_json(routes, file_path):
    # Преобразуем маршруты в JSON
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(routes, file, ensure_ascii=False, indent=4)

# Пример использования
save_routes_to_json(routes, './src/Map/routes.json')
# Вывод найденных маршрутов
print(json.dumps(routes, indent=4, ensure_ascii=False))
