from Algorithm.FindCheapestWay import get_cheapest_route

# Пример использования
travel_plan = [
    ("Москва", 0),          # Город отправления
    ("Санкт-Петербург", 3), # Промежуточный город
    ("Казань", 4),
    ("Сочи", 1),# Промежуточный город
    ("Екатеринбург", 0)     # Город прибытия
]

start_date = "2023-11-01"

try:
    cheapest_route, min_cost = get_cheapest_route(travel_plan, start_date)
    print("Самый дешевый маршрут:")
    for step in cheapest_route:
        print(step)
    print("Общая стоимость:", min_cost)
except ValueError as e:
    print("Ошибка при поиске маршрута:", e)