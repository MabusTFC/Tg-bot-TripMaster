import datetime
import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,

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

    # Отправка маршрутов на сервер
    user_id = callback_query.from_user.id  # ID пользователя из Telegram
    server_url = "https://5d66-57-129-20-222.ngrok-free.app/api/save-routes"
    response = requests.post(server_url, json={"user_id": str(user_id), "routes": routes})

    if response.status_code != 200:
        await callback_query.message.answer("Ошибка при сохранении маршрутов. Попробуйте позже.")
        return

    # Создание клавиатуры с кнопкой для открытия карты
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

    keyboard = [
        [InlineKeyboardButton(
            text="Открыть карту",
            web_app=WebAppInfo(url="https://e985-45-8-147-174.ngrok-free.app")
        )]
    ]

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # Отправка сообщения с кнопкой
    await callback_query.message.edit_text(
        "Маршрут сохранен! Нажмите кнопку, чтобы открыть карту:",
        reply_markup=reply_markup
    )
    await callback_query.answer()
