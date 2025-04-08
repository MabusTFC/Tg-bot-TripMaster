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
from database.database_manager import *
class AuthStates(StatesGroup):
    waiting_for_auth_code_save = State()
    waiting_for_auth_code_add = State()


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


@router.callback_query(lambda c: c.data == "save_key")
async def save_auth_code_handler(callback_query: CallbackQuery, state: FSMContext):
    try:
        user_id = callback_query.from_user.id
        username = callback_query.from_user.username

        await callback_query.message.answer(
            "Пожалуйста, введите код авторизации, который вы получили после авторизации через Google:"
        )
        await state.set_state(AuthStates.waiting_for_auth_code_save)
        await state.update_data(user_id=user_id, username=username)

    except Exception as e:
        logger.error(f"Error in save_auth_code_handler: {str(e)}")
        await callback_query.message.answer("Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.")
    finally:
        await callback_query.answer()


@router.message(AuthStates.waiting_for_auth_code_save)
async def process_save_auth_code(message: Message, state: FSMContext):
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            auth_code = message.text.strip()
            data = await state.get_data()
            user_id = data.get('user_id')
            username = data.get('username')

            if not auth_code:
                await message.answer("Код авторизации не может быть пустым. Пожалуйста, попробуйте еще раз.")
                return

            await update_auth_code(user_id, auth_code)
            await message.answer("Код авторизации успешно сохранен!")
            await state.clear()
            return

        except asyncpg.exceptions.ConnectionDoesNotExistError:
            retry_count += 1
            if retry_count < max_retries:
                await asyncio.sleep(1)  # Подождать перед повторной попыткой
                continue
            logger.error("Failed to save auth code after retries: connection issue")
            await message.answer("Не удалось сохранить код из-за проблем с соединением. Пожалуйста, попробуйте позже.")

        except Exception as e:
            logger.error(f"Error in process_save_auth_code: {str(e)}")
            await message.answer(f"Произошла ошибка при сохранении кода: {str(e)}")

        finally:
            if 'state' in locals():
                await state.clear()


@router.callback_query(lambda c: c.data == "add_event")
async def add_event_to_calendar(callback_query: CallbackQuery, state: FSMContext):
    try:
        user_id = callback_query.from_user.id
        auth_code = await get_auth_code(user_id)

        if not auth_code:
            await callback_query.message.answer(
                "У вас нет сохраненного кода авторизации. Пожалуйста, сначала сохраните его через кнопку авторизации."
            )
            return

        await callback_query.message.answer(
            "Используем сохраненный код авторизации. Создаем события в календаре..."
        )

        # Получаем маршруты из состояния или файла
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

        # Авторизация и создание сервиса
        flow = Flow.from_client_secrets_file(
            'Google/config_g/credentials.json',
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        flow.fetch_token(code=auth_code)
        creds = flow.credentials

        service = build('calendar', 'v3', credentials=creds)
        events_added = 0

        # Проверяем наличие календаря TripMaster
        calendar_list = service.calendarList().list().execute()
        trip_master_calendar = None

        for calendar in calendar_list.get('items', []):
            if calendar['summary'] == 'TripMaster':
                trip_master_calendar = calendar
                break

        # Создаем календарь если его нет
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

        # Добавляем события для каждого маршрута
        for route in routes:
            for path in route['full_path']:
                start_time = datetime.fromisoformat(path['departure_datetime'])
                end_time = datetime.fromisoformat(path['arrival_datetime'])

                if start_time >= end_time:
                    await callback_query.message.answer(
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

                try:
                    service.events().insert(calendarId=trip_master_calendar_id, body=event).execute()
                    events_added += 1
                except Exception as e:
                    await callback_query.message.answer(
                        f"Ошибка при добавлении события {path['origin']} -> {path['destination']}: {str(e)}"
                    )

        # Формируем ссылку на календарь
        calendar_link = f"https://calendar.google.com/calendar/u/0/r?cid={trip_master_calendar_id}"

        # Создаем кнопку с ссылкой
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Открыть Google Календарь", url=calendar_link)]
        ])

        # Отправляем сообщение с кнопкой
        await callback_query.message.answer(
            f'Успешно добавлено {events_added} событий в календарь TripMaster',
            reply_markup=keyboard
        )

    except Exception as e:
        await callback_query.message.answer(f'Ошибка при добавлении событий в календарь: {str(e)}')
    finally:
        await state.clear()