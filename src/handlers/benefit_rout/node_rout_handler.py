from datetime import datetime
from pathlib import Path

import requests
import json
from aiogram import Router, types

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from urllib.parse import urlencode

from handlers.utils.state_machine import RoutStates
from handlers.utils.keyboards import get_zveno_rout_keyboard
from Algorithm.FindCheapestWay import get_routes
from config import MAP_URL, SERVER_URL

from database.database_manager import save_route_db

router = Router()


@router.callback_query(lambda c: c.data == "benefit_rout")
async def node_rout_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(RoutStates.ZVENO_ROUT)
    await callback_query.message.answer(text="Введите список городов через запятую:")


@router.message(RoutStates.ZVENO_ROUT)
async def node_input_cities(message: types.Message, state: FSMContext):

    user_data = await state.get_data()
    total_days = user_data.get("total_days", 30)
    max_days = user_data.get("max_days", total_days)

    temp_cities = [city.strip() for city in message.text.split(",") if city.strip()]

    await state.update_data(temp_cities=temp_cities, current_days_zveno=1)

    await message.answer(
        "Настройте количество дней:",
        reply_markup=await get_zveno_rout_keyboard(1, max_days)
    )


@router.callback_query(lambda c: c.data in ["pluse_days", "minus_days"])
async def change_days_count(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    max_days = user_data.get("max_days", user_data.get("total_days", 30))
    current_days = user_data.get("current_days_zveno", 1)

    action = callback_query.data

    if action == "pluse_days" and current_days < max_days:
        current_days += 1
        max_days -= 1
    elif action == "minus_days" and current_days > 1:
        current_days -= 1
        max_days += 1

    await state.update_data(current_days_zveno=current_days, max_days=max_days)

    new_markup = await get_zveno_rout_keyboard(current_days, max_days)

    print(f"DEBUG: Action: {action}, max_days: {max_days}, current_days_zveno: {current_days}")

    if str(callback_query.message.reply_markup) != str(new_markup):
        await callback_query.message.edit_reply_markup(reply_markup=new_markup)

    await callback_query.answer()


@router.callback_query(lambda c: c.data == "add_zveno")
async def add_node(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    temp_cities = user_data.get("temp_cities", [])
    days_count = user_data.get("current_days_zveno", 1)
    zveno_list = user_data.get("zveno_list", [])

    if temp_cities:
        new_zveno = {city: days_count for city in temp_cities}
        zveno_list.append(new_zveno)

        await state.update_data(zveno_list=zveno_list, temp_cities=[], current_days_zveno=1)

    await callback_query.message.answer("Введите список городов для нового звена:")
    await state.set_state(RoutStates.ZVENO_ROUT)


@router.callback_query(lambda c: c.data == "save_zveno")
async def save_node(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    route = user_data.get("route", [])
    start_date = user_data.get("start_date")
    temp_cities = user_data.get("temp_cities", [])
    days_count = user_data.get("current_days_zveno", 1)
    zveno_list = user_data.get("zveno_list", [])
    tg_id = callback_query.from_user.id

    if temp_cities:
        new_zveno = {city: days_count for city in temp_cities}
        zveno_list.append(new_zveno)


    await state.update_data(zveno_list=zveno_list, temp_cities=[], current_days_zveno=1)
    print(route, temp_cities, zveno_list,new_zveno)
    CITIES_PATH = Path("Algorithm/city_to_yandex_code.json")

    with open(CITIES_PATH, encoding="utf-8") as f:
        CITY_DATA = json.load(f)

    # Преобразуем все названия в нижний регистр для быстрой проверки
    VALID_CITIES = set(city.lower() for city in CITY_DATA.keys())

    start_city = route[0], 0  # Начальный город
    end_city = route[1], 0  # Конечный город
    start_city_toDB = route[0]  # Начальный город
    end_city_toDB = route[1]  # Конечный город
    cities = [city for group in zveno_list for city in group]
    cities = [start_city_toDB] + cities + [end_city_toDB]
    invalid_cities = [city for city in cities if city.lower() not in VALID_CITIES]

    if invalid_cities:
        await callback_query.message.answer(
            f"Некорректные города: {', '.join(invalid_cities)}\nПожалуйста, попробуйте снова."
        )
        await state.clear()
        await callback_query.bot.send_message(
            callback_query.from_user.id,
            text="Возврат в начало...",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Начать заново", callback_data="create_trip")]
            ])
        )
        return




    formatted_zveno_list = "\n".join(
        [f"{i + 1} звено: {zveno}" for i, zveno in enumerate(zveno_list)]
    )




    departure_date = datetime.strptime(start_date, "%Y-%m-%d")  # Дата отправления

    await save_route_db(tg_id, cities)

    # Сегменты маршрута (пример данных)
    segments = [[(city, days) for city, days in group.items()] for group in zveno_list]
    print(segments,start_city,end_city,type(departure_date))

    # Вызов функции для получения маршрутов
    routes = get_routes(start_city, end_city, departure_date, segments)

    # Отправка маршрутов на сервер
    user_id = callback_query.from_user.id  # ID пользователя из Telegram
    server_url = SERVER_URL
    response = requests.post(server_url, json={"user_id": str(user_id), "routes": routes}, verify = False)

    if response.status_code != 200:
        await callback_query.message.answer("Ошибка при сохранении маршрутов. Попробуйте позже.")
        return

    # Создание клавиатуры с кнопкой для открытия карты


    base_url = MAP_URL
    params = urlencode({"user_id": user_id})
    full_url = f"{base_url}?{params}"

    keyboard = [
        [InlineKeyboardButton(
            text="Открыть карту",
            web_app=WebAppInfo(url=full_url)
        )]
    ]

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # Отправка сообщения с кнопкой
    await callback_query.message.edit_text(
        f"Маршрут сохранен! Нажмите кнопку, чтобы открыть карту:\nВаш маршрут:\n{formatted_zveno_list}",
        reply_markup=reply_markup
    )
    await callback_query.answer()

@router.callback_query(lambda c: c.data.startswith("web_app_data"))
async def handle_web_app_data(callback_query: CallbackQuery):
    # Извлекаем данные из callback_query
    data = callback_query.data.split(":")[1]  # Предполагается, что данные разделены ":"
    try:
        parsed_data = json.loads(data)  # Парсим JSON-строку
        user_id = parsed_data.get("user_id")

        if not user_id:
            await callback_query.message.answer("Ошибка: Не удалось получить user_id.")
            return

        # Запрашиваем маршруты с сервера
        server_url = f"https://6660-45-8-147-174.ngrok-free.app/api/final-routes?user_id={user_id}"
        response = requests.get(server_url)

        if response.status_code == 200:
            routes = response.json()
            formatted_routes = "\n".join(routes)
            print("123")
            await callback_query.message.answer(f"Ваши маршруты:\n{formatted_routes}")
        else:
            await callback_query.message.answer("Ошибка: Не удалось получить маршруты.")

    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка: {str(e)}")




