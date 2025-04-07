from Algorithm.FindCheapestWay import get_routes
import datetime
import json

# Исходные данные
cites = ["Москва", "Владивосток"]
start_city = cites[0],0
end_city = cites[1],0
departure_date = datetime.date(2025, 4, 29)

segments = [
    [("Челябинск", 5), ("Санкт-Петербург", 3), ("Самара", 2)],
    [("Казань", 4), ("Екатеринбург", 2), ("Пермь", 3)],
    [("Сочи",3), ("Красноярск", 2)],

]

# Вызов функции
routes = get_routes(start_city, end_city, departure_date, segments)

# Вывод найденных маршрутов
print(json.dumps(routes, indent=4, ensure_ascii=False))
