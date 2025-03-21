import json
import datetime
import os

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, WebAppInfo
from aiogram.types import InputFile, InputMediaDocument,BufferedInputFile
from telegram import InlineKeyboardButton
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

from Google.config_g.config_google import *
from Algorithm.FindCheapestWay import get_routes

from handlers.utils.keyboards import get_google_calendar_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "authorization")
async def authorization_google(callback_query: CallbackQuery, state: FSMContext):
    try:
        with open('Google/config_g/credentials.json', 'r') as file:
            client_config = json.load(file)
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        await callback_query.message.reply(f'Пожалуйста, авторизуйтесь через Google: {auth_url}')

        @router.message()
        async def handle_auth_code(message: types.Message):
            try:
                auth_code = message.text.strip()
                flow.fetch_token(code=auth_code)
                creds = flow.credentials

                # Сохранение учетных данных в базу

                await message.reply('Авторизация прошла успешно!')
            except Exception as e:
                await message.reply(f'Ошибка авторизации: {e}')
    except Exception as e:
        await callback_query.message.reply(f'Ошибка при создании потока авторизации: {e}')


@router.callback_query(lambda c: c.data == "add_event")
async def add_event_to_calendar(callback_query: CallbackQuery, state: FSMContext):
    try:
        #Получить данные пользователя и его путь.
        creds = None
        routes = []
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
        await callback_query.message.reply(f'Все события добавлены в календарь')
    except Exception as e:
        await callback_query.message.reply(f'Ошибка!')



@router.callback_query(lambda c: c.data == "print_calendar")
async def export_calendar_to_pdf(callback_query: types.CallbackQuery, state: FSMContext):
    # Пример данных о событиях
    events = [
        {"date": "2023-10-15", "event": "Поездка в Париж"},
        {"date": "2023-11-01", "event": "Экскурсия по Риму"},
        {"date": "2023-12-10", "event": "Отдых на Бали"},
    ]

    # Создаем PDF
    pdf_filename = "travel_calendar.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()

    # Регистрируем шрифт с поддержкой кириллицы
    # Убедитесь, что файл шрифта DejaVuSerif.ttf находится в вашей директории
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))

    # Устанавливаем шрифт для стилей
    styles['Title'].fontName = 'DejaVuSerif'
    styles['Normal'].fontName = 'DejaVuSerif'

    elements = []

    # Заголовок календаря
    title = Paragraph("Календарь событий путешествий", styles['Title'])
    elements.append(title)

    # Создаем таблицу с событиями
    data = [["Дата", "Событие"]]
    for event in events:
        date = datetime.strptime(event["date"], "%Y-%m-%d").strftime("%d.%m.%Y")
        data.append([date, event["event"]])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),  # Шрифт для всей таблицы
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Генерируем PDF
    doc.build(elements)

    # Читаем содержимое файла в байты
    with open(pdf_filename, "rb") as file:
        pdf_data = file.read()

    # Создаем объект BufferedInputFile
    input_file = BufferedInputFile(pdf_data, filename=pdf_filename)

    # Отправляем PDF пользователю
    await callback_query.bot.send_document(chat_id=callback_query.from_user.id, document=input_file)

    # Удаляем временный файл
    os.remove(pdf_filename)