#import json
from datetime import datetime, timedelta

from datetime import datetime

def getTicket_Avi(origin, destination, departure_date):
    """
    Возвращает список билетов на самолет из origin в destination на заданную дату.
    """
    tickets = TICKETS_DATA["avi"]
    filtered_tickets = [
        ticket for ticket in tickets
        if ticket["origin"] == origin
        and ticket["destination"] == destination
        and datetime.fromisoformat(ticket["departure"]).date() == departure_date  # Убран вызов .date()
    ]
    return filtered_tickets


def getTicket_Train(origin, destination, departure_date):
    """
    Возвращает список билетов на поезд из origin в destination на заданную дату.
    """
    tickets = TICKETS_DATA["train"]
    filtered_tickets = [
        ticket for ticket in tickets
        if ticket["origin"] == origin
        and ticket["destination"] == destination
        and datetime.fromisoformat(ticket["departure"]).date() == departure_date  # Убран вызов .date()
    ]
    return filtered_tickets




TICKETS_DATA = {
    "avi": [
        # Москва -> Челябинск
        {"origin": "Москва", "destination": "Челябинск", "departure": "2025-04-26T10:00:00", "arrival": "2025-04-26T13:00:00", "flight_number": "AV101", "price": 4000, "duration": 3.0},
        {"origin": "Москва", "destination": "Челябинск", "departure": "2025-04-26T15:00:00", "arrival": "2025-04-26T18:00:00", "flight_number": "AV102", "price": 4200, "duration": 3.0},

        # Москва -> Санкт-Петербург
        {"origin": "Москва", "destination": "Санкт-Петербург", "departure": "2025-04-26T11:00:00", "arrival": "2025-04-26T12:30:00", "flight_number": "AV201", "price": 2500, "duration": 1.5},
        {"origin": "Москва", "destination": "Санкт-Петербург", "departure": "2025-04-26T16:00:00", "arrival": "2025-04-26T17:30:00", "flight_number": "AV202", "price": 2700, "duration": 1.5},

        # Челябинск -> Казань
        {"origin": "Челябинск", "destination": "Казань", "departure": "2025-05-02T09:00:00", "arrival": "2025-05-02T11:00:00", "flight_number": "AV301", "price": 3000, "duration": 2.0},
        {"origin": "Челябинск", "destination": "Казань", "departure": "2025-05-02T14:00:00", "arrival": "2025-05-02T16:00:00", "flight_number": "AV302", "price": 3200, "duration": 2.0},

        # Челябинск -> Екатеринбург
        {"origin": "Челябинск", "destination": "Екатеринбург", "departure": "2025-05-02T10:00:00", "arrival": "2025-05-02T12:00:00", "flight_number": "AV351", "price": 2800, "duration": 2.0},
        {"origin": "Челябинск", "destination": "Екатеринбург", "departure": "2025-05-02T15:00:00", "arrival": "2025-05-02T17:00:00", "flight_number": "AV352", "price": 3000, "duration": 2.0},

        # Санкт-Петербург -> Казань
        {"origin": "Санкт-Петербург", "destination": "Казань", "departure": "2025-04-30T10:00:00", "arrival": "2025-04-30T14:00:00", "flight_number": "AV451", "price": 3300, "duration": 4.0},
        {"origin": "Санкт-Петербург", "destination": "Казань", "departure": "2025-04-30T16:00:00", "arrival": "2025-04-30T20:00:00", "flight_number": "AV452", "price": 3500, "duration": 4.0},

        # Санкт-Петербург -> Екатеринбург
        {"origin": "Санкт-Петербург", "destination": "Екатеринбург", "departure": "2025-04-30T10:00:00", "arrival": "2025-04-30T14:00:00", "flight_number": "AV401", "price": 3500, "duration": 4.0},
        {"origin": "Санкт-Петербург", "destination": "Екатеринбург", "departure": "2025-04-30T16:00:00", "arrival": "2025-04-30T20:00:00", "flight_number": "AV402", "price": 3700, "duration": 4.0},

        # Екатеринбург -> Сочи
        {"origin": "Екатеринбург", "destination": "Сочи", "departure": "2025-05-03T08:00:00", "arrival": "2025-05-03T12:00:00", "flight_number": "AV551", "price": 3800, "duration": 4.0},
        {"origin": "Екатеринбург", "destination": "Сочи", "departure": "2025-05-03T14:00:00", "arrival": "2025-05-03T18:00:00", "flight_number": "AV552", "price": 4000, "duration": 4.0},
        {"origin": "Екатеринбург", "destination": "Сочи", "departure": "2025-05-05T08:00:00", "arrival": "2025-05-05T12:00:00", "flight_number": "AV551", "price": 3800, "duration": 4.0},
        {"origin": "Екатеринбург", "destination": "Сочи", "departure": "2025-05-05T14:00:00", "arrival": "2025-05-05T18:00:00", "flight_number": "AV552", "price": 4000, "duration": 4.0},


        # Екатеринбург -> Новосибирск
        {"origin": "Екатеринбург", "destination": "Новосибирск", "departure": "2025-05-05T12:00:00", "arrival": "2025-05-05T16:00:00", "flight_number": "AV601", "price": 3300, "duration": 4.0},
        {"origin": "Екатеринбург", "destination": "Новосибирск", "departure": "2025-05-05T18:00:00", "arrival": "2025-05-05T22:00:00", "flight_number": "AV602", "price": 3500, "duration": 4.0},
        {"origin": "Екатеринбург", "destination": "Новосибирск", "departure": "2025-05-03T12:00:00", "arrival": "2025-05-03T16:00:00", "flight_number": "AV601", "price": 3300, "duration": 4.0},
        {"origin": "Екатеринбург", "destination": "Новосибирск", "departure": "2025-05-03T18:00:00", "arrival": "2025-05-03T22:00:00", "flight_number": "AV602", "price": 3500, "duration": 4.0},

        # Казань -> Сочи
        {"origin": "Казань", "destination": "Сочи", "departure": "2025-05-04T08:00:00", "arrival": "2025-05-04T11:00:00", "flight_number": "AV501", "price": 2800, "duration": 3.0},
        {"origin": "Казань", "destination": "Сочи", "departure": "2025-05-04T13:00:00", "arrival": "2025-05-04T16:00:00", "flight_number": "AV502", "price": 3000, "duration": 3.0},
        {"origin": "Казань", "destination": "Сочи", "departure": "2025-05-07T08:00:00", "arrival": "2025-05-07T11:00:00", "flight_number": "AV501", "price": 2800, "duration": 3.0},
        {"origin": "Казань", "destination": "Сочи", "departure": "2025-05-07T13:00:00", "arrival": "2025-05-07T16:00:00", "flight_number": "AV502", "price": 3000, "duration": 3.0},


        {"origin": "Казань", "destination": "Новосибирск", "departure": "2025-05-07T10:00:00", "arrival": "2025-05-07T16:00:00", "flight_number": "AV511", "price": 3500, "duration": 6.0},
        {"origin": "Казань", "destination": "Новосибирск", "departure": "2025-05-07T18:00:00", "arrival": "2025-05-08T00:00:00", "flight_number": "AV512", "price": 3700, "duration": 6.0},
        {"origin": "Казань", "destination": "Новосибирск", "departure": "2025-05-07T10:00:00", "arrival": "2025-05-05T16:00:00", "flight_number": "AV511", "price": 3500, "duration": 6.0},
        {"origin": "Казань", "destination": "Новосибирск", "departure": "2025-05-07T18:00:00", "arrival": "2025-05-05T00:00:00", "flight_number": "AV512", "price": 3700, "duration": 6.0},

        # Сочи -> Владивосток
        {"origin": "Сочи", "destination": "Владивосток", "departure": "2025-05-09T06:00:00", "arrival": "2025-05-09T18:00:00", "flight_number": "AV701", "price": 6000, "duration": 12.0},
        {"origin": "Сочи", "destination": "Владивосток", "departure": "2025-05-09T10:00:00", "arrival": "2025-05-09T22:00:00", "flight_number": "AV702", "price": 6200, "duration": 12.0},
        {"origin": "Сочи", "destination": "Владивосток", "departure": "2025-05-07T06:00:00", "arrival": "2025-05-07T18:00:00", "flight_number": "AV701", "price": 6000, "duration": 12.0},
        {"origin": "Сочи", "destination": "Владивосток", "departure": "2025-05-07T10:00:00", "arrival": "2025-05-07T22:00:00", "flight_number": "AV702", "price": 6200, "duration": 12.0},

        # Новосибирск -> Владивосток
        {"origin": "Новосибирск", "destination": "Владивосток", "departure": "2025-05-06T07:00:00", "arrival": "2025-05-06T15:00:00", "flight_number": "AV801", "price": 4500, "duration": 8.0},
        {"origin": "Новосибирск", "destination": "Владивосток", "departure": "2025-05-06T12:00:00", "arrival": "2025-05-06T20:00:00", "flight_number": "AV802", "price": 4700, "duration": 8.0},
    ],
    "train": [
        # Москва -> Челябинск
        {"origin": "Москва", "destination": "Челябинск", "departure": "2025-04-26T18:00:00", "arrival": "2025-04-27T12:00:00", "train_number": "TR101", "price": 2000, "duration": 18.0},
        {"origin": "Москва", "destination": "Челябинск", "departure": "2025-04-26T22:00:00", "arrival": "2025-04-27T16:00:00", "train_number": "TR102", "price": 2200, "duration": 18.0},

        # Москва -> Санкт-Петербург
        {"origin": "Москва", "destination": "Санкт-Петербург", "departure": "2025-04-26T20:00:00", "arrival": "2025-04-27T08:00:00", "train_number": "TR201", "price": 1500, "duration": 12.0},
        {"origin": "Москва", "destination": "Санкт-Петербург", "departure": "2025-04-26T23:00:00", "arrival": "2025-04-27T11:00:00", "train_number": "TR202", "price": 1700, "duration": 12.0},

        # Челябинск -> Казань
        {"origin": "Челябинск", "destination": "Казань", "departure": "2025-05-02T18:00:00", "arrival": "2025-05-03T06:00:00", "train_number": "TR301", "price": 1800, "duration": 12.0},
        {"origin": "Челябинск", "destination": "Казань", "departure": "2025-05-02T22:00:00", "arrival": "2025-05-03T10:00:00", "train_number": "TR302", "price": 2000, "duration": 12.0},

        # Челябинск -> Екатеринбург
        {"origin": "Челябинск", "destination": "Екатеринбург", "departure": "2025-05-02T18:00:00", "arrival": "2025-05-03T06:00:00", "train_number": "TR351", "price": 1800, "duration": 12.0},
        {"origin": "Челябинск", "destination": "Екатеринбург", "departure": "2025-05-02T22:00:00", "arrival": "2025-05-03T10:00:00", "train_number": "TR352", "price": 2000, "duration": 12.0},

        # Санкт-Петербург -> Казань
        {"origin": "Санкт-Петербург", "destination": "Казань", "departure": "2025-04-30T18:00:00", "arrival": "2025-05-01T06:00:00", "train_number": "TR451", "price": 2200, "duration": 12.0},
        {"origin": "Санкт-Петербург", "destination": "Казань", "departure": "2025-04-30T22:00:00", "arrival": "2025-05-01T10:00:00", "train_number": "TR452", "price": 2400, "duration": 12.0},

        # Санкт-Петербург -> Екатеринбург
        {"origin": "Санкт-Петербург", "destination": "Екатеринбург", "departure": "2025-04-30T20:00:00", "arrival": "2025-05-01T12:00:00", "train_number": "TR401", "price": 2200, "duration": 16.0},
        {"origin": "Санкт-Петербург", "destination": "Екатеринбург", "departure": "2025-04-30T23:00:00", "arrival": "2025-05-01T15:00:00", "train_number": "TR402", "price": 2400, "duration": 16.0},

        # Екатеринбург -> Сочи
        {"origin": "Екатеринбург", "destination": "Сочи", "departure": "2025-05-03T18:00:00", "arrival": "2025-05-04T12:00:00", "train_number": "TR551", "price": 2500, "duration": 18.0},
        {"origin": "Екатеринбург", "destination": "Сочи", "departure": "2025-05-03T22:00:00", "arrival": "2025-05-04T16:00:00", "train_number": "TR552", "price": 2700, "duration": 18.0},

        # Екатеринбург -> Новосибирск
        {"origin": "Екатеринбург", "destination": "Новосибирск", "departure": "2025-05-03T18:00:00", "arrival": "2025-05-04T12:00:00", "train_number": "TR601", "price": 2800, "duration": 18.0},
        {"origin": "Екатеринбург", "destination": "Новосибирск", "departure": "2025-05-03T22:00:00", "arrival": "2025-05-04T16:00:00", "train_number": "TR602", "price": 3000, "duration": 18.0},

        # Казань -> Сочи
        {"origin": "Казань", "destination": "Сочи", "departure": "2025-05-04T20:00:00", "arrival": "2025-05-05T12:00:00", "train_number": "TR501", "price": 2500, "duration": 16.0},
        {"origin": "Казань", "destination": "Сочи", "departure": "2025-05-04T23:00:00", "arrival": "2025-05-05T15:00:00", "train_number": "TR502", "price": 2700, "duration": 16.0},
        {"origin": "Казань", "destination": "Сочи", "departure": "2025-05-07T20:00:00", "arrival": "2025-05-08T12:00:00", "train_number": "TR503", "price": 2500, "duration": 16.0},
        {"origin": "Казань", "destination": "Сочи", "departure": "2025-05-07T23:00:00", "arrival": "2025-05-08T15:00:00", "train_number": "TR504", "price": 2700, "duration": 16.0},

        # Сочи -> Владивосток
        {"origin": "Сочи", "destination": "Владивосток", "departure": "2025-05-09T18:00:00", "arrival": "2025-05-11T06:00:00", "train_number": "TR701", "price": 5000, "duration": 36.0},
        {"origin": "Сочи", "destination": "Владивосток", "departure": "2025-05-09T22:00:00", "arrival": "2025-05-11T10:00:00", "train_number": "TR702", "price": 5200, "duration": 36.0},

        # Новосибирск -> Владивосток
        {"origin": "Новосибирск", "destination": "Владивосток", "departure": "2025-05-06T18:00:00", "arrival": "2025-05-07T12:00:00", "train_number": "TR801", "price": 4000, "duration": 18.0},
        {"origin": "Новосибирск", "destination": "Владивосток", "departure": "2025-05-06T22:00:00", "arrival": "2025-05-07T16:00:00", "train_number": "TR802", "price": 4200, "duration": 18.0},
    ]
}