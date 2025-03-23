import json
import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    WebAppInfo,
    InlineKeyboardButton,
)

from Algorithm.FindCheapestWay import get_routes
import logging

from handlers.utils.keyboards import (
    get_days_keyboard,
    get_list_sity_keyboard,
)

from handlers.utils.state_machine import RoutStates

router = Router()

@router.callback_query(lambda c: c.data.startswith("select_"))
async def select_city(callback_query: CallbackQuery, state: FSMContext):
    city_index = int(callback_query.data.split("_")[1])
    user_data = await state.get_data()
    total_days = user_data.get("total_days")
    max_days = user_data.get("max_days", total_days)
    route = user_data.get("route", [])
    user_days = user_data.get("user_days", {})

    if city_index >= len(route):
        await callback_query.answer("Ошибка! Город не найден.")
        return

    city = route[city_index]
    days = user_days.get(city, 1)

    await state.update_data(selected_city=city)
    await callback_query.message.edit_text(
        f"Вы выбрали город: {city}\nВыберите количество дней пребывания:",
        reply_markup=await get_days_keyboard(city, days, max_days)
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "finish_selection")
async def finish_selection(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    route = user_data.get("route", [])
    user_days = user_data.get("user_days", {})


    final_selection = [(city, user_days.get(city, 1)) for city in route]

    await state.update_data(final_selection=final_selection)
    await state.set_state(RoutStates.FINAL_ROUTE)

    cities = ["Москва", "Владивосток"]  # Города начала и конца маршрута
    start_city = (cities[0], 0)  # Начальный город
    end_city = (cities[1], 0)  # Конечный город
    departure_date = datetime.date(2025, 3, 25)  # Дата отправления

    # Сегменты маршрута (пример данных)
    segments = [
        [("Челябинск", 5), ("Санкт-Петербург", 3)],
        [("Казань", 4), ("Екатеринбург", 2)],
        [("Сочи", 3), ("Новосибирск", 2)]
    ]

    # Вызов функции для получения маршрутов
    routes = get_routes(start_city, end_city, departure_date, segments)

    # Сохранение маршрутов в JSON-файл
    file_path = './src/Map/routes.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(routes, file, ensure_ascii=False, indent=4)
    # Создание клавиатуры с кнопкой для открытия карты
    keyboard = [
        [InlineKeyboardButton("Открыть карту", web_app=WebAppInfo(url="http://localhost:8000"))]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # Отправка сообщения с кнопкой
    await callback_query.message.edit_text(
        "Маршрут сохранен! Нажмите кнопку, чтобы открыть карту:",
        reply_markup=reply_markup
    )
    await callback_query.answer()
