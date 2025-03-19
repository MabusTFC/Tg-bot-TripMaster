from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json
from datetime import datetime


def add_event_to_calendar(creds):
    try:
        # Загружаем данные из JSON
        with open('routes.json', 'r', encoding='utf-8') as f:
            routes = json.load(f)

        service = build('calendar', 'v3', credentials=creds)

        for route in routes:
            for path in route['full_path']:
                # Проверяем, что даты не перекрываются
                start_time = datetime.fromisoformat(path['departure_datetime'])
                end_time = datetime.fromisoformat(path['arrival_datetime'])

                if start_time >= end_time:
                    print(f"Ошибка: Дата начала события {path['origin']} -> {path['destination']} должна быть раньше даты окончания.")
                    continue

                event = {
                    'summary': f"Путешествие: {path['origin']} -> {path['destination']}",
                    'description': f"Транспорт: {'Поезд' if path['train_number'] else 'Самолет'} {path['train_number'] or path['flight_number']}\nЦена: {path['price']} руб.",
                    'start': {
                        'dateTime': path['departure_datetime'],
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'dateTime': path['arrival_datetime'],
                        'timeZone': 'UTC',
                    },
                }

                event = service.events().insert(calendarId='primary', body=event).execute()
                print(f"Событие создано: {event.get('htmlLink')}")

        print('Все события из маршрута добавлены в календарь!')
    except Exception as e:
        print(f'Ошибка при создании события: {e}')