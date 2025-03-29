import json
import datetime
import os

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import uuid
from src.Google.config_g.config_google import *
from pathlib import Path
router = Router()

class AuthStates(StatesGroup):
    waiting_for_auth_code = State()

@router.callback_query(lambda c: c.data == "authorization")
async def authorization_google(callback_query: CallbackQuery, state: FSMContext):
    try:
        session_id = str(uuid.uuid4())
        await state.update_data(chat_id=callback_query.message.chat.id, session_id=session_id)

        flow = Flow.from_client_secrets_file(
            'Google/config_g/credentials.json',
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )

        state_param = f"{callback_query.message.chat.id}:{session_id}"
        auth_url = flow.authorization_url(
            prompt='consent',
            state=state_param,
            access_type='offline',
            include_granted_scopes='true'
        )[0]

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Авторизоваться через Google", url=auth_url)]
        ])

        await callback_query.message.answer(
            "Пожалуйста, авторизуйтесь через Google:",
            reply_markup=keyboard
        )

    except Exception as e:
        await callback_query.message.answer(f'Ошибка при создании ссылки авторизации: {str(e)}')


@router.callback_query(lambda c: c.data == "add_event")
async def request_auth_code(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        "Пожалуйста, введите код авторизации, который вы получили после авторизации через Google:"
    )
    await state.set_state(AuthStates.waiting_for_auth_code)
    await callback_query.answer()


@router.message(AuthStates.waiting_for_auth_code)
async def process_auth_code(message: Message, state: FSMContext):
    try:
        auth_code = message.text.strip()
        await state.update_data(auth_code=auth_code)

        data = await state.get_data()
        routes = data.get('routes', [])
        current_file = Path(__file__).absolute()

        routes_path = (
                current_file.parent
                .parent
                .parent
                .parent
                / 'docs'
                / 'routes.json'
        )

        if not routes:
            with open(routes_path, 'r', encoding='utf-8') as f:
                routes = json.load(f)

        flow = Flow.from_client_secrets_file(
            'Google/config_g/credentials.json',
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        flow.fetch_token(code=auth_code)
        creds = flow.credentials

        # Create calendar service
        service = build('calendar', 'v3', credentials=creds)
        events_added = 0

        calendar_list = service.calendarList().list().execute()
        trip_master_calendar = None

        for calendar in calendar_list.get('items', []):
            if calendar['summary'] == 'TripMaster':
                trip_master_calendar = calendar
                break

        if not trip_master_calendar:
            new_calendar = {
                'summary': 'TripMaster',
                'description': 'Календарь для событий о путешествиях',
                'timeZone': 'UTC'
            }
            created_calendar = service.calendars().insert(body=new_calendar).execute()
            trip_master_calendar_id = created_calendar['id']
        else:
            trip_master_calendar_id = trip_master_calendar['id']

        for route in routes:
            for path in route['full_path']:
                start_time = datetime.fromisoformat(path['departure_datetime'])
                end_time = datetime.fromisoformat(path['arrival_datetime'])

                if start_time >= end_time:
                    await message.answer(
                        f"Ошибка: Дата начала события {path['origin']} -> {path['destination']} "
                        "должна быть раньше даты окончания."
                    )
                    continue

                event = {
                    'summary': f"Путешествие: {path['origin']} -> {path['destination']}",
                    'description': f"Транспорт: {'Поезд' if path['train_number'] else 'Самолет'} "
                                   f"{path['train_number'] or path['flight_number']}\n"
                                   f"Цена: {path['price']} руб.",
                    'start': {
                        'dateTime': path['departure_datetime'],
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'dateTime': path['arrival_datetime'],
                        'timeZone': 'UTC',
                    },
                }

                # Insert event into TripMaster calendar
                service.events().insert(calendarId=trip_master_calendar_id, body=event).execute()
                events_added += 1

        await message.answer(f'Успешно добавлено {events_added} событий в календарь TripMaster')
        await state.clear()

    except Exception as e:
        await message.answer(f'Ошибка при добавлении событий в календарь: {str(e)}')
        await state.clear()

@router.callback_query(lambda c: c.data == "print_calendar")
async def export_calendar_to_pdf(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    routes = data.get('routes', [])
    current_file = Path(__file__).absolute()

    routes_path = (
            current_file.parent
            .parent
            .parent
            .parent
            / 'docs'
            / 'routes.json'
    )
    if not routes:
        with open(routes_path, 'r', encoding='utf-8') as f:
            routes = json.load(f)

    pdf_filename = "travel_routes.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()

    try:
        pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
        styles['Title'].fontName = 'DejaVuSerif'
        styles['Normal'].fontName = 'DejaVuSerif'
        styles['Heading2'].fontName = 'DejaVuSerif'
    except:
        pass

    elements = []

    title = Paragraph("Маршруты путешествий", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    for i, route in enumerate(routes, 1):
        route_title = Paragraph(f"Маршрут #{i}", styles['Heading2'])
        elements.append(route_title)

        cities = " → ".join(route['route'])
        elements.append(Paragraph(f"Города: {cities}", styles['Normal']))

        price = f"{route['total_price']:,.2f}".replace(',', ' ') + " руб."
        duration = f"{route['total_duration']:.1f} часов"
        elements.append(Paragraph(f"Общая стоимость: {price}", styles['Normal']))
        elements.append(Paragraph(f"Общая продолжительность: {duration}", styles['Normal']))
        elements.append(Spacer(1, 12))

        segments_data = [
            ["Отправление", "Прибытие", "Откуда", "Куда", "Тип", "Цена", "Длительность"]
        ]

        for segment in route['full_path']:
            # Format datetimes
            dep_datetime = datetime.fromisoformat(segment['departure_datetime'].replace(' ', 'T'))
            arr_datetime = datetime.fromisoformat(segment['arrival_datetime'].replace(' ', 'T'))

            dep_str = dep_datetime.strftime("%d.%m %H:%M")
            arr_str = arr_datetime.strftime("%d.%m %H:%M")

            transport_type = "Авиа" if segment['transport_type'] == "avia" else "Поезд"
            price = f"{segment['price']:,.2f}".replace(',', ' ') + " руб."
            duration = f"{segment['duration_hours']:.1f} ч."

            segments_data.append([
                dep_str,
                arr_str,
                segment['origin'],
                segment['destination'],
                transport_type,
                price,
                duration
            ])

        table = Table(segments_data, colWidths=[70, 70, 90, 90, 60, 70, 60])  # Увеличил ширину столбцов
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSerif'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 24))

    doc.build(elements)

    with open(pdf_filename, 'rb') as file:
        pdf_data = file.read()

        input_file = types.BufferedInputFile(
            file=pdf_data,
            filename=pdf_filename
        )

        await callback_query.bot.send_document(
            chat_id=callback_query.from_user.id,
            document=input_file,
            caption="Ваши маршруты путешествий"
        )

    os.remove(pdf_filename)