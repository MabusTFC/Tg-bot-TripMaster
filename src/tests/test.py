import unittest
import time
from src.Algorithm.FindCheapestWay import get_routes
import datetime

class TestFindCheapestWay(unittest.TestCase):
    def setUp(self):
        # Исходные данные для тестов
        self.cities = ["Москва", "Владивосток"]
        self.start_city = (self.cities[0], 0)
        self.end_city = (self.cities[1], 0)
        self.departure_date = datetime.date(2025, 5, 29)
        self.segments = [
            [("Челябинск", 2)],
            [("Казань", 1), ("Екатеринбург", 3)],
            [("Сочи", 4)]
        ]

    def test_execution_time_small_segments(self):
        """Тест на время выполнения с малым количеством сегментов."""
        start_time = time.time()

        # Вызов функции
        routes = get_routes(self.start_city, self.end_city, self.departure_date, self.segments)

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Время выполнения (малое количество сегментов): {execution_time:.4f} секунд")

        # Проверяем, что результат не пустой
        self.assertIsNotNone(routes)
        self.assertIsInstance(routes, list)
        self.assertGreater(len(routes), 0)

        # Дополнительно проверяем, что время выполнения находится в разумных пределах
        self.assertLess(execution_time, 5.0)  # Например, менее 5 секунд

    def test_execution_time_large_segments(self):
        """Тест на время выполнения с большим количеством сегментов."""
        large_segments = [
            [("Сочи", 1), ("Санкт-Петербург", 1), ("Казань", 1)],
            [("Омск", 1), ("Пермь", 1), ("Краснодар", 1)],
            [("Челябинск", 1), ("Тверь", 1), ("Екатеринбург", 1)],
            [("Уфа", 1), ("Самара", 1), ("Саратов", 1)]
        ]

        start_time = time.time()

        # Вызов функции
        routes = get_routes(self.start_city, self.end_city, self.departure_date, large_segments)

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Время выполнения (большое количество сегментов): {execution_time:.4f} секунд")

        # Проверяем, что результат не пустой
        self.assertIsNotNone(routes)
        self.assertIsInstance(routes, list)
        self.assertGreater(len(routes), 0)

        # Дополнительно проверяем, что время выполнения находится в разумных пределах
        self.assertLess(execution_time, 1000)  # Например, менее 10 секунд

    def test_no_stay_duration(self):
        """Тест на маршрут без времени пребывания в городах."""
        segments = [
            [("Челябинск", 0)],  # Время пребывания = 0
            [("Казань", 0)]
        ]

        routes = get_routes(self.start_city, self.end_city, self.departure_date, segments)

        # Проверяем, что результат не пустой
        self.assertIsNotNone(routes)
        self.assertIsInstance(routes, list)
        self.assertGreater(len(routes), 0)

        # Проверяем формат первого маршрута
        first_route = routes[0]
        self.assertIn("route", first_route)
        self.assertIn("total_price", first_route)
        self.assertIn("total_duration", first_route)


if __name__ == "__main__":
    unittest.main()