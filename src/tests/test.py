import unittest
from unittest.mock import patch
from src.Algorithm.FindCheapestWay import get_routes
import datetime

class TestFindCheapestWay(unittest.TestCase):
    def setUp(self):
        # Исходные данные для тестов
        self.cities = ["Москва", "Владивосток"]
        self.start_city = (self.cities[0], 0)
        self.end_city = (self.cities[1], 0)
        self.departure_date = datetime.date(2025, 5, 29)

        # Моковые данные для авиа и ж/д билетов
        self.mock_avia_tickets = [
            {
                "price": 5000,
                "departure_at": "2025-05-29T10:00:00Z",
                "duration": 180,
                "flight_number": "AV123",
                "link": "/tickets/avia/123"
            }
        ]
        self.mock_train_tickets = [
            {
                "price": 3000,
                "departure_at": "2025-05-29T08:00:00Z",
                "duration": 360,
                "train_number": "TR789",
                "link": "/tickets/train/789"
            }
        ]

    @patch("src.Algorithm.FindCheapestWay.fetch_cached_ticket")
    def test_single_segment_route(self, mock_fetch_cached_ticket):
        """Тест на маршрут с одним сегментом."""
        segments = [[("Челябинск", 2)]]

        # Настройка мока для fetch_cached_ticket
        def side_effect(origin, destination, departure_date, transport_type):
            if transport_type == "avia":
                return {"data": self.mock_avia_tickets}
            elif transport_type == "train":
                return self.mock_train_tickets
            return None

        mock_fetch_cached_ticket.side_effect = side_effect

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

    @patch("src.Algorithm.FindCheapestWay.fetch_cached_ticket")
    def test_multiple_segments(self, mock_fetch_cached_ticket):
        """Тест на маршрут с несколькими сегментами."""
        segments = [
            [("Челябинск", 2)],
            [("Казань", 1), ("Екатеринбург", 3)],
            [("Сочи", 4)]
        ]

        # Настройка мока для fetch_cached_ticket
        def side_effect(origin, destination, departure_date, transport_type):
            if transport_type == "avia":
                return {"data": self.mock_avia_tickets}
            elif transport_type == "train":
                return self.mock_train_tickets
            return None

        mock_fetch_cached_ticket.side_effect = side_effect

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

    @patch("src.Algorithm.FindCheapestWay.fetch_cached_ticket")
    def test_high_cost_route(self, mock_fetch_cached_ticket):
        """Тест на маршрут с высокой стоимостью билетов."""
        high_cost_tickets = [
            {
                "price": 50000,
                "departure_at": "2025-05-29T10:00:00Z",
                "duration": 180,
                "flight_number": "AV123",
                "link": "/tickets/avia/123"
            }
        ]
        segments = [[("Челябинск", 2)]]

        # Настройка мока для fetch_cached_ticket
        def side_effect(origin, destination, departure_date, transport_type):
            if transport_type == "avia":
                return {"data": high_cost_tickets}
            elif transport_type == "train":
                return self.mock_train_tickets
            return None

        mock_fetch_cached_ticket.side_effect = side_effect

        routes = get_routes(self.start_city, self.end_city, self.departure_date, segments)

        # Проверяем, что результат не пустой
        self.assertIsNotNone(routes)
        self.assertIsInstance(routes, list)
        self.assertGreater(len(routes), 0)

        # Проверяем, что стоимость маршрута соответствует ожидаемой
        first_route = routes[0]
        self.assertEqual(first_route["total_price"], 50000)

    @patch("src.Algorithm.FindCheapestWay.fetch_cached_ticket")
    def test_long_duration_route(self, mock_fetch_cached_ticket):
        """Тест на маршрут с длительным временем в пути."""
        long_duration_tickets = [
            {
                "price": 5000,
                "departure_at": "2025-05-29T10:00:00Z",
                "duration": 1440,  # 24 часа
                "flight_number": "AV123",
                "link": "/tickets/avia/123"
            }
        ]
        segments = [[("Челябинск", 2)]]

        # Настройка мока для fetch_cached_ticket
        def side_effect(origin, destination, departure_date, transport_type):
            if transport_type == "avia":
                return {"data": long_duration_tickets}
            elif transport_type == "train":
                return self.mock_train_tickets
            return None

        mock_fetch_cached_ticket.side_effect = side_effect

        routes = get_routes(self.start_city, self.end_city, self.departure_date, segments)

        # Проверяем, что результат не пустой
        self.assertIsNotNone(routes)
        self.assertIsInstance(routes, list)
        self.assertGreater(len(routes), 0)

        # Проверяем, что время в пути соответствует ожидаемому
        first_route = routes[0]
        self.assertEqual(first_route["total_duration"], 24)  # 1440 минут = 24 часа

    @patch("src.Algorithm.FindCheapestWay.fetch_cached_ticket")
    def test_multiple_routes(self, mock_fetch_cached_ticket):
        """Тест на случай, когда доступно несколько маршрутов."""
        segments = [
            [("Челябинск", 2), ("Санкт-Петербург", 1)],
            [("Казань", 1), ("Екатеринбург", 3)]
        ]

        # Настройка мока для fetch_cached_ticket
        def side_effect(origin, destination, departure_date, transport_type):
            if transport_type == "avia":
                return {"data": self.mock_avia_tickets}
            elif transport_type == "train":
                return self.mock_train_tickets
            return None

        mock_fetch_cached_ticket.side_effect = side_effect

        routes = get_routes(self.start_city, self.end_city, self.departure_date, segments)

        # Проверяем, что найдено несколько маршрутов
        self.assertGreater(len(routes), 1)

        # Проверяем формат каждого маршрута
        for route in routes:
            self.assertIn("route", route)
            self.assertIn("total_price", route)
            self.assertIn("total_duration", route)

    @patch("src.Algorithm.FindCheapestWay.fetch_cached_ticket")
    def test_no_stay_duration(self, mock_fetch_cached_ticket):
        """Тест на маршрут без времени пребывания в городах."""
        segments = [
            [("Челябинск", 0)],  # Время пребывания = 0
            [("Казань", 0)]
        ]

        # Настройка мока для fetch_cached_ticket
        def side_effect(origin, destination, departure_date, transport_type):
            if transport_type == "avia":
                return {"data": self.mock_avia_tickets}
            elif transport_type == "train":
                return self.mock_train_tickets
            return None

        mock_fetch_cached_ticket.side_effect = side_effect

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